"""Merge the two coder sheets with the adjudication, and compute the counts fixed in README.md.

Usage: python3 adjudicate.py CLAUDE_SHEET CHATGPT_SHEET FINAL_RULINGS OUT_JSON

A cell the coders agree on keeps its mark, with both coders' paragraphs. A cell
they differ on takes the adjudication: the ruling where all three adjudicators
agree, otherwise `disputed` with the three readings kept. X1, X2 and O1 are not
adjudicated: both coders' entries are kept side by side.

Counts are given three ways: with `disputed` as its own category, and with every
disputed item at the lowest and at the highest reading any adjudicator gave
(README, note of 17 November 2026, 19:30). In each bound, the X4 tie follows the
sheet's rule: it is n/a unless X4 is yes and T1 or T2 is alleged.
"""
import copy
import json
import sys

import compare_sheets

TACTICS = compare_sheets.TACTICS
MARKS = ['alleged', 'not alleged', 'unclear', 'unavailable', 'disputed']
RANK = {'not alleged': 0, 'unclear': 1, 'alleged': 2, 'no': 0, 'yes': 1}
READ_BEFORE = ['U01', 'U06', 'U12']  # read for the paper before the protocol (README, limits)
GROUPS = {'could be exposed by the records': ['T1', 'T2', 'T3', 'T5', 'T6'],
          'no record exposes': ['T4'], 'not a record gap': ['T7']}


def by_num(ps):
    return sorted(set(ps), key=int)


def merge(a, b, rulings):
    A = {c['unit']: c for c in a['complaints']}
    B = {c['unit']: c for c in b['complaints']}
    R = {(r['unit'], r['field']): r for r in rulings}
    _, _, diffs = compare_sheets.compare(a, b)
    need = {(d[0], d[1]) for d in diffs}
    if set(R) != need:
        raise SystemExit(f'rulings do not match the differences: missing {sorted(need - set(R))}, extra {sorted(set(R) - need)}')
    out = []
    for u in sorted(A):
        c = {'unit': u}
        for f in TACTICS + ['X3', 'X4']:
            if (u, f) in R:
                r = R[(u, f)]
                if r.get('disputed'):
                    key = 'mark' if f.startswith('T') else 'answer'
                    c[f] = {key: 'disputed', 'readings': r['readings'], 'source': r['id']}
                else:
                    c[f] = dict(r['ruling'], paragraphs=by_num(r['ruling']['paragraphs']), source=r['id'])
            elif f.startswith('T'):
                c[f] = {'mark': A[u][f]['mark'], 'paragraphs': by_num(A[u][f]['paragraphs'] + B[u][f]['paragraphs']),
                        'quote': A[u][f]['quote'] or B[u][f]['quote'], 'source': 'agreed'}
            else:
                c[f] = dict(A[u][f], paragraphs=by_num(A[u][f]['paragraphs'] + B[u][f]['paragraphs']), source='agreed')
        c['X1'] = {'coder_1': A[u]['X1'], 'coder_2': B[u]['X1']}
        c['X2'] = {'coder_1': A[u]['X2'], 'coder_2': B[u]['X2']}
        c['O1'] = {'coder_1': A[u]['O1'], 'coder_2': B[u]['O1']}
        out.append(c)
    return out


