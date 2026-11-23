"""Test the anonymous review package: it builds, names no author and keeps the supplement's layout. The builder
must stop when it cannot read a PDF, and must find a forbidden string in PDF text, in a link target inside a
compressed object stream and in a PDF inside the finished package. It must also stop when the anonymous supplement
is missing, and fail the check when the finished package lacks it. With --require-tools a missing PDF tool fails the test
instead of skipping the PDF checks."""
import os
import pathlib
import shutil
import subprocess
import sys
import tempfile
import zipfile
import zlib

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import build_review_package as pkg

REAL = pkg.B
BAD = pkg.forbidden()
NAME = BAD[0].capitalize()  # read at run time, so this file carries no forbidden string


def make_pdf(text, uri=None):
    """One-page PDF whose text sits in a Flate-compressed stream; optional link annotation."""
    content = zlib.compress(f'BT /F1 12 Tf 72 720 Td ({text}) Tj ET'.encode())
    objs = [b'<< /Type /Catalog /Pages 2 0 R >>', b'<< /Type /Pages /Kids [3 0 R] /Count 1 >>',
            (b'<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] /Resources << /Font << /F1 4 0 R >> >> '
             b'/Contents 6 0 R' + (b' /Annots [5 0 R]' if uri else b'') + b' >>'),
            b'<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>',
            (b'<< /Type /Annot /Subtype /Link /Rect [72 700 200 720] /A << /S /URI /URI (%s) >> >>' % uri.encode()
             if uri else b'null'),
            b'<< /Length %d /Filter /FlateDecode >>\nstream\n' % len(content) + content + b'\nendstream']
    out, offs = bytearray(b'%PDF-1.5\n'), []
    for i, o in enumerate(objs, 1):
        offs.append(len(out)); out += b'%d 0 obj\n' % i + o + b'\nendobj\n'
    x = len(out)
    out += b'xref\n0 %d\n0000000000 65535 f \n' % (len(objs) + 1) + b''.join(b'%010d 00000 n \n' % o for o in offs)
    out += b'trailer\n<< /Size %d /Root 1 0 R >>\nstartxref\n%d\n%%%%EOF\n' % (len(objs) + 1, x)
    return bytes(out)


def tree(root, supplement=None):
    """A small repository: the folders the builder reads, the forbidden list, and optionally the anonymous supplement."""
    for rel, data in (('SUPPLEMENT/a.csv', b'x\n'), ('FIGURES/f.txt', b'x\n'), ('tools/t.py', b'x = 1\n'),
                      ('JOURNAL_BUILD.py', (REAL / 'JOURNAL_BUILD.py').read_bytes()), ('JOURNAL/SUPPLEMENT_ANONYMOUS.pdf', supplement),
                      ('JOURNAL/MANUSCRIPT_ACM_ANONYMOUS.pdf', make_pdf('Anonymous manuscript'))):
        if data is not None:
            (root / rel).parent.mkdir(parents=True, exist_ok=True); (root / rel).write_bytes(data)


def stops(fn):
    try:
        fn()
    except SystemExit as e:
        return str(e).startswith('STOP')
    return False


with tempfile.TemporaryDirectory() as d:
    d = pathlib.Path(d)
    leak = d / 'leak.pdf'; leak.write_bytes(make_pdf('Prepared by J. ' + NAME))
    assert BAD[0] not in pkg.norm(leak.read_bytes().decode('latin-1')), 'the test PDF must hide the name'

    # Missing tools: the build stops instead of passing the file.
    path = os.environ.get('PATH', '')
    os.environ['PATH'] = str(d / 'none')
    assert stops(lambda: pkg.leaks(leak, 'x/leak.pdf', BAD))
    os.environ['PATH'] = path

    # A missing anonymous supplement: the build stops before it reads any PDF, so this runs without the PDF tools.
    pkg.B = d / 'no_supplement'; tree(pkg.B)
    assert stops(lambda: pkg.build(d / 'ns.zip')) and not (d / 'ns.zip').exists()
    pkg.B = REAL

    if not all(shutil.which(t) for t in ('pdftotext', 'pdfinfo', 'qpdf')):
        if '--require-tools' in sys.argv:
            sys.exit('FAIL: pdftotext, pdfinfo or qpdf is missing, so the PDF checks cannot run. Install poppler-utils and qpdf.')
        print('review package: stop check ok; pdftotext, pdfinfo or qpdf missing, other checks skipped')
        sys.exit(0)

    # --require-tools makes a missing PDF tool a failure instead of a skip. The pull-request job passes it.
    for flag, code in (('--require-tools', 1), (None, 0)):
        r = subprocess.run([sys.executable, __file__] + ([flag] if flag else []), env={'PATH': str(d / 'none')},
                           capture_output=True)
        assert r.returncode == code, (flag, r.returncode, r.stdout, r.stderr)

    assert pkg.leaks(leak, 'x/leak.pdf', BAD) == [BAD[0]]
    clean = d / 'clean.pdf'; clean.write_bytes(make_pdf('Prepared by the author'))
    assert pkg.leaks(clean, 'x/clean.pdf', BAD) == []
    # A tool that fails: the build stops.
    broken = d / 'broken.pdf'; broken.write_bytes(b'%PDF-1.5\nnot a pdf\n')
    assert stops(lambda: pkg.leaks(broken, 'x/broken.pdf', BAD))
    # The name only in a link target, inside a compressed object stream.
    plain = d / 'link.pdf'; plain.write_bytes(make_pdf('Code', uri='https://example.org/' + BAD[0] + '/x'))
    packed = d / 'link_os.pdf'
    subprocess.run(['qpdf', '--object-streams=generate', str(plain), str(packed)], check=True)
    assert b'/ObjStm' in packed.read_bytes() and BAD[0] not in pkg.norm(packed.read_bytes().decode('latin-1'))
    assert pkg.leaks(packed, 'x/link.pdf', BAD) == [BAD[0]]
    # A PDF inside the finished package.
    z = d / 'p.zip'
    with zipfile.ZipFile(z, 'w', zipfile.ZIP_DEFLATED) as f:
        f.writestr('JOURNAL/leak.pdf', leak.read_bytes()); f.writestr('README_PACKAGE.md', 'x\n')
    assert [p for p in pkg.check(z) if p.startswith('JOURNAL/leak.pdf')]

    # A package without the anonymous supplement fails the check, and with it the check passes.
    pkg.B = d / 'with_supplement'; tree(pkg.B, make_pdf('Anonymous supplement'))
    ok = d / 'ok.zip'; pkg.build(ok)
    assert pkg.check(ok) == [] and 'JOURNAL/SUPPLEMENT_ANONYMOUS.pdf' in zipfile.ZipFile(ok).namelist()
    lacks = d / 'lacks.zip'
    with zipfile.ZipFile(lacks, 'w') as f:
        f.writestr('README_PACKAGE.md', 'x\n'); f.writestr('SUPPLEMENT/a.csv', 'x\n')
    assert [p for p in pkg.check(lacks) if p.startswith('JOURNAL/SUPPLEMENT_ANONYMOUS.pdf')]
    # A supplement that names the author is left out, and the check then fails for the missing file.
    (pkg.B / 'JOURNAL/SUPPLEMENT_ANONYMOUS.pdf').write_bytes(make_pdf('Prepared by J. ' + NAME))
    gone = d / 'gone.zip'; kept, left = pkg.build(gone)
    assert 'JOURNAL/SUPPLEMENT_ANONYMOUS.pdf' in left and pkg.check(gone)
    pkg.B = REAL

    # The real package.
    out = d / 'REVIEW_PACKAGE.zip'
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
