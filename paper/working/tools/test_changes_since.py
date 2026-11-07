"""Check the change record: edits are marked, Markdown is shown literally and counts are right.

Run from the package root: python3 tools/test_changes_since.py
"""
from pathlib import Path
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


if __name__ == '__main__':
    unittest.main()
