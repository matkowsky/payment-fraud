"""Check that text removed from the manuscript was moved to the supplement, not lost.

  python3 tools/move_check.py [BASE] [--covered FILE] [--renumber FILE]     BASE is a git ref; default origin/main

Compares SOURCE/manuscript.md and SOURCE/supplement.md with BASE, sentence by sentence
(table rows and list items count as one unit each), and fails unless:
  1. every sentence removed from the manuscript appears word for word in the supplement, or is
     reported as edited: one added manuscript sentence that keeps most of its words or only adds words;
  2. an edited sentence keeps every citation key and every number of the sentence it replaces;
  3. the two documents together cite the same works as before.
In the supplement a moved sentence may say "manuscript Section N" (or Table N, Figure N) for "Section N",
and "S4" where the manuscript said "Supplement S4". Nothing else may differ.
--covered FILE names a JSON list of {"removed": sentence, "covered_by": [supplement sentences]} for
sentences removed because the supplement already states them in its own words. Each "removed" must be a
sentence this change removes, each "covered_by" must be in the supplement word for word, and together they
must contain every number of the removed sentence (labels such as E3 and section references aside). The
check confirms the quotations exist; a reviewer confirms they say the same thing.
--renumber FILE names a JSON map of old table and figure labels to new ones, used when a table or
figure moves to the supplement and the rest are renumbered. The map is applied to the old manuscript
first, so only real changes are reported.
Prints a Markdown report: moved sentences, edited sentences (before and after) and added sentences.
"""
import re, subprocess, sys, difflib, json
from collections import Counter
from pathlib import Path

B = Path(__file__).resolve().parents[1]
# Sentence ends, and the end of a bold lead-in such as "**Label.** Text".
SPLIT = re.compile(r'(?<=[.?!])\s+(?=[A-Z*\[`$“"(])|(?<=[.?!:]\*\*)\s+(?=\S)')


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
    return re.sub(r'\bSupplement ((?:(?:Table|Figure) )?S\d)', r'\1', s)


def renumber(text, mapping):
    # Replace every old label at once, so "Table 4" -> "Table 1" and "Table 1" -> "Table S1.1" cannot chain.
    if not mapping: return text
    rx = re.compile('|'.join(r'\b' + re.escape(k) + r'(?!\d)' for k in sorted(mapping, key=len, reverse=True)))
    return rx.sub(lambda m: mapping[m.group(0)], text)


def squash(s):
    return re.sub(r'\s+', ' ', s)


def keys(s): return set(re.findall(r'@([A-Za-z][A-Za-z0-9]+)', s))
def numbers(s): return re.findall(r'\d[\d.,]*\d|\d', s)
def plain_numbers(s):
    # Numbers other than labels (E3, S7.1, C1, RQ2) and section references.
    return numbers(re.sub(r'\b(?:E|S|C|RQ)\d+(?:\.\d+)?\b|\b(?:manuscript )?Sections? \d+(?:\.\d+)?', '', s))
def words(s): return re.findall(r"[A-Za-z0-9']+", s.lower())


def extends(a, b):
    # True when b keeps every word of a, in order, and only adds words.
    it = iter(words(b))
    return all(w in it for w in words(a))


