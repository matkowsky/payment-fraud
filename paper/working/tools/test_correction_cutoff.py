"""OR-10 reads a correction only once the system has learned it. Synthetic records; run from paper/working:
python3 tools/test_correction_cutoff.py"""
import copy
import json
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import outcome_conformance as oc  # noqa: E402

CORRECTION_LEARNED = '2026-04-01T00:00:00Z'


class CorrectionCutoffTests(unittest.TestCase):
    def setUp(self):
        self.schema = json.loads(oc.SCHEMA.read_text(encoding='utf-8'))
        self.records = json.loads(oc.VALID.read_text(encoding='utf-8'))['records']
        self.t4 = next(r for r in self.records if r['record_id'] == 'T-4')        # PA-3's chargeback channel, open
        self.reading = next(r for r in self.records if r['record_id'] == 'RD-2')  # read on 1 March: open, pending

    def history(self, read_time, state):
        """The valid history, plus a correction of T-4 learned on 1 April and one more reading of PA-3."""
        records = copy.deepcopy(self.records)
        fix = copy.deepcopy(self.t4)
        fix.update(record_id='T-4-FIX', corrects='T-4', state='unknown', learned_at=CORRECTION_LEARNED,
                   cause={'kind': 'unknown', 'reason': 'synthetic correction'})
        extra = copy.deepcopy(self.reading)
        extra.update(record_id='RD-X', read_time=read_time, channel_state=state)  # the window is still open: pending
        return records + [fix, extra]

    def findings(self, records):
        return [f for f in oc.check(records, self.schema) if f[1] in ('RD-2', 'RD-X')]

    def test_correction_is_schema_valid(self):
        self.assertFalse([f for f in oc.check(self.history('2026-03-01T00:00:00Z', 'open'), self.schema) if f[0] == 'SCHEMA'])

    def test_read_before_the_correction_was_learned_sees_the_earlier_state(self):
        # On 1 March the system had not learned the correction, so the channel still reads open.
        self.assertEqual(self.findings(self.history('2026-03-01T00:00:00Z', 'open')), [])

    def test_read_before_the_correction_cannot_use_it(self):
        found = self.findings(self.history('2026-03-01T00:00:00Z', 'unknown'))
        self.assertEqual({f[:2] for f in found if f[0] == 'OR-10'}, {('OR-10', 'RD-X')})

    def test_read_after_the_correction_was_learned_uses_it(self):
        self.assertEqual(self.findings(self.history('2026-04-02T00:00:00Z', 'unknown')), [])
        found = self.findings(self.history('2026-04-02T00:00:00Z', 'open'))
        self.assertEqual({f[:2] for f in found if f[0] == 'OR-10'}, {('OR-10', 'RD-X')})


if __name__ == '__main__':
    unittest.main()
