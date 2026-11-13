"""Build the manuscript in ACM's journal format and check it against the source.

Same source as BUILD.py (SOURCE/manuscript.md); only the layout differs.
  python3 JOURNAL_BUILD.py               build both copies, run every check, write JOURNAL/
  python3 JOURNAL_BUILD.py --check-only  text checks only (needs Pandoc, not LaTeX)

Copies, both in ACM's large format (acmlarge), which DTRAP uses:
  preprint   [acmlarge,nonacm]            author, acknowledgments and links kept; no ACM copyright block
  anonymous  [acmlarge,review,anonymous]  SOURCE/anonymize.txt removals applied; author hidden; line numbers

The supplement gets an anonymous copy too, in its own layout (the same Pandoc and XeLaTeX settings as
BUILD.py): JOURNAL/SUPPLEMENT_ANONYMOUS.pdf is the supplement without its byline and status line.

Checks (any failure stops the build):
  1. Text: every heading, paragraph, list item, caption, table cell, image and citation key in each copy
     equals the source, in order, except the removals listed in SOURCE/anonymize.txt.
  2. Numbering: the section, subsection, table and figure numbers the template prints equal the numbers
     typed in the source, so cross-references such as "Section 6.3" and "Table 4" stay correct.
  3. PDF: each paragraph, heading, list item and caption appears in the PDF text, so typesetting dropped
     nothing; every citation resolves.
  4. Anonymous copy: the author's surname and the preprint's DOI appear nowhere in its PDF text or properties.
  5. Anonymous supplement: its TeX equals the supplement's except for the byline, the status line and the
     author property; the surname and the DOI appear nowhere in its source, PDF text or properties.
References: the same data and style as BUILD.py (REFERENCES.json, SOURCE/references.csl).
Requires Pandoc, XeLaTeX, pdftotext and TeX Live's acmart, libertine, inconsolata and newtx.
"""
from pathlib import Path
import subprocess, json, re, os, sys, shutil, difflib, unicodedata

B = Path(__file__).resolve().parent
W = B / 'build' / 'journal'
OUT = B / 'JOURNAL'
FORBIDDEN = ['matkowsky', '1052815zenodo23772005']  # normalized: lowercase letters and digits only


def run(args, cwd=B, env=None):
    r = subprocess.run(args, cwd=cwd, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, env=env)
    if r.returncode:
        raise RuntimeError(' '.join(map(str, args)) + '\n' + r.stdout[-6000:])
    return r.stdout


def source_text():
    # As in BUILD.py: figure paths relative to the working folder, and the reference list at the end.
    src = re.sub(r'\]\(\.\./', '](', (B / 'SOURCE' / 'manuscript.md').read_text(encoding='utf-8'))
    return src + '\n\n## References\n\n::: {#refs}\n:::\n'


def pandoc_json(text, mode=None):
    W.mkdir(parents=True, exist_ok=True)
    tmp = W / 'input.md'; tmp.write_text(text, encoding='utf-8')
    args = ['pandoc', str(tmp), '-f', 'markdown-implicit_figures', '-t', 'json']
    if mode:
        args += ['--lua-filter=SOURCE/acm.lua', '-M', 'acm-mode=' + mode, '-M', 'anonymize=SOURCE/anonymize.txt']
    return json.loads(run(args))


# ---------- Flattening: the document as an ordered list of text units ----------

