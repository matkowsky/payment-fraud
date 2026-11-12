"""Check the practitioner-study scoring on a synthetic export and a made-up key (not the real one).

Run from the package root: python3 tools/test_score_responses.py
"""
import csv
import itertools
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

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
    r = {'C0': consent, 'P3': years, 'P4': read, 'V4': 'No'}
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
                r = {'C0': 'Yes', 'P3': '6 to 10', 'P4': read, item: before, item + '-R': after}
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
            p.write_text('C0. Consent,P3. Years,P4. Read,A1. Before,A1-R. After\nYes,6 to 10,No,,Yes\n')
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

    def test_export_columns_by_code(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / 'export.csv'
            with p.open('w', newline='', encoding='utf-8') as f:
                w = csv.writer(f)
                w.writerow(['ID', 'C0. I agree', 'A1. Was the burst', 'A1-R. Was the burst', 'R1 For each decision', 'R1-H For each decision'])
                w.writerow(['1', 'Yes', 'Yes', 'Cannot tell', 'Partly', 'Hard'])
            rs = sr.read_export(p)
        self.assertEqual(rs, [{'C0': 'Yes', 'A1': 'Yes', 'A1-R': 'Cannot tell', 'R1': 'Partly', 'R1-H': 'Hard'}])

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
