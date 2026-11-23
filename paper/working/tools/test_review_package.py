"""Test the anonymous review package: it builds, names no author and keeps the supplement's layout."""
import pathlib
import sys
import tempfile
import zipfile

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import build_review_package as pkg

with tempfile.TemporaryDirectory() as d:
    out = pathlib.Path(d) / 'REVIEW_PACKAGE.zip'
    kept, left = pkg.build(out)
    assert pkg.check(out) == [], pkg.check(out)
    names = set(zipfile.ZipFile(out).namelist())
    assert 'README_PACKAGE.md' in names
    assert 'SUPPLEMENT/S1_CITED_SOURCE_NOTES.csv' in names and 'tools/investigation_conformance.py' in names
    assert 'tools/build_review_package.py' in names
    assert not any('__pycache__' in n or n.endswith('.pyc') for n in names)
    readme = zipfile.ZipFile(out).read('README_PACKAGE.md').decode('utf-8')
    assert all(('- ' + r) in readme for r in left) and f'({len(left)} files)' in readme
    assert set(left).isdisjoint(names) and len(names) == len(kept) + 1
print('review package: ok')
