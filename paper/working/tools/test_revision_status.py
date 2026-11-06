"""Exercise merge gates, label synchronization and checksum failure detection."""
import copy
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from revision_status import validate_merge, sync_labels, refresh_manifest, check_package

STATE = {'status': 'proposed', 'version': '1.1', 'proposal_pr': 3,
         'drafting_credit': 'Jointly drafted by the test contributor and Claude, from the contributor\'s notes.'}
HEAD = 'a' * 40
REPO = 'matkowsky/payment-fraud'
PR = {'number': 3, 'merged': True, 'merge_commit_sha': HEAD,
      'merged_at': '2026-11-06T00:00:00Z', 'merged_by': {'login': 'test-reviewer'},
      'base': {'ref': 'main', 'repo': {'full_name': REPO}}}


class StatusTests(unittest.TestCase):
    def validate(self, pr=None, ref='refs/heads/main', head=HEAD):
        return validate_merge(PR if pr is None else pr, STATE, REPO, head, ref)

    def test_verified_merge_records_attribution(self):
        result = self.validate()
        self.assertEqual(result['status'], 'accepted')
        self.assertEqual(result['merged_by'], 'test-reviewer')
        self.assertEqual(result['merge_commit_sha'], HEAD)
        self.assertEqual(STATE['status'], 'proposed')

    def test_unmerged_and_closed_without_merge_cannot_accept(self):
        for state in ('open', 'closed'):
            with self.subTest(state=state), self.assertRaises(ValueError):
                self.validate({**PR, 'state': state, 'merged': False})

    def test_other_branch_cannot_accept(self):
        with self.assertRaises(ValueError):
            self.validate(ref='refs/heads/proposal')

    def test_wrong_checked_out_commit_cannot_accept(self):
        with self.assertRaises(ValueError):
            self.validate(head='b' * 40)

    def test_wrong_proposal_cannot_accept(self):
        with self.assertRaises(ValueError):
            self.validate({**PR, 'number': 1})

    def test_other_target_cannot_accept(self):
        for field, value in [('ref', 'release'), ('repo', {'full_name': 'elsewhere/repo'})]:
            pr = copy.deepcopy(PR)
            pr['base'][field] = value
            with self.subTest(field=field), self.assertRaises(ValueError):
                self.validate(pr)

    def test_missing_attribution_cannot_accept(self):
        with self.assertRaises(ValueError):
            self.validate({**PR, 'merged_by': None})

    def test_labels_idempotence_and_tamper_detection(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / 'SOURCE').mkdir()
            body = '\n\n## Research\n\nUnchanged scientific content.\n'
            for name in ('manuscript', 'supplement'):
                (root / 'SOURCE' / (name + '.md')).write_text(
                    '# Title\n\n6 November 2026 · Proposed revision for version 1.1 · Not accepted or published · Not peer reviewed' + body)
            (root / 'README.md').write_text('<!-- revision-status -->\nOld status\n<!-- /revision-status -->\n')
            state = self.validate()
            sync_labels(state, root)
            self.assertIn(STATE['drafting_credit'], (root / 'STATUS.md').read_text())
            before = {p: p.read_bytes() for p in root.rglob('*') if p.is_file()}
            sync_labels(state, root)
            self.assertEqual(before, {p: p.read_bytes() for p in root.rglob('*') if p.is_file()})
            for source, reader in [('manuscript', 'MANUSCRIPT.md'), ('supplement', 'SUPPLEMENT.md')]:
                text = (root / 'SOURCE' / (source + '.md')).read_text()
                self.assertTrue(text.endswith(body))
                self.assertIn('Accepted working draft', text)
                self.assertIn('Not published', text)
                (root / reader).write_text(text)
            refresh_manifest(root)
            check_package(root)
            with patch.dict('os.environ', {'PROPOSAL_NUMBER': '3'}):
                with self.assertRaisesRegex(ValueError, 'retain proposed status'):
                    check_package(root)
            (root / 'MANUSCRIPT.md').write_text((root / 'MANUSCRIPT.md').read_text() + 'unrecorded edit')
            with self.assertRaisesRegex(ValueError, 'Manifest mismatch'):
                check_package(root)


if __name__ == '__main__':
    unittest.main()
