"""Count the open-field entries (O1) by kind.

Usage: python3 open_field.py CLAUDE_SHEET CHATGPT_SHEET OPEN_FIELD_CSV

OPEN_FIELD.csv lists every open-field entry from both coders, word for word,
with one kind each. The kinds were assigned by coder 1 after coding and were
not adjudicated. This script checks that the file matches the two sheets and
counts, for each kind, the complaints with an entry from either coder and from
both coders.
"""
import csv
import json
import sys

KINDS = ['business type or category code misstated',
         'own limit raised or not applied',
         'other false statement to the acquirer or bank',
         'kept off termination lists',
         'rail or nested processor outside monitoring',
         'other']


def expected(a, b):
    rows = []
    for n, s in (('1', a), ('2', b)):
        for c in s['complaints']:
            for i, o in enumerate(c['O1']):
                rows.append((c['unit'], n, str(i + 1), o['tactic'], ' '.join(o['paragraphs'])))
    return sorted(rows)


def check(a, b, rows):
    errs = []
    got = sorted((r['unit'], r['coder'], r['entry'], r['tactic'], r['paragraphs']) for r in rows)
    if got != expected(a, b):
        errs.append('the file does not match the two sheets\' open-field entries')
    errs += [f"{r['unit']} coder {r['coder']} entry {r['entry']}: unknown kind {r['kind']!r}" for r in rows if r['kind'] not in KINDS]
    return errs


def count(rows):
    units = sorted({r['unit'] for r in rows})
    out = {'complaints with an entry': {'either coder': len(units),
                                        'both coders': sum({r['coder'] for r in rows if r['unit'] == u} == {'1', '2'} for u in units)},
           'entries': {'coder 1': sum(r['coder'] == '1' for r in rows), 'coder 2': sum(r['coder'] == '2' for r in rows)},
           'by kind': {}}
    for k in KINDS:
        by = {n: sorted({r['unit'] for r in rows if r['kind'] == k and r['coder'] == n}) for n in ('1', '2')}
        out['by kind'][k] = {'either coder': sorted(set(by['1']) | set(by['2'])), 'both coders': sorted(set(by['1']) & set(by['2']))}
    return out


def main():
    a, b = (json.load(open(p, encoding='utf-8')) for p in sys.argv[1:3])
    rows = list(csv.DictReader(open(sys.argv[3], newline='', encoding='utf-8')))
    errs = check(a, b, rows)
    if errs:
        print('\n'.join(errs))
        raise SystemExit(1)
    res = count(rows)
    print(json.dumps(res, indent=1))
    print('\n| Kind | Either coder | Both coders |\n|---|---|---|')
    for k, v in res['by kind'].items():
        print(f"| {k} | {len(v['either coder'])} | {len(v['both coders'])} |")


if __name__ == '__main__':
    main()
