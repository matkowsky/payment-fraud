#!/usr/bin/env python3
"""Parameter sweeps for the two FTC replays (Supplement S10): where each view of the outcome records stops
flagging, and how often a view flags merchants assumed legitimate.

All data are synthetic and every parameter is an assumption. Complaint content is allegation. The generating
processes and monitoring rules are the replays' own (ftc_first_data_replay.py, allied_wallet_replay.py); each
point is 500 runs with seeds separate from the replays' main results, which this script leaves unchanged.
Standard library only; Python 3.12 or later.

Usage: python3 tools/replays/sweeps.py [OUT_DIR]   about three minutes
       python3 tools/replays/sweeps.py --figure      redraw the figure from SUPPLEMENT/S10_REPLAYS/sweep_results.json
Writes sweep_results.json to OUT_DIR (default SUPPLEMENT/S10_REPLAYS) and FIGURES/FIG3_REPLAY_SWEEPS.svg.
"""
import json
import random
import sys
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import allied_wallet_replay as aw  # noqa: E402
import ftc_first_data_replay as fd  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]
SEEDS = range(1, 501)
RULE = 'SYN-MON-1'   # First Data: the previous period's captures as denominator, as in S10's main figures

# First Data, scenario A: eight related accounts at the alleged 4 percent, splitting a volume.
SPLIT_VOLUMES = [100, 150, 200, 250, 300, 350, 400, 500, 700, 1000, 1500, 2000, 2500, 3000, 3500, 4000, 5000]
# First Data: the linked view at one report rate, for the eight related accounts and the forty merchants
# assumed legitimate that share a call center (scenario L2).
RATES = [0.005, 0.0075, 0.01, 0.0125, 0.015, 0.0175, 0.02, 0.025, 0.03, 0.035, 0.04, 0.045, 0.05, 0.06]
GROUPS = {'8 related accounts, 350 captures each': (8, 350), '40 merchants assumed legitimate, 300 captures each': (40, 300)}
# Allied Wallet: one account at the complaint's fraud-report rate, and one at an assumed legitimate rate.
AW_VOLUMES = [25, 50, 100, 185, 300, 500, 1000, 2000, 3000, 4000, 5000, 6000, 8000]
AW_RATES = {'alleged 3.14 percent': aw.R_REPORT, 'assumed legitimate 0.3 percent': 0.003}


def first_data_split():
    rows = []
    for v in SPLIT_VOLUMES:
        s = fd.cluster_shares([dict(id=f'X{i}', start=0, end=120, vol=v, rate=0.04) for i in range(8)])
        rows.append({'captures_per_account_period': v, 'account_view': s[f'{RULE}:any_account'],
                     'linked_view': s[f'{RULE}:cluster']})
    return rows


def first_data_rates():
    out = {}
    for name, (k, v) in GROUPS.items():
        out[name] = []
        for r in RATES:
            s = fd.cluster_shares([dict(id=f'X{i}', start=0, end=120, vol=v, rate=r) for i in range(k)])
            out[name].append({'rate': r, 'account_view': s[f'{RULE}:any_account'], 'linked_view': s[f'{RULE}:cluster']})
    return out


def aw_tallies(rng, n, r):
    """One account with n payments a month for the replay's eight months; reports as in allied_wallet_replay."""
    sales_n, sales_c, cb, fr_c = (defaultdict(int) for _ in range(4))
    for p in aw.PERIODS:
        lo = (p - 1) * aw.P
        sales_n['X', p] = n
        sales_c['X', p] = sum(round(rng.lognormvariate(aw.TICKET_MU, aw.TICKET_SIGMA) * 100) for _ in range(n))
        for _ in range(rng.binomialvariate(n, r)):
            t = rng.uniform(lo, lo + aw.P)
            cents = round(rng.lognormvariate(aw.TICKET_MU, aw.TICKET_SIGMA) * 100)
            claim = t + aw.draw_lag(rng)
            fr_c['X', aw.period(claim + rng.uniform(0.5, 7))] += cents
            if rng.random() >= aw.Q_REFUND:
                cb['X', aw.period(claim + rng.uniform(5, 20))] += 1
    return sales_n, sales_c, cb, fr_c


