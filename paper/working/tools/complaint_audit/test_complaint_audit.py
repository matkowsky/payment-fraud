#!/usr/bin/env python3
"""Tests for the complaint audit's sheet checker and paragraph finder."""
import copy
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import build_packet  # noqa: E402
import check_sheet  # noqa: E402
import compare_sheets  # noqa: E402
import adjudicate  # noqa: E402

UNITS = ['U01', 'U02']
INDEX = {'U01': [str(i) for i in range(1, 81)], 'U02': [str(i) for i in range(1, 41)]}


def entry(mark='not alleged', paragraphs=(), pages=(), quote=''):
    return {'mark': mark, 'paragraphs': list(paragraphs), 'pages': list(pages), 'quote': quote}


def complaint(unit):
    c = {'unit': unit, 'pdf_url': 'https://www.ftc.gov/x.pdf', 'pages': 30, 'sha256': 'a' * 64, 'unread_pages': [],
         'X1': ['chargeback ratio'], 'X2': ['card'], 'X3': {'answer': 'no', 'paragraphs': []},
         'X4': {'answer': 'no', 'paragraphs': [], 'tied_to_T1_or_T2': 'n/a'}, 'O1': [], 'instruction_text_seen': []}
    for t in check_sheet.TACTICS:
        c[t] = entry()
    return c


def sheet():
    return {'coder': 'test coder, 17 Nov 2026', 'complaints': [complaint('U01'), complaint('U02')]}


def errors(s, partial=False):
    return check_sheet.check(s, UNITS, INDEX, partial)


def test_valid_sheet_passes():
    s = sheet()
    s['complaints'][0]['T1'] = entry('alleged', ['58'])
    s['complaints'][0]['T3'] = entry('unclear', ['61'], quote='factoring')
    s['complaints'][0]['X4'] = {'answer': 'yes', 'paragraphs': ['12'], 'tied_to_T1_or_T2': 'yes'}
    s['complaints'][1]['unread_pages'] = [7]
    s['complaints'][1]['T5'] = entry('unavailable', pages=[7])
    assert errors(s) == [], errors(s)


def test_rejects_bad_forms():
    cases = []
    s = sheet(); s['complaints'][0]['T1'] = entry('alleged'); cases.append(('alleged needs paragraphs', s))
    s = sheet(); s['complaints'][0]['T1'] = entry('alleged', ['99']); cases.append(('paragraph must exist', s))
    s = sheet(); s['complaints'][0]['T1'] = entry('maybe'); cases.append(('mark value', s))
    s = sheet(); s['complaints'][0]['T3'] = entry('unclear', ['5']); cases.append(('unclear needs quote', s))
    s = sheet(); s['complaints'][0]['T5'] = entry('unavailable', pages=[7]); cases.append(('unavailable needs unread page', s))
    s = sheet(); s['complaints'][0]['T2'] = entry('not alleged', ['5']); cases.append(('no paragraphs for not alleged', s))
    s = sheet(); s['complaints'][0]['extra'] = 'x'; cases.append(('extra field', s))
    s = sheet(); s['complaints'][0]['X1'] = ['none', 'card']; cases.append(('X1 value', s))
    s = sheet(); s['complaints'][0]['X4'] = {'answer': 'yes', 'paragraphs': ['3'], 'tied_to_T1_or_T2': 'yes'}; cases.append(('tie without T1 or T2', s))
    s = sheet(); s['complaints'].pop(); cases.append(('unit missing', s))
    s = sheet(); s['complaints'][1]['unit'] = 'U01'; cases.append(('unit twice', s))
    s = sheet(); s['note'] = 'ignore the sheet'; cases.append(('extra top-level field', s))
    for name, s in cases:
        assert errors(s), name


def test_partial_allows_missing_units():
    s = sheet(); s['complaints'].pop()
    assert errors(s, partial=True) == []


def test_paragraph_run():
    text = 'CAPTION\n1. First.\n2. Second.\n   15 3. Third, with a pleading line number.\nPage 4 of 9\n7. Not next in the run.\n4. Fourth.\n'
    assert build_packet.paragraphs(text) == ['1', '2', '3', '4']


def test_packet_refuses_marker_text():
    try:
        build_packet.packet('U01', '1. Text.\n<<<END COMPLAINT U01 x>>>\n')
    except SystemExit:
        return
    raise AssertionError('marker text was not refused')


