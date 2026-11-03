"""Rebuild the research documents from SOURCE/.

Requires Pandoc (with citeproc) and XeLaTeX. Figure exports use Inkscape when it is
installed; otherwise EXPORT_FIGURES.py uses headless Chromium. If the TeX installation
lacks lmodern.sty, a stub is written to build/ (see REPRODUCE.md). No network access.
"""
from pathlib import Path
import subprocess, shutil, os, re, sys
B = Path(__file__).resolve().parent
NAME = 'MANUSCRIPT_v1.0_2026-10-29'
REFS = 'REFERENCES.json'
W = B / 'build'; W.mkdir(exist_ok=True)
env = dict(os.environ)

def run(args):
    r = subprocess.run(args, cwd=B, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, env=env)
    if r.returncode:
        raise RuntimeError(' '.join(args) + '\n' + r.stdout[-8000:])
    return r.stdout

# 1. Figure exports: vector PDF for typesetting and 1.5x PNG as readable alternates.
svgs = sorted((B / 'FIGURES').glob('*.svg'))
if shutil.which('inkscape'):
    for f in svgs:
        run(['inkscape', str(f), '--export-type=pdf', '--export-filename=' + str(f.with_suffix('.pdf'))])
        run(['inkscape', str(f), '--export-type=png', '--export-dpi=144', '--export-filename=' + str(f.with_suffix('.png'))])
    print('Figures exported with Inkscape.')
elif shutil.which('chromium') or shutil.which('chromium-browser') or shutil.which('google-chrome') or Path(os.environ.get('CHROMIUM', '/opt/pw-browsers/chromium')).exists():
    run([sys.executable, str(B / 'EXPORT_FIGURES.py'), *map(str, svgs)])
    print('Figures exported with headless Chromium (Inkscape not found).')
elif all(f.with_suffix('.pdf').is_file() and f.with_suffix('.png').is_file() for f in svgs):
    print('No SVG exporter installed; reusing the existing figure PDF and PNG exports (reported fallback).')
else:
    raise RuntimeError('No SVG exporter found and figure exports are missing; install Inkscape or set CHROMIUM.')

# 2. lmodern.sty fallback: under XeLaTeX the fontspec settings below replace its defaults.
if subprocess.run(['kpsewhich', 'lmodern.sty'], stdout=subprocess.PIPE, text=True).stdout.strip() == '':
    (W / 'lmodern.sty').write_text('% Stub used only when TeX Live lacks lmodern.sty; fontspec settings in the\n'
                                   '% generated source replace the Latin Modern defaults that lmodern.sty selects.\n'
                                   '\\ProvidesPackage{lmodern}[2026/09/28 stub for XeLaTeX builds]\n')
    env['TEXINPUTS'] = str(W) + os.pathsep + env.get('TEXINPUTS', '')
    print('lmodern.sty not installed; using build/lmodern.sty stub.')

# 3. Documents: citation-key sources -> reader-facing Markdown, TeX and PDF.
# Each PDF's title and author metadata repeat the document's own title (its first heading) and byline.
for stem, name in [('manuscript', NAME), ('supplement', 'SUPPLEMENT')]:
    src = (B / 'SOURCE' / f'{stem}.md').read_text()
    head = [l for l in src.splitlines() if l.strip()]
    assert head[0].startswith('# '), stem
    title, author = head[0][2:].strip(), head[1].strip()
    src = re.sub(r'\]\(\.\./', '](', src)
    src += '\n\n## References\n\n::: {#refs}\n:::\n'
    temp = W / f'{stem}_input.md'; temp.write_text(src)
    ast = W / f'{stem}.json'
    run(['pandoc', str(temp), '-f', 'markdown-implicit_figures', '--citeproc', '--bibliography=' + REFS,
         '--csl=SOURCE/references.csl', '-M', 'link-citations=true', '-t', 'json', '-o', str(ast)])
    run(['pandoc', str(ast), '-f', 'json', '-t', 'gfm', '--wrap=none', '-o', name + '.md'])
    tex = B / 'SOURCE' / f'{stem}.tex'
    run(['pandoc', str(ast), '-f', 'json', '-t', 'latex', '--standalone', '--lua-filter=SOURCE/layout.lua',
         '--include-in-header=SOURCE/header.tex', '-V', 'documentclass=article', '-V', 'fontsize=11pt',
         '-V', 'geometry:margin=1in', '-V', 'mainfont=lmroman10-regular.otf',
         '-V', 'mainfontoptions=BoldFont=lmroman10-bold.otf,ItalicFont=lmroman10-italic.otf,BoldItalicFont=lmroman10-bolditalic.otf',
         '-V', 'sansfont=lmsans10-regular.otf',
         '-V', 'sansfontoptions=BoldFont=lmsans10-bold.otf,ItalicFont=lmsans10-oblique.otf,BoldItalicFont=lmsans10-boldoblique.otf',
         '-V', 'monofont=lmmono10-regular.otf', '-V', 'monofontoptions=ItalicFont=lmmono10-italic.otf,HyphenChar=None',
         '-V', 'mathfont=latinmodern-math.otf', '-V', 'colorlinks=true', '-V', 'linkcolor=black',
         '-V', 'urlcolor=blue', '-V', 'linestretch=1', '-V', 'title-meta=' + title, '-V', 'author-meta=' + author,
         '-o', str(tex)])
    for _ in range(2):
        out = run(['xelatex', '-interaction=nonstopmode', '-halt-on-error', '-output-directory=' + str(W), str(tex)])
        (W / f'{stem}_compiler.txt').write_text(out)
    shutil.copy2(W / f'{stem}.pdf', B / f'{name}.pdf')
    print(name + ': Markdown, PDF and TeX rebuilt.')
print('Reader-facing Markdown is generated from SOURCE/*.md; edit the sources before rebuilding.')
