"""Merge the two coder sheets with the rulings, and compute the counts fixed in README.md.

Usage: python3 adjudicate.py CLAUDE_SHEET CHATGPT_SHEET RULINGS OUT_JSON

A cell the coders agree on keeps its mark, with both coders' paragraphs. A cell
they differ on takes the ruling. Every ruled cell names its ruling. X1, X2 and
O1 are not ruled: both coders' entries are kept side by side. An agreed X4 tie
becomes n/a when the rulings leave neither T1 nor T2 alleged (the sheet's rule).
"""
import json
import sys

import compare_sheets

TACTICS = compare_sheets.TACTICS
MARKS = ['alleged', 'not alleged', 'unclear', 'unavailable']
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
        for t in TACTICS:
            if (u, t) in R:
                r = R[(u, t)]
                c[t] = {'mark': r['ruling']['mark'], 'paragraphs': by_num(r['ruling']['paragraphs']),
                        'quote': r['ruling'].get('quote', ''), 'source': r['id']}
            else:
                c[t] = {'mark': A[u][t]['mark'], 'paragraphs': by_num(A[u][t]['paragraphs'] + B[u][t]['paragraphs']),
                        'quote': A[u][t]['quote'] or B[u][t]['quote'], 'source': 'agreed'}
        for x in ('X3', 'X4'):
            if (u, x) in R:
                r = R[(u, x)]
                c[x] = dict(r['ruling'], paragraphs=by_num(r['ruling']['paragraphs']), source=r['id'])
            else:
                c[x] = dict(A[u][x], paragraphs=by_num(A[u][x]['paragraphs'] + B[u][x]['paragraphs']), source='agreed')
        t12 = 'alleged' in (c['T1']['mark'], c['T2']['mark'])
        if c['X4']['source'] == 'agreed' and not (c['X4']['answer'] == 'yes' and t12) and c['X4']['tied_to_T1_or_T2'] != 'n/a':
            # The sheet's rule: the tie is n/a unless X4 is yes and T1 or T2 is alleged. A ruling that
            # removes T1 and T2 makes an agreed tie n/a; nothing else is changed without a ruling.
            c['X4'] = dict(c['X4'], tied_to_T1_or_T2='n/a', source='rule: no T1 or T2 after rulings')
        c['X1'] = {'coder_1': A[u]['X1'], 'coder_2': B[u]['X1']}
        c['X2'] = {'coder_1': A[u]['X2'], 'coder_2': B[u]['X2']}
        c['O1'] = {'coder_1': A[u]['O1'], 'coder_2': B[u]['O1']}
        out.append(c)
    return out


def problems(adj):
    """X4's tie field must agree with the final T1 and T2 marks."""
    errs = []
    for c in adj:
        t12 = 'alleged' in (c['T1']['mark'], c['T2']['mark'])
        tie = c['X4'].get('tied_to_T1_or_T2')
        if c['X4']['answer'] == 'yes' and t12 and tie not in ('yes', 'no'):
            errs.append(f"{c['unit']} X4: T1 or T2 is alleged, so the tie must be yes or no, not {tie}")
        if (c['X4']['answer'] != 'yes' or not t12) and tie != 'n/a':
            errs.append(f"{c['unit']} X4: tie must be n/a, not {tie}")
    return errs


def counts(adj, units):
    cs = [c for c in adj if c['unit'] in units]
    res = {'complaints': len(cs), 'by_tactic': {}, 'by_group': {}}
    for t in TACTICS:
        res['by_tactic'][t] = {m: sum(c[t]['mark'] == m for c in cs) for m in MARKS}
    for g, ts in GROUPS.items():
        res['by_group'][g] = {'complaints alleging at least one': sum(any(c[t]['mark'] == 'alleged' for t in ts) for c in cs)}
    res['no tactic alleged'] = sum(all(c[t]['mark'] == 'not alleged' for t in TACTICS) for c in cs)
    t12 = [c for c in cs if 'alleged' in (c['T1']['mark'], c['T2']['mark'])]
    res['T1 or T2 alleged'] = len(t12)
    res['of those, shared attribute tied to those accounts'] = sum(c['X4'].get('tied_to_T1_or_T2') == 'yes' for c in t12)
    res['of those, shared attribute alleged elsewhere only'] = sum(c['X4'].get('tied_to_T1_or_T2') == 'no' for c in t12)
    res['open field: complaints with an entry (either coder)'] = sum(bool(c['O1']['coder_1'] or c['O1']['coder_2']) for c in cs)
    return res


def main():
    a, b, r = (json.load(open(p, encoding='utf-8')) for p in sys.argv[1:4])
    adj = merge(a, b, r)
    errs = problems(adj)
    if errs:
        print('\n'.join(errs))
        raise SystemExit('X4 tie fields are inconsistent with the final marks')
    units = [c['unit'] for c in adj]
    report = {'all': counts(adj, units),
              'without the three read before the protocol (U01, U06, U12)': counts(adj, [u for u in units if u not in READ_BEFORE])}
    json.dump({'complaints': adj, 'counts': report}, open(sys.argv[4], 'w', encoding='utf-8'), indent=1, ensure_ascii=False)
    print(json.dumps(report, indent=1))


if __name__ == '__main__':
    main()
