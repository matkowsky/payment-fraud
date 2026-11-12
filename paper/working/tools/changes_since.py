"""Write a readable record of what changed in the working draft since version 1.0.

Usage, from the package root: python3 tools/changes_since.py
It compares SOURCE/manuscript.md and SOURCE/supplement.md with the published
version 1.0 sources in ../v1.0/SOURCE/ and writes CHANGES_SINCE_v1.0.md.
Each change names the pull requests that made it, traced through main's merge
history; the trace needs the full git history and is omitted without it.
Citations show the numbers used in the current documents.
"""
from pathlib import Path
import difflib
import json
import re
import subprocess
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
import move_check as mc  # noqa: E402

PACKAGE = Path(__file__).resolve().parents[1]
BASELINE = PACKAGE.parent / 'v1.0'
OUTPUT = 'CHANGES_SINCE_v1.0.md'
REPO_URL = 'https://github.com/matkowsky/payment-fraud'
BASELINE_URL = REPO_URL + '/tree/main/paper/v1.0'
DOCUMENTS = (('Manuscript', 'SOURCE/manuscript.md', 'MANUSCRIPT'),
             ('Supplement', 'SOURCE/supplement.md', 'SUPPLEMENT'))
SPECIAL = re.compile(r'([\\`*_\[\]()<>#|$~])')
PR_SUBJECT = re.compile(r'^Merge pull request #(\d+)|\(#(\d+)\)$')
STATUS_AUTHOR = 'github-actions[bot]'
CITATION = re.compile(r'\[(-?@[^\[\]]+)\]')
REFERENCE = re.compile(r'<div id="ref-([^"]+)" class="csl-entry">\s*\\\[(\d+)\\\]')


def escape(text):
    """Show Markdown source literally so a redline cannot alter the page or form a link."""
    return SPECIAL.sub(r'\\\1', text).replace('\n', '<br>')


def paragraphs(text):
    return [p.strip() for p in re.split(r'\n[ \t]*\n', text) if p.strip()]


def redline(old, new):
    a, b = re.findall(r'\S+|\s+', old), re.findall(r'\S+|\s+', new)
    out = []
    for op, i1, i2, j1, j2 in difflib.SequenceMatcher(None, a, b, autojunk=False).get_opcodes():
        if op == 'equal':
            out.append(escape(''.join(a[i1:i2])))
            continue
        if i2 > i1:
            out.append('<del>' + escape(''.join(a[i1:i2])) + '</del>')
        if j2 > j1:
            out.append('<ins>' + escape(''.join(b[j1:j2])) + '</ins>')
    return ''.join(out)


def headings(paras):
    """The nearest heading at or before each paragraph."""
    current, result = 'Opening', []
    for p in paras:
        if p.startswith('#'):
            current = p.lstrip('#').strip()
        result.append(current)
    return result


def align(old, new):
    """Pair old and new paragraphs: (i, j, edited), with None for an added or removed paragraph."""
    pairs = []
    for op, i1, i2, j1, j2 in difflib.SequenceMatcher(None, old, new, autojunk=False).get_opcodes():
        if op == 'equal':
            pairs += [(i1 + k, j1 + k, False) for k in range(i2 - i1)]
            continue
        i, j = i1, j1
        while i < i2 or j < j2:
            if i < i2 and j < j2 and difflib.SequenceMatcher(None, old[i], new[j], autojunk=False).ratio() >= 0.4:
                pairs.append((i, j, True))
                i, j = i + 1, j + 1
            elif i < i2 and (j >= j2 or i2 - i > j2 - j):
                pairs.append((i, None, True))
                i += 1
            else:
                pairs.append((None, j, True))
                j += 1
    return pairs


