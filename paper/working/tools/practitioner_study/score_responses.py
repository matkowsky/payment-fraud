"""Score the practitioner study (Supplement S8) from the form's export, using the private answer key.

Fixed before the first response. Run from the package root:

    python3 tools/practitioner_study/score_responses.py EXPORT.xlsx ANSWER_KEY.md --out results/

EXPORT is the Microsoft Forms export (.xlsx or .csv). Each question title, and each grid row label,
starts with its code from INSTRUMENT.md: A1. to B6. for Part 2, A1-R. to B6-R. for Part 3, and
E0, C0, P1 to P4, F1 to F5, R1 to R5, R1-H to R5-H, S1 to S11, O1 to O24 and V1 to V4.

An export without a column for a required question is refused. A row whose E0, C0, P3 or P4 holds
anything but one of that question's choices is not read as an answer: the script stops and names the
row and the column, not the value. With --set-aside-invalid it scores the other rows and reports the
rows set aside. The live form cannot produce such a row; a damaged or hand-edited export can.

The key's SHA-256 must match the hash recorded in README.md; otherwise nothing is scored.
Outputs: results.json and results.md with counts only. Free text is not copied; answers to V1 to V3
and F5 are written to permitted_quotes.json only for participants who answered Yes to V4, for the
author to review and strip of identifying detail before any use.
"""
import argparse
import csv
import hashlib
import json
import re
from collections import Counter
from pathlib import Path

KEY_SHA256 = '3438ef22c7491a0adbe01b3702515b2b7699dc2b6675c405e70500f081b3f8f0'
ITEMS = [f'A{i}' for i in range(1, 6)] + [f'B{i}' for i in range(1, 7)]
# The form's required questions (INSTRUMENT.md) and the choices of the four that decide who is counted.
REQUIRED = ['E0', 'C0', 'P1', 'P2', 'P3', 'P4'] + ITEMS + [f'{i}-R' for i in ITEMS]
YES_NO = ('yes', 'no')
P3_CHOICES = ('under 2', '2 to 5', '6 to 10', 'more than 10')
ABOUT_CHOICES = {
    'P1': ('investigator or analyst', 'fraud or risk data science', 'threat intelligence', 'trust and safety',
           'engineering for fraud or risk systems', 'manager of one of these', 'other'),
    'P2': ('payment processor or acquirer', 'card issuer or bank', 'marketplace or platform', 'fintech',
           'vendor or consultancy', 'other'),
    'P3': P3_CHOICES, 'P4': YES_NO}
CODE = re.compile(r'^\s*([A-Z]\d{1,2}(?:-[RH])?)\s*[.:)\s]')
ROW_CODE = re.compile(r'\.\s*([A-Z]\d{1,2}(?:-[RH])?)\s*[.:)\s]')  # grid rows exported as "question.row"


def norm(x):
    return re.sub(r'\s+', ' ', str(x or '')).strip().casefold()


def parse_key(text):
    """Item -> supported answer, counted error, requirement; plus the Part 2 'Cannot tell' items."""
    key = {}
    for line in text.splitlines():
        cells = [c.strip() for c in line.strip().strip('|').split('|')]
        if len(cells) >= 4 and cells[0] in ITEMS:
            key[cells[0]] = {'supported': norm(cells[1]), 'error': norm(cells[2]), 'requirement': cells[3]}
    m = re.search(r'"Cannot tell" is also supported for ([A-Z0-9, and]+);', text)
    also = set(re.findall(r'[AB]\d', m.group(1))) if m else set()
    missing = [i for i in ITEMS if i not in key]
    if missing:
        raise ValueError(f'answer key lacks items {missing}')
    return key, also