def inl(xs):
    out = []
    for x in xs:
        t, c = x['t'], x.get('c')
        if t == 'Str': out.append(c)
        elif t in ('Space', 'SoftBreak', 'LineBreak'): out.append(' ')
        elif t in ('Emph', 'Strong', 'Underline', 'Strikeout', 'Superscript', 'Subscript', 'SmallCaps'): out.append(inl(c))
        elif t == 'Span': out.append(inl(c[1]))
        elif t == 'Quoted': q = '"' if c[0]['t'] == 'DoubleQuote' else "'"; out.append(q + inl(c[1]) + q)
        elif t == 'Cite': out.append('[' + '; '.join('@' + k['citationId'] for k in c[0]) + ']')
        elif t == 'Code': out.append('`' + c[1] + '`')
        elif t == 'Math': out.append('$' + c[1] + '$')
        elif t == 'Link': out.append(inl(c[1]) + '<' + c[2][0] + '>')
        elif t == 'Image': out.append('{image ' + inl(c[1]) + ' ' + re.sub(r'\.(svg|pdf)$', '', c[2][0]) + '}')
        elif t == 'RawInline': out.append(c[1])
        elif t == 'Note': out.append('(' + ' '.join(u for _, u in blocks(c)) + ')')
        else: raise ValueError('unhandled inline ' + t)
    return ''.join(out)


def attr_get(attr, key):
    return dict(attr[2]).get(key)


def blocks(bs, numbers=None):
    """Yield (kind, text). For the journal copy, `numbers` collects the typed numbers to re-add."""
    for b in bs:
        t, c = b['t'], b.get('c')
        if t in ('Para', 'Plain'): yield 'para', inl(c)
        elif t == 'Header':
            num = attr_get(c[1], 'typed-number')
            text = inl(c[2])
            if num: text = num + ('. ' if '.' not in num else ' ') + text
            yield 'heading', text
        elif t in ('BulletList', 'OrderedList'):
            items = c if t == 'BulletList' else c[1]
            for item in items:
                for k, u in blocks(item): yield 'item', u
        elif t == 'Table':
            attr, caption = c[0], c[1]
            cap = ' '.join(u for _, u in blocks(caption[1]))
            if cap:
                yield 'caption', 'Table ' + attr_get(attr, 'typed-number') + '. ' + cap
            head, bodies = c[3], c[4]
            rows = list(head[1])
            for body in bodies: rows += body[2] + body[3]
            for row in rows:
                for cell in row[1]:
                    yield 'cell', ' '.join(u for _, u in blocks(cell[4]))
        elif t == 'Figure':
            attr, caption, content = c
            yield 'caption', 'Figure ' + attr_get(attr, 'typed-number') + '. ' + ' '.join(u for _, u in blocks(caption[1]))
            for k, u in blocks([x for x in content if x['t'] != 'RawBlock']): yield 'image', u
        elif t == 'RawBlock': continue  # layout commands only (font size, figure descriptions)
        elif t == 'Div': yield from blocks(c[1])
        elif t == 'BlockQuote': yield from blocks(c)
        elif t == 'Math': yield 'para', '$' + c + '$'
        else: raise ValueError('unhandled block ' + t)


def source_units(doc):
    units = []
    for k, u in blocks(doc['blocks']):
        # Captioned tables and figures: the source types the caption as a bold paragraph before them.
        units.append(('caption' if re.match(r'^(Table|Figure) \d+\. ', u) and k == 'para' else k, u))
    # A source image paragraph flattens as a para; the journal copy holds it as a figure image.
    return [('image', u) if k == 'para' and u.startswith('{image ') and u.endswith('}') else (k, u) for k, u in units]


def journal_units(doc):
    m = doc['meta']
    def meta_inl(key): return inl(m[key]['c'])
    def meta_str(key): return m[key]['c'] if m[key]['t'] == 'MetaString' else inl(m[key]['c'])
    body = list(blocks(doc['blocks']))
    units = [('heading', meta_inl('title')), ('para', meta_str('acm-author')),
             ('para', '%s, %s. Correspondence: %s' % (meta_str('acm-city'), meta_str('acm-state'), meta_str('acm-email')))]
    if doc['blocks'] and doc['blocks'][0]['t'] == 'Para':
        units.append(body.pop(0))  # dated status line
    units.append(('heading', 'Abstract'))
    units += list(blocks(m['abstract']['c']))
    units.append(('para', 'Keywords: ' + meta_inl('keywords')))
    return units + body