def compare_indexed(old_text, new_text):
    """Return (heading, kind, redline, old index, new index) for each changed, added or removed paragraph."""
    old, new = paragraphs(old_text), paragraphs(new_text)
    old_head, new_head = headings(old), headings(new)
    changes = []
    for i, j, edited in align(old, new):
        if not edited:
            continue
        if i is not None and j is not None:
            changes.append((new_head[j], 'changed', redline(old[i], new[j]), i, j))
        elif j is None:
            changes.append((old_head[i], 'removed', '<del>' + escape(old[i]) + '</del>', i, None))
        else:
            changes.append((new_head[j], 'added', '<ins>' + escape(new[j]) + '</ins>', None, j))
    return changes


def compare(old_text, new_text):
    """Return (heading, kind, redline) for each changed, added or removed paragraph."""
    return [c[:3] for c in compare_indexed(old_text, new_text)]


def citation_numbers(document):
    """Map citation keys to the numbers in a built Markdown document, if it exists."""
    if not document.exists():
        return {}
    return {key: int(n) for key, n in REFERENCE.findall(document.read_text(encoding='utf-8'))}


def number_citations(text, numbers):
    """Replace [@Key; @Other] with [3, 7] where every key has a number; leave other citations as written."""
    def swap(match):
        keys = [part.strip().lstrip('-').lstrip('@').split(',')[0].strip() for part in match.group(1).split(';')]
        if not all(k in numbers for k in keys):
            return match.group(0)
        return '[' + ', '.join(str(n) for n in sorted({numbers[k] for k in keys})) + ']'
    return CITATION.sub(swap, text)


def numbered(paras, pattern, form, start):
    """The nearest numbered section at or before each paragraph, as form(number); subsection headings are skipped."""
    current, result = start, []
    for p in paras:
        m = re.match(r'#+\s*(' + pattern + r')[.\s]', p) if p.startswith('#') else None
        if m:
            current = form(m.group(1))
        result.append(current)
    return result


def moves(ms_old, ms_new, sup_old, sup_new, maps=()):
    """Sentences that left the manuscript and arrived in the supplement, matched as the move check matches them.

    Returns (out, into): out maps each moved manuscript sentence to its supplement section; into maps each
    arrived supplement sentence to the manuscript heading it came from.
    """
    sq = mc.squash
    ms_now = {sq(u) for u in mc.units(ms_new)}
    sup_before = {sq(u) for u in mc.units(sup_old)}
    arrived = {}
    paras = paragraphs(sup_new)
    for p, h in zip(paras, numbered(paras, r'S\d+(?:\.\d+)*', lambda n: n, 'opening')):
        for u in mc.units(p):
            arrived.setdefault(sq(u), h)
    out, into = {}, {}
    paras = paragraphs(ms_old)
    for p, h in zip(paras, numbered(paras, r'\d+(?:\.\d+)*', lambda n: 'Section ' + n, 'opening')):
        for u in mc.units(p):
            if sq(u) in ms_now:
                continue
            forms = [u] + [mc.renumber(u, m) for m in maps]
            for v in (sq(x) for f in forms for x in (f, mc.as_supplement(f))):
                if v in arrived and v not in sup_before:
                    out[sq(u)] = arrived[v]
                    into[v] = h
                    break
    return out, into


def renumber_maps(package):
    return [json.loads(f.read_text(encoding='utf-8')) for f in sorted((package / 'tools' / 'covered').glob('renumber-*.json'))]


def git(args, cwd):
    try:
        result = subprocess.run(['git', *args], cwd=cwd, capture_output=True, text=True)
    except OSError:
        return None
    return result.stdout if result.returncode == 0 else None