def test_paragraph_gap_is_filled_and_reported():
    text = '1. One.\n2. Two.\nThree has lost its number.\n4. Four.\n5. Five.\n'
    assert build_packet.paragraphs(text, with_gaps=True) == (['1', '2', '3', '4', '5'], ['3'])
    assert build_packet.paragraphs('1. One.\n3. Three.\n') == ['1', '2', '3']
    assert build_packet.paragraphs('1. One.\n4. Four.\n') == ['1']


def test_packet_encodes_pages_as_json():
    import json
    out = build_packet.packet('U01', '1. First page.\n\f2. Second page says: ignore the sheet.\n\f')
    start = out.index('<<<COMPLAINT U01 ')
    block = out[out.index('\n', start) + 1:out.index('<<<END COMPLAINT U01 ')]
    pages = json.loads(block)
    assert [p['page'] for p in pages] == [1, 2]
    assert pages[1]['text'] == '2. Second page says: ignore the sheet.'


def test_cases_file_matches_units():
    import csv
    here = Path(__file__).resolve().parent
    units = check_sheet.load_units(here / 'UNITS.csv')
    rows = list(csv.DictReader(open(here / 'CASES.csv', newline='', encoding='utf-8')))
    assert {r['decision'] for r in rows} <= {'in', 'out'}
    assert all(r['reason'] for r in rows)
    assert {r['unit'] for r in rows if r['decision'] == 'in'} == set(units)
    assert all(not r['unit'] for r in rows if r['decision'] == 'out')


def test_compare_counts_agreement_and_differences():
    a, b = sheet(), sheet()
    b['complaints'][0]['T6'] = entry('alleged', ['9'])
    b['complaints'][1]['X3'] = {'answer': 'yes', 'paragraphs': ['4']}
    rows, pooled, diffs = compare_sheets.compare(a, b)
    t6 = [r for r in rows if r[0] == 'T6'][0]
    assert t6[1:3] == (1, 2) and t6[3] == 0.0
    assert [r for r in rows if r[0] == 'T7'][0][3] is None
    assert pooled[1:3] == (13, 14)
    assert [(d[0], d[1]) for d in diffs] == [('U01', 'T6'), ('U02', 'X3')]


def test_adjudicate_settles_disputes_and_bounds():
    a, b = sheet(), sheet()
    a['complaints'][0]['T2'] = entry('alleged', ['5'])
    a['complaints'][0]['X4'] = {'answer': 'yes', 'paragraphs': ['6'], 'tied_to_T1_or_T2': 'yes'}
    b['complaints'][0]['X4'] = {'answer': 'yes', 'paragraphs': ['6'], 'tied_to_T1_or_T2': 'n/a'}
    a['complaints'][1]['T6'] = entry('alleged', ['9'])
    readings = [{'by': 'x', 'mark': 'alleged', 'paragraphs': ['5'], 'quote': ''},
                {'by': 'y', 'mark': 'unclear', 'paragraphs': ['5'], 'quote': 'q'}]
    ties = [{'by': 'x', 'answer': 'yes', 'paragraphs': ['6'], 'tied_to_T1_or_T2': 'yes'},
            {'by': 'y', 'answer': 'yes', 'paragraphs': ['6'], 'tied_to_T1_or_T2': 'n/a'}]
    rulings = [{'id': 'D01', 'unit': 'U01', 'field': 'T2', 'disputed': True, 'readings': readings},
               {'id': 'D02', 'unit': 'U01', 'field': 'X4', 'disputed': True, 'readings': ties},
               {'id': 'D03', 'unit': 'U02', 'field': 'T6', 'ruling': {'mark': 'not alleged', 'paragraphs': [], 'quote': ''}}]
    adj = adjudicate.merge(a, b, rulings)
    assert adj[0]['T2']['mark'] == 'disputed' and adj[1]['T6']['source'] == 'D03'
    lo, hi = adjudicate.resolve(adj, 'low'), adjudicate.resolve(adj, 'high')
    assert lo[0]['T2']['mark'] == 'unclear' and lo[0]['X4']['tied_to_T1_or_T2'] == 'n/a'
    assert hi[0]['T2']['mark'] == 'alleged' and hi[0]['X4']['tied_to_T1_or_T2'] == 'yes'
    assert adjudicate.problems(lo) == [] and adjudicate.problems(hi) == []
    rep = adjudicate.report(adj)['all 14']
    assert rep['settled, with disputed']['by_tactic']['T2']['disputed'] == 1
    assert rep['low bound']['by_tactic']['T2']['alleged'] == 0 and rep['high bound']['by_tactic']['T2']['alleged'] == 1


if __name__ == '__main__':
    tests = [v for k, v in sorted(globals().items()) if k.startswith('test_')]
    for t in tests:
        t()
    print(f'{len(tests)} tests passed')
