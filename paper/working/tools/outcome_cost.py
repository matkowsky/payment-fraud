#!/usr/bin/env python3
"""Measure the storage and query cost of the C1 outcome records on synthetic payments (Supplement S4.3).

Usage:
  python3 tools/outcome_cost.py                  1,000,000 payments, results to stdout
  python3 tools/outcome_cost.py --payments N     another volume
  python3 tools/outcome_cost.py --out FILE.json  also write the results

Every record is built from a record in the valid conformance case, with identifiers replaced and
times shifted, so each has that record's fields. A sample is checked against the schema and rules
OR-01 to OR-14 before measuring. Rates are illustrative assumptions, not any platform's values.
Standard library only. Timings depend on the machine and engine; they give an order of magnitude.
"""
import argparse
import copy
import gzip
import io
import json
import os
import platform
import random
import re
import sqlite3
import statistics
import sys
import tempfile
import time
from datetime import datetime, timedelta, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import outcome_conformance as oc  # noqa: E402

ASSUMPTIONS = {
    'days': 90,
    'payments_per_account': 100,
    'channels_per_payment': 2,
    'block_rate': 0.01,
    'chargeback_rate_of_allowed': 0.005,
    'events_per_chargeback': 3,
    'account_hold_rate': 0.01,
    'successor_link_rate': 0.01,
    'cited_readings': 'one per blocked payment',
    'seed': 7,
}
DT = re.compile(r'^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$')
FMT = '%Y-%m-%dT%H:%M:%SZ'
START = datetime(2026, 3, 1, tzinfo=timezone.utc)


def parse(s):
    return datetime.strptime(s, FMT).replace(tzinfo=timezone.utc)


def remap(obj, ids, shift):
    """Copy obj, replacing identifiers in ids and shifting every timestamp by shift."""
    if isinstance(obj, dict):
        return {k: remap(v, ids, shift) for k, v in obj.items()}
    if isinstance(obj, list):
        return [remap(v, ids, shift) for v in obj]
    if isinstance(obj, str):
        if obj in ids:
            return ids[obj]
        if DT.match(obj):
            return (parse(obj) + shift).strftime(FMT)
    return obj


def templates():
    valid = json.loads(oc.VALID.read_text(encoding='utf-8'))['records']
    by = {r['record_id']: r for r in valid}
    ia = {r['item']['item_id']: r for r in valid if r['record_type'] == 'ItemAttribution'}
    return valid, by, ia


