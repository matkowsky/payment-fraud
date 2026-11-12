"""Synthetic exact-equality and normal/optimized validation regressions."""
import copy
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

import investigation_conformance as ic
import outcome_conformance as oc


class TimestampTests(unittest.TestCase):
    def setUp(self):
        self.schema = json.loads(ic.SCHEMA.read_text())
        self.records = json.loads(ic.VALID.read_text())['records']

    def findings(self, start, end):
        records = copy.deepcopy(self.records)
        q = next(r for r in records if r['record_id'] == 'Q-2')
        q['evaluated_interval'] = {'from': start, 'to': end}
        return {f[0] for f in ic.check(records, self.schema)}

    def test_equivalent_spelling(self):
        pairs = [
            ('2026-04-01T00:00:00+00:00', '2026-04-30T00:00:00+00:00'),
            ('2026-04-01T05:30:00+05:30', '2026-04-30T05:30:00+05:30'),
            ('2026-03-31T17:00:00-07:00', '2026-04-29T17:00:00-07:00'),
            ('2026-04-01T00:00Z', '2026-04-30T00:00Z'),
            ('2026-04-01T00:00:00-00:00', '2026-04-30T00:00:00-00:00')]
        for digits in ['000', '0' * 5000]:
            pairs.append(('2026-04-01T00:00:00.' + digits + 'Z', '2026-04-30T00:00:00Z'))
        for start, end in pairs:
            with self.subTest(start=start[:50]):
                self.assertEqual(self.findings(start, end), set())

    def test_true_narrowing(self):
        for fraction in ['0000001', '0' * 4999 + '1']:
            self.assertEqual(self.findings('2026-04-01T00:00:00.' + fraction + 'Z',
                                           '2026-04-30T00:00:00Z'), {'IR-05'})
        self.assertEqual(self.findings('2026-04-02T00:00:00Z', '2026-04-30T00:00:00Z'), {'IR-05', 'IR-08'})
        self.assertEqual(self.findings('2026-04-01T00:00:00Z', '2026-04-29T23:59:59.9999999Z'), {'IR-05', 'IR-08'})

    def test_key_boundaries_and_fraction(self):
        # Represent an instant before UTC year 1 without constructing a UTC datetime.
        self.assertEqual(ic.exact_instant('0001-01-01T00:00:00+23:59')[0],
                         ic.exact_instant('0001-01-01T00:00:00Z')[0] - 86340)
        self.assertEqual(ic.exact_instant('9999-12-31T23:59:59-23:59')[1], '')
        self.assertEqual(ic.exact_instant('2026-04-01T00:00:00.12300Z'), ic.exact_instant('2026-04-01T05:30:00.123+05:30'))
        self.assertNotEqual(ic.exact_instant('2026-04-01T00:00:00.0000001Z'), ic.exact_instant('2026-04-01T00:00:00.0000002Z'))

    def test_naive_rejected_in_normal_and_optimized_python(self):
        records = copy.deepcopy(self.records)
        q = next(r for r in records if r['record_id'] == 'Q-2')
        q['evaluated_interval']['from'] = '2026-04-01T00:00:00'
        self.assertTrue(oc.validate('2026-04-01T00:00:00', {'type':'string', 'format':'date-time'}, {}))
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / 'naive.json'
            p.write_text(json.dumps({'records': records}))
            for flags in [[], ['-O']]:
                run = subprocess.run([sys.executable, *flags, str(Path(ic.__file__)), str(p)], capture_output=True, text=True)
                self.assertEqual(run.returncode, 1, run.stderr)
                self.assertIn('SCHEMA', run.stdout)
                self.assertNotIn('Traceback', run.stderr)


if __name__ == '__main__':
    unittest.main()