def apply_removals(units):
    """Independent of the Lua filter: apply SOURCE/anonymize.txt to the source's text units."""
    entries = [tuple(l.split(': ', 1)) for l in (B / 'SOURCE' / 'anonymize.txt').read_text(encoding='utf-8').splitlines()
               if re.match(r'^(status|block|text): ', l)]
    units = list(units)
    applied = []
    for kind, body in entries:
        if kind == 'status':
            # The status line is the fourth unit: title, author, byline, status.
            assert units[3][0] == 'para' and units[4] == ('heading', 'Abstract'), 'status line not found'
            applied.append((kind, units[3][1])); units.pop(3)
        elif kind == 'block':
            hits = [i for i, (k, u) in enumerate(units) if k == 'para' and u.startswith(body)]
            assert len(hits) == 1, f'{body!r} matched {len(hits)} paragraphs'
            applied.append((kind, units[hits[0]][1])); units.pop(hits[0])
        else:
            hits = [i for i, (k, u) in enumerate(units) if body in u]
            assert len(hits) == 1 and units[hits[0]][1].count(body) == 1, f'{body!r} must occur once'
            k, u = units[hits[0]]
            units[hits[0]] = (k, re.sub(r'  +', ' ', u.replace(body, '')).strip())
            applied.append((kind, body))
    return units, applied


def numbering_check(doc):
    """The numbers acmart will print must equal the numbers typed in the source."""
    sec = sub = tab = fig = 0
    problems, counts = [], {'sections': 0, 'subsections': 0, 'tables': 0, 'figures': 0}
    for b in doc['blocks']:
        t, c = b['t'], b.get('c')
        if t == 'Header':
            if 'unnumbered' in c[1][1]:
                assert attr_get(c[1], 'typed-number') is None
                continue
            if c[0] == 2: sec += 1; sub = 0; printed = str(sec); counts['sections'] += 1
            elif c[0] == 3: sub += 1; printed = f'{sec}.{sub}'; counts['subsections'] += 1
            else: problems.append('numbered heading below level 3: ' + inl(c[2])); continue
            if attr_get(c[1], 'typed-number') != printed:
                problems.append(f'heading {inl(c[2])!r}: typed {attr_get(c[1], "typed-number")}, printed {printed}')
        elif t == 'Table':
            tab += 1; counts['tables'] += 1
            if attr_get(c[0], 'typed-number') != str(tab): problems.append(f'table {tab}: typed {attr_get(c[0], "typed-number")}')
        elif t == 'Figure':
            fig += 1; counts['figures'] += 1
            if attr_get(c[0], 'typed-number') != str(fig): problems.append(f'figure {fig}: typed {attr_get(c[0], "typed-number")}')
    return problems, counts


def text_check(src_doc, mode):
    jdoc = pandoc_json(source_text(), mode)
    expected = source_units(src_doc)
    applied = []
    if mode == 'anonymous':
        expected, applied = apply_removals(expected)
    got = journal_units(jdoc)
    diff = list(difflib.unified_diff([f'{k}: {u}' for k, u in expected], [f'{k}: {u}' for k, u in got],
                                     'source', mode, lineterm='', n=1))
    problems, counts = numbering_check(jdoc)
    cites = sorted(set(re.findall(r'@([A-Za-z0-9]+)', ' '.join(u for _, u in got if '[@' in u))))
    return jdoc, got, diff, problems, counts, applied, cites


# ---------- Typesetting and PDF checks ----------

def norm(s):
    return re.sub(r'[^a-z0-9]', '', unicodedata.normalize('NFKC', s).lower())


def fragments(unit):
    # Split at citations, math, code, links and images, which the PDF renders differently.
    unit = re.sub(r'^Keywords: ', '', unit)  # ACM prints its own label
    parts = re.split(r'\[@[^\]]*\]|\$[^$]*\$|`[^`]*`|<[^>]*>|\{image [^}]*\}', unit)
    return [n for n in (norm(p) for p in parts) if len(n) >= 12]


