"""Exercise merge gates, merge-commit lookup, label synchronization, source-only checks and checksum failures.

GitHub and git are mocked: no network access, no repository changes.
Run from the package root: python3 tools/test_revision_status.py
"""
import copy
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import changes_since
import revision_status as rs

HEAD = 'a' * 40
REPO = 'matkowsky/payment-fraud'
CREDIT = "Jointly drafted by the test contributor and Claude, from the contributor's notes."
STATE = {'status': 'proposed', 'version': '1.1', 'accepted': [], 'drafting_credit': CREDIT}
PR = {'number': 3, 'title': 'Test proposal', 'merged': True, 'merge_commit_sha': HEAD, 'body': '',
      'merged_at': '2026-11-06T00:00:00Z', 'merged_by': {'login': 'test-reviewer'},
      'base': {'ref': 'main', 'repo': {'full_name': REPO}}}
PROPOSED_LINE = '6 November 2026 · Proposed revision for version 1.1 · Not accepted or published · Not peer reviewed'
BODY = '\n\n## Research\n\nUnchanged scientific content.\n'


def make_package(root, state=STATE):
    """A minimal working package beside a minimal version 1.0 baseline."""
    package, baseline = root / 'working', root / 'v1.0'
    for base, line in ((package, PROPOSED_LINE), (baseline, '29 October 2026 · Preprint, version 1.0')):
        (base / 'SOURCE').mkdir(parents=True)
        for name in ('manuscript', 'supplement'):
            (base / 'SOURCE' / (name + '.md')).write_text('# Title\n\n' + line + BODY)
    (package / 'README.md').write_text('<!-- revision-status -->\nOld status\n<!-- /revision-status -->\n')
    (package / 'REVISION_STATUS.json').write_text(json.dumps(state))
    return package, baseline


def build(package, baseline):
    """Stand-in for BUILD.py: copy sources to reader-facing files, then write the change record and manifest."""
    for source, reader in (('manuscript', 'MANUSCRIPT.md'), ('supplement', 'SUPPLEMENT.md')):
        (package / reader).write_text((package / 'SOURCE' / (source + '.md')).read_text())
    changes_since.write(package, baseline)
    rs.refresh_manifest(package)


def snapshot(root):
    return {p: p.read_bytes() for p in root.rglob('*') if p.is_file()}


class MergeGateTests(unittest.TestCase):
    def validate(self, pr=None, ref='refs/heads/main', head=HEAD, state=STATE):
        return rs.validate_merge(PR if pr is None else pr, state, REPO, head, ref)

    def test_verified_merge_records_attribution(self):
        result = self.validate()
        self.assertEqual(result['status'], 'accepted')
        entry = result['accepted'][0]
        self.assertEqual((entry['pr'], entry['merged_by'], entry['merge_commit_sha']), (3, 'test-reviewer', HEAD))
        self.assertEqual(entry['credit'], CREDIT)
        self.assertNotIn('drafting_credit', result)
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

    def test_review_only_pr_cannot_accept(self):
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

    def test_credit_falls_back_to_pr_description_then_pointer(self):
        state = {k: v for k, v in STATE.items() if k != 'drafting_credit'}
        described = self.validate({**PR, 'body': 'Account used: x\nDrafting contribution: Edited by A. Reviewer\n'}, state=state)
        self.assertEqual(described['accepted'][0]['credit'], 'Edited by A. Reviewer')
        undescribed = self.validate(state=state)
        self.assertEqual(undescribed['accepted'][0]['credit'], 'Recorded in PR #3.')


