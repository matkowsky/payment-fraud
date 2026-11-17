#!/usr/bin/env python3
"""Check a coder's sheet before it is committed (README, "Coding").

Usage: python3 check_sheet.py SHEET.json [--paragraphs DIR] [--units UNITS.csv] [--partial]

It accepts only the sheet's fields and allowed values, requires paragraph numbers for every
`alleged` or `unclear` mark and unread page numbers for every `unavailable` mark, and requires
each cited paragraph number to exist in that complaint's paragraph index (DIR/<unit>.json,
written by build_packet.py). It checks form, not meaning: whether a cited paragraph supports a
mark is settled by the second coder and the author's rulings. Exit status 1 on any error.
"""
import csv
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
TACTICS = [f'T{i}' for i in range(1, 8)]
MARKS = {'alleged', 'not alleged', 'unclear', 'unavailable'}
X1 = {'chargeback ratio', 'chargeback count', 'fraud-report ratio', 'return rate', 'other', 'none'}
X2 = {'card', 'bank debit', 'remotely created check or payment order', 'other'}
COMPLAINT_KEYS = {'unit', 'pdf_url', 'pages', 'sha256', 'unread_pages', *TACTICS, 'X1', 'X2', 'X3', 'X4', 'O1', 'instruction_text_seen'}