def typeset(mode):
    stem = 'MANUSCRIPT_ACM' + ('_ANONYMOUS' if mode == 'anonymous' else '')
    opts = 'acmlarge,review,anonymous' if mode == 'anonymous' else 'acmlarge,nonacm'
    tex = W / (stem + '.tex')
    tmp = W / 'input.md'; tmp.write_text(source_text(), encoding='utf-8')
    # References use the same CSL style and data as the preprint build, so the list is identical.
    args = ['pandoc', str(tmp), '-f', 'markdown-implicit_figures', '-t', 'latex',
            '--lua-filter=SOURCE/acm.lua', '--citeproc', '--bibliography=REFERENCES.json',
            '--csl=SOURCE/references.csl', '-M', 'link-citations=true', '--template=SOURCE/acm-template.tex',
            '-M', 'acm-mode=' + mode, '-M', 'anonymize=SOURCE/anonymize.txt',
            '-V', 'acm-options=' + opts, '-o', str(tex)]
    if mode == 'anonymous': args += ['-V', 'acm-anonymous=true']
    citeproc = run(args)
    env = dict(os.environ, TEXINPUTS=str(B) + os.pathsep)
    xe = ['xelatex', '-interaction=nonstopmode', '-halt-on-error', '-output-directory=' + str(W), str(tex)]
    for _ in range(3): run(xe, env=env)
    log = (W / (stem + '.log')).read_text(encoding='latin-1')
    # For the PDF text check only: the same source with graphicx in draft mode, so each figure keeps its
    # box and the page layout is unchanged, but the figures' own labels do not mix into the text.
    draft = ['xelatex', '-interaction=nonstopmode', '-halt-on-error', '-output-directory=' + str(W),
             '-jobname=' + stem + '_TEXTCHECK', r'\PassOptionsToPackage{draft}{graphicx}\input{' + str(tex) + '}']
    for _ in range(2): run(draft, env=env)
    draft_pages = int(re.search(r'Pages:\s+(\d+)', run(['pdfinfo', str(W / (stem + '_TEXTCHECK.pdf'))])).group(1))
    pdf = W / (stem + '.pdf')
    pages = int(re.search(r'Pages:\s+(\d+)', run(['pdfinfo', str(pdf)])).group(1))
    assert pages == draft_pages, f'draft-figure copy has {draft_pages} pages, not {pages}; layouts differ'
    return stem, tex, pdf, pages, log, citeproc


def pdf_text(pdf, mode, title):
    """PDF text without running heads, page numbers and footers, which would otherwise split a
    paragraph that crosses a page break. `pdf` is the draft-figure copy, so figure labels are absent."""
    info = run(['pdfinfo', str(pdf)])
    w, h = map(float, re.search(r'Page size:\s+([\d.]+) x ([\d.]+)', info).groups())
    # Review copies carry line numbers in the left margin (x below 66 pt); read only the text block.
    crop = ['-x', '70', '-y', '0', '-W', str(int(w) - 70), '-H', str(int(h))] if mode == 'anonymous' else []
    pages = run(['pdftotext', *crop, str(pdf), '-']).split('\f')
    heads = {norm(title), norm('Jonathan Matkowsky'), norm('Anon.'), ''}
    out = []
    for n, page in enumerate(pages, 1):
        page = re.sub(r'Digit\. Threat\. Res\. Pract\., Vol\. \d+, No\. \d+, Article \S*\. Publication date: \w+ \d{4}\.', '', page)
        lines = page.split('\n')
        # Running head and folio: the first lines of each page, in whatever order pdftotext reads them.
        head, folio = [], False
        for k, l in enumerate(lines[:8]):
            s = norm(l)
            if s in heads: head.append(k)
            elif not folio and s == str(n): head.append(k); folio = True
        lines = [l for k, l in enumerate(lines) if k not in head]
        # Draft-mode figure boxes print their file name.
        out.append('\n'.join(l for l in lines if not re.fullmatch(r'\s*FIGURES/\S+\.pdf\s*', l)))
    return '\n'.join(out)