def generate(n, a, emit):
    """Emit records for n payments; return counts by record type."""
    valid, by, ia = templates()
    rnd = random.Random(a['seed'])
    for r in valid:
        if r['record_type'] == 'OutcomeChannel':
            emit(r)
    accounts = max(1, n // a['payments_per_account'])
    base_allow = parse(by['D-4-rec']['decided_at'])
    base_block = parse(by['D-1-rec']['decided_at'])
    base_report = parse(by['D-2-rec']['decided_at'])
    ia_allow = ia['PA-3'] if 'PA-3' in ia else ia['PA-2']
    span = a['days'] * 86400
    blocked = []
    for i in range(n):
        acc = f'ACC-{i % accounts}'
        when = START + timedelta(seconds=rnd.randrange(span))
        pa, d = f'PA-{i}', f'D-{i}'
        if rnd.random() < a['block_rate']:
            ids = {'PA-1': pa, 'D-1': d, 'D-1-rec': f'{d}-rec', 'T-1': f'T-{i}-1', 'T-2': f'T-{i}-2', 'ACC-1': acc}
            shift = when - base_block
            for rid in ('D-1-rec', 'T-1', 'T-2'):
                emit(remap(by[rid], ids, shift))
            emit(remap(ia_allow, dict(ids, **{ia_allow['item']['item_id']: pa, ia_allow['record_id']: f'IA-{i}'}), when - parse(ia_allow['effective_from'])))
            blocked.append((pa, when))
            continue
        ids = {'PA-3': pa, 'D-4': d, 'D-4-rec': f'{d}-rec', 'T-4': f'T-{i}-1', 'T-5': f'T-{i}-2', 'ACC-1': acc}
        shift = when - base_allow
        for rid in ('D-4-rec', 'T-4', 'T-5'):
            emit(remap(by[rid], ids, shift))
        emit(remap(ia_allow, dict(ids, **{ia_allow['item']['item_id']: pa, ia_allow['record_id']: f'IA-{i}'}), when - parse(ia_allow['effective_from'])))
        if rnd.random() < a['chargeback_rate_of_allowed']:
            rids = {'PA-2': pa, 'D-2': d, 'R-1': f'R-{i}', 'LE-1': f'LE-{i}-1', 'LE-2': f'LE-{i}-2', 'LE-3': f'LE-{i}-3', 'K-1': f'K-{i}', 'ACC-1': acc}
            rshift = when - base_report
            for rid in ('LE-1', 'LE-2', 'LE-3')[:a['events_per_chargeback']]:
                emit(remap(by[rid], rids, rshift))
            emit(remap(by['K-1'], rids, rshift))
    holds = rnd.sample(range(accounts), max(0, round(accounts * a['account_hold_rate'])))
    for j, k in enumerate(holds):
        ids = {'ACC-1': f'ACC-{k}', 'D-3': f'DH-{j}', 'D-3-rec': f'DH-{j}-rec'}
        emit(remap(by['D-3-rec'], ids, START - parse(by['D-6-rec']['decided_at']) + timedelta(days=rnd.randrange(a['days']))))
    links = max(0, round(accounts * a['successor_link_rate']))
    for j in range(links):
        ids = {'ACC-0': f'ACC-OLD-{j}', 'ACC-1': f'ACC-{rnd.randrange(accounts)}', 'D-6': f'DC-{j}', 'D-6-rec': f'DC-{j}-rec', 'EL-1': f'EL-{j}'}
        shift = START - parse(by['D-6-rec']['decided_at'])
        emit(remap(by['D-6-rec'], ids, shift))
        emit(remap(by['EL-1'], ids, shift))
    rd = by['RD-1']
    for j, (pa, when) in enumerate(blocked):
        emit(remap(rd, {'PA-1': pa, 'RD-1': f'RD-{j}'}, when - base_block))


def sample_conformance(a):
    out = []
    generate(300, dict(a, block_rate=0.2, chargeback_rate_of_allowed=0.2, payments_per_account=1), out.append)
    schema = json.loads(oc.SCHEMA.read_text(encoding='utf-8'))
    found = oc.check(out, schema)
    return len(out), found


def key_columns(r):
    item = r.get('item') or {}
    targets = r.get('targets') or [{}]
    return (r['record_id'], r['record_type'], item.get('item_id') or targets[0].get('item_id'),
            r.get('channel_id'), r.get('state'), r.get('effective_from'), r.get('learned_at'))


def measure(n, a):
    counts, raw = {}, {}
    gz_buf = io.BytesIO()
    gz = gzip.GzipFile(fileobj=gz_buf, mode='wb', compresslevel=6)
    tmp = tempfile.mkdtemp()
    db_path = os.path.join(tmp, 'outcomes.db')
    db = sqlite3.connect(db_path)
    db.execute('PRAGMA journal_mode=OFF')
    db.execute('PRAGMA synchronous=OFF')
    db.execute('CREATE TABLE records (record_id TEXT PRIMARY KEY, record_type TEXT, item_id TEXT, channel_id TEXT, '
               'state TEXT, effective_from TEXT, learned_at TEXT, body TEXT) WITHOUT ROWID')
    batch = []

    def emit(r):
        line = json.dumps(r, separators=(',', ':'), ensure_ascii=False).encode('utf-8')
        t = r['record_type']
        counts[t] = counts.get(t, 0) + 1
        raw[t] = raw.get(t, 0) + len(line) + 1
        gz.write(line + b'\n')
        batch.append(key_columns(r) + (line.decode('utf-8'),))
        if len(batch) >= 50000:
            db.executemany('INSERT INTO records VALUES (?,?,?,?,?,?,?,?)', batch)
            batch.clear()

    t0 = time.perf_counter()
    generate(n, a, emit)
    if batch:
        db.executemany('INSERT INTO records VALUES (?,?,?,?,?,?,?,?)', batch)
    db.commit()
    gz.close()
    t_load = time.perf_counter() - t0
    t0 = time.perf_counter()
    db.execute('CREATE INDEX asof ON records (item_id, channel_id, record_type, learned_at, effective_from)')
    db.commit()
    t_index = time.perf_counter() - t0
    db.execute('VACUUM')
    db_bytes = os.path.getsize(db_path)

    rnd = random.Random(a['seed'] + 1)
    state_sql = ("SELECT state FROM records WHERE item_id=? AND channel_id=? AND record_type='ChannelStateTransition' "
                 "AND learned_at<=? AND effective_from<=? ORDER BY effective_from DESC LIMIT 1")
    report_sql = ("SELECT count(*) FROM records WHERE item_id=? AND channel_id=? AND record_type='LabelEvent' "
                  "AND learned_at<=?")
    end = (START + timedelta(days=a['days'] + 30)).strftime(FMT)
    lat = []
    for _ in range(10000):
        pa = f'PA-{rnd.randrange(n)}'
        t1 = time.perf_counter()
        db.execute(state_sql, (pa, 'CH-CB-FRAUD', end, end)).fetchone()
        db.execute(report_sql, (pa, 'CH-CB-FRAUD', end)).fetchone()
        lat.append((time.perf_counter() - t1) * 1e6)
    lat.sort()
    day = (START + timedelta(days=10)).strftime('%Y-%m-%d')
    cohort_sql = ("SELECT p.item_id, (SELECT t.state FROM records t WHERE t.item_id=p.item_id AND t.channel_id='CH-CB-FRAUD' "
                  "AND t.record_type='ChannelStateTransition' AND t.learned_at<=?1 AND t.effective_from<=?1 "
                  "ORDER BY t.effective_from DESC LIMIT 1), (SELECT count(*) FROM records l WHERE l.item_id=p.item_id "
                  "AND l.channel_id='CH-CB-FRAUD' AND l.record_type='LabelEvent' AND l.learned_at<=?1) "
                  "FROM records p WHERE p.record_type='ControlAction' AND p.item_id LIKE 'PA-%' AND p.learned_at LIKE ?2")
    t1 = time.perf_counter()
    cohort = db.execute(cohort_sql, (end, day + '%')).fetchall()
    t_cohort = time.perf_counter() - t1
    db.close()
    os.remove(db_path)
    total_raw = sum(raw.values())
    per_m = 1_000_000 / n
    return {
        'payments': n,
        'assumptions': a,
        'machine': f'{platform.processor() or platform.machine()}, {os.cpu_count()} CPUs; SQLite {sqlite3.sqlite_version}; Python {platform.python_version()}',
        'records_by_type': dict(sorted(counts.items())),
        'records_per_payment': round(sum(counts.values()) / n, 3),
        'json_bytes_by_type': dict(sorted(raw.items())),
        'mean_json_bytes_by_type': {k: round(raw[k] / counts[k]) for k in sorted(raw)},
        'json_mb_per_million_payments': round(total_raw * per_m / 1e6, 1),
        'gzip_mb_per_million_payments': round(len(gz_buf.getvalue()) * per_m / 1e6, 1),
        'sqlite_mb_per_million_payments_with_index': round(db_bytes * per_m / 1e6, 1),
        'load_seconds': round(t_load, 1),
        'index_seconds': round(t_index, 1),
        'point_query_microseconds': {'median': round(statistics.median(lat)), 'p99': round(lat[int(0.99 * len(lat)) - 1])},
        'cohort_day_payments': len(cohort),
        'cohort_day_seconds': round(t_cohort, 3),
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--payments', type=int, default=1_000_000)
    ap.add_argument('--out')
    args = ap.parse_args()
    n_sample, found = sample_conformance(ASSUMPTIONS)
    if found:
        print(json.dumps({'sample_records': n_sample, 'findings': found[:10]}, indent=1))
        sys.exit(1)
    res = measure(args.payments, ASSUMPTIONS)
    res['sample_check'] = f'{n_sample} generated records pass the schema and OR-01 to OR-14'
    text = json.dumps(res, indent=1)
    print(text)
    if args.out:
        Path(args.out).write_text(text + '\n', encoding='utf-8')


if __name__ == '__main__':
    main()
