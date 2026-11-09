#!/usr/bin/env python3
"""Replay: allegations in FTC v. AlliedWallet, Inc. et al., No. 2:19-cv-04355 (C.D. Cal.), ECF 24,
rebuilt as synthetic outcome records (Supplement S4.2).

All data are synthetic. Complaint content is allegation, not established fact. The monitoring thresholds are the
complaint's own descriptions (par. 72, 75, 92), not any network's current rules. Standard library only.

Usage: python3 tools/replays/allied_wallet_replay.py [OUT_DIR]
Writes records.json (seed 1) and results.json to OUT_DIR.
"""
import hashlib
import json
import math
import random
import statistics
import sys
from collections import defaultdict
from datetime import datetime, timedelta, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import outcome_conformance as oc  # noqa: E402

T0 = datetime(2015, 7, 1, tzinfo=timezone.utc)   # day 0: Stark's account approved in July 2015 (par. 91)
P = 30
PERIODS = range(1, 9)                             # days 0 to 240
SEEDS = range(1, 1001)

# Monitoring rules as the complaint describes them, same-month denominators (par. 72, 75, 92)
CB_MIN, CB_RATIO = 100, 0.01                      # chargeback count and count ratio
FR_DOLLARS, FR_RATIO = 75_000, 0.01               # fraud-report dollars, or dollar ratio ("either", par. 92)

# Stark group (par. 88-99): three accounts, one payout beneficiary (par. 89)
DAY_S_OFF, DAY_AT_OFF, DAY_RP_OFF = 119, 152, 216  # 28 Oct 2015 (par. 95), 30 Nov 2015 (par. 97), 2 Feb 2016 (par. 99)
VOL = 185                                           # payments per account-period: about $1.15m over 7.2 periods (par. 103)
TICKET_MU, TICKET_SIGMA = math.log(250), 0.6        # lognormal amount, mean about $300 (assumed)
R_REPORT = 0.0314                                   # mean of the four monthly fraud ratios in par. 93
Q_REFUND = 0.2                                      # share refunded before a dispute; sets chargebacks near 2.5% (par. 91)
LAG = [(0.35, 5, 30), (0.40, 30, 60), (0.18, 60, 90), (0.07, 90, 118)]  # capture to cardholder claim (assumed)
CH_CB, CH_EFW, ACQ = 'CH-CB', 'CH-EFW', 'AQ-SYN-EU'


def iso(day):
    return (T0 + timedelta(days=day)).strftime('%Y-%m-%dT%H:%M:%SZ')


