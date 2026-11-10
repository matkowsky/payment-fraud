#!/usr/bin/env python3
"""Replay: allegations in FTC v. First Data Merchant Services LLC and Chi W. Ko,
No. 1:20-cv-03867 (S.D.N.Y.), ECF 1, rebuilt as synthetic outcome records (Supplement S4.2).

All data are synthetic. Complaint content is allegation, not established fact. Every parameter
below is illustrative; none is a network's actual rule. Standard library only.

Usage: python3 tools/replays/ftc_first_data_replay.py [OUT_DIR]
Writes records.json (seed 1) and results.json to OUT_DIR.
The 1,000-run figures use fast_draw, the same generating process without writing records; captures match the
records exactly (checked in main), report draws come from a separate random stream.
"""
import hashlib
import json
import random
import statistics
import sys
from collections import defaultdict
from datetime import datetime, timedelta, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import outcome_conformance as oc  # noqa: E402

T0 = datetime(2026, 1, 5, tzinfo=timezone.utc)   # synthetic day 0
P = 30                                            # days per monitoring period; P1 = days [0, 30)
N_MIN, R_MIN = 100, 0.015                         # illustrative rules SYN-MON-1 and -2 (count floor, ratio)
WINDOW = 120                                      # illustrative reporting window SYN-CB-1
LAG = [(0.35, 5, 30), (0.40, 30, 60), (0.18, 60, 90), (0.07, 90, 118)]  # capture-to-arrival days
CH, ACQ = 'CH-CB-FRAUD', 'AQ-SYN-1'
PERIODS = range(1, 10)
SEEDS = range(1, 1001)

ACCOUNTS = (
    # A: eight related accounts, opened the same day in pairs (par. 49, 84a); load balancing (par. 35)
    [dict(id=f'A{k}', scen='A', desc=[(0, f'SYNSLIM{k}')], start=0, end=120, vol=350, rate=0.04)
     for k in range(1, 9)]
    # B: account closed for chargebacks, successor applies two weeks later (par. 61, 91)
    + [dict(id='B0', scen='B', desc=[(0, 'SYNEDU')], start=0, end=90, vol=3000, rate=0.05),
       dict(id='B1', scen='B', desc=[(0, 'SYNEDUPRO')], start=104, end=210, vol=3000, rate=0.05),
       # Bc control: the same closure and link, but the successor's own report rate is low
       dict(id='B0c', scen='Bc', desc=[(0, 'SYNTUTOR')], start=0, end=90, vol=3000, rate=0.05),
       dict(id='B1c', scen='Bc', desc=[(0, 'SYNTUTORPRO')], start=104, end=210, vol=3000, rate=0.003)]
    # D: one account reused for a second business under a switched descriptor (par. 75)
    + [dict(id='D1', scen='D', desc=[(0, 'SYNDEBT'), (90, 'SYNSUPP')], start=0, end=180, vol=4000, rate=0.03)]
    # L2 control: forty merchants, assumed legitimate, sharing one call-center phone number (par. 86)
    + [dict(id=f'C{k:02d}', scen='L2', desc=[(0, f'SYNSVC{k:02d}')], start=0, end=120, vol=300, rate=0.016)
       for k in range(1, 41)])
ACC = {a['id']: a for a in ACCOUNTS}


def iso(day):
    return (T0 + timedelta(days=day)).strftime('%Y-%m-%dT%H:%M:%SZ')


def day_of(stamp):
    return (oc.ts(stamp) - T0).total_seconds() / 86400


