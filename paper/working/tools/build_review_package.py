"""Build the anonymous review package: the supplement's data, figures and tools.

    python3 tools/build_review_package.py [OUTPUT.zip]

Default output: build/review_package/REVIEW_PACKAGE.zip. The package keeps the repository layout
(SUPPLEMENT/, FIGURES/, tools/ and JOURNAL/SUPPLEMENT_ANONYMOUS.pdf), so the anonymous supplement's links
resolve when it is opened from the package's JOURNAL folder.

A file is left out when its path or contents contain a string that JOURNAL_BUILD.py forbids in the anonymous
copies (the author's surname and the preprint's DOIs), or when it is a compiled Python cache. A PDF is also read
with pdftotext (text), pdfinfo (properties) and qpdf (every object decompressed, so link targets count). The
build stops if any of the three is missing or fails. README_PACKAGE.md in the package lists every file left out.
After the build, every entry of the finished package, PDFs read the same way, and the anonymous manuscript are
checked again. Repository files are only read.
"""
import ast
import pathlib
import re
import shutil
import subprocess
import sys
import tempfile
import unicodedata
import zipfile

B = pathlib.Path(__file__).resolve().parent.parent
FOLDERS = ('SUPPLEMENT', 'FIGURES', 'tools')
EXTRA = ('JOURNAL/SUPPLEMENT_ANONYMOUS.pdf',)
UPLOADS = ('JOURNAL/MANUSCRIPT_ACM_ANONYMOUS.pdf',)  # uploaded beside the package, not in it
STAMP = (2026, 1, 1, 0, 0, 0)


def norm(s):
    return re.sub(r'[^a-z0-9]', '', unicodedata.normalize('NFKC', s).lower())


def forbidden():
    """The same list as JOURNAL_BUILD.py: its surname entry and each DOI in its DOIS list."""
    src = (B / 'JOURNAL_BUILD.py').read_text(encoding='utf-8')
    dois = ast.literal_eval(re.search(r'^DOIS = (\[.*?\])', src, re.M).group(1))
    surname = re.search(r"^FORBIDDEN = \['([a-z]+)'\] \+ \[norm\(d\) for d in DOIS\]$", src, re.M).group(1)
    return [surname] + [norm(d) for d in dois]


def pdf_text(path):
    """Text, properties and decompressed objects of a PDF. Stops the build if a tool is missing or fails."""
    out = []
    for tool, ok in ((['pdftotext', '-q', str(path), '-'], (0,)), (['pdfinfo', str(path)], (0,)),
                     (['qpdf', '--qdf', '--object-streams=disable', str(path), '-'], (0, 3))):  # qpdf: 3 = warnings
        if not shutil.which(tool[0]):
            sys.exit(f'STOP: {tool[0]} is missing, so {path} cannot be checked. Install poppler-utils and qpdf.')
        r = subprocess.run(tool, capture_output=True)
        if r.returncode not in ok:
            sys.exit(f'STOP: {tool[0]} failed on {path} (exit {r.returncode}), so it cannot be checked.')
        out.append(r.stdout.decode('latin-1'))
    return '\n'.join(out)


def leaks(path, rel, bad):
    text = rel + '\n' + path.read_bytes().decode('latin-1')
    if path.suffix.lower() == '.pdf':
        text += '\n' + pdf_text(path)
    n = norm(text)
    return [f for f in bad if f in n]


def candidates():
    for folder in FOLDERS:
        for p in sorted((B / folder).rglob('*')):
            if p.is_file():
                yield p
    for rel in EXTRA:
        p = B / rel
        if p.is_file():
            yield p


def build(out):
    bad = forbidden()
    kept, left = [], []
    for p in candidates():
        rel = p.relative_to(B).as_posix()
        if '__pycache__' in p.parts or p.suffix == '.pyc':
            continue
        found = leaks(p, rel, bad)
        (left if found else kept).append(rel)
    readme = ['# Review package', '',
              'This package holds the data, figures and scripts that the supplement links to, in the same layout.',
              "Open JOURNAL/SUPPLEMENT_ANONYMOUS.pdf from this folder so that its links resolve.", '',
              '- SUPPLEMENT/: the CSV tables and record schemas.',
              '- FIGURES/: the figures.',
              '- tools/: scripts, prompts, packets, run records, rulings and results.', '',
              'Run scripts from this folder with Python 3. Some also need the manuscript sources or build scripts, '
              'which are not included.', '',
              f'Left out for anonymous review ({len(left)} files): files that name the author or cite the preprint.', '']
    readme += ['- ' + r for r in left]
    out.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(out, 'w', zipfile.ZIP_DEFLATED) as z:
        info = zipfile.ZipInfo('README_PACKAGE.md', STAMP)
        z.writestr(info, '\n'.join(readme) + '\n', zipfile.ZIP_DEFLATED)
        for rel in kept:
            info = zipfile.ZipInfo(rel, STAMP)
            info.external_attr = ((B / rel).stat().st_mode & 0o777) << 16
            z.writestr(info, (B / rel).read_bytes(), zipfile.ZIP_DEFLATED)
    return kept, left


def check(out):
    """Reopen the package and confirm no entry, and no uploaded PDF, names the author or cites the preprint."""
    bad = forbidden()
    problems = []
    with zipfile.ZipFile(out) as z, tempfile.TemporaryDirectory() as tmp:
        for i, name in enumerate(z.namelist()):
            path = pathlib.Path(tmp) / (str(i) + pathlib.PurePosixPath(name).suffix)
            path.write_bytes(z.read(name))
            found = leaks(path, name, bad)
            if found:
                problems.append(f'{name}: {found}')
    for rel in UPLOADS:
        if not (B / rel).is_file():
            sys.exit(f'STOP: {rel} is missing; build it with JOURNAL_BUILD.py first.')
        found = leaks(B / rel, rel, bad)
        if found:
            problems.append(f'{rel}: {found}')
    return problems


if __name__ == '__main__':
    out = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else B / 'build' / 'review_package' / 'REVIEW_PACKAGE.zip'
    kept, left = build(out)
    problems = check(out)
    print(f'{out}: {len(kept)} files kept, {len(left)} left out')
    for r in left:
        print('  left out:', r)
    if problems:
        print('FAIL:', *problems, sep='\n  ')
        sys.exit(1)
