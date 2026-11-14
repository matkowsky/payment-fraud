"""Check the practitioner-study scoring on a synthetic export and a made-up key (not the real one).

Run from the package root: python3 tools/test_score_responses.py
"""
import csv
import hashlib
import io
import itertools
import json
import subprocess
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from unittest import mock

sys.path.insert(0, str(Path(__file__).parent / 'practitioner_study'))
import score_responses as sr  # noqa: E402

ITEMS = sr.ITEMS
# A made-up key in the real key's format. Every item: supported "No", error "Yes", except two controls.
FAKE_KEY = '\n'.join(
    ['| Item | Supported answer | Error counted | Requirement | Record |', '|---|---|---|---|---|']
    + [f'| {i} | {"Yes" if i in ("A5", "B6") else "No"} | {"No" if i in ("A5", "B6") else "Yes"} | '
       f'{"Control" if i in ("A5", "B6") else "C2 coverage"} | x |' for i in ITEMS]
    + ['', 'In Part 2 (without the records), "Cannot tell" is also supported for A2, B1 and B4; it is not counted as an error.'])


def row(consent='Yes', years='6 to 10', read='No', before='Yes', after='No'):
    r = {'E0': 'Yes', 'C0': consent, 'P1': 'Investigator or analyst', 'P2': 'Fintech', 'P3': years, 'P4': read, 'V4': 'No'}
    for i in ITEMS:
        r[i] = before
        r[f'{i}-R'] = after
    return r