def check(sheet, units, index, partial=False):
    err = []
    if not isinstance(sheet, dict) or set(sheet) != {'coder', 'complaints'}:
        return ['top level must have exactly "coder" and "complaints"']
    if not isinstance(sheet['coder'], str) or not sheet['coder'].strip():
        err.append('"coder" must name the coder, model and date')
    seen = set()
    for c in sheet['complaints'] if isinstance(sheet['complaints'], list) else []:
        u = c.get('unit') if isinstance(c, dict) else None
        where = f'{u or "?"}'
        if not isinstance(c, dict) or set(c) != COMPLAINT_KEYS:
            got = set(c) if isinstance(c, dict) else set()
            err.append(f'{where}: fields must be exactly {sorted(COMPLAINT_KEYS)}; missing {sorted(COMPLAINT_KEYS - got)}, extra {sorted(got - COMPLAINT_KEYS)}')
            continue
        if u not in units:
            err.append(f'{where}: unit is not in UNITS.csv')
            continue
        if u in seen:
            err.append(f'{where}: coded twice')
        seen.add(u)
        paras = set(index.get(u, []))
        if not paras:
            err.append(f'{where}: no paragraph index ({u}.json)')
        if not (isinstance(c['pdf_url'], str) and c['pdf_url'].startswith('https://')):
            err.append(f'{where}: pdf_url must be an https address')
        pages = c['pages']
        if not (isinstance(pages, int) and pages > 0):
            err.append(f'{where}: pages must be a positive integer')
            pages = 0
        if not (isinstance(c['sha256'], str) and re.fullmatch(r'[0-9a-f]{64}', c['sha256'])):
            err.append(f'{where}: sha256 must be 64 lower-case hex characters')
        unread = c['unread_pages']
        if not (isinstance(unread, list) and all(isinstance(p, int) and 1 <= p <= pages for p in unread)):
            err.append(f'{where}: unread_pages must list page numbers within the complaint')
            unread = []

        def cite(field, lst, need):
            if not (isinstance(lst, list) and all(isinstance(p, str) for p in lst)):
                err.append(f'{where} {field}: paragraphs must be a list of strings')
                return
            if need and not lst:
                err.append(f'{where} {field}: paragraph numbers required')
            if not need and lst:
                err.append(f'{where} {field}: no paragraph numbers allowed')
            for p in lst:
                if p not in paras:
                    err.append(f'{where} {field}: paragraph {p} is not in the complaint')

        for t in TACTICS:
            e = c[t]
            if not isinstance(e, dict) or set(e) != {'mark', 'paragraphs', 'pages', 'quote'}:
                err.append(f'{where} {t}: fields must be exactly mark, paragraphs, pages, quote')
                continue
            m = e['mark']
            if m not in MARKS:
                err.append(f'{where} {t}: mark must be one of {sorted(MARKS)}')
                continue
            cite(t, e['paragraphs'], m in ('alleged', 'unclear'))
            if m == 'unclear' and not (isinstance(e['quote'], str) and e['quote'].strip()):
                err.append(f'{where} {t}: an unclear mark must quote the wording')
            if m != 'unclear' and e['quote'] != '':
                err.append(f'{where} {t}: quote only for an unclear mark')
            if m == 'unavailable':
                if not unread:
                    err.append(f'{where} {t}: unavailable, but no page is listed as unread')
                if not e['pages'] or not set(e['pages']) <= set(unread):
                    err.append(f'{where} {t}: unavailable must name unread pages')
            elif e['pages'] != []:
                err.append(f'{where} {t}: pages only for an unavailable mark')
        for key, allowed in (('X1', X1), ('X2', X2)):
            v = c[key]
            if not (isinstance(v, list) and v and set(v) <= allowed):
                err.append(f'{where} {key}: must be a non-empty list from {sorted(allowed)}')
            elif 'none' in v and len(v) > 1:
                err.append(f'{where} {key}: "none" stands alone')
        x3 = c['X3']
        if not (isinstance(x3, dict) and set(x3) == {'answer', 'paragraphs'} and x3['answer'] in ('yes', 'no')):
            err.append(f'{where} X3: must be {{"answer": yes|no, "paragraphs": [...]}}')
        else:
            cite('X3', x3['paragraphs'], x3['answer'] == 'yes')
        x4 = c['X4']
        if not (isinstance(x4, dict) and set(x4) == {'answer', 'paragraphs', 'tied_to_T1_or_T2'} and x4['answer'] in ('yes', 'no')):
            err.append(f'{where} X4: must be {{"answer", "paragraphs", "tied_to_T1_or_T2"}}')
        else:
            cite('X4', x4['paragraphs'], x4['answer'] == 'yes')
            split = any(isinstance(c[t], dict) and c[t].get('mark') == 'alleged' for t in ('T1', 'T2'))
            want = {'yes', 'no'} if (x4['answer'] == 'yes' and split) else {'n/a'}
            if x4['tied_to_T1_or_T2'] not in want:
                err.append(f'{where} X4: tied_to_T1_or_T2 must be one of {sorted(want)}')
        if not isinstance(c['O1'], list):
            err.append(f'{where} O1: must be a list')
        else:
            for i, o in enumerate(c['O1']):
                if not (isinstance(o, dict) and set(o) == {'tactic', 'paragraphs'} and isinstance(o['tactic'], str) and o['tactic'].strip()):
                    err.append(f'{where} O1[{i}]: must be {{"tactic", "paragraphs"}}')
                else:
                    cite(f'O1[{i}]', o['paragraphs'], True)
        its = c['instruction_text_seen']
        if not (isinstance(its, list) and all(isinstance(x, dict) and set(x) == {'where', 'text'} for x in its)):
            err.append(f'{where} instruction_text_seen: must be a list of {{"where", "text"}}')
    if not isinstance(sheet['complaints'], list):
        err.append('"complaints" must be a list')
    elif not partial and seen != set(units):
        err.append(f'units not coded: {sorted(set(units) - seen)}')
    return err


def load_units(path):
    with open(path, newline='', encoding='utf-8') as f:
        return [r['unit'] for r in csv.DictReader(f)]


def main(argv):
    args = [a for a in argv if not a.startswith('--')]
    opts = dict(a.split('=', 1) if '=' in a else (a, '') for a in argv if a.startswith('--'))
    if len(args) != 1:
        print(__doc__)
        return 2
    units = load_units(opts.get('--units') or HERE / 'UNITS.csv')
    pdir = Path(opts.get('--paragraphs') or HERE / 'paragraphs')
    index = {u: json.loads((pdir / f'{u}.json').read_text()) for u in units if (pdir / f'{u}.json').exists()}
    sheet = json.loads(Path(args[0]).read_text(encoding='utf-8'))
    err = check(sheet, units, index, partial='--partial' in opts)
    for e in err:
        print('ERROR', e)
    print('sheet passes' if not err else f'{len(err)} errors; return the sheet to its coder')
    return 1 if err else 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
