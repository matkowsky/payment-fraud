#!/usr/bin/env python3
"""Measure the storage and read cost of the query-run and release records on synthetic investigations (Supplement S4.4).

Usage:
  python3 tools/investigation_cost.py                    100,000 investigations, results to stdout
  python3 tools/investigation_cost.py --investigations N another volume
  python3 tools/investigation_cost.py --out FILE.json    also write the results

Each investigation is a copy of the valid conformance case (two linked cases: four query runs, seven stored
records, two drafts, one release and one memory read) with identifiers replaced. A sample is checked against
the schema and rules IR-01 to IR-14 before measuring. Standard library only. Timings depend on the machine
and engine; they give an order of magnitude.
"""
import argparse
import gzip
import io
import json
import os
import platform
import random
import sqlite3
import statistics
import sys
import tempfile
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import investigation_conformance as ic  # noqa: E402


def rename(obj, suffix, keep):
    if isinstance(obj, dict):
        return {k: rename(v, suffix, keep) for k, v in obj.items()}
    if isinstance(obj, list):
        return [rename(v, suffix, keep) for v in obj]
    if isinstance(obj, str) and obj in keep:
        return f'{obj}-{suffix}'
    return obj


def generate(n, emit):
    valid = json.loads(ic.VALID.read_text(encoding='utf-8'))['records']
    actors = [r for r in valid if r['record_type'] == 'Actor']
    rest = [r for r in valid if r['record_type'] != 'Actor']
    keep = {r['record_id'] for r in rest} | {'K-1', 'K-2', 'ACC-1'}
    for a in actors:
        emit(a)
    for i in range(n):
        for r in rest:
            emit(rename(r, i, keep))


def measure(n):
    sample = []
    generate(50, sample.append)
    schema = json.loads(ic.SCHEMA.read_text(encoding='utf-8'))
    assert not ic.check(sample, schema), 'generated sample fails conformance'
    counts, raw = {}, {}
    buf = io.BytesIO()
    gz = gzip.GzipFile(fileobj=buf, mode='wb', compresslevel=6)
    path = os.path.join(tempfile.mkdtemp(), 'investigation.db')
    db = sqlite3.connect(path)
    db.execute('PRAGMA journal_mode=OFF')
    db.execute('PRAGMA synchronous=OFF')
    db.execute('CREATE TABLE records (record_id TEXT PRIMARY KEY, record_type TEXT, body TEXT) WITHOUT ROWID')
    batch = []

    def emit(r):
        line = json.dumps(r, separators=(',', ':')).encode('utf-8')
        t = r['record_type']
        counts[t] = counts.get(t, 0) + 1
        raw[t] = raw.get(t, 0) + len(line) + 1
        gz.write(line + b'\n')
        batch.append((r['record_id'], t, line.decode('utf-8')))
        if len(batch) >= 50000:
            db.executemany('INSERT INTO records VALUES (?,?,?)', batch)
            batch.clear()

    generate(n, emit)
    db.executemany('INSERT INTO records VALUES (?,?,?)', batch)
    db.commit()
    gz.close()
    db.execute('VACUUM')
    size = os.path.getsize(path)

    def get(rid):
        return json.loads(db.execute('SELECT body FROM records WHERE record_id=?', (rid,)).fetchone()[0])

    rnd = random.Random(7)
    absence, reuse = [], []
    for _ in range(10000):
        i = rnd.randrange(n)
        t = time.perf_counter()
        draft = get(f'DR-1-{i}')
        claim = next(c for c in draft['claims'] if c['claim_type'] == 'absence')
        ok = all(ic.derive_statuses(q) == q['statuses'] and ic.supports_absence(q, claim) for q in map(get, claim['query_runs']))
        absence.append((time.perf_counter() - t) * 1e6)
        assert ok
        t = time.perf_counter()
        read = get(f'MR-1-{i}')
        item = get(read['item_id'])
        rel = get(item['release_id'])
        ok = rel['decision'] == 'released' and ic.ts(item['created_at']) <= ic.ts(read['read_at']) < ic.ts(rel['expires_at'])
        reuse.append((time.perf_counter() - t) * 1e6)
        assert ok
    db.close()
    os.remove(path)
    absence.sort()
    reuse.sort()
    per = 1000 / n
    c2 = ('QueryRun',)
    c3 = ('DraftOutput', 'OutputExposure', 'ReleaseDecision', 'ReleasedItem', 'MemoryRead')
    return {
        'investigations': n,
        'machine': f'{platform.machine()}, {os.cpu_count()} CPUs; SQLite {sqlite3.sqlite_version}; Python {platform.python_version()}',
        'records_by_type': dict(sorted(counts.items())),
        'mean_json_bytes_by_type': {k: round(raw[k] / counts[k]) for k in sorted(raw)},
        'records_per_investigation': round((sum(counts.values()) - counts['Actor']) / n, 1),
        'json_kb_per_investigation': round(sum(raw.values()) / n / 1000, 1),
        'query_run_kb_per_investigation': round(sum(raw[k] for k in c2) / n / 1000, 1),
        'release_record_kb_per_investigation': round(sum(raw[k] for k in c3) / n / 1000, 1),
        'json_mb_per_thousand_investigations': round(sum(raw.values()) * per / 1e6, 1),
        'gzip_mb_per_thousand_investigations': round(len(buf.getvalue()) * per / 1e6, 2),
        'sqlite_mb_per_thousand_investigations': round(size * per / 1e6, 1),
        'absence_check_microseconds': {'median': round(statistics.median(absence)), 'p99': round(absence[int(0.99 * len(absence)) - 1])},
        'reuse_check_microseconds': {'median': round(statistics.median(reuse)), 'p99': round(reuse[int(0.99 * len(reuse)) - 1])},
        'sample_check': 'generated records pass the schema and IR-01 to IR-14',
    }


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--investigations', type=int, default=100_000)
    ap.add_argument('--out')
    args = ap.parse_args()
    text = json.dumps(measure(args.investigations), indent=1)
    print(text)
    if args.out:
        Path(args.out).write_text(text + '\n', encoding='utf-8')
