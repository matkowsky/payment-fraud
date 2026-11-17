"""Compare two coder sheets: agreement per tactic and the list of disagreements.

Usage: python3 compare_sheets.py SHEET_A SHEET_B

Agreement is the share of complaints given the same mark. Cohen's kappa is
reported per tactic and pooled over T1 to T7; it is undefined when both
coders give one mark to every complaint. With 14 complaints, kappa moves a
lot with one mark, so the raw counts are the primary figure.
"""
import json
import sys
from collections import Counter

TACTICS = ['T1', 'T2', 'T3', 'T4', 'T5', 'T6', 'T7']


def kappa(pairs):
    n = len(pairs)
    po = sum(a == b for a, b in pairs) / n
    ca = Counter(a for a, _ in pairs)
    cb = Counter(b for _, b in pairs)
    pe = sum(ca[k] * cb[k] for k in set(ca) | set(cb)) / (n * n)
    return None if pe == 1 else (po - pe) / (1 - pe)


def compare(a, b):
    A = {c['unit']: c for c in a['complaints']}
    B = {c['unit']: c for c in b['complaints']}
    if set(A) != set(B):
        raise SystemExit(f'units differ: {sorted(set(A) ^ set(B))}')
    units = sorted(A)
    rows, diffs, pooled = [], [], []
    for t in TACTICS:
        pairs = [(A[u][t]['mark'], B[u][t]['mark']) for u in units]
        pooled += pairs
        rows.append((t, sum(x == y for x, y in pairs), len(units), kappa(pairs)))
        for u in units:
            if A[u][t]['mark'] != B[u][t]['mark']:
                diffs.append((u, t, A[u][t]['mark'], A[u][t]['paragraphs'], B[u][t]['mark'], B[u][t]['paragraphs']))
    for u in units:
        for x in ('X3', 'X4'):
            ka = (A[u][x]['answer'], A[u][x].get('tied_to_T1_or_T2'))
            kb = (B[u][x]['answer'], B[u][x].get('tied_to_T1_or_T2'))
            if ka != kb:
                diffs.append((u, x, '/'.join(filter(None, ka)), A[u][x]['paragraphs'], '/'.join(filter(None, kb)), B[u][x]['paragraphs']))
    pooled_row = ('T1-T7', sum(x == y for x, y in pooled), len(pooled), kappa(pooled))
    return rows, pooled_row, diffs


def fmt(k):
    return 'undefined' if k is None else f'{k:.2f}'


def main():
    a = json.load(open(sys.argv[1], encoding='utf-8'))
    b = json.load(open(sys.argv[2], encoding='utf-8'))
    rows, pooled, diffs = compare(a, b)
    print(f'A: {a["coder"]}\nB: {b["coder"]}\n')
    print('| Tactic | Same mark | Kappa |\n|---|---|---|')
    for t, s, n, k in rows + [pooled]:
        print(f'| {t} | {s} of {n} | {fmt(k)} |')
    print(f'\n{len(diffs)} differences\n\n| Unit | Item | A | A paragraphs | B | B paragraphs |\n|---|---|---|---|---|---|')
    for u, t, ma, pa, mb, pb in diffs:
        print(f'| {u} | {t} | {ma} | {", ".join(pa)} | {mb} | {", ".join(pb)} |')


if __name__ == '__main__':
    main()
