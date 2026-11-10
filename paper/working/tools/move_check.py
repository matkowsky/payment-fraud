"""Check that text removed from the manuscript was moved to the supplement, not lost.

  python3 tools/move_check.py [BASE]     BASE is a git ref; default origin/main

Compares SOURCE/manuscript.md and SOURCE/supplement.md with BASE, sentence by sentence
(table rows and list items count as one unit each), and fails unless:
  1. every sentence removed from the manuscript appears word for word in the supplement, or is
     reported as edited: one added manuscript sentence that keeps most of its words;
  2. an edited sentence keeps every citation key and every number of the sentence it replaces;
  3. the two documents together cite the same works as before.
In the supplement a moved sentence may say "manuscript Section N" (or Table N, Figure N) for "Section N",
and "S4" where the manuscript said "Supplement S4". Nothing else may differ.
Prints a Markdown report: moved sentences, edited sentences (before and after) and added sentences.
"""
import re, subprocess, sys, difflib
from pathlib import Path

B = Path(__file__).resolve().parents[1]
SPLIT = re.compile(r'(?<=[.?!])\s+(?=[A-Z*\[`$“"(])')


def units(text):
    out = []
    for line in text.split('\n'):
        line = line.strip()
        if not line: continue
        if line.startswith(('|', '#', '$$', '![', ':::')) or re.match(r'^[-*] ', line):
            out.append(line)
        else:
            out += [s.strip() for s in SPLIT.split(line) if s.strip()]
    return out


def as_supplement(s):
    s = re.sub(r'(?<!manuscript )\b((?:Sections?|Tables?|Figures?) \d)', r'manuscript \1', s)
    return re.sub(r'\bSupplement (S\d)', r'\1', s)


def squash(s):
    return re.sub(r'\s+', ' ', s)


def keys(s): return set(re.findall(r'@([A-Za-z][A-Za-z0-9]+)', s))
def numbers(s): return re.findall(r'\d[\d.,]*\d|\d', s)
def words(s): return re.findall(r"[A-Za-z0-9']+", s.lower())


def compare(old_ms, new_ms, old_sup, new_sup):
    old_u, new_u = units(old_ms), units(new_ms)
    sm = difflib.SequenceMatcher(None, old_u, new_u, autojunk=False)
    removed, added = [], []
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag in ('replace', 'delete'): removed += old_u[i1:i2]
        if tag in ('replace', 'insert'): added += new_u[j1:j2]
    sup = squash(new_sup)
    moved, edited, lost = [], [], []
    free = list(added)
    for s in removed:
        if squash(s) in sup or squash(as_supplement(s)) in sup:
            moved.append(s); continue
        best = max(free, key=lambda a: difflib.SequenceMatcher(None, words(s), words(a)).ratio(), default=None)
        if best is not None and difflib.SequenceMatcher(None, words(s), words(best)).ratio() >= 0.6:
            edited.append((s, best)); free.remove(best)
        else:
            lost.append(s)
    problems = [f'removed and not in the supplement: {s}' for s in lost]
    both = new_ms + '\n' + new_sup
    # An edited sentence must keep every citation key and every number of the sentence it replaces.
    from collections import Counter
    for a, b in edited:
        for k in sorted(keys(a) - keys(b)): problems.append(f'citation @{k} dropped by an edit: {a[:80]}')
        for n in sorted((Counter(numbers(a)) - Counter(numbers(b))).elements()):
            problems.append(f'number {n} dropped by an edit: {a[:80]}')
    before, after = keys(old_ms + old_sup), keys(both)
    if before != after:
        problems.append(f'cited works changed: removed {sorted(before - after)}, added {sorted(after - before)}')
    return moved, edited, free, problems


def report(moved, edited, added, problems, wc):
    out = [f'Manuscript words: {wc[0]:,} to {wc[1]:,}. Supplement words: {wc[2]:,} to {wc[3]:,}.', '',
           f'**Moved to the supplement word for word ({len(moved)}):**']
    out += [f'- {s}' for s in moved]
    out += ['', f'**Edited in the manuscript ({len(edited)}):**']
    for a, b in edited: out += [f'- Before: {a}', f'  After: {b}']
    out += ['', f'**Added to the manuscript ({len(added)}):**'] + [f'- {s}' for s in added]
    out += ['', '**Check: ' + ('pass' if not problems else 'FAIL') + '**'] + [f'- {p}' for p in problems]
    return '\n'.join(out)


def main():
    base = sys.argv[1] if len(sys.argv) > 1 else 'origin/main'
    def show(name):
        return subprocess.run(['git', 'show', f'{base}:paper/working/SOURCE/{name}'], cwd=B, text=True,
                              stdout=subprocess.PIPE, check=True).stdout
    old_ms, old_sup = show('manuscript.md'), show('supplement.md')
    new_ms = (B / 'SOURCE' / 'manuscript.md').read_text(encoding='utf-8')
    new_sup = (B / 'SOURCE' / 'supplement.md').read_text(encoding='utf-8')
    moved, edited, added, problems = compare(old_ms, new_ms, old_sup, new_sup)
    print(report(moved, edited, added, problems, [len(x.split()) for x in (old_ms, new_ms, old_sup, new_sup)]))
    if problems: sys.exit(1)


if __name__ == '__main__':
    main()