class AcceptTests(unittest.TestCase):
    """accept() with GitHub's API and git mocked: one test for each path."""

    def run_accept(self, responses, state=STATE):
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        root = Path(directory.name)
        package, _ = make_package(root, state)
        output = root / 'github_output'
        output.write_text('')
        env = {'GITHUB_REF': 'refs/heads/main', 'GITHUB_REPOSITORY': REPO, 'GITHUB_OUTPUT': str(output)}
        before = snapshot(package)
        with patch.dict('os.environ', env), \
                patch.object(rs, 'current_head', return_value=HEAD), \
                patch.object(rs, 'github_get', side_effect=lambda path: copy.deepcopy(responses[path])) as get:
            try:
                changed = rs.accept(package)
                error = None
            except ValueError as exc:
                changed, error = None, exc
        return package, before, output.read_text(), changed, error, [c.args[0] for c in get.call_args_list]

    def test_merged_pr_is_found_from_merge_commit(self):
        unrelated_open = {'number': 7, 'merged_at': None, 'merge_commit_sha': 'c' * 40, 'base': {'ref': 'main'}}
        listed = {k: PR[k] for k in ('number', 'merged_at', 'merge_commit_sha', 'base')}
        responses = {'repos/' + REPO + '/branches/main': {'commit': {'sha': HEAD}},
                     'repos/' + REPO + '/commits/' + HEAD + '/pulls': [unrelated_open, listed],
                     'repos/' + REPO + '/pulls/3': PR}
        package, _, output, changed, error, calls = self.run_accept(responses)
        self.assertIsNone(error)
        self.assertTrue(changed)
        self.assertIn('repos/' + REPO + '/commits/' + HEAD + '/pulls', calls)
        state = json.loads((package / 'REVISION_STATUS.json').read_text())
        self.assertEqual([e['pr'] for e in state['accepted']], [3])
        self.assertIn('changed=true', output)
        self.assertIn('Accepted working draft', (package / 'SOURCE' / 'manuscript.md').read_text())
        self.assertIn('[#3]', (package / 'STATUS.md').read_text())

    def test_commit_without_merged_pr_is_refused(self):
        responses = {'repos/' + REPO + '/branches/main': {'commit': {'sha': HEAD}},
                     'repos/' + REPO + '/commits/' + HEAD + '/pulls': []}
        package, before, output, _, error, _ = self.run_accept(responses)
        self.assertRegex(str(error), 'No single merged pull request')
        self.assertEqual(snapshot(package), before)
        self.assertEqual(output, '')

    def test_main_advanced_is_refused(self):
        responses = {'repos/' + REPO + '/branches/main': {'commit': {'sha': 'b' * 40}}}
        package, before, output, _, error, calls = self.run_accept(responses)
        self.assertRegex(str(error), 'Main advanced')
        self.assertEqual(calls, ['repos/' + REPO + '/branches/main'])
        self.assertEqual(snapshot(package), before)
        self.assertEqual(output, '')

    def test_already_recorded_merge_is_a_no_op(self):
        recorded = rs.validate_merge(PR, STATE, REPO, HEAD, 'refs/heads/main')
        package, before, output, changed, error, calls = self.run_accept({}, state=recorded)
        self.assertIsNone(error)
        self.assertFalse(changed)
        self.assertEqual(calls, [])
        self.assertEqual(snapshot(package), before)
        self.assertEqual(output, '')


class PackageCheckTests(unittest.TestCase):
    def setUp(self):
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        self.package, self.baseline = make_package(Path(directory.name))

    def test_labels_idempotence_and_tamper_detection(self):
        state = rs.validate_merge(PR, STATE, REPO, HEAD, 'refs/heads/main')
        rs.sync_labels(state, self.package)
        before = snapshot(self.package)
        rs.sync_labels(state, self.package)
        self.assertEqual(before, snapshot(self.package))
        for name in ('manuscript', 'supplement'):
            text = (self.package / 'SOURCE' / (name + '.md')).read_text()
            self.assertTrue(text.endswith(BODY))
            self.assertIn('Accepted working draft for version 1.1 · Not published', text)
        self.assertIn(CREDIT, (self.package / 'STATUS.md').read_text())
        build(self.package, self.baseline)
        rs.check_package(self.package, self.baseline)
        (self.package / 'MANUSCRIPT.md').write_text((self.package / 'MANUSCRIPT.md').read_text() + 'unrecorded edit')
        with self.assertRaisesRegex(ValueError, 'Manifest mismatch'):
            rs.check_package(self.package, self.baseline)

    def test_stale_change_record_is_detected(self):
        build(self.package, self.baseline)
        source = self.package / 'SOURCE' / 'supplement.md'
        source.write_text(source.read_text().replace('Unchanged scientific content.', 'Revised scientific content.'))
        for reader in ('MANUSCRIPT.md', 'SUPPLEMENT.md'):
            self.assertTrue((self.package / reader).is_file())
        with self.assertRaisesRegex(ValueError, 'Stale change record'):
            rs.check_package(self.package, self.baseline)

    def test_sources_only_check_accepts_unbuilt_contributor_edit(self):
        build(self.package, self.baseline)
        source = self.package / 'SOURCE' / 'manuscript.md'
        source.write_text(source.read_text() + '\nA contributor paragraph.\n')
        rs.check_package(self.package, self.baseline, sources_only=True)
        with self.assertRaises(ValueError):
            rs.check_package(self.package, self.baseline)

    def test_sources_only_check_rejects_a_hand_edited_status(self):
        source = self.package / 'SOURCE' / 'manuscript.md'
        source.write_text(source.read_text().replace('Proposed revision for version 1.1 · Not accepted or published',
                                                     'Accepted working draft for version 1.1 · Not published'))
        with self.assertRaisesRegex(ValueError, 'Stale or duplicated document status'):
            rs.check_package(self.package, self.baseline, sources_only=True)


if __name__ == '__main__':
    unittest.main()