def period(day):
    return int(day // P) + 1


def draw_lag(rng):
    u, acc = rng.random(), 0.0
    for w, lo, hi in LAG:
        acc += w
        if u < acc:
            return rng.uniform(lo, hi)
    return rng.uniform(LAG[-1][1], LAG[-1][2])


def segments():
    """(account, start, end, rate multiplier): Stark's and Atlantic's traffic moves to Rolling Plains (par. 96-97)."""
    return [('S', 0, DAY_S_OFF, 1), ('AT', 0, DAY_AT_OFF, 1),
            ('RP', 0, DAY_S_OFF, 1), ('RP', DAY_S_OFF, DAY_AT_OFF, 2), ('RP', DAY_AT_OFF, DAY_RP_OFF, 3)]


def payments(rng):
    """Yield (account, capture day, amount in cents) for the Stark group."""
    for acct, lo, hi, mult in segments():
        n = round(VOL * mult * (hi - lo) / P)
        for i in range(n):
            yield acct, lo + (i + 0.5) * (hi - lo) / n, round(rng.lognormvariate(TICKET_MU, TICKET_SIGMA) * 100)


def outcomes(rng, t):
    """None, or (claim day, EFW arrival, refund day or None, chargeback arrival or None) for one payment."""
    if rng.random() >= R_REPORT:
        return None
    claim = t + draw_lag(rng)
    efw = claim + rng.uniform(0.5, 7)
    if rng.random() < Q_REFUND:
        return claim, efw, claim + rng.uniform(0, 4), None   # refund prevents the dispute, not the fraud report
    return claim, efw, None, claim + rng.uniform(5, 20)


# ---------- monitoring ----------
def tallies(seed):
    rng = random.Random(seed)
    sales_n, sales_c, cb, fr_c, fr_n, refunded_clean = (defaultdict(int) for _ in range(6))
    for acct, t, cents in payments(rng):
        p = period(t)
        sales_n[acct, p] += 1
        sales_c[acct, p] += cents
        o = outcomes(rng, t)
        if o is None:
            continue
        claim, efw, ref, chb = o
        fr_c[acct, period(efw)] += cents
        fr_n[acct, period(efw)] += 1
        if chb is not None:
            cb[acct, period(chb)] += 1
        else:
            refunded_clean[acct] += 1
    return sales_n, sales_c, cb, fr_c, fr_n, refunded_clean


def flags(sales_n, sales_c, cb, fr_c, unit):
    """{(program, unit, period): status} with status flag, below or undefined (reports and no same-month sales)."""
    out = {}
    for p in PERIODS:
        n, c, k, f = defaultdict(int), defaultdict(int), defaultdict(int), defaultdict(int)
        for (a, q), v in sales_n.items():
            if q == p:
                n[unit(a)] += v
        for (a, q), v in sales_c.items():
            if q == p:
                c[unit(a)] += v
        for (a, q), v in cb.items():
            if q == p:
                k[unit(a)] += v
        for (a, q), v in fr_c.items():
            if q == p:
                f[unit(a)] += v
        for u in set(n) | set(k) | set(f):
            out['CB', u, p] = ('undefined' if not n[u] else
                               'flag' if k[u] >= CB_MIN and k[u] / n[u] >= CB_RATIO else 'below')
            dollars = f[u] / 100
            out['FR', u, p] = ('flag' if dollars >= FR_DOLLARS else 'undefined' if not c[u] else
                               'flag' if f[u] / c[u] >= FR_RATIO else 'below')
    return out


def monte_carlo():
    first = defaultdict(list)
    cb_any = undefined_fr = 0
    max_cb, refunded, late_n, late_usd, after_n, after_usd = [], [], [], [], [], []
    for s in SEEDS:
        sn, sc, cb, fr, fn, rc = tallies(10_000 + s)
        refunded.append(sum(rc.values()))
        late_n.append(sum(v for k, v in fn.items() if not sn.get(k) and k[1] in PERIODS))
        late_usd.append(sum(v for k, v in fr.items() if not sn.get(k) and k[1] in PERIODS) / 100)
        after_n.append(sum(v for k, v in fn.items() if k[1] not in PERIODS))
        after_usd.append(sum(v for k, v in fr.items() if k[1] not in PERIODS) / 100)
        max_cb.append(max(cb.values(), default=0))
        acc = flags(sn, sc, cb, fr, lambda a: a)
        grp = flags(sn, sc, cb, fr, lambda a: 'group')
        cb_any += any(v == 'flag' for (prog, u, p), v in list(acc.items()) + list(grp.items()) if prog == 'CB')
        undefined_fr += sum(1 for (prog, u, p), v in acc.items() if prog == 'FR' and v == 'undefined')
        for view, fl in (('account', acc), ('group', grp)):
            for u in sorted({u for _, u, _ in fl}):
                hits = sorted(p for (prog, uu, p), v in fl.items() if prog == 'FR' and uu == u and v == 'flag')
                first[view, u].append(hits[0] if hits else None)
                first[view, u + ':flagged_periods'].append(len(hits))
    n = len(SEEDS)
    res = {'cb_program_ever_flags_share': round(cb_any / n, 3),
           'max_monthly_chargebacks_any_account': {'mean': round(statistics.mean(max_cb), 1), 'max': max(max_cb)},
           'refunded_reported_payments_per_run': round(statistics.mean(refunded), 1),
           'fr_account_periods_with_reports_but_no_sales_per_run': round(undefined_fr / n, 2),
           'fraud_reports_on_closed_accounts_by_day_240_per_run': {'count': round(statistics.mean(late_n), 1),
                                                                    'usd': round(statistics.mean(late_usd))},
           'fraud_reports_after_day_240_per_run': {'count': round(statistics.mean(after_n), 1),
                                                   'usd': round(statistics.mean(after_usd))}}
    for (view, u), xs in sorted(first.items()):
        if u.endswith(':flagged_periods'):
            res[f'{view}:{u}'] = round(statistics.mean(xs), 2)
        else:
            hit = [x for x in xs if x is not None]
            res[f'{view}:{u}:first_FR_flag'] = {'share': round(len(hit) / n, 3),
                                                'counts': {str(q): hit.count(q) for q in sorted(set(hit))}}
    return res


# ---------- records for seed 1 ----------
def channel(cid, name, adjudicates):
    return {'record_type': 'OutcomeChannel', 'record_id': f'{cid}-v1', 'channel_id': cid, 'name': name, 'rail': 'card',
            'clock_start_event': 'processing date of the payment',
            'reporting_window': {'status': 'defined', 'days': 120, 'source': 'illustrative network rule (synthetic)',
                                 'rule_version': 'SYN-CB-1'},
            'window_depends_on': ['claim type'], 'adjudicates_truth': adjudicates, 'learned_at': iso(-5)}


def label(rid, rtype, cid, item, cents, t, arr, attribution_id):
    return {'record_type': 'LabelEvent', 'record_id': rid, 'report_id': rid.replace('LE-', 'R-'), 'revision_kind': 'initial',
            'report_type': rtype, 'source': 'issuer through the card network (synthetic)', 'reason': 'fraud',
            'channel_id': cid, 'item': item, 'attribution': {'basis': attribution_id, 'verified': True},
            'amount': {'status': 'known', 'value_minor': cents, 'currency': 'USD'},
            'occurred_at': {'status': 'exact', 'value': iso(t)}, 'reported_at': {'status': 'exact', 'value': iso(arr - 0.5)},
            'arrived_at': iso(arr), 'learned_at': iso(arr + 5 / 1440), 'status': 'filed',
            'adjudicated': 'not_applicable', 'truth_assessment_ids': []}


def control(did, kind, item_type, item_id, day, authority, effects):
    return {'record_type': 'ControlAction', 'record_id': f'{did}-rec', 'decision_id': did, 'decision_kind': kind,
            'targets': [{'item_type': item_type, 'item_id': item_id}], 'decided_at': iso(day), 'learned_at': iso(day),
            'authority': authority, 'rule_or_model_version': 'SYN-1',
            'channel_effects': [{'channel_id': c, 'effect': e} for c, e in effects]}


def build_records(seed):
    rng = random.Random(10_000 + seed)   # the same draws as tallies(10_000 + seed)
    recs = [channel(CH_CB, 'card chargeback, fraud reason', 'yes'),
            channel(CH_EFW, 'issuer fraud report (early fraud warning)', 'no')]
    for acct, day in (('S', DAY_S_OFF), ('AT', DAY_AT_OFF), ('RP', DAY_RP_OFF)):
        recs.append(control(f'D-{acct}-CLOSE', 'close_account', 'account', acct, day, 'facilitator risk review (synthetic)',
                            [(CH_CB, 'none'), (CH_EFW, 'none')]))
    for a in ('S', 'AT'):
        recs.append({'record_type': 'EntityLink', 'record_id': f'EL-PAY-{a}-RP', 'link_type': 'other',
                     'from': {'entity_type': 'account', 'entity_id': a}, 'to': {'entity_type': 'account', 'entity_id': 'RP'},
                     'basis': 'same payout beneficiary on both accounts (modeled on par. 89)', 'basis_kind': 'verified_identifier',
                     'verified': True, 'confidence': 'high',
                     'confounders': ['one business operating several storefronts under one merchant of record'],
                     'effective_from': iso(0), 'learned_at': iso(0), 'source': 'facilitator payout records (synthetic)',
                     'purpose_scope': 'fraud investigation'})
        recs.append({'record_type': 'EntityLink', 'record_id': f'EL-WEB-{a}-RP', 'link_type': 'other',
                     'from': {'entity_type': 'account', 'entity_id': a}, 'to': {'entity_type': 'account', 'entity_id': 'RP'},
                     'basis': 'websites built from one developer template (modeled on par. 89, 94)', 'basis_kind': 'shared_attribute',
                     'verified': False, 'confidence': 'low', 'confounders': ['a developer template used by unrelated clients'],
                     'effective_from': iso(0), 'learned_at': iso(0), 'source': 'underwriting review (synthetic)',
                     'purpose_scope': 'fraud investigation'})
    n_item, k = defaultdict(int), 0
    for acct, t, cents in payments(rng):
        item_id = f'{acct}-{n_item[acct]:05d}'
        n_item[acct] += 1
        item = {'item_type': 'payment_attempt', 'item_id': item_id}
        recs.append({'record_type': 'ItemAttribution', 'record_id': f'IA-{item_id}', 'item': item, 'merchant_account': acct,
                     'platform_account': 'PF-1', 'acquirer': {'status': 'known', 'value': ACQ},
                     'descriptor_static': {'status': 'known', 'value': f'AW*{acct}'}, 'basis': 'facilitator ledger (synthetic)',
                     'verified': True, 'effective_from': iso(t), 'learned_at': iso(t)})
        o = outcomes(rng, t)
        if o is None:
            continue
        claim, efw, ref, chb = o
        k += 1
        recs.append(label(f'LE-EFW-{k:05d}', 'early_fraud_warning', CH_EFW, item, cents, t, efw, 'network transaction identifier'))
        if ref is not None:
            recs.append(control(f'D-REF-{k:05d}', 'other', 'payment_attempt', item_id, ref,
                                'business refund before dispute (synthetic)', [(CH_CB, 'closed'), (CH_EFW, 'none')]))
            recs.append({'record_type': 'ChannelStateTransition', 'record_id': f'T-REF-{k:05d}', 'item': item, 'channel_id': CH_CB,
                         'state': 'closed', 'effective_from': iso(ref), 'cause': {'kind': 'decision', 'decision_id': f'D-REF-{k:05d}'},
                         'learned_at': iso(ref)})
        else:
            recs.append(label(f'LE-CB-{k:05d}', 'dispute', CH_CB, item, cents, t, chb, 'network transaction identifier'))
    return recs


def wrong_stores(recs, schema):
    """Altered stores: two should be rejected; omitting refund closures passes every rule."""
    refunds = [r for r in recs if r['record_type'] == 'ControlAction' and r['decision_id'].startswith('D-REF-')]
    both = {r['decision_id'] for r in refunds}
    w_both = [dict(r, channel_effects=[{'channel_id': CH_CB, 'effect': 'closed'}, {'channel_id': CH_EFW, 'effect': 'closed'}])
              if r.get('decision_id') in both and r['record_type'] == 'ControlAction' else r for r in recs]
    w_both += [{'record_type': 'ChannelStateTransition', 'record_id': f"WT-{r['decision_id']}", 'item': r['targets'][0] | {},
                'channel_id': CH_EFW, 'state': 'closed', 'effective_from': r['decided_at'],
                'cause': {'kind': 'decision', 'decision_id': r['decision_id']}, 'learned_at': r['decided_at']} for r in refunds]
    w_omit = [r for r in recs if not (r['record_type'] == 'ChannelStateTransition' and r['record_id'].startswith('T-REF-'))
              and not (r['record_type'] == 'ControlAction' and r['decision_id'].startswith('D-REF-'))]
    w_link = [dict(r, verified=True, confidence='high') if r['record_type'] == 'EntityLink' and r['basis_kind'] == 'shared_attribute'
              else r for r in recs]
    res = {}
    for name, rs in (('refund_recorded_as_closing_both_channels', w_both), ('refund_closures_omitted', w_omit),
                     ('template_link_marked_verified', w_link)):
        f = oc.check(rs, schema)
        res[name] = {'rules': sorted({x[0] for x in f}), 'findings': len(f), 'first': f[:2]}
    return res


def displacement(recs):
    """Captures per account and for the payout-linked group, by period, from the records."""
    caps = defaultdict(int)
    for r in recs:
        if r['record_type'] == 'ItemAttribution':
            d = (datetime.strptime(r['effective_from'], '%Y-%m-%dT%H:%M:%SZ').replace(tzinfo=timezone.utc) - T0).days
            caps[r['merchant_account'], period(d)] += 1
    rows = {}
    for p in PERIODS:
        row = {a: caps.get((a, p), 0) for a in ('S', 'AT', 'RP')}
        row['group'] = sum(row.values())
        rows[str(p)] = row
    return rows


def label_errors(recs):
    """Reported payments a chargeback-only store reads as having no report, and why."""
    efw = {r['item']['item_id'] for r in recs if r['record_type'] == 'LabelEvent' and r['channel_id'] == CH_EFW}
    cbk = {r['item']['item_id'] for r in recs if r['record_type'] == 'LabelEvent' and r['channel_id'] == CH_CB}
    closed = {r['item']['item_id'] for r in recs if r['record_type'] == 'ChannelStateTransition' and r['state'] == 'closed'}
    refunded_first = sum(1 for r in recs if r['record_type'] == 'LabelEvent' and r['channel_id'] == CH_EFW
                         and r['item']['item_id'] in closed and any(
                             c['record_type'] == 'ChannelStateTransition' and c['item']['item_id'] == r['item']['item_id']
                             and c['effective_from'] < r['arrived_at'] for c in recs if c['record_type'] == 'ChannelStateTransition'))
    return {'fraud_reports': len(efw), 'chargebacks': len(cbk), 'reported_without_chargeback': len(efw - cbk),
            'of_which_dispute_channel_closed_by_refund': len((efw - cbk) & closed),
            'fraud_report_arrived_after_refund': refunded_first}


# ---------- padding (par. 75-76, 82-86): arithmetic, not simulated ----------
SCALES = {'Stark group (par. 103)': 167_000, 'Digital Altitude first month (par. 144)': 600_000,
          'TelexFree peak month (par. 108)': 11_000_000, 'opportunity Wells described (par. 83)': 70_000_000}
TICKET = 300                 # assumed sale amount
CB_RATE = 0.025              # par. 91
FR_RATE = 0.0314             # par. 93, mean
FEE_PCT, FEE_FIXED = 0.04, 0.30   # assumed processing fees on padded purchases
TARGET = 0.009               # padding aims just under the 1% ratios
PAD_SMALL, PAD_LARGE = 1, 500    # assumed padded purchase amounts


def padding():
    rows = []
    for name, sales in SCALES.items():
        n = sales / TICKET
        cb, fraud = n * CB_RATE, sales * FR_RATE
        cb_applies = cb >= CB_MIN
        pad_n = max(0.0, cb / TARGET - n) if cb_applies else 0.0
        pad_d = max(0.0, fraud / TARGET - sales)
        cost_count = pad_n * (FEE_PCT * PAD_SMALL + FEE_FIXED)
        cost_dollar = pad_d * FEE_PCT + (pad_d / PAD_LARGE) * FEE_FIXED
        rows.append({'merchant': name, 'sales_usd_per_month': sales, 'sales_count': round(n),
                     'chargebacks': round(cb), 'fraud_report_usd': round(fraud),
                     'cb_program_flags_unpadded': cb_applies and CB_RATE >= CB_RATIO,
                     'count_padding_purchases': round(pad_n), 'count_padding_cost_pct_of_sales': round(100 * cost_count / sales, 2),
                     'dollar_padding_usd': round(pad_d), 'dollar_padding_cost_pct_of_sales': round(100 * cost_dollar / sales, 2),
                     'fraud_dollars_reach_75k_either_reading': fraud >= FR_DOLLARS})
    return rows


def main(out_dir):
    out_dir.mkdir(parents=True, exist_ok=True)
    schema = json.loads(oc.SCHEMA.read_text(encoding='utf-8'))
    recs = build_records(1)
    findings = oc.check(recs, schema)
    blob = json.dumps({'records': recs}, sort_keys=True).encode()
    (out_dir / 'records.json').write_bytes(blob)
    sn, sc, cb, fr, fn, rc = tallies(10_001)
    assert sum(sn.values()) == sum(1 for r in recs if r['record_type'] == 'ItemAttribution')
    assert sum(cb.values()) == sum(1 for r in recs if r['record_type'] == 'LabelEvent' and r['channel_id'] == CH_CB)
    results = {
        'conformance_findings_seed1': findings,
        'record_counts': {k: sum(1 for r in recs if r['record_type'] == k) for k in sorted({r['record_type'] for r in recs})},
        'records_sha256': hashlib.sha256(blob).hexdigest(),
        'label_errors_seed1': label_errors(recs),
        'displacement_seed1': displacement(recs),
        'wrong_stores': wrong_stores(recs, schema),
        'monte_carlo': monte_carlo(),
        'padding': padding(),
        'parameters': {'period_days': P, 'CB_MIN': CB_MIN, 'CB_RATIO': CB_RATIO, 'FR_DOLLARS': FR_DOLLARS, 'FR_RATIO': FR_RATIO,
                       'VOL': VOL, 'R_REPORT': R_REPORT, 'Q_REFUND': Q_REFUND, 'lag': LAG,
                       'closures': [DAY_S_OFF, DAY_AT_OFF, DAY_RP_OFF], 'seeds': [SEEDS.start, SEEDS.stop - 1]},
    }
    (out_dir / 'results.json').write_text(json.dumps(results, indent=1, sort_keys=True), encoding='utf-8')
    print(json.dumps({'findings': len(findings), 'records': len(recs), 'sha256': results['records_sha256']}))


if __name__ == '__main__':
    main(Path(sys.argv[1]) if len(sys.argv) > 1 else Path('replay_out'))