def compare(old_ms, new_ms, old_sup, new_sup, covered=()):
    old_u, new_u = units(old_ms), units(new_ms)
    sm = difflib.SequenceMatcher(None, old_u, new_u, autojunk=False)
    removed, added = [], []
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag in ('replace', 'delete'): removed += old_u[i1:i2]
        if tag in ('replace', 'insert'): added += new_u[j1:j2]
    sup = squash(new_sup)
    moved, edited, lost, cov, problems = [], [], [], [], []
    free = list(added)
    declared = {squash(c['removed']): c['covered_by'] for c in covered}
    for d in set(declared) - {squash(s) for s in removed}:
        problems.append(f'declared as covered but not removed by this change: {d[:80]}')
    for s in removed:
        if squash(s) in declared:
            quotes = declared[squash(s)]
            for q in quotes:
                if squash(q) not in sup: problems.append(f'covering text is not in the supplement: {q[:80]}')
            missing = Counter(plain_numbers(s)) - Counter(plain_numbers(' '.join(quotes)))
            for n in sorted(set(missing)): problems.append(f'number {n} is not in the covering text: {s[:80]}')
            cov.append((s, quotes)); continue
        if squash(s) in sup or squash(as_supplement(s)) in sup:
            moved.append(s); continue
        best = max(free, key=lambda a: (extends(s, a), difflib.SequenceMatcher(None, words(s), words(a)).ratio()), default=None)
        if best is not None and (extends(s, best) or difflib.SequenceMatcher(None, words(s), words(best)).ratio() >= 0.6):
            edited.append((s, best)); free.remove(best)
        else:
            lost.append(s)
    problems += [f'removed and not in the supplement: {s}' for s in lost]
    both = new_ms + '\n' + new_sup
    # An edited sentence must keep every citation key and every number of the sentence it replaces.
    for a, b in edited:
        for k in sorted(keys(a) - keys(b)): problems.append(f'citation @{k} dropped by an edit: {a[:80]}')
        for n in sorted((Counter(numbers(a)) - Counter(numbers(b))).elements()):
            problems.append(f'number {n} dropped by an edit: {a[:80]}')
    before, after = keys(old_ms + old_sup), keys(both)
    if before != after:
        problems.append(f'cited works changed: removed {sorted(before - after)}, added {sorted(after - before)}')
    return moved, edited, free, problems, cov


def report(moved, edited, added, problems, wc, cov=()):
    out = [f'Manuscript words: {wc[0]:,} to {wc[1]:,}. Supplement words: {wc[2]:,} to {wc[3]:,}.', '',
           f'**Moved to the supplement word for word ({len(moved)}):**']
    out += [f'- {s}' for s in moved]
    out += ['', f'**Removed because the supplement already states it ({len(cov)}):**']
    for s, quotes in cov: out += [f'- Removed: {s}'] + [f'  Supplement: {q}' for q in quotes]
    out += ['', f'**Edited in the manuscript ({len(edited)}):**']
    for a, b in edited: out += [f'- Before: {a}', f'  After: {b}']
    out += ['', f'**Added to the manuscript ({len(added)}):**'] + [f'- {s}' for s in added]
    out += ['', '**Check: ' + ('pass' if not problems else 'FAIL') + '**'] + [f'- {p}' for p in problems]
    return '\n'.join(out)


def main():
    args = sys.argv[1:]
    covered = []
    mapping = {}
    if '--renumber' in args:
        i = args.index('--renumber'); mapping = json.loads(Path(args[i + 1]).read_text(encoding='utf-8')); del args[i:i + 2]
    if '--covered' in args:
        i = args.index('--covered'); covered = json.loads(Path(args[i + 1]).read_text(encoding='utf-8')); del args[i:i + 2]
    base = args[0] if args else 'origin/main'
    def show(name):
        return subprocess.run(['git', 'show', f'{base}:paper/working/SOURCE/{name}'], cwd=B, text=True,
                              stdout=subprocess.PIPE, check=True).stdout
    old_ms, old_sup = renumber(show('manuscript.md'), mapping), show('supplement.md')
    if mapping:
        print('**Renumbered before comparing:** ' + '; '.join(f'{k} is now {v}' for k, v in mapping.items()) + '.\n')
    new_ms = (B / 'SOURCE' / 'manuscript.md').read_text(encoding='utf-8')
    new_sup = (B / 'SOURCE' / 'supplement.md').read_text(encoding='utf-8')
    moved, edited, added, problems, cov = compare(old_ms, new_ms, old_sup, new_sup, covered)
    print(report(moved, edited, added, problems, [len(x.split()) for x in (old_ms, new_ms, old_sup, new_sup)], cov))
    if problems: sys.exit(1)


if __name__ == '__main__':
    main()