def pdf_check(units, pdf, mode, log, citeproc):
    text = norm(pdf_text(pdf.with_name(pdf.stem + '_TEXTCHECK.pdf'), mode, units[0][1]))
    missing, total = [], 0
    # Heading numbers are checked in the numbering check; pdftotext may read a number apart from its heading.
    checked = [(i, k, re.sub(r'^\d+(\.\d+)?\.? ', '', u) if k == 'heading' else re.sub(r'^Figure (\d+)\. ', r'Fig. \1. ', u))
               for i, (k, u) in enumerate(units)
               # Table cells and images are compared in the text check; the author block's layout is the template's.
               if k not in ('cell', 'image') and i not in (1, 2)]
    # Captions first: each is found, then removed, because a float's caption can sit inside a paragraph
    # that crosses a page break.
    for i, k, u in sorted(checked, key=lambda x: x[1] != 'caption'):
        for f in fragments(u):
            total += 1
            if f not in text: missing.append((k, u[:90]))
            elif k == 'caption': text = text.replace(f, '', 1)
    problems = []
    if 'not found' in citeproc: problems.append('citation keys missing from REFERENCES.json')
    if 'There were undefined references' in log: problems.append('undefined cross-references')
    if mode == 'anonymous':
        # Whole PDF text, running heads and all.
        whole = norm(run(['pdftotext', str(pdf), '-']) + run(['pdfinfo', str(pdf)]))  # text and document properties
        for f in FORBIDDEN:
            if f in whole: problems.append('anonymous PDF contains ' + f)
    return missing, total, problems


# ---------- Anonymous supplement ----------

# The settings BUILD.py passes to Pandoc for both documents. The full build compares the TeX made here
# with BUILD.py's SOURCE/supplement.tex, so a difference between the two lists stops the build.
ARTICLE_LATEX = [
    '-V', 'documentclass=article', '-V', 'fontsize=11pt', '-V', 'geometry:margin=1in',
    '-V', 'mainfont=lmroman10-regular.otf',
    '-V', 'mainfontoptions=BoldFont=lmroman10-bold.otf,ItalicFont=lmroman10-italic.otf,BoldItalicFont=lmroman10-bolditalic.otf',
    '-V', 'sansfont=lmsans10-regular.otf',
    '-V', 'sansfontoptions=BoldFont=lmsans10-bold.otf,ItalicFont=lmsans10-oblique.otf,BoldItalicFont=lmsans10-boldoblique.otf',
    '-V', 'monofont=lmmono10-regular.otf', '-V', 'monofontoptions=ItalicFont=lmmono10-italic.otf,HyphenChar=None',
    '-V', 'mathfont=latinmodern-math.otf', '-V', 'colorlinks=true', '-V', 'linkcolor=black',
    '-V', 'urlcolor=blue', '-V', 'linestretch=1']


def strip_byline(supplement, manuscript):
    """The supplement without its byline and status line: (text, author, status).

    The supplement opens with its title, the author's name and a dated status line, each its own
    paragraph. The name must equal the manuscript's byline, so a reordered opening is refused."""
    paras = supplement.split('\n\n')
    author = manuscript.split('\n\n')[1]
    assert paras[0].startswith('# ') and '\n' not in paras[0], 'the supplement must open with its title'
    assert paras[1] == author, 'the supplement\'s second paragraph must be the byline'
    assert ' · ' in paras[2] and '\n' not in paras[2] and not paras[2].endswith('.'), 'the supplement\'s third paragraph must be the status line'
    return '\n\n'.join(paras[:1] + paras[3:]), author, paras[2]


