"""Check the change record: edits are marked, Markdown is shown literally and counts are right.

Run from the package root: python3 tools/test_changes_since.py
"""
from pathlib import Path
import subprocess
import tempfile
import unittest

import changes_since


class ChangeRecordTests(unittest.TestCase):
    def test_redline_marks_edits_and_neutralizes_markdown(self):
        old = '# Title\n\nKept paragraph.\n\nThe rule uses bias with [a link](../X.md) and $|q-r|$.\n\nRemoved paragraph about nothing else.\n'
        new = '# Title\n\nKept paragraph.\n\nThe rule uses error with [a link](../X.md) and $|q-r|$.\n'
        changes = changes_since.compare(old, new)
        self.assertEqual([kind for _, kind, _ in changes], ['changed', 'removed'])
        heading, _, text = changes[0]
        self.assertEqual(heading, 'Title')
        self.assertIn('<del>bias</del><ins>error</ins>', text)
        self.assertIn('\\[a link\\]\\(../X.md\\)', text)
        self.assertIn('\\$\\|q-r\\|\\$', text)

    def test_record_lists_both_documents(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            for base, word in ((root / 'v1.0', 'old'), (root / 'working', 'new')):
                (base / 'SOURCE').mkdir(parents=True)
                (base / 'SOURCE' / 'manuscript.md').write_text('# M\n\nAn ' + word + ' sentence.\n')
                (base / 'SOURCE' / 'supplement.md').write_text('# S\n\nSame.\n')
            text = changes_since.render(root / 'working', root / 'v1.0')
            self.assertIn('| Manuscript | [Markdown](MANUSCRIPT.md), [PDF](MANUSCRIPT.pdf) | 1 | 0 | 0 |', text)
            self.assertIn('| Supplement | [Markdown](SUPPLEMENT.md), [PDF](SUPPLEMENT.pdf) | 0 | 0 | 0 |', text)
            self.assertIn('No changes.', text)


    def test_citations_show_current_numbers(self):
        text = changes_since.number_citations('See [@A; @B], [@A] and [@Z].', {'A': 7, 'B': 3})
        self.assertEqual(text, 'See [3, 7], [7] and [@Z].')

    def test_each_change_names_its_pull_request(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            work, base = root / 'paper' / 'working', root / 'paper' / 'v1.0'
            for d in (work, base):
                (d / 'SOURCE').mkdir(parents=True)
                (d / 'SOURCE' / 'supplement.md').write_text('# S\n\nSame.\n')
            (base / 'SOURCE' / 'manuscript.md').write_text('# M\n\n1 May · Preprint\n\nKept.\n\nOld claim.\n')
            def commit(text, subject, author='Someone'):
                (work / 'SOURCE' / 'manuscript.md').write_text(text)
                subprocess.run(['git', 'add', '-A'], cwd=root, check=True)
                subprocess.run(['git', '-c', 'user.name=' + author, '-c', 'user.email=a@example.com', 'commit', '-q', '-m', subject],
                               cwd=root, check=True)
            subprocess.run(['git', 'init', '-q'], cwd=root, check=True)
            commit('# M\n\n1 May · Preprint\n\nKept.\n\nOld claim.\n', 'Copy version 1.0')
            commit('# M\n\n1 May · Preprint\n\nKept.\n\nNew claim.\n', 'Merge pull request #7 from a/b')
            commit('# M\n\n2 May · Draft\n\nKept.\n\nNew claim.\n', 'Synchronize', changes_since.STATUS_AUTHOR)
            text = changes_since.render(work, base)
            self.assertIn('by [#7](' + changes_since.REPO_URL + '/pull/7):**', text)
            self.assertIn('by the automatic status update:**', text)
            self.assertIn('<del>Old</del><ins>New</ins>', text)

    def test_record_without_history_omits_attribution(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            for base, word in ((root / 'v1.0', 'old'), (root / 'working', 'new')):
                (base / 'SOURCE').mkdir(parents=True)
                (base / 'SOURCE' / 'manuscript.md').write_text('# M\n\nAn ' + word + ' sentence.\n')
                (base / 'SOURCE' / 'supplement.md').write_text('# S\n\nSame.\n')
            text = changes_since.render(root / 'working', root / 'v1.0')
            self.assertIn('**Changed, under "M":**', text)
            self.assertNotIn(', by ', text)


if __name__ == '__main__':
    unittest.main()
