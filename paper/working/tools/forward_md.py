#!/usr/bin/env python3
"""Forward path identical to BUILD.py step 3 for Markdown only (no TeX/PDF).
Usage: forward_md.py SOURCE.md REFS.json OUT_READER.md  (run from package root)"""
import re, subprocess, sys, tempfile
from pathlib import Path
src = Path(sys.argv[1]).read_text()
src = re.sub(r'\]\(\.\./', '](', src)
src += '\n\n## References\n\n::: {#refs}\n:::\n'
with tempfile.TemporaryDirectory() as d:
    t = Path(d) / 'in.md'; t.write_text(src); a = Path(d) / 'ast.json'
    subprocess.run(['pandoc', str(t), '-f', 'markdown-implicit_figures', '--citeproc', '--bibliography=' + sys.argv[2],
                    '--csl=SOURCE/references.csl', '-M', 'link-citations=true', '-t', 'json', '-o', str(a)], check=True)
    subprocess.run(['pandoc', str(a), '-f', 'json', '-t', 'gfm', '--wrap=none', '-o', sys.argv[3]], check=True)