def article_tex(text, stem, author=None):
    """Pandoc's LaTeX for one document, as BUILD.py makes it; no author property when author is None."""
    W.mkdir(parents=True, exist_ok=True)
    title = text.split('\n', 1)[0][2:].strip()
    tmp = W / (stem + '_input.md')
    tmp.write_text(re.sub(r'\]\(\.\./', '](', text) + '\n\n## References\n\n::: {#refs}\n:::\n', encoding='utf-8')
    ast, tex = W / (stem + '.json'), W / (stem + '.tex')
    run(['pandoc', str(tmp), '-f', 'markdown-implicit_figures', '--citeproc', '--bibliography=REFERENCES.json',
         '--csl=SOURCE/references.csl', '-M', 'link-citations=true', '-t', 'json', '-o', str(ast)])
    run(['pandoc', str(ast), '-f', 'json', '-t', 'latex', '--standalone', '--lua-filter=SOURCE/layout.lua',
         '--include-in-header=SOURCE/header.tex', *ARTICLE_LATEX, '-V', 'title-meta=' + title,
         *(['-V', 'author-meta=' + author] if author else []), '-o', str(tex)])
    return tex


def tex_removals(public, anonymous):
    """Lines of the public TeX that the anonymous TeX lacks, and lines it adds. Blank lines are ignored."""
    diff = list(difflib.ndiff(public.splitlines(), anonymous.splitlines()))
    return ([l[2:] for l in diff if l.startswith('- ') and l[2:].strip()],
            [l[2:] for l in diff if l.startswith('+ ') and l[2:].strip()])


def anonymous_supplement(check_only):
    """Build and check the supplement's anonymous copy. Returns (report lines, failed)."""
    supplement = (B / 'SOURCE' / 'supplement.md').read_text(encoding='utf-8')
    text, author, status = strip_byline(supplement, (B / 'SOURCE' / 'manuscript.md').read_text(encoding='utf-8'))
    problems = ['the source still contains ' + f for f in FORBIDDEN if f in norm(text)]
    public = article_tex(supplement, 'SUPPLEMENT_PUBLIC', author).read_text(encoding='utf-8')
    tex = article_tex(text, 'SUPPLEMENT_ANONYMOUS')
    removed, added = tex_removals(public, tex.read_text(encoding='utf-8'))
    # Pandoc may wrap the status line; compare the removed lines joined, letters and digits only.
    expected = norm('pdfauthor={' + author + '},' + author + status)
    if added or norm(''.join(removed)) != expected:
        problems.append('the anonymous TeX differs from the supplement beyond the byline, status line and author property')
    report = ['## Anonymous supplement\n',
              '- Removed: the byline and the status line. The author property is not set.',
              f'- TeX check: {"pass" if not problems else "FAIL"}. The anonymous TeX equals the supplement\'s except for '
              f'those {len(removed)} lines; the surname and the preprint DOI are not in its source.']
    if not check_only:
        built = B / 'SOURCE' / 'supplement.tex'
        if built.read_text(encoding='utf-8') != public:
            problems.append('SOURCE/supplement.tex differs from the TeX made here; BUILD.py and ARTICLE_LATEX disagree, or BUILD.py has not run')
        for _ in range(2):
            run(['xelatex', '-interaction=nonstopmode', '-halt-on-error', '-output-directory=' + str(W), str(tex)])
        pdf = W / 'SUPPLEMENT_ANONYMOUS.pdf'
        info = run(['pdfinfo', str(pdf)])
        whole = norm(run(['pdftotext', str(pdf), '-']) + info)
        found = [f for f in FORBIDDEN if f in whole]
        problems += ['anonymous supplement PDF contains ' + f for f in found]
        report.append('- The author\'s surname and the preprint DOI appear nowhere in the PDF text or document properties.'
                      if not found else '- Identifying text found.')
        report.append(f'- Pages: {int(re.search(r"Pages:\s+(\d+)", info).group(1))}.')
        OUT.mkdir(exist_ok=True)
        shutil.copy2(pdf, OUT / 'SUPPLEMENT_ANONYMOUS.pdf')
        shutil.copy2(tex, OUT / 'SUPPLEMENT_ANONYMOUS.tex')
    report += ['  - ' + p for p in problems] + ['']
    return report, bool(problems)