def history(package, baseline, source):
    """Trace each paragraph through main's first-parent history and label the commits that edited it.

    Returns (final paragraphs, labels per final paragraph, labels per removed version 1.0 paragraph,
    final paragraph index for each surviving version 1.0 paragraph), or None without full history.
    """
    root = git(['rev-parse', '--show-toplevel'], package)
    if root is None or (git(['rev-parse', '--is-shallow-repository'], package) or '').strip() != 'false':
        return None
    root = Path(root.strip())
    path = (package / source).resolve().relative_to(root).as_posix()
    log = git(['log', '--first-parent', '--reverse', '--format=%H%x09%an%x09%s', 'HEAD', '--', path], root)
    if log is None:
        return None
    current = paragraphs((baseline / source).read_text(encoding='utf-8'))
    labels = [[] for _ in current]
    origin = list(range(len(current)))
    removed = {}
    steps = []
    for line in log.splitlines():
        sha, author, subject = line.split('\t', 2)
        match = PR_SUBJECT.search(subject)
        tag = '#' + (match.group(1) or match.group(2)) if match else ('status' if author == STATUS_AUTHOR else sha[:7])
        text = git(['show', sha + ':' + path], root)
        if text is not None:
            steps.append((tag, text))
    head = git(['show', 'HEAD:' + path], root)
    working = (package / source).read_text(encoding='utf-8')
    if head is not None and working != head:
        steps.append(('uncommitted', working))
    for tag, text in steps:
        new = paragraphs(text)
        new_labels, new_origin = [[] for _ in new], [None] * len(new)
        for i, j, edited in align(current, new):
            if j is None:
                if origin[i] is not None:
                    removed[origin[i]] = labels[i] + [tag]
                continue
            if i is None:
                new_labels[j] = [tag]
                continue
            new_labels[j] = labels[i] + ([tag] if edited and tag not in labels[i] else [])
            new_origin[j] = origin[i]
        current, labels, origin = new, new_labels, new_origin
    survivors = {o: j for j, o in enumerate(origin) if o is not None}
    return current, labels, removed, survivors


def describe(tags):
    names = []
    for tag in dict.fromkeys(tags):
        if tag.startswith('#'):
            names.append('[' + tag + '](' + REPO_URL + '/pull/' + tag[1:] + ')')
        elif tag == 'status':
            names.append('the automatic status update')
        elif tag == 'uncommitted':
            names.append('uncommitted edits')
        else:
            names.append('commit `' + tag + '`')
    return ', '.join(names)


def accepted(package):
    path = package / 'REVISION_STATUS.json'
    if not path.exists():
        return []
    return json.loads(path.read_text(encoding='utf-8')).get('accepted', [])