def read_export(path, required=(), with_rows=False):
    path = Path(path)
    if path.suffix.lower() == '.csv':
        with path.open(encoding='utf-8-sig', newline='') as f:
            rows = list(csv.reader(f))
    else:
        import openpyxl
        ws = openpyxl.load_workbook(path, read_only=True, data_only=True).active
        rows = [[c for c in r] for r in ws.iter_rows(values_only=True)]
    header, body = rows[0], rows[1:]
    cols = {}
    for j, h in enumerate(header):
        h = str(h or '') + ' '
        m = CODE.match(h) or ROW_CODE.search(h)
        if m:
            if m.group(1) in cols:
                raise ValueError(f'two columns start with code {m.group(1)}')
            cols[m.group(1)] = j
    missing = [c for c in required if c not in cols]
    if missing:
        raise ValueError(f'the export has no column for required questions {missing}')
    kept = [(n, r) for n, r in enumerate(body, 2) if any(r)]   # the header is row 1; empty rows are skipped
    responses = [{code: (r[j] if j < len(r) else None) for code, j in cols.items()} for _, r in kept]
    return (responses, [n for n, _ in kept]) if with_rows else responses


def classify(r):
    """('eligible', []) or (why the row is not counted, the columns that decided it).

    The form ends at a No to E0 or C0, so later answers are read only after a Yes to both. A missing, blank
    or unlisted value is never read as Yes or as No: the row needs review."""
    e0, c0, p3, p4 = (norm(r.get(c)) for c in ('E0', 'C0', 'P3', 'P4'))
    if e0 not in YES_NO:
        return 'needs_review', ['E0']
    if e0 == 'no':
        return 'not_eligible', ['E0']
    if c0 not in YES_NO:
        return 'needs_review', ['C0']
    if c0 == 'no':
        return 'no_consent', ['C0']
    bad = [c for c, v, choices in (('P3', p3, P3_CHOICES), ('P4', p4, YES_NO)) if v not in choices]
    if bad:
        return 'needs_review', bad
    return ('under_two_years', ['P3']) if p3 == 'under 2' else ('eligible', [])


def about(r, c):
    """A participant's answer to a Part 1 question; text typed under "other" is counted, never copied."""
    v = norm(r.get(c))
    return v if v in ABOUT_CHOICES[c] else '(blank)' if not v else 'other (typed)'


def score(responses, key, also, rows=None):
    status = [classify(r) for r in responses]
    rows = rows or range(2, len(responses) + 2)   # each response's row in the export
    eligible = [r for r, (s, _) in zip(responses, status) if s == 'eligible']
    groups = {'main': [r for r in eligible if norm(r.get('P4')) == 'no'],
              'read_section_8': [r for r in eligible if norm(r.get('P4')) == 'yes']}
    out = {'responses': len(responses), 'eligible': len(eligible),
           'excluded': {s: sum(x == s for x, _ in status)
                        for s in ('not_eligible', 'no_consent', 'under_two_years', 'needs_review')},
           # Column codes only, never the values.
           'needs_review_rows': [{'row': n, 'columns': cols} for n, (s, cols) in zip(rows, status) if s == 'needs_review'],
           'about': {c: dict(Counter(about(r, c) for r in eligible)) for c in ('P1', 'P2', 'P3', 'P4')}}
    for name, rs in groups.items():
        items = {}
        for i in ITEMS:
            k = key[i]
            before = [norm(r.get(i)) for r in rs]
            after = [norm(r.get(f'{i}-R')) for r in rs]
            items[i] = {
                'requirement': k['requirement'],
                'part2_answers': dict(Counter(a or '(blank)' for a in before)),
                'part3_answers': dict(Counter(a or '(blank)' for a in after)),
                'part2_errors': sum(a == k['error'] for a in before),
                'part3_errors': sum(a == k['error'] for a in after),
                'part2_supported': sum(a == k['supported'] or (i in also and a == 'cannot tell') for a in before),
                'part3_supported': sum(a == k['supported'] for a in after),
                'error_to_supported': sum(b == k['error'] and a == k['supported'] for b, a in zip(before, after)),
                'supported_to_error': sum((b == k['supported'] or (i in also and b == 'cannot tell')) and a == k['error'] for b, a in zip(before, after)),
            }
        by_req = {}
        for i, v in items.items():
            req = 'Control' if v['requirement'] == 'Control' else v['requirement'].split()[0]
            agg = by_req.setdefault(req, Counter())
            for f in ('part2_errors', 'part3_errors', 'error_to_supported', 'supported_to_error'):
                agg[f] += v[f]
            agg['answers'] += len(rs)
        out[name] = {'participants': len(rs), 'items': items, 'by_requirement': {k: dict(v) for k, v in by_req.items()}}
    codes = ([f'F{i}' for i in range(1, 5)] + [f'R{i}' for i in range(1, 6)] + [f'R{i}-H' for i in range(1, 6)]
             + [f'S{i}' for i in range(1, 12)] + [f'O{i}' for i in range(1, 25)] + ['V4'])
    out['practice'] = {c: dict(Counter(norm(r.get(c)) or '(blank)' for r in eligible)) for c in codes}
    out['free_text_answers'] = {c: sum(bool(norm(r.get(c))) for r in eligible) for c in ('F5', 'V1', 'V2', 'V3')}
    return out