class ScoringTests(unittest.TestCase):
    def test_reverse_transitions(self):
        key, also = sr.parse_key(FAKE_KEY)
        values = [None, '', ' \t', 'Cannot tell', 'No', 'Yes', 'unexpected']
        # Independent category sets from the public made-up key, not the scoring predicate.
        for item, before, after, read in itertools.product(ITEMS, values, values, ['No', 'Yes']):
            with self.subTest(item=item, before=before, after=after, read=read):
                supported = {'yes'} if item in {'A5', 'B6'} else {'no'}
                error = 'no' if item in {'A5', 'B6'} else 'yes'
                before_support = supported | ({'cannot tell'} if item in {'A2', 'B1', 'B4'} else set())
                clean = lambda x: ' '.join(str(x or '').split()).casefold()
                r = {'E0': 'Yes', 'C0': 'Yes', 'P3': '6 to 10', 'P4': read, item: before, item + '-R': after}
                res = sr.score([r], key, also)
                g = res['read_section_8' if read == 'Yes' else 'main']
                v = g['items'][item]
                expected = int(clean(before) in before_support and clean(after) == error)
                self.assertEqual(v['supported_to_error'], expected)
                self.assertLessEqual(expected, min(v['part2_supported'], v['part3_errors']))
                self.assertEqual(v['error_to_supported'], int(clean(before) == error and clean(after) in supported))
                req = 'Control' if item in {'A5', 'B6'} else 'C2'
                self.assertEqual(g['by_requirement'][req]['supported_to_error'], expected)

    def test_blank_export_reverse_and_render(self):
        key, also = sr.parse_key(FAKE_KEY)
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / 'export.csv'
            p.write_text('E0. Eligible,C0. Consent,P3. Years,P4. Read,A1. Before,A1-R. After\nYes,Yes,6 to 10,No,,Yes\n')
            res = sr.score(sr.read_export(p), key, also)
        a1 = res['main']['items']['A1']
        self.assertEqual((a1['part2_supported'], a1['part3_errors'], a1['supported_to_error']), (0, 1, 0))
        rendered = sr.to_markdown(res)
        self.assertIn('Supported to counted error (Part 2 → Part 3)', rendered)
        self.assertIn('| A1 | C2 coverage | 0 | 1 | 0 | 0 |', rendered)
        self.assertIn('| C2 | 9 | 0 | 1 | 0 | 0 |', rendered)

    def test_key_parsing(self):
        key, also = sr.parse_key(FAKE_KEY)
        self.assertEqual(set(key), set(ITEMS))
        self.assertEqual(key['A1'], {'supported': 'no', 'error': 'yes', 'requirement': 'C2 coverage'})
        self.assertEqual(also, {'A2', 'B1', 'B4'})

    def test_counts_and_exclusions(self):
        key, also = sr.parse_key(FAKE_KEY)
        rs = [row(), row(), row(before='Cannot tell', after='No'), row(read='Yes'),
              row(consent='No'), row(years='Under 2')]
        res = sr.score(rs, key, also)
        self.assertEqual((res['responses'], res['eligible']), (6, 4))
        self.assertEqual(res['main']['participants'], 3)
        self.assertEqual(res['read_section_8']['participants'], 1)
        a1, a2 = res['main']['items']['A1'], res['main']['items']['A2']
        self.assertEqual((a1['part2_errors'], a1['part3_errors'], a1['error_to_supported']), (2, 0, 2))
        self.assertEqual((a1['part2_supported'], a2['part2_supported']), (0, 1))
        self.assertEqual(res['main']['by_requirement']['C2']['part2_errors'], 2 * 9)
        self.assertEqual(res['excluded'], {'not_eligible': 0, 'no_consent': 1, 'under_two_years': 1, 'needs_review': 0})
        self.assertEqual(res['needs_review_rows'], [])

    def test_export_columns_by_code(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / 'export.csv'
            with p.open('w', newline='', encoding='utf-8') as f:
                w = csv.writer(f)
                w.writerow(['ID', 'C0. I agree', 'A1. Was the burst', 'A1-R. Was the burst', 'R1 For each decision', 'R1-H For each decision'])
                w.writerow(['1', 'Yes', 'Yes', 'Cannot tell', 'Partly', 'Hard'])
            rs = sr.read_export(p)
        self.assertEqual(rs, [{'C0': 'Yes', 'A1': 'Yes', 'A1-R': 'Cannot tell', 'R1': 'Partly', 'R1-H': 'Hard'}])

    def test_eligibility_and_consent_are_read_in_form_order(self):
        key, also = sr.parse_key(FAKE_KEY)
        ended_at_e0 = {'E0': 'No'}                      # the form ends at a No, so the later columns are blank
        ended_at_c0 = {'E0': 'Yes', 'C0': 'No'}
        contradicts = dict(row(), E0='No')              # a No to E0 is not overridden by later answers
        res = sr.score([row(), ended_at_e0, ended_at_c0, contradicts, row(years='Under 2')], key, also)
        self.assertEqual(res['eligible'], 1)
        self.assertEqual(res['excluded'], {'not_eligible': 2, 'no_consent': 1, 'under_two_years': 1, 'needs_review': 0})

    def test_a_value_outside_the_choices_is_never_read_as_an_answer(self):
        key, also = sr.parse_key(FAKE_KEY)
        def without(code):
            r = row(); del r[code]; return r
        bad = [(without('P4'), ['P4']), (dict(row(), P4=''), ['P4']), (dict(row(), P4='Maybe'), ['P4']),
               (dict(row(), P3='3 years'), ['P3']), (dict(row(), P3=None), ['P3']), (dict(row(), P3='', P4='x'), ['P3', 'P4']),
               (without('E0'), ['E0']), (dict(row(), E0=' '), ['E0']), (dict(row(), E0='Y'), ['E0']),
               (dict(row(), C0=None), ['C0']), (dict(row(), C0='I agree'), ['C0'])]
        for r, columns in bad:
            with self.subTest(columns=columns, row=r):
                res = sr.score([row(), r, row(read='Yes')], key, also)
                self.assertEqual((res['eligible'], res['main']['participants'], res['read_section_8']['participants']), (2, 1, 1))
                self.assertEqual(res['excluded']['needs_review'], 1)
                self.assertEqual(res['needs_review_rows'], [{'row': 3, 'columns': columns}])
        # The same eleven rows together: none is counted as someone who has read neither, or as anything else.
        res = sr.score([r for r, _ in bad], key, also)
        self.assertEqual((res['eligible'], res['excluded']['needs_review'], len(res['needs_review_rows'])), (0, 11, 11))

    def test_typed_other_is_counted_not_copied(self):
        key, also = sr.parse_key(FAKE_KEY)
        res = sr.score([dict(row(), P1='Head of fraud at Example Bank', P2='Other'), row()], key, also)
        self.assertEqual(res['about']['P1'], {'other (typed)': 1, 'investigator or analyst': 1})
        self.assertEqual(res['about']['P2'], {'other': 1, 'fintech': 1})
        self.assertNotIn('example bank', json.dumps(res).casefold())

    def test_missing_required_column_is_refused(self):
        header = [f'{c}. q' for c in sr.REQUIRED]
        with tempfile.TemporaryDirectory() as d:
            full, short = Path(d) / 'full.csv', Path(d) / 'short.csv'
            for path, cols in ((full, header), (short, [h for h in header if not h.startswith('P4.')])):
                with path.open('w', newline='', encoding='utf-8') as f:
                    csv.writer(f).writerows([cols, ['Yes'] * len(cols)])
            self.assertEqual(len(sr.read_export(full, sr.REQUIRED)), 1)
            self.assertEqual(len(sr.read_export(short)), 1)          # reading alone does not require them
            with self.assertRaisesRegex(ValueError, r"required questions \['P4'\]"):
                sr.read_export(short, sr.REQUIRED)

    def test_command_stops_on_an_invalid_row_unless_told_to_set_it_aside(self):
        def export(path, rows):
            with path.open('w', newline='', encoding='utf-8') as f:
                w = csv.writer(f)
                w.writerow([f'{c}. q' for c in sr.REQUIRED] + ['V4. Quote?', 'V1. Missing?'])
                for r in rows:
                    w.writerow([r.get(c, '') for c in sr.REQUIRED] + [r.get('V4', ''), r.get('V1', '')] if r else [])
        invalid = dict(row(), P4='PRIVATE ANSWER', V4='Yes', V1='a quote from a row set aside')
        with tempfile.TemporaryDirectory() as d:
            k, e, o = Path(d) / 'key.md', Path(d) / 'export.csv', Path(d) / 'out'
            k.write_text(FAKE_KEY, encoding='utf-8')
            export(e, [row(), None, invalid, row(read='Yes')])   # an empty row before the invalid one
            with mock.patch.object(sr, 'KEY_SHA256', hashlib.sha256(FAKE_KEY.encode()).hexdigest()):
                with mock.patch.object(sys, 'argv', ['score_responses.py', str(e), str(k), '--out', str(o)]):
                    with self.assertRaises(SystemExit) as stop:
                        sr.main()
                self.assertIn('nothing scored: row 4 (P4)', str(stop.exception))
                self.assertNotIn('PRIVATE', str(stop.exception))
                self.assertFalse(o.exists())
                with mock.patch.object(sys, 'argv', ['score_responses.py', str(e), str(k), '--out', str(o), '--set-aside-invalid']):
                    printed = io.StringIO()
                    with redirect_stdout(printed):
                        sr.main()
            self.assertEqual(json.loads(printed.getvalue()), {'eligible': 2, 'main': 1, 'read_section_8': 1, 'set_aside_for_review': 1})
            written = ''.join((o / n).read_text(encoding='utf-8') for n in ('results.json', 'results.md', 'permitted_quotes.json'))
            self.assertIn('Set aside for review, in neither group: row 4 (P4).', written)
            self.assertIn('## Had read neither Section 8 nor Supplement S6 (1 participants)', written)
            self.assertNotIn('PRIVATE', written)
            self.assertNotIn('a quote from a row set aside', written)

    def test_wrong_key_is_refused(self):
        with tempfile.TemporaryDirectory() as d:
            k, e = Path(d) / 'key.md', Path(d) / 'export.csv'
            k.write_text(FAKE_KEY, encoding='utf-8')
            e.write_text('C0. I agree\nYes\n', encoding='utf-8')
            run = subprocess.run([sys.executable, str(Path(__file__).parent / 'practitioner_study' / 'score_responses.py'),
                                  str(e), str(k), '--out', str(Path(d) / 'o')], capture_output=True, text=True)
        self.assertNotEqual(run.returncode, 0)
        self.assertIn('does not match', run.stderr)


if __name__ == '__main__':
    unittest.main()