def allied_wallet():
    out = {}
    for name, r in AW_RATES.items():
        out[name] = []
        for n in AW_VOLUMES:
            hits = defaultdict(int)
            for s in SEEDS:
                fl = aw.flags(*aw_tallies(random.Random(40_000 + s), n, r), lambda a: a)
                for prog in ('CB', 'FR'):
                    hits[prog] += any(v == 'flag' for (pg, _, _), v in fl.items() if pg == prog)
            out[name].append({'payments_per_month': n, 'chargeback_rule': round(hits['CB'] / len(SEEDS), 3),
                              'fraud_report_rule': round(hits['FR'] / len(SEEDS), 3)})
    return out


# ---------- figure ----------
FONT = 'DejaVu Sans,Arial,sans-serif'
INK, GRID, MUTED = '#213447', '#d5dde3', '#657e91'
STYLES = [('#213447', '', 'circle'), ('#b4532a', '9 6', 'square'), ('#4f7f3a', '2 5', 'triangle')]
PW, PH, LEFT, TOP = 225, 140, 64, 58   # plot width and height, left margin and top of each panel


def panel(x0, title, x_label, series, xlog, xticks, vline=None):
    """One panel: series is [(label, [(x, y)]), ...] drawn with STYLES in order; y is a share of runs."""
    import math
    fx = (lambda x: math.log10(x)) if xlog else (lambda x: x)
    lo, hi = fx(xticks[0][0]), fx(xticks[-1][0])
    X = lambda x: x0 + LEFT + (fx(x) - lo) / (hi - lo) * PW
    Y = lambda y: TOP + (1 - y) * PH
    t = lambda x, y, txt, size=21, anchor='start', fill=INK, weight='normal': (
        f'<text x="{x:.1f}" y="{y:.1f}" text-anchor="{anchor}" font-family="{FONT}" font-size="{size}" '
        f'font-weight="{weight}" fill="{fill}">{txt}</text>')
    out = [t(x0 + LEFT - 52, TOP - 26, title, 22, weight='bold')]
    for y, lab in ((0, '0'), (0.5, '50%'), (1, '100%')):
        out.append(f'<line x1="{x0 + LEFT}" y1="{Y(y):.1f}" x2="{x0 + LEFT + PW}" y2="{Y(y):.1f}" stroke="{GRID}" />')
        out.append(t(x0 + LEFT - 8, Y(y) + 7, lab, anchor='end'))
    for x, lab in xticks:
        out.append(f'<line x1="{X(x):.1f}" y1="{TOP + PH}" x2="{X(x):.1f}" y2="{TOP + PH + 6}" stroke="{INK}" />')
        out.append(t(X(x), TOP + PH + 28, lab, anchor='middle'))
    out.append(f'<line x1="{x0 + LEFT}" y1="{TOP + PH}" x2="{x0 + LEFT + PW}" y2="{TOP + PH}" stroke="{INK}" />')
    out.append(t(x0 + LEFT + PW / 2, TOP + PH + 56, x_label, anchor='middle'))
    if vline:
        out.append(f'<line x1="{X(vline[0]):.1f}" y1="{TOP}" x2="{X(vline[0]):.1f}" y2="{TOP + PH}" stroke="{MUTED}" stroke-dasharray="3 4" />')
    for (label, pts), (color, dash, mark) in zip(series, STYLES):
        d = ' '.join(f'{X(x):.1f},{Y(y):.1f}' for x, y in pts)
        out.append(f'<polyline points="{d}" fill="none" stroke="{color}" stroke-width="2.5"'
                   + (f' stroke-dasharray="{dash}"' if dash else '') + ' />')
        for x, y in pts:
            cx, cy = X(x), Y(y)
            out.append(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="4" fill="{color}" />' if mark == 'circle' else
                       f'<rect x="{cx - 4:.1f}" y="{cy - 4:.1f}" width="8" height="8" fill="{color}" />' if mark == 'square' else
                       f'<polygon points="{cx:.1f},{cy - 5:.1f} {cx - 5:.1f},{cy + 4:.1f} {cx + 5:.1f},{cy + 4:.1f}" fill="{color}" />')
    for i, (label, _) in enumerate(series):
        color, dash, _ = STYLES[i]
        ly = TOP + PH + 86 + i * 26
        out.append(f'<line x1="{x0 + LEFT - 52}" y1="{ly - 7}" x2="{x0 + LEFT - 16}" y2="{ly - 7}" stroke="{color}" stroke-width="2.5"'
                   + (f' stroke-dasharray="{dash}"' if dash else '') + ' />')
        out.append(t(x0 + LEFT - 8, ly, label))
    return out