def permitted_quotes(responses):
    return [{c: r.get(c) for c in ('F5', 'V1', 'V2', 'V3') if norm(r.get(c))}
            for r in responses if classify(r)[0] == 'eligible' and norm(r.get('V4')) == 'yes']


def to_markdown(res):
    lines = [f"# Practitioner study results", '',
             f"Responses: {res['responses']}. Eligible: {res['eligible']}. Excluded: {res['excluded']}.", '']
    if res['needs_review_rows']:
        lines += ['Set aside for review, in neither group: '
                  + '; '.join(f"row {x['row']} ({', '.join(x['columns'])})" for x in res['needs_review_rows']) + '.', '']
    labels = {'main': 'Had read neither Section 8 nor Supplement S6',
              'read_section_8': 'Had read Section 8 or Supplement S6'}
    for name in ('main', 'read_section_8'):
        g = res[name]
        lines += [f"## {labels[name]} ({g['participants']} participants)", '',
                  '| Item | Requirement | Errors without records | Errors with records | Error to supported | Supported to counted error (Part 2 → Part 3) |',
                  '|---|---|---|---|---|---|']
        for i, v in g['items'].items():
            lines.append(f"| {i} | {v['requirement']} | {v['part2_errors']} | {v['part3_errors']} | "
                         f"{v['error_to_supported']} | {v['supported_to_error']} |")
        lines += ['', '| Requirement | Answers | Errors without | Errors with | Error to supported | Supported to counted error (Part 2 → Part 3) |',
                  '|---|---|---|---|---|---|']
        for k, v in sorted(g['by_requirement'].items()):
            lines.append(f"| {k} | {v['answers']} | {v['part2_errors']} | {v['part3_errors']} | "
                         f"{v['error_to_supported']} | {v['supported_to_error']} |")
        lines.append('')
    return '\n'.join(lines) + '\n'


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('export')
    ap.add_argument('key')
    ap.add_argument('--out', default='practitioner_results')
    ap.add_argument('--set-aside-invalid', action='store_true',
                    help='score the other rows when a row holds a value outside a question\'s choices')
    a = ap.parse_args()
    raw = Path(a.key).read_bytes()
    if hashlib.sha256(raw).hexdigest() != KEY_SHA256:
        raise SystemExit('answer key does not match the hash recorded before the first response')
    key, also = parse_key(raw.decode('utf-8'))
    try:
        responses, rows = read_export(a.export, REQUIRED, with_rows=True)
    except ValueError as e:
        raise SystemExit(str(e))
    res = score(responses, key, also, rows)
    if res['needs_review_rows'] and not a.set_aside_invalid:
        raise SystemExit('nothing scored: ' + '; '.join(f"row {x['row']} ({', '.join(x['columns'])})"
                                                         for x in res['needs_review_rows'])
                         + ' holds a value outside the question\'s choices. Check the export, or pass '
                           '--set-aside-invalid to score the other rows and report these.')
    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    (out / 'results.json').write_text(json.dumps(res, indent=1) + '\n', encoding='utf-8')
    (out / 'results.md').write_text(to_markdown(res), encoding='utf-8')
    (out / 'permitted_quotes.json').write_text(json.dumps(permitted_quotes(responses), indent=1) + '\n', encoding='utf-8')
    print(json.dumps({'eligible': res['eligible'], 'main': res['main']['participants'],
                      'read_section_8': res['read_section_8']['participants'],
                      'set_aside_for_review': len(res['needs_review_rows'])}))


if __name__ == '__main__':
    main()