def main():
    check_only = '--check-only' in sys.argv
    src_doc = pandoc_json(source_text())
    report, failed = [], False
    report.append('# Journal-format build check\n')
    report.append('Generated by `JOURNAL_BUILD.py` from `SOURCE/manuscript.md`. Layout files: `SOURCE/acm.lua`, '
                  '`SOURCE/acm-template.tex`; removals for the anonymous copy: `SOURCE/anonymize.txt`. The anonymous '
                  'supplement comes from `SOURCE/supplement.md`, in the supplement\'s own layout.\n')
    for mode in ('preprint', 'anonymous'):
        jdoc, units, diff, num_problems, counts, applied, cites = text_check(src_doc, mode)
        ok_text = not diff and not num_problems
        failed |= not ok_text
        report.append(f'## {mode.capitalize()} copy\n')
        report.append(f'- Text check: {"pass" if not diff else "FAIL"}. {len(units)} headings, paragraphs, list items, '
                      f'captions, table cells and images compared with the source, in order.')
        report.append(f'- Numbering check: {"pass" if not num_problems else "FAIL"}. {counts["sections"]} sections, '
                      f'{counts["subsections"]} subsections, {counts["tables"]} tables and {counts["figures"]} figures '
                      'print the numbers typed in the source.')
        report.append(f'- Citation keys in the text: {len(cites)}.')
        if mode == 'anonymous':
            report.append(f'- Removed for anonymous review ({len(applied)} entries in `SOURCE/anonymize.txt`, each matched once):')
            for kind, body in applied:
                report.append(f'  - {kind}: {body[:160]}{"…" if len(body) > 160 else ""}')
        report.append('- Supplied by the template, not the source: the country "USA" in the author block (ACM requires a '
                      'country), and ACM\'s own labels, such as "Additional Key Words and Phrases" for the keywords line.')
        if diff: report.append('\n```diff\n' + '\n'.join(diff[:200]) + '\n```')
        for p in num_problems: report.append('  - ' + p)
        if not check_only:
            stem, tex, pdf, pages, log, citeproc = typeset(mode)
            missing, total, pdf_problems = pdf_check(units, pdf, mode, log, citeproc)
            ok_pdf = not missing and not pdf_problems
            failed |= not ok_pdf
            report.append(f'- PDF check: {"pass" if ok_pdf else "FAIL"}. {total - len(missing)} of {total} text '
                          'fragments found in the PDF; all citations resolved.' if ok_pdf else
                          f'- PDF check: FAIL. {len(missing)} of {total} fragments missing; {", ".join(pdf_problems)}')
            for k, u in missing[:20]: report.append(f'  - missing {k}: {u}')
            if mode == 'anonymous':
                report.append('- The author\'s surname and the preprint DOI appear nowhere in the PDF text or document properties.'
                              if not any(p.startswith('anonymous PDF') for p in pdf_problems) else '- Identifying text found.')
            report.append(f'- Pages: {pages}.')
            OUT.mkdir(exist_ok=True)
            shutil.copy2(pdf, OUT / (stem + '.pdf'))
            shutil.copy2(tex, OUT / (stem + '.tex'))
        report.append('')
    lines, bad = anonymous_supplement(check_only)
    report += lines
    failed |= bad
    text = '\n'.join(report) + '\n'
    if check_only:
        print(text)
    else:
        (OUT / 'CHECK_REPORT.md').write_text(text, encoding='utf-8')
        print(text)
    if failed:
        sys.exit('Journal-format check failed; see the report above.')


if __name__ == '__main__':
    main()
