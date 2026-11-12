"""Score the practitioner study (Supplement S8) from the form's export, using the private answer key.

Fixed before the first response. Run from the package root:

    python3 tools/practitioner_study/score_responses.py EXPORT.xlsx ANSWER_KEY.md --out results/

EXPORT is the Microsoft Forms export (.xlsx or .csv). Each question title, and each grid row label,
starts with its code from INSTRUMENT.md: A1. to B6. for Part 2, A1-R. to B6-R. for Part 3, and
C0, P1 to P4, F1 to F5, R1 to R5, R1-H to R5-H, S1 to S11, O1 to O24 and V1 to V4.

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


def read_export(path):
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
    return [{code: (r[j] if j < len(r) else None) for code, j in cols.items()} for r in body if any(r)]


def score(responses, key, also):
    eligible = [r for r in responses if norm(r.get('C0')) == 'yes' and norm(r.get('P3')) not in ('under 2', '')]
    groups = {'main': [r for r in eligible if norm(r.get('P4')) != 'yes'],
              'read_section_8': [r for r in eligible if norm(r.get('P4')) == 'yes']}
    out = {'responses': len(responses), 'eligible': len(eligible),
           'excluded': {'no_consent': sum(norm(r.get('C0')) != 'yes' for r in responses),
                        'under_two_years_or_blank': sum(norm(r.get('C0')) == 'yes' and norm(r.get('P3')) in ('under 2', '')
                                                        for r in responses)},
           'about': {c: dict(Counter(norm(r.get(c)) or '(blank)' for r in eligible)) for c in ('P1', 'P2', 'P3', 'P4')}}
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
                'supported_to_error': sum(b != k['error'] and a == k['error'] for b, a in zip(before, after)),
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
            for r in responses if norm(r.get('C0')) == 'yes' and norm(r.get('V4')) == 'yes']


def to_markdown(res):
    lines = [f"# Practitioner study results", '',
             f"Responses: {res['responses']}. Eligible: {res['eligible']}. Excluded: {res['excluded']}.", '']
    for name in ('main', 'read_section_8'):
        g = res[name]
        lines += [f"## {name} ({g['participants']} participants)", '',
                  '| Item | Requirement | Errors without records | Errors with records | Error to supported | Supported to error |',
                  '|---|---|---|---|---|---|']
        for i, v in g['items'].items():
            lines.append(f"| {i} | {v['requirement']} | {v['part2_errors']} | {v['part3_errors']} | "
                         f"{v['error_to_supported']} | {v['supported_to_error']} |")
        lines += ['', '| Requirement | Answers | Errors without | Errors with | Error to supported | Supported to error |',
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
    a = ap.parse_args()
    raw = Path(a.key).read_bytes()
    if hashlib.sha256(raw).hexdigest() != KEY_SHA256:
        raise SystemExit('answer key does not match the hash recorded before the first response')
    key, also = parse_key(raw.decode('utf-8'))
    responses = read_export(a.export)
    res = score(responses, key, also)
    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    (out / 'results.json').write_text(json.dumps(res, indent=1) + '\n', encoding='utf-8')
    (out / 'results.md').write_text(to_markdown(res), encoding='utf-8')
    (out / 'permitted_quotes.json').write_text(json.dumps(permitted_quotes(responses), indent=1) + '\n', encoding='utf-8')
    print(json.dumps({'eligible': res['eligible'], 'main': res['main']['participants'],
                      'read_section_8': res['read_section_8']['participants']}))


if __name__ == '__main__':
    main()