def figure(res):
    split, rates, awr = res['first_data_split'], res['first_data_rates'], res['allied_wallet']
    g = list(GROUPS)
    a = panel(40, 'A. Splitting a volume', 'Captures per account a period', [
        ('Account view', [(r['captures_per_account_period'], r['account_view']) for r in split]),
        ('Linked view', [(r['captures_per_account_period'], r['linked_view']) for r in split])],
        True, [(100, '100'), (300, '300'), (1000, '1,000'), (5000, '5,000')])
    b = panel(376, 'B. Two linked groups', 'Report rate (percent)', [
        ('8 related accounts', [(r['rate'] * 100, r['linked_view']) for r in rates[g[0]]]),
        ('40 legitimate merchants', [(r['rate'] * 100, r['linked_view']) for r in rates[g[1]]])],
        False, [(0, '0'), (1.5, '1.5'), (3, '3'), (4.5, '4.5'), (6, '6')], vline=(1.5, None))
    al, lg = awr['alleged 3.14 percent'], awr['assumed legitimate 0.3 percent']
    c = panel(712, 'C. Two channels', 'Payments a month', [
        ('Chargebacks, alleged', [(r['payments_per_month'], r['chargeback_rule']) for r in al]),
        ('Fraud reports, alleged', [(r['payments_per_month'], r['fraud_report_rule']) for r in al]),
        ('Fraud reports, legitimate', [(r['payments_per_month'], r['fraud_report_rule']) for r in lg])],
        True, [(25, '25'), (100, '100'), (1000, '1,000'), (8000, '8,000')])
    w, h = 1038, TOP + PH + 86 + 2 * 26 + 8
    ylab = (f'<text x="0" y="0" transform="translate(22,{TOP + PH / 2:.1f}) rotate(-90)" text-anchor="middle" '
            f'font-family="{FONT}" font-size="21" fill="{INK}">Runs flagged</text>')
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">'
            f'<rect width="{w}" height="{h}" fill="white" />\n' + '\n'.join([ylab] + a + b + c) + '\n</svg>\n')


def main(out_dir):
    res = {'note': 'Synthetic; every parameter is an assumption; complaint content is allegation. Share of 500 runs in '
                   'which the view flags at least once.',
           'runs_per_point': len(SEEDS), 'first_data_rule': RULE,
           'first_data_split': first_data_split(), 'first_data_rates': first_data_rates(), 'allied_wallet': allied_wallet()}
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / 'sweep_results.json').write_text(json.dumps(res, indent=1) + '\n', encoding='utf-8')
    (ROOT / 'FIGURES' / 'FIG3_REPLAY_SWEEPS.svg').write_text(figure(res), encoding='utf-8')
    print(json.dumps({'points': len(SPLIT_VOLUMES) + len(RATES) * len(GROUPS) + len(AW_VOLUMES) * len(AW_RATES)}))


if __name__ == '__main__':
    if sys.argv[1:2] == ['--figure']:   # redraw the figure from saved results
        res = json.loads((ROOT / 'SUPPLEMENT' / 'S10_REPLAYS' / 'sweep_results.json').read_text(encoding='utf-8'))
        (ROOT / 'FIGURES' / 'FIG3_REPLAY_SWEEPS.svg').write_text(figure(res), encoding='utf-8')
    else:
        main(Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / 'SUPPLEMENT' / 'S10_REPLAYS')