def resolve(adj, bound):
    """Every disputed item at the lowest (bound='low') or highest ('high') reading given, then the tie rule."""
    pick = min if bound == 'low' else max
    res = copy.deepcopy(adj)
    for c in res:
        for t in TACTICS:
            if c[t]['mark'] == 'disputed':
                c[t] = {'mark': pick((r['mark'] for r in c[t]['readings']), key=RANK.get), 'source': c[t]['source'] + ' ' + bound}
        if c['X3']['answer'] == 'disputed':
            c['X3'] = {'answer': pick((r['answer'] for r in c['X3']['readings']), key=RANK.get), 'source': c['X3']['source'] + ' ' + bound}
        x4 = c['X4']
        ties = []
        if x4['answer'] == 'disputed':
            ties = [r.get('tied_to_T1_or_T2') for r in x4['readings'] if r.get('tied_to_T1_or_T2') in ('yes', 'no')]
            x4 = {'answer': pick((r['answer'] for r in x4['readings']), key=RANK.get), 'source': x4['source'] + ' ' + bound}
        elif x4.get('tied_to_T1_or_T2') in ('yes', 'no'):
            ties = [x4['tied_to_T1_or_T2']]
        t12 = 'alleged' in (c['T1']['mark'], c['T2']['mark'])
        if x4['answer'] == 'yes' and t12:
            if not ties:
                raise SystemExit(f"{c['unit']} X4: T1 or T2 is alleged in the {bound} bound but no reading gives a tie")
            tie = pick(ties, key=RANK.get)
        else:
            tie = 'n/a'
        c['X4'] = dict(x4, tied_to_T1_or_T2=tie)
    return res


def problems(adj):
    """In a sheet without disputed items, X4's tie must agree with the final T1 and T2 marks."""
    errs = []
    for c in adj:
        t12 = 'alleged' in (c['T1']['mark'], c['T2']['mark'])
        tie = c['X4'].get('tied_to_T1_or_T2')
        if c['X4']['answer'] == 'yes' and t12 and tie not in ('yes', 'no'):
            errs.append(f"{c['unit']} X4: T1 or T2 is alleged, so the tie must be yes or no, not {tie}")
        if (c['X4']['answer'] != 'yes' or not t12) and tie != 'n/a':
            errs.append(f"{c['unit']} X4: tie must be n/a, not {tie}")
    return errs


def tactic_counts(adj, units):
    cs = [c for c in adj if c['unit'] in units]
    return {t: {m: sum(c[t]['mark'] == m for c in cs) for m in MARKS} for t in TACTICS}


def counts(adj, units):
    cs = [c for c in adj if c['unit'] in units]
    res = {'complaints': len(cs), 'by_tactic': tactic_counts(adj, units), 'by_group': {}}
    for g, ts in GROUPS.items():
        res['by_group'][g] = {'complaints alleging at least one': sum(any(c[t]['mark'] == 'alleged' for t in ts) for c in cs)}
    res['no tactic alleged'] = sum(all(c[t]['mark'] == 'not alleged' for t in TACTICS) for c in cs)
    t12 = [c for c in cs if 'alleged' in (c['T1']['mark'], c['T2']['mark'])]
    res['T1 or T2 alleged'] = len(t12)
    res['of those, shared attribute tied to those accounts'] = sum(c['X4'].get('tied_to_T1_or_T2') == 'yes' for c in t12)
    res['of those, shared attribute alleged elsewhere only'] = sum(c['X4'].get('tied_to_T1_or_T2') == 'no' for c in t12)
    res['X3 rates or counts given'] = sum(c['X3']['answer'] == 'yes' for c in cs)
    res['open field: complaints with an entry (either coder)'] = sum(bool(c['O1']['coder_1'] or c['O1']['coder_2']) for c in cs)
    return res


def report(adj):
    units = [c['unit'] for c in adj]
    sets = {'all 14': units, 'without the three read before the protocol (U01, U06, U12)': [u for u in units if u not in READ_BEFORE]}
    out = {}
    for name, us in sets.items():
        out[name] = {'settled, with disputed': {'complaints': len(us), 'by_tactic': tactic_counts(adj, us)}}
        for bound in ('low', 'high'):
            res = resolve(adj, bound)
            errs = problems(res)
            if errs:
                raise SystemExit('\n'.join(errs))
            out[name][f'{bound} bound'] = counts(res, us)
    return out


def main():
    a, b, r = (json.load(open(p, encoding='utf-8')) for p in sys.argv[1:4])
    adj = merge(a, b, r)
    rep = report(adj)
    json.dump({'complaints': adj, 'counts': rep}, open(sys.argv[4], 'w', encoding='utf-8'), indent=1, ensure_ascii=False)
    print(json.dumps(rep, indent=1))


if __name__ == '__main__':
    main()
