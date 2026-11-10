"""Show that JOURNAL_BUILD.py's text and numbering checks fail when the journal copy differs from the source.
Needs Pandoc only."""
import importlib.util, copy, json
from pathlib import Path
spec = importlib.util.spec_from_file_location('jb', Path(__file__).resolve().parents[1] / 'JOURNAL_BUILD.py')
jb = importlib.util.module_from_spec(spec); spec.loader.exec_module(jb)

src = jb.pandoc_json(jb.source_text())
real = jb.pandoc_json


def with_change(change):
    def fake(text, mode=None):
        doc = real(text, mode)
        if mode: change(doc)
        return doc
    jb.pandoc_json = fake
    try:
        return jb.text_check(src, 'preprint')
    finally:
        jb.pandoc_json = real


def first(doc, t, pred=lambda b: True):
    return next(b for b in doc['blocks'] if b['t'] == t and pred(b))


# Unchanged: passes.
_, _, diff, problems, *_ = jb.text_check(src, 'preprint')
assert not diff and not problems, 'unchanged copy should pass'

# One word changed in a paragraph: the text check fails.
def word(doc):
    p = first(doc, 'Para', lambda b: any(x['t'] == 'Str' and x['c'] == 'chargeback' for x in b['c']))
    next(x for x in p['c'] if x['t'] == 'Str' and x['c'] == 'chargeback')['c'] = 'chargebacks'
_, _, diff, _, *_ = with_change(word)
assert any('chargebacks' in l for l in diff), 'a changed word must fail the text check'

# A paragraph dropped: the text check fails.
def drop(doc):
    i = next(i for i, b in enumerate(doc['blocks']) if b['t'] == 'Para' and i > 10)
    doc['blocks'].pop(i)
_, _, diff, _, *_ = with_change(drop)
assert diff, 'a dropped paragraph must fail the text check'

# A citation key changed: the text check fails.
def cite(doc):
    for b in doc['blocks']:
        for x in b['c'] if b['t'] == 'Para' else []:
            if x['t'] == 'Cite':
                x['c'][0][0]['citationId'] = 'Changed2026'; return
_, _, diff, _, *_ = with_change(cite)
assert any('Changed2026' in l for l in diff), 'a changed citation key must fail the text check'

# A heading whose printed number would differ from the typed one: the numbering check fails.
def number(doc):
    h = [b for b in doc['blocks'] if b['t'] == 'Header' and 'unnumbered' not in b['c'][1][1]]
    h[1]["c"][1][1].append('unnumbered')  # the template would then renumber every later heading
    h[1]["c"][1][2] = [kv for kv in h[1]['c'][1][2] if kv[0] != 'typed-number']
_, _, diff, problems, *_ = with_change(number)
assert problems, 'a numbering shift must fail the numbering check'

# Removal entries: one that matches twice is refused.
units = jb.source_units(src)
orig = (jb.B / 'SOURCE' / 'anonymize.txt').read_text(encoding='utf-8')
try:
    (jb.B / 'SOURCE' / 'anonymize.txt').write_text('block: The\n', encoding='utf-8')
    try:
        jb.apply_removals(units); raise SystemExit('an ambiguous removal must be refused')
    except AssertionError:
        pass
finally:
    (jb.B / 'SOURCE' / 'anonymize.txt').write_text(orig, encoding='utf-8')
print('OK')