def period(day):
    return int(day // P) + 1


def desc_at(acct, day):
    return [d for f, d in ACC[acct]['desc'] if f <= day][-1]


LAG_FAST = [(0.60, 5, 30), (0.35, 30, 60), (0.05, 60, 90)]                      # sensitivity only
LAG_SLOW = [(0.15, 5, 30), (0.30, 30, 60), (0.30, 60, 90), (0.25, 90, 118)]    # sensitivity only


def draw_lag(rng, lag=None):
    lag = lag or LAG
    u, acc = rng.random(), 0.0
    for w, lo, hi in lag:
        acc += w
        if u < acc:
            return rng.uniform(lo, hi)
    return rng.uniform(lag[-1][1], lag[-1][2])


def slices(a):
    """(period, lo, hi, n) for each period an account is active in."""
    out = []
    for p in PERIODS:
        lo, hi = max(a['start'], (p - 1) * P), min(a['end'], p * P)
        if hi > lo:
            out.append((p, lo, hi, round(a['vol'] * (hi - lo) / P)))
    return out


# ---------- links (as recorded at boarding or application) ----------
def link(rid, kind, frm, to, basis, basis_kind, conf, confounders, day, source):
    return {'record_type': 'EntityLink', 'record_id': rid, 'link_type': kind,
            'from': {'entity_type': 'account', 'entity_id': frm}, 'to': {'entity_type': 'account', 'entity_id': to},
            'basis': basis, 'basis_kind': basis_kind, 'verified': False, 'confidence': conf,
            'confounders': confounders, 'effective_from': iso(day), 'learned_at': iso(day),
            'source': source, 'purpose_scope': 'fraud investigation'}


def link_records():
    out = []
    for i in (1, 3, 5, 7):
        out.append(link(f'EL-A{i}-A{i+1}', 'shared_principal', f'A{i}', f'A{i+1}',
                        'same purported principal and merchant name; opened the same day (modeled on par. 49)',
                        'shared_attribute', 'low', ['a common principal name'], 0, 'merchant applications (synthetic)'))
    for i in (3, 5, 7):
        out.append(link(f'EL-A1-A{i}', 'other', 'A1', f'A{i}', 'related billing descriptors (modeled on par. 84a)',
                        'shared_attribute', 'low', ['a legitimate multi-brand business using related descriptors'],
                        0, 'merchant applications (synthetic)'))
    for frm, to in (('B0', 'B1'), ('B0c', 'B1c')):
        out.append(link(f'EL-{frm}-{to}', 'suspected_successor_account', frm, to,
                        'application lists a prior account under a different business name, closed two weeks '
                        'earlier, with the same business model (modeled on par. 61)', 'documented_relationship',
                        'medium', ['an unrelated applicant reusing a common business model'], 104,
                        'merchant application (synthetic)'))
    for k in range(2, 41):
        out.append(link(f'EL-C01-C{k:02d}', 'other', 'C01', f'C{k:02d}', 'same customer-service phone number',
                        'shared_attribute', 'low', ['one call center serving many merchants (modeled on par. 86)'],
                        0, 'merchant applications (synthetic)'))
    return out


# ---------- full records for one seed ----------
def build_records(seed):
    rng = random.Random(seed)
    recs = [{'record_type': 'OutcomeChannel', 'record_id': 'CH-CB-FRAUD-v1', 'channel_id': CH,
             'name': 'card chargeback, fraud reason', 'rail': 'card', 'clock_start_event': 'processing date of the payment',
             'reporting_window': {'status': 'defined', 'days': WINDOW, 'source': 'illustrative network rule (synthetic)',
                                  'rule_version': 'SYN-CB-1'},
             'window_depends_on': ['claim type'], 'adjudicates_truth': 'yes', 'learned_at': iso(-5)},
            ] + [{'record_type': 'ControlAction', 'record_id': f'D-{a}-CLOSE-rec', 'decision_id': f'D-{a}-CLOSE',
                  'decision_kind': 'close_account', 'targets': [{'item_type': 'account', 'item_id': a}],
                  'decided_at': iso(90), 'learned_at': iso(90), 'authority': 'processor risk review (synthetic)',
                  'rule_or_model_version': 'SYN-REVIEW-1', 'channel_effects': [{'channel_id': CH, 'effect': 'none'}]}
                 for a in ('B0', 'B0c')]
    recs += link_records()
    sample = set()
    for a in ACCOUNTS:
        n_item = 0
        for p, lo, hi, n in slices(a):
            for i in range(n):
                t = lo + (i + 0.5) * (hi - lo) / n
                item = f"{a['id']}-{n_item:05d}"
                n_item += 1
                ref = {'item_type': 'payment_attempt', 'item_id': item}
                recs.append({'record_type': 'ItemAttribution', 'record_id': f'IA-{item}', 'item': ref,
                             'merchant_account': a['id'], 'platform_account': 'ISO-1',
                             'acquirer': {'status': 'known', 'value': ACQ},
                             'descriptor_static': {'status': 'known', 'value': desc_at(a['id'], t)},
                             'basis': 'processor ledger (synthetic)', 'verified': True,
                             'effective_from': iso(t), 'learned_at': iso(t)})
                if rng.random() < a['rate']:
                    arr = t + draw_lag(rng)
                    recs.append({'record_type': 'LabelEvent', 'record_id': f'LE-{item}', 'report_id': f'R-{item}',
                                 'revision_kind': 'initial', 'report_type': 'dispute',
                                 'source': 'issuer through the card network (synthetic)', 'reason': 'fraud',
                                 'channel_id': CH, 'item': ref,
                                 'attribution': {'basis': 'network transaction identifier', 'verified': True},
                                 'amount': {'status': 'unknown', 'reason': 'amounts not modeled in this replay'},
                                 'occurred_at': {'status': 'exact', 'value': iso(t)},
                                 'reported_at': {'status': 'exact', 'value': iso(arr - 0.5)},
                                 'arrived_at': iso(arr), 'learned_at': iso(arr + 5 / 1440),
                                 'status': 'filed', 'adjudicated': 'not_applicable', 'truth_assessment_ids': []})
                if a['scen'] == 'A' and p in (1, 4) and i < 3:
                    sample.add((item, t))
    for item, t in sorted(sample):  # open channel from capture, for the sampled no-report readings
        recs.append({'record_type': 'ChannelStateTransition', 'record_id': f'T-{item}',
                     'item': {'item_type': 'payment_attempt', 'item_id': item}, 'channel_id': CH, 'state': 'open',
                     'effective_from': iso(t),
                     'cause': {'kind': 'rule_event', 'source': 'card network dispute rule (synthetic)',
                               'rule_version': 'SYN-CB-1'},
                     'clock_start': {'status': 'exact', 'value': iso(t)}, 'learned_at': iso(t)})
    learned = {r['item']['item_id']: day_of(r['learned_at']) for r in recs if r['record_type'] == 'LabelEvent'}
    for item, t in sorted(sample):
        for rd in (30, 150, 250):
            if rd < t:
                continue
            present = item in learned and learned[item] <= rd
            status = 'not_applicable' if present else ('pending' if rd < t + WINDOW else 'matured_absent')
            r = {'record_type': 'ChannelStatusReading', 'record_id': f'RD-{item}-d{rd}',
                 'item': {'item_type': 'payment_attempt', 'item_id': item}, 'channel_id': CH, 'read_time': iso(rd),
                 'report_presence': 'present' if present else 'none_arrived', 'channel_state': 'open',
                 'query_access': 'full', 'no_report_status': status, 'clock_start': {'status': 'exact', 'value': iso(t)}}
            if status == 'matured_absent':
                r['matured_under_rule_version'] = 'SYN-CB-1'
            recs.append(r)
    return recs


def from_records(recs):
    """Captures and report arrivals, keyed (account, descriptor at capture, period), derived from records only."""
    ia = {r['item']['item_id']: r for r in recs if r['record_type'] == 'ItemAttribution'}
    cap, rep = defaultdict(int), defaultdict(int)
    for r in ia.values():
        cap[r['merchant_account'], r['descriptor_static']['value'], period(day_of(r['effective_from']))] += 1
    for r in recs:
        if r['record_type'] == 'LabelEvent':
            a = ia[r['item']['item_id']]
            rep[a['merchant_account'], a['descriptor_static']['value'], period(day_of(r['arrived_at']))] += 1
    links = [r for r in recs if r['record_type'] == 'EntityLink']
    return cap, rep, links


def fast_draw(seed):
    """Same generating process without writing records: only paid-fraud draws are simulated."""
    rng = random.Random(10_000 + seed)
    cap, rep = defaultdict(int), defaultdict(int)
    for a in ACCOUNTS:
        for p, lo, hi, n in slices(a):
            cap[a['id'], desc_at(a['id'], lo), p] += n
            for _ in range(rng.binomialvariate(n, a['rate'])):
                t = rng.uniform(lo, hi)
                rep[a['id'], desc_at(a['id'], t), period(t + draw_lag(rng))] += 1
    return cap, rep


# ---------- units and the illustrative monitoring rule ----------
def cluster_fn(links, tiers, p):
    parent = {}

    def find(x):
        parent.setdefault(x, x)
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x
    for el in links:
        if el['basis_kind'] in tiers and day_of(el['learned_at']) <= p * P:
            parent[find(el['from']['entity_id'])] = find(el['to']['entity_id'])
    return lambda acct: 'cluster:' + find(acct)


CURRENT = {a['id']: a['desc'][-1][1] for a in ACCOUNTS}
TIER1 = {'verified_identifier', 'documented_relationship'}
TIER2 = TIER1 | {'shared_attribute', 'analyst_judgment'}


def unit_fn(view, links, p):
    if view == 'account':
        return lambda a, d: a
    if view == 'monitored_unit':
        return lambda a, d: f'{ACQ}/{d}'
    if view == 'monitored_unit_overwritten':
        return lambda a, d: f'{ACQ}/{CURRENT[a]}'
    c = cluster_fn(links, TIER1 if view == 'cluster_tier1' else TIER2, p)
    return lambda a, d: c(a)


VIEWS = ['account', 'monitored_unit', 'monitored_unit_overwritten', 'cluster_tier1', 'cluster_tier2']


RULES = {'SYN-MON-1': 1, 'SYN-MON-2': 0}  # denominator from the previous period, or from the same period


def evaluate(cap, rep, links, view, lag=1):
    """{(unit, period): (count, denominator, status, members)}; members are every account mapped to the unit."""
    out = {}
    pairs = sorted({(a, d) for a, d, q in cap} | {(a, d) for a, d, q in rep})
    for p in PERIODS:
        u = unit_fn(view, links, p)
        cnt, den, mem = defaultdict(int), defaultdict(int), defaultdict(set)
        for a, d in pairs:
            mem[u(a, d)].add(a)
        for (a, d, q), n in rep.items():
            if q == p:
                cnt[u(a, d)] += n
        for (a, d, q), n in cap.items():
            if q == p - lag:
                den[u(a, d)] += n
        for k in sorted(set(cnt) | set(den)):
            c, n = cnt[k], den[k]
            status = 'undefined' if n == 0 else ('flag' if c >= N_MIN and c / n >= R_MIN else 'below')
            out[k, p] = (c, n, status, mem[k])
    return out


def first_flag(ev, accounts, start=1):
    hits = [p for (k, p), v in ev.items() if v[2] == 'flag' and v[3] & accounts and p >= start]
    return min(hits) if hits else None


TARGETS = {'A': {f'A{k}' for k in range(1, 9)}, 'B0': {'B0'}, 'B1': {'B1'}, 'B1c': {'B1c'}, 'D': {'D1'},
           'L2': {f'C{k:02d}' for k in range(1, 41)}}
METRICS = {'A': ('A', 1), 'B0': ('B0', 1), 'B1': ('B1', 1), 'B1@P5+': ('B1', 5), 'B1c': ('B1c', 1),
           'B1c@P5+': ('B1c', 5), 'D': ('D', 1), 'D@P4+': ('D', 4), 'L2': ('L2', 1)}


def unit_first_flag(ev, unit):
    hits = [p for (k, p), v in ev.items() if v[2] == 'flag' and k == unit]
    return min(hits) if hits else None


ESCAPE = {'B': ({'B0', 'B1'}, 5, 8), 'Bc': ({'B0c', 'B1c'}, 5, 8), 'D': ({'D1'}, 4, 7)}


def escaped(ev, accounts, lo, hi):
    """Reports that arrive in a unit-period with no denominator, so no ratio test applies; and flagged periods."""
    rows = [(p, v) for (k, p), v in ev.items() if lo <= p <= hi and v[3] & accounts]
    return (sum(v[0] for p, v in rows if v[2] == 'undefined'), len({p for p, v in rows if v[2] == 'flag'}))


def pooled_check(cap, rep, links):
    """Section 8.2: with every member's denominator positive, a pooled ratio cannot exceed the highest member ratio."""
    acct = evaluate(cap, rep, links, 'account')
    held = exceeded = 0
    examples = []
    for view in ('cluster_tier2',):  # tier 2 contains every tier 1 cluster
        for (k, p), (c, n, s, mem) in sorted(evaluate(cap, rep, links, view).items(), key=lambda x: (x[0][1], x[0][0])):
            if len(mem) < 2 or n == 0:
                continue
            parts = [acct.get((a, p), (0, 0, 'none', set())) for a in mem]
            defined = [pc / pn for pc, pn, _, _ in parts if pn > 0]
            if all(pn > 0 for pc, pn, _, _ in parts if pc > 0):
                assert c / n <= max(defined) + 1e-12, (view, k, p)
                held += 1
            elif defined and c / n > max(defined):
                exceeded += 1
                examples.append({'view': view, 'unit': k, 'period': p, 'pooled': round(c / n, 4),
                                 'max_defined_account_ratio': round(max(defined), 4),
                                 'accounts_with_reports_and_no_denominator': sorted(
                                     a for a in mem if acct.get((a, p), (0, 0))[0] > 0 and acct.get((a, p), (0, 0))[1] == 0)})
    return {'cluster_periods_all_denominators_positive': held, 'pooled_exceeds_every_defined': exceeded,
            'examples': examples}


def maturity(recs):
    """Scenario A: naive observed rate versus what the records state at each read day."""
    ia = {r['item']['item_id']: day_of(r['effective_from']) for r in recs
          if r['record_type'] == 'ItemAttribution' and r['merchant_account'].startswith('A')}
    le = {r['item']['item_id']: day_of(r['learned_at']) for r in recs
          if r['record_type'] == 'LabelEvent' and r['item']['item_id'] in ia}
    out = []
    for rd in (30, 60, 90, 120, 150, 240):
        cap = [i for i, t in ia.items() if t <= rd]
        got = sum(1 for i in cap if i in le and le[i] <= rd)
        pend = sum(1 for i in cap if not (i in le and le[i] <= rd) and rd < ia[i] + WINDOW)
        out.append({'read_day': rd, 'captured': len(cap), 'reports_learned': got,
                    'naive_rate': round(got / len(cap), 4), 'pending_share': round(pend / len(cap), 4),
                    'eventual_rate_same_items': round(sum(1 for i in cap if i in le) / len(cap), 4)})
    return out


def wrong_stores(recs, schema):
    """Three altered stores: the first two should be rejected; the third, an in-place edit, passes every rule."""
    late = [r for r in recs if r['record_type'] == 'LabelEvent' and r['item']['item_id'].startswith('B0-')
            and day_of(r['arrived_at']) > 90][:3]
    w_close = recs + [{'record_type': 'ChannelStateTransition', 'record_id': f"WT-{r['item']['item_id']}",
                       'item': r['item'], 'channel_id': CH, 'state': 'closed', 'effective_from': iso(90),
                       'cause': {'kind': 'decision', 'decision_id': 'D-B0-CLOSE'}, 'learned_at': iso(90)}
                      for r in late]
    old = [r for r in recs if r['record_type'] == 'ItemAttribution' and r['merchant_account'] == 'D1'
           and r['descriptor_static']['value'] == 'SYNDEBT']
    w_dup = recs + [dict(r, descriptor_static={'status': 'known', 'value': 'SYNSUPP'}, learned_at=iso(90))
                    for r in old[:3]]
    old_ids = {r['record_id'] for r in old}
    w_over = [dict(r, descriptor_static={'status': 'known', 'value': 'SYNSUPP'}) if r['record_id'] in old_ids else r
              for r in recs]
    res = {}
    for name, rs in (('closure_recorded_as_channel_closed', w_close),
                     ('second_record_under_reused_id', w_dup),
                     ('descriptor_overwritten_in_place', w_over)):
        f = oc.check(rs, schema)
        res[name] = {'rules': sorted({x[0] for x in f}), 'findings': len(f), 'first': f[:2]}
    return res


def sensitivity():
    """Scenario A at expected values: par. 84a's $340,000 at an 8% combined chargeback-and-refund rate."""
    rows = []
    for ticket in (20, 30, 50):
        for share in (0.25, 0.5, 0.75):
            for periods in (3, 4):
                vol = 340_000 / ticket / 8 / periods
                acct = vol * 0.08 * share
                rows.append({'ticket_usd': ticket, 'chargeback_share_of_8pct': share, 'periods': periods,
                             'captures_per_account_period': round(vol), 'expected_reports_per_account_period': round(acct, 1),
                             'expected_reports_cluster_period': round(8 * acct, 1),
                             'account_reaches_floor': acct >= N_MIN, 'cluster_reaches_floor': 8 * acct >= N_MIN,
                             'ratio_condition_met': 0.08 * share >= R_MIN})
    return rows


# ---------- extension: parameter sweeps (fast path only) ----------
SWEEP_SEEDS = range(1, 501)


def sim_counts(accts, rng, lag=None):
    """Captures and report arrivals per (account, period) for simple accounts: start, end, vol, rate."""
    cap, rep = defaultdict(int), defaultdict(int)
    for a in accts:
        for p, lo, hi, n in slices(a):
            cap[a['id'], p] += n
            for _ in range(rng.binomialvariate(n, a['rate'])):
                rep[a['id'], period(rng.uniform(lo, hi) + draw_lag(rng, lag))] += 1
    return cap, rep


def flagged(cap, rep, unit_of, lag=1):
    """Set of (unit, period) flagged under the illustrative rule; unit_of(account, period) gives the unit."""
    out = set()
    for p in PERIODS:
        cnt, den = defaultdict(int), defaultdict(int)
        for (a, q), n in rep.items():
            if q == p:
                cnt[unit_of(a, p)] += n
        for (a, q), n in cap.items():
            if q == p - lag:
                den[unit_of(a, p)] += n
        for k, n in den.items():
            if n and cnt[k] >= N_MIN and cnt[k] / n >= R_MIN:
                out.add((k, p))
    return out


def sweep_cluster():
    """A and L2 generalized: k linked accounts, v captures per period each, report rate r, 4 periods."""
    rows = []
    for k, vols in ((8, (350, 1500, 5000)), (40, (75, 300, 1000))):
        for v in vols:
            for r in (0.005, 0.01, 0.015, 0.02, 0.03, 0.04, 0.06):
                accts = [dict(id=f'X{i}', start=0, end=120, vol=v, rate=r) for i in range(k)]
                rows.append({'accounts': k, 'captures_per_account_period': v, 'rate': r, **cluster_shares(accts)})
    return rows


def cluster_shares(accts, lag=None, seed0=20_000):
    """Share of runs in which the linked group, and any single account, is flagged, under both rules."""
    hits = defaultdict(int)
    for s in SWEEP_SEEDS:
        cap, rp = sim_counts(accts, random.Random(seed0 + s), lag)
        for rule, lg in RULES.items():
            hits[f'{rule}:cluster'] += bool(flagged(cap, rp, lambda a, p: 'cluster', lg))
            hits[f'{rule}:any_account'] += bool(flagged(cap, rp, lambda a, p: a, lg))
            hits[f'{rule}:high_rate_account'] += bool({k for k, q in flagged(cap, rp, lambda a, p: a, lg)} & {'H'})
    return {k: round(c / len(SWEEP_SEEDS), 3) for k, c in sorted(hits.items())}


def sweep_unequal():
    """Groups whose members differ: a combination flag, and dilution by large low-rate members (one false link each)."""
    cases = {
        'combination: H 1,500 at 5% + L 10,000 at 1.2%':
            [dict(id='H', start=0, end=120, vol=1500, rate=0.05), dict(id='L', start=0, end=120, vol=10000, rate=0.012)],
        'dilution: H 3,500 at 4% + 3 x L 10,000 at 0.3%':
            [dict(id='H', start=0, end=120, vol=3500, rate=0.04)]
            + [dict(id=f'L{i}', start=0, end=120, vol=10000, rate=0.003) for i in range(3)],
    }
    return {name: cluster_shares(accts) for name, accts in cases.items()}


def sweep_lag():
    """Scenario A's base cell and the successor case under faster and slower reporting."""
    a = [dict(id=f'X{i}', start=0, end=120, vol=350, rate=0.04) for i in range(8)]
    out = {}
    for name, lag in (('base', LAG), ('fast', LAG_FAST), ('slow', LAG_SLOW)):
        out[name] = {'A_cell': cluster_shares(a, lag), 'successor': successor_shares(3000, 0.003, lag),
                     'successor_high_rate': successor_shares(3000, 0.05, lag)}
    return out


def sweep_successor():
    """B generalized: predecessor volume and successor rate; flags in P5 (cluster) and by P6 (account)."""
    rows = []
    for vol in (1000, 3000, 6000):
        for r in (0.003, 0.01, 0.02, 0.03, 0.05):
            rows.append({'captures_per_period_each': vol, 'successor_rate': r, **successor_shares(vol, r)})
    return rows


def successor_shares(vol, r, lag=None):
    """Predecessor (5%) and successor at the same volume; flags in P4 and P5 (cluster) and by P6 (successor alone)."""
    accts = [dict(id='P', start=0, end=90, vol=vol, rate=0.05), dict(id='S', start=104, end=210, vol=vol, rate=r)]
    hits = defaultdict(int)
    for s in SWEEP_SEEDS:
        cap, rp = sim_counts(accts, random.Random(30_000 + s), lag)
        for rule, lg in RULES.items():
            cl = flagged(cap, rp, lambda a, p: 'cluster' if p >= 4 else a, lg)
            ac = flagged(cap, rp, lambda a, p: a, lg)
            hits[f'{rule}:cluster_P4'] += ('cluster', 4) in cl
            hits[f'{rule}:cluster_P5'] += ('cluster', 5) in cl
            hits[f'{rule}:successor_alone_by_P6'] += any(k == 'S' and q <= 6 for k, q in ac)
    return {k: round(c / len(SWEEP_SEEDS), 3) for k, c in sorted(hits.items())}


# ---------- extension: report attribution (scenario E) ----------
# Connected account E1 (fraudulent) and E2 (clean) on one platform. A share q of E1's reports is recorded at the
# platform account (as with destination charges, manuscript Section 8.2). A share u of all reports links to its
# payment only by card number and amount (unverified); half of those point to a payment on the other account.
E_ACCTS = [dict(id='E1', start=0, end=120, vol=3500, rate=0.04), dict(id='E2', start=0, end=120, vol=1000, rate=0.003)]
E_BASE = dict(q=0.3, u=0.2, w=0.5)


E_ACCTS_NEAR = [E_ACCTS[0], dict(id='E2', start=0, end=120, vol=7000, rate=0.013)]  # clean account near the floor


def e_draw(rng, q, u, w, accts=None):
    """Reports as (true account, recorded account, linked account, verified, arrival period); captures by account."""
    cap, reps = defaultdict(int), []
    for a in accts or E_ACCTS:
        other = 'E2' if a['id'] == 'E1' else 'E1'
        for p, lo, hi, n in slices(a):
            cap[a['id'], p] += n
            for _ in range(rng.binomialvariate(n, a['rate'])):
                arr = period(rng.uniform(lo, hi) + draw_lag(rng))
                recorded = 'PLAT-E' if a['id'] == 'E1' and rng.random() < q else a['id']
                verified = rng.random() >= u
                linked = a['id'] if verified or rng.random() >= w else other
                reps.append((a['id'], recorded, linked, verified, arr))
    return cap, reps


def e_views(cap, reps):
    """Flags for E1 and E2 under truth, recorded account, all links, and verified links with bounds."""
    def tally(key, keep=lambda r: True):
        rp = defaultdict(int)
        for r in reps:
            if keep(r):
                rp[key(r), r[4]] += 1
        return {a for a, p in flagged(cap, rp, lambda a, p: a)}
    truth = tally(lambda r: r[0])
    recorded = tally(lambda r: r[1])
    linked_all = tally(lambda r: r[2])
    lower = tally(lambda r: r[2], lambda r: r[3])
    upper = tally(lambda r: r[2] if r[3] else 'E1')  # every unverified report charged to E1
    upper2 = tally(lambda r: r[2] if r[3] else 'E2')  # every unverified report charged to E2
    out = {'truth': truth, 'recorded_account': recorded, 'all_links': linked_all}
    out['verified_links'] = {a: ('flag' if a in lower else 'inconclusive' if a in (upper if a == 'E1' else upper2)
                                 else 'no_flag') for a in ('E1', 'E2')}
    return out


def sweep_attribution(accts=None):
    rows = []
    for q in (0.0, 0.3, 0.6):
        for u in (0.0, 0.1, 0.2, 0.3, 0.5):
            agg = defaultdict(int)
            for s in SWEEP_SEEDS:
                v = e_views(*e_draw(random.Random(40_000 + s), q, u, E_BASE['w'], accts))
                for a in ('E1', 'E2'):
                    agg[f'{a}_truth'] += a in v['truth']
                    agg[f'{a}_recorded'] += a in v['recorded_account']
                    agg[f'{a}_all_links'] += a in v['all_links']
                    agg[f'{a}_verified_{v["verified_links"][a]}'] += 1
            n = len(SWEEP_SEEDS)
            rows.append({'q_recorded_at_platform': q, 'u_unverified': u,
                         **{k: round(c / n, 3) for k, c in sorted(agg.items())}})
    return rows


def e_records(seed):
    """Seed-specific E records at the base parameters, plus the generator's truth for each report (not a record)."""
    rng = random.Random(50_000 + seed)
    recs, truth, items = [], {}, {'E1': [], 'E2': []}
    for a in E_ACCTS:
        n_item = 0
        for p, lo, hi, n in slices(a):
            for i in range(n):
                t = lo + (i + 0.5) * (hi - lo) / n
                item = f"{a['id']}-{n_item:05d}"
                n_item += 1
                items[a['id']].append((item, t))
                recs.append({'record_type': 'ItemAttribution', 'record_id': f'IA-{item}',
                             'item': {'item_type': 'payment_attempt', 'item_id': item},
                             'merchant_account': a['id'], 'platform_account': 'PLAT-E',
                             'acquirer': {'status': 'known', 'value': ACQ},
                             'descriptor_static': {'status': 'known', 'value': f"SYN{a['id']}"},
                             'basis': 'platform ledger (synthetic)', 'verified': True,
                             'effective_from': iso(t), 'learned_at': iso(t)})
    k = 0
    for a in E_ACCTS:
        other = 'E2' if a['id'] == 'E1' else 'E1'
        for item, t in items[a['id']]:
            if rng.random() >= a['rate']:
                continue
            arr = t + draw_lag(rng)
            recorded = 'PLAT-E' if a['id'] == 'E1' and rng.random() < E_BASE['q'] else a['id']
            verified = rng.random() >= E_BASE['u']
            linked_item = item if verified or rng.random() >= E_BASE['w'] else \
                min(items[other], key=lambda x: abs(x[1] - t))[0]
            k += 1
            recs.append({'record_type': 'LabelEvent', 'record_id': f'LE-E{k:05d}', 'report_id': f'R-E{k:05d}',
                         'revision_kind': 'initial', 'report_type': 'dispute',
                         'source': 'issuer through the card network (synthetic)', 'reason': 'fraud',
                         'channel_id': CH, 'item': {'item_type': 'payment_attempt', 'item_id': linked_item},
                         'attribution': ({'basis': 'network transaction identifier', 'verified': True} if verified
                                         else {'basis': 'card number and amount only', 'verified': False}),
                         'amount': {'status': 'unknown', 'reason': 'amounts not modeled in this replay'},
                         'occurred_at': {'status': 'exact', 'value': iso(t)},
                         'reported_at': {'status': 'exact', 'value': iso(arr - 0.5)},
                         'arrived_at': iso(arr), 'learned_at': iso(arr + 5 / 1440),
                         'status': 'filed', 'adjudicated': 'not_applicable', 'truth_assessment_ids': [],
                         'recorded_at_account': recorded})
            truth[f'LE-E{k:05d}'] = a['id']
    return recs, truth


def e_from_records(recs, truth):
    """The four E views computed from records (truth from the generator)."""
    ia = {r['item']['item_id']: r['merchant_account'] for r in recs if r['record_type'] == 'ItemAttribution'}
    cap = defaultdict(int)
    for r in recs:
        if r['record_type'] == 'ItemAttribution':
            cap[r['merchant_account'], period(day_of(r['effective_from']))] += 1
    reps = [(truth[r['record_id']], r['recorded_at_account'], ia[r['item']['item_id']], r['attribution']['verified'],
             period(day_of(r['arrived_at']))) for r in recs if r['record_type'] == 'LabelEvent']
    v = e_views(cap, reps)
    return {'reports': len(reps), 'unverified': sum(1 for r in reps if not r[3]),
            'misattributed': sum(1 for r in reps if r[0] != r[2]), 'recorded_elsewhere': sum(1 for r in reps if r[1] != r[0]),
            'truth': sorted(v['truth']), 'recorded_account': sorted(v['recorded_account']),
            'all_links': sorted(v['all_links']), 'verified_links': v['verified_links']}


def main(out_dir):
    out_dir.mkdir(parents=True, exist_ok=True)
    schema = json.loads(oc.SCHEMA.read_text(encoding='utf-8'))
    base = build_records(1)
    e_recs, e_truth = e_records(1)
    recs = base + e_recs
    findings = oc.check(recs, schema)
    blob = json.dumps({'records': recs}, sort_keys=True).encode()
    (out_dir / 'records.json').write_bytes(blob)
    cap, rep, links = from_records(base)
    seed1 = {v: evaluate(cap, rep, links, v) for v in VIEWS}

    def series(view, accounts):
        return {p: [(k, c, n, s) for (k, q), (c, n, s, m) in sorted(seed1[view].items()) if q == p and m & accounts]
                for p in PERIODS}
    seed1_tables = {f'{t}:{v}': {p: rows for p, rows in series(v, TARGETS[t]).items() if rows}
                    for t in TARGETS for v in VIEWS}
    c1, _ = fast_draw(1)
    assert dict(c1) == dict(cap), 'captures in the records differ from the fast path'
    dist, esc, at, comp, totals = (defaultdict(list) for _ in range(5))
    for s in SEEDS:
        c2, r2 = fast_draw(s)
        totals['reports'].append(sum(r2.values()))
        for pred, succ in (('B0', 'B1'), ('B0c', 'B1c')):
            for q in (4, 5):
                pc = sum(n for (a, d, pp), n in r2.items() if a == pred and pp == q)
                sc = sum(n for (a, d, pp), n in r2.items() if a == succ and pp == q)
                comp[f'{succ}:P{q}'].append((pc, sc))
        for rule, lag in RULES.items():
            for v in VIEWS:
                ev = evaluate(c2, r2, links, v, lag)
                for m, (t, start) in METRICS.items():
                    dist[rule, m, v].append(first_flag(ev, TARGETS[t], start))
                dist[rule, 'D-new-unit', v].append(unit_first_flag(ev, f'{ACQ}/SYNSUPP'))
                for m, (accts, lo, hi) in ESCAPE.items():
                    esc[rule, m, v].append(escaped(ev, accts, lo, hi))
                for t in ('B1', 'B1c'):
                    for q in (4, 5, 6, 7):
                        at[rule, t, v, q].append(any(st == 'flag' and m & TARGETS[t]
                                                     for (k, pp), (c, n, st, m) in ev.items() if pp == q))
    summary = {}
    for (rule, t, v), xs in sorted(dist.items()):
        hit = [x for x in xs if x is not None]
        summary[f'{rule}:{t}:{v}'] = {'share_flagged_by_P9': round(len(hit) / len(xs), 3),
                                      'median_first_period': statistics.median(hit) if hit else None,
                                      'first_period_counts': {str(q): hit.count(q) for q in sorted(set(hit))}}
    esc_summary = {f'{rule}:{m}:{v}': {'mean_reports_without_ratio_test': round(statistics.mean(x[0] for x in xs), 1),
                                        'mean_flagged_periods': round(statistics.mean(x[1] for x in xs), 2),
                                        'periods': list(ESCAPE[m][1:])}
                   for (rule, m, v), xs in sorted(esc.items())}
    results = {
        'flagged_in_period_share': {f'{rule}:{t}:{v}:P{q}': round(sum(xs) / len(xs), 3)
                                    for (rule, t, v, q), xs in sorted(at.items())},
        'successor_cluster_composition': {k: {'mean_predecessor_reports': round(statistics.mean(x[0] for x in xs), 1),
                                              'mean_successor_reports': round(statistics.mean(x[1] for x in xs), 1)}
                                          for k, xs in sorted(comp.items())},
        'fast_path_reports': {'expected': round(sum(n * a['rate'] for a in ACCOUNTS for _, _, _, n in slices(a)), 1),
                              'mean': round(statistics.mean(totals['reports']), 1),
                              'sd': round(statistics.stdev(totals['reports']), 1),
                              'records_seed1': sum(rep.values()), 'captures_match_records': True},
        'escaped_reports_over_seeds': esc_summary,
        'conformance_findings_seed1': findings,
        'record_counts': {k: sum(1 for r in recs if r['record_type'] == k)
                          for k in sorted({r['record_type'] for r in recs})},
        'records_sha256': hashlib.sha256(blob).hexdigest(),
        'parameters': {'period_days': P, 'N_MIN': N_MIN, 'R_MIN': R_MIN, 'window_days': WINDOW, 'lag_mixture': LAG,
                       'seeds': [SEEDS.start, SEEDS.stop - 1],
                       'accounts': [{k: v for k, v in a.items()} for a in ACCOUNTS if k_first(a)]},
        'first_flag_over_seeds': summary,
        'seed1_tables': {k: {str(p): rows for p, rows in v.items()} for k, v in seed1_tables.items()},
        'pooled_ratio_check_seed1': pooled_check(cap, rep, links),
        'pooled_ratio_check_all_seeds': None,
        'maturity_A_seed1': maturity(base),
        'sensitivity_A': sensitivity(),
        'wrong_stores': wrong_stores(base, schema),
        'sweep_cluster': sweep_cluster(),
        'sweep_successor': sweep_successor(),
        'attribution_seed1_records': e_from_records(e_recs, e_truth),
        'sweep_attribution': sweep_attribution(),
        'sweep_attribution_clean_account_near_floor': sweep_attribution(E_ACCTS_NEAR),
        'sweep_unequal': sweep_unequal(),
        'sweep_lag': sweep_lag(),
    }
    held = exc = 0
    for s in SEEDS:
        pc = pooled_check(*fast_draw(s), links)  # tier 2 clusters, previous-period rule
        held += pc['cluster_periods_all_denominators_positive']
        exc += pc['pooled_exceeds_every_defined']
    results['pooled_ratio_check_all_seeds'] = {'held': held, 'exceeded_with_undefined_member': exc}
    (out_dir / 'results.json').write_text(json.dumps(results, indent=1, default=sorted), encoding='utf-8')
    print(json.dumps({'findings': len(findings), 'records': len(recs), 'sha256': results['records_sha256']}))


def k_first(a):
    """One representative account per scenario in the parameter listing."""
    return a['id'] in ('A1', 'B0', 'B1', 'B0c', 'B1c', 'D1', 'C01')


if __name__ == '__main__':
    main(Path(sys.argv[1]) if len(sys.argv) > 1 else Path('replay_out'))
