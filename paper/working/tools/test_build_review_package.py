"""build_review_package.py must stop when it cannot read a PDF, and must find a forbidden string in PDF text,
in a link target inside a compressed object stream and in a PDF inside the finished package."""
import importlib.util
import os
import shutil
import subprocess
import tempfile
import zipfile
import zlib
from pathlib import Path

spec = importlib.util.spec_from_file_location('brp', Path(__file__).resolve().parent / 'build_review_package.py')
brp = importlib.util.module_from_spec(spec); spec.loader.exec_module(brp)
BAD = brp.forbidden()
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


def stops(fn):
    try:
        fn()
    except SystemExit as e:
        return str(e).startswith('STOP')
    return False


with tempfile.TemporaryDirectory() as tmp:
    tmp = Path(tmp)
    leak = tmp / 'leak.pdf'; leak.write_bytes(make_pdf('Prepared by J. ' + NAME))
    assert BAD[0] not in brp.norm(leak.read_bytes().decode('latin-1')), 'the test PDF must hide the name'

    # Missing tools: the build stops instead of passing the file.
    path = os.environ.get('PATH', '')
    os.environ['PATH'] = str(tmp / 'none')
    assert stops(lambda: brp.leaks(leak, 'x/leak.pdf', BAD))
    os.environ['PATH'] = path

    if all(shutil.which(t) for t in ('pdftotext', 'pdfinfo', 'qpdf')):
        assert brp.leaks(leak, 'x/leak.pdf', BAD) == [BAD[0]]
        clean = tmp / 'clean.pdf'; clean.write_bytes(make_pdf('Prepared by the author'))
        assert brp.leaks(clean, 'x/clean.pdf', BAD) == []
        # A tool that fails: the build stops.
        broken = tmp / 'broken.pdf'; broken.write_bytes(b'%PDF-1.5\nnot a pdf\n')
        assert stops(lambda: brp.leaks(broken, 'x/broken.pdf', BAD))
        # The name only in a link target, inside a compressed object stream.
        plain = tmp / 'link.pdf'; plain.write_bytes(make_pdf('Code', uri='https://example.org/' + BAD[0] + '/x'))
        packed = tmp / 'link_os.pdf'
        subprocess.run(['qpdf', '--object-streams=generate', str(plain), str(packed)], check=True)
        assert b'/ObjStm' in packed.read_bytes() and BAD[0] not in brp.norm(packed.read_bytes().decode('latin-1'))
        assert brp.leaks(packed, 'x/link.pdf', BAD) == [BAD[0]]
        # A PDF inside the finished package.
        z = tmp / 'p.zip'
        with zipfile.ZipFile(z, 'w', zipfile.ZIP_DEFLATED) as f:
            f.writestr('JOURNAL/leak.pdf', leak.read_bytes()); f.writestr('README_PACKAGE.md', 'x\n')
        assert [p for p in brp.check(z) if p.startswith('JOURNAL/leak.pdf')]
        with zipfile.ZipFile(z, 'w', zipfile.ZIP_DEFLATED) as f:
            f.writestr('JOURNAL/clean.pdf', clean.read_bytes())
        assert brp.check(z) == []
        print('build_review_package: all checks passed')
    else:
        print('build_review_package: stop check passed; pdftotext, pdfinfo or qpdf missing, other checks skipped')
