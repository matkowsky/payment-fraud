#!/usr/bin/env python3
"""Reverse converter: reader-facing Markdown (citeproc output) -> citation-key SOURCE markdown.

Usage: reverse_source.py READER.md OUT_SOURCE.md
Round-trip contract: forward(reverse(R)) == R, where forward() is the BUILD.py
Markdown path (pandoc --citeproc, gfm, wrap=none). Verified with verify_roundtrip.py.
"""
import re, sys
from pathlib import Path

REFSEP = '\n## References'
REFID = re.compile(r'<div id="ref-([^"]+)" class="csl-entry">\s*\n\s*\\\[(\d+)\\\]')
ITEM = r'\[(\d+)\]\(#ref-[^)]+\)'
GROUP = re.compile(r'\\\[(' + ITEM + r'(?:(?:, |–)' + ITEM + r')*)\\\]')
PART = re.compile(ITEM + r'|, |–')

def reverse(reader: str) -> str:
    i = reader.rfind(REFSEP)
    assert i > 0, 'no References section'
    body, refs = reader[:i], reader[i:]
    num2key = {int(n): k for k, n in REFID.findall(refs)}
    assert num2key and sorted(num2key) == list(range(1, len(num2key) + 1)), 'reference numbering not contiguous'

    def cite(m):
        inner, keys, pos, last = m.group(1), [], 0, None
        toks = re.findall(r'\[(\d+)\]\(#ref-([^)]+)\)|(, |–)', inner)
        prev = None; rng = False
        for n, k, sep in toks:
            if sep:
                rng = (sep == '–'); continue
            n = int(n)
            assert num2key[n] == k, ('number/key mismatch', n, k, num2key[n])
            if rng:
                keys.extend(num2key[x] for x in range(prev + 1, n + 1))
            else:
                keys.append(k)
            prev, rng = n, False
        return '[' + '; '.join('@' + k for k in keys) + ']'

    out = GROUP.sub(cite, body)
    assert '](#ref-' not in out, 'unconverted citation remains'
    out = re.sub(r'\]\((FIGURES/|SUPPLEMENT/|SUPPLEMENT\.md|MANUSCRIPT_|REFERENCES\.|README\.md|REPRODUCE\.md)', r'](../\1', out)
    # gfm pads pipe tables to column width; compact them (whitespace only, pandoc re-pads identically)
    def compact(line):
        if not line.startswith('|'): return line
        if re.fullmatch(r'\|[-:| ]+\|', line): return re.sub(r'-{3,}', '---', re.sub(r' ', '', line)).replace(':---:', ':---:')
        return re.sub(r' {2,}\|', ' |', line)
    out = '\n'.join(compact(l) for l in out.split('\n'))
    return out.rstrip('\n') + '\n'

def repair_quotes(source: str, reader: str, rebuilt: str):
    """Where the reader text has straight quotes that pandoc would curl, escape them in the
    source so they survive. Only touches lines whose sole difference is straight vs curly quotes.
    Returns (new_source, list_of_line_numbers)."""
    rl, bl = reader.split('\n'), rebuilt.split('\n')
    if len(rl) != len(bl): return source, []
    fixed = []
    sl = source.split('\n')
    # map reader paragraph lines to source lines by order of non-empty lines is unsafe; match by normalised text
    norm = lambda s: re.sub(r'\\(.)', r'\1', s)
    for n, (a, b) in enumerate(zip(rl, bl), 1):
        if a != b and b.replace('’', "'").replace('‘', "'").replace('“', '"').replace('”', '"') == a:
            hits = [j for j, s in enumerate(sl) if s.startswith(a[:60]) or norm(s).startswith(norm(a)[:60])]
            assert len(hits) == 1, ('ambiguous source line', n, len(hits))
            j = hits[0]
            sl[j] = re.sub(r"(?<!\\)'", r"\\'", sl[j]); sl[j] = re.sub(r'(?<!\\)"', r'\\"', sl[j])
            fixed.append(n)
    return '\n'.join(sl), fixed

if __name__ == '__main__':
    Path(sys.argv[2]).write_text(reverse(Path(sys.argv[1]).read_text()))