def render(package=PACKAGE, baseline=BASELINE):
    lines = ['# What changed since version 1.0', '',
             'This page is generated by `tools/changes_since.py` from the sources. It compares this working draft '
             'with the published [version 1.0](' + BASELINE_URL + '). <del>Struck text</del> was removed and <ins>underlined text</ins> '
             'was added. Each change names the pull requests that made it. Citations show the numbers used in the current '
             'documents; Markdown formatting appears as written in the sources. Text moved between the manuscript and the supplement '
             'is labeled with where it went or where it came from. The page is rebuilt automatically after each merge.', '']
    merges = accepted(package)
    if merges:
        lines += ['Accepted pull requests:', '']
        lines += ['- [#' + str(m['pr']) + '](' + REPO_URL + '/pull/' + str(m['pr']) + ') ' + escape(m['title']) for m in merges]
        lines.append('')
    lines += ['| Document | Read the current version | Paragraphs changed | Added | Removed | Moved between documents |',
              '|---|---|---|---|---|---|']
    texts = {source: ((baseline / source).read_text(encoding='utf-8'), (package / source).read_text(encoding='utf-8'))
             for _, source, _ in DOCUMENTS}
    (ms_old, ms_new), (sup_old, sup_new) = texts['SOURCE/manuscript.md'], texts['SOURCE/supplement.md']
    out, into = moves(ms_old, ms_new, sup_old, sup_new, renumber_maps(package))
    sections = []
    for title, source, stem in DOCUMENTS:
        old_text, new_text = texts[source]
        trace = history(package, baseline, source)
        if trace is not None and trace[0] != paragraphs(new_text):
            trace = None
        numbers = citation_numbers(package / (stem + '.md'))
        old_shown = '\n\n'.join(number_citations(p, numbers) for p in paragraphs(old_text))
        new_shown = '\n\n'.join(number_citations(p, numbers) for p in paragraphs(new_text))
        changes = compare_indexed(old_shown, new_shown)
        old_raw, new_raw = paragraphs(old_text), paragraphs(new_text)
        if source == 'SOURCE/manuscript.md':
            place = numbered(old_raw, r'\d+(?:\.\d+)*', lambda n: 'Section ' + n, 'the opening')
        else:
            place = numbered(new_raw, r'S\d+(?:\.\d+)*', lambda n: n, 'the opening')
        sq = mc.squash
        moved_map = out if source == 'SOURCE/manuscript.md' else into

        def moved_units(raw):
            units = mc.units(raw)
            return units, [u for u in units if sq(u) in moved_map]

        def where(found):
            dests = sorted({moved_map[sq(u)] for u in found})
            if source == 'SOURCE/manuscript.md':
                return 'Supplement ' + ', '.join(dests)
            return 'manuscript ' + ', '.join(dests)

        entries, counts = [], {'changed': 0, 'added': 0, 'removed': 0, 'moved': 0}
        for heading, kind, text, i, j in changes:
            raw = old_raw[i] if kind == 'removed' else new_raw[j] if kind == 'added' else None
            note, label = '', kind.capitalize() + ', under "' + escape(heading) + '"'
            if raw is not None:
                units, found = moved_units(raw)
                if found and len(found) == len(units):
                    counts['moved'] += 1
                    label = ('Moved to ' + where(found) + ', from ' + place[i] if kind == 'removed'
                             else 'Moved from ' + where(found) + ', to ' + place[j])
                else:
                    counts[kind] += 1
                    if found:
                        note = (' (' + str(len(found)) + ' of ' + str(len(units)) + ' sentences '
                                + ('now in ' if kind == 'removed' else 'moved from ') + where(found) + ')')
            else:
                counts['changed'] += 1
                before, after = mc.units(old_raw[i]), mc.units(new_raw[j])
                gone = [u for u in (before if source == 'SOURCE/manuscript.md' else after)
                        if sq(u) not in {sq(x) for x in (after if source == 'SOURCE/manuscript.md' else before)}]
                found = [u for u in gone if sq(u) in moved_map]
                if found:
                    note = ('; ' + str(len(found)) + (' removed sentence' if source == 'SOURCE/manuscript.md' else ' added sentence')
                            + ('s' if len(found) > 1 else '') + (' now in ' if source == 'SOURCE/manuscript.md' else ' moved from ')
                            + where(found))
            entries.append((label, note, text, i, j))
        lines.append('| ' + title + ' | [Markdown](' + stem + '.md), [PDF](' + stem + '.pdf) | '
                     + ' | '.join(str(counts[k]) for k in ('changed', 'added', 'removed', 'moved')) + ' |')
        sections += ['', '## ' + title, '']
        if not changes:
            sections.append('No changes.')
        for label, note, text, i, j in entries:
            by = ''
            if trace is not None:
                _, labels, removed, survivors = trace
                if j is not None:
                    tags = labels[j]
                else:
                    tags = removed.get(i) or (labels[survivors[i]] if i in survivors else [])
                if 'status' in tags:
                    tags = ['status']  # the status line is rewritten whole by each automatic update
                if tags:
                    by = ', by ' + describe(tags)
            sections += ['**' + label + by + note + ':**', '', text, '']
    return '\n'.join(lines + sections).rstrip() + '\n'


def write(package=PACKAGE, baseline=BASELINE):
    (package / OUTPUT).write_text(render(package, baseline), encoding='utf-8')


if __name__ == '__main__':
    write()
    print('Wrote ' + OUTPUT)
