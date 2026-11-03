#!/usr/bin/env python3
"""Usage: verify_roundtrip.py READER.md REFS.json [ORIGINAL_SOURCE.md]
Reverse READER -> source, rebuild, require byte-identical reader output."""
import hashlib, subprocess, sys, difflib
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from reverse_source import reverse, repair_quotes
R = Path(sys.argv[1]).read_bytes(); refs = sys.argv[2]
S = reverse(R.decode('utf-8'))
Path('/tmp/_rt_source.md').write_text(S); Path('/tmp/_rt_reader.md').unlink(missing_ok=True)
subprocess.run([sys.executable, str(Path(__file__).parent / 'forward_md.py'), '/tmp/_rt_source.md', refs, '/tmp/_rt_reader.md'], check=True)
R2 = Path('/tmp/_rt_reader.md').read_bytes()
if R != R2:
    S2, fixed = repair_quotes(S, R.decode(), R2.decode())
    if fixed:
        print('quote-only repairs on reader lines:', fixed)
        S = S2; Path('/tmp/_rt_source.md').write_text(S)
        subprocess.run([sys.executable, str(Path(__file__).parent / 'forward_md.py'), '/tmp/_rt_source.md', refs, '/tmp/_rt_reader.md'], check=True)
        R2 = Path('/tmp/_rt_reader.md').read_bytes()
print('reader sha256   ', hashlib.sha256(R).hexdigest()); print('roundtrip sha256', hashlib.sha256(R2).hexdigest())
print('ROUNDTRIP', 'IDENTICAL' if R == R2 else 'DIFFERENT')
if R != R2:
    for l in list(difflib.unified_diff(R.decode().splitlines(), R2.decode().splitlines(), lineterm='', n=0))[:40]: print(l[:200])
if len(sys.argv) > 3:
    O = Path(sys.argv[3]).read_text()
    print('vs original source: identical' if O == S else 'vs original source: %d diff lines' % sum(1 for l in difflib.unified_diff(O.splitlines(), S.splitlines(), lineterm='', n=0) if l[:1] in '+-' and l[:3] not in ('+++','---')))
