"""Convert SVG figures to single-page vector PDFs and 1.5x PNGs with headless Chromium.

Used by BUILD.py when Inkscape is not installed. Usage: python3 EXPORT_FIGURES.py FIGURES/*.svg
Set CHROMIUM to a browser executable if it is not found automatically.
"""
import sys, re, subprocess, tempfile, pathlib, os
CH = os.environ.get('CHROMIUM', '/opt/pw-browsers/chromium')
if not pathlib.Path(CH).exists():
    import shutil
    CH = shutil.which('chromium') or shutil.which('chromium-browser') or shutil.which('google-chrome')
def dims(svg):
    t = pathlib.Path(svg).read_text()
    w = float(re.search(r'<svg[^>]*\bwidth="([\d.]+)"', t).group(1)); h = float(re.search(r'<svg[^>]*\bheight="([\d.]+)"', t).group(1))
    return w, h
def to_pdf(svg, pdf):
    w, h = dims(svg)
    html = f"""<!doctype html><html><head><meta charset="utf-8"><style>@page{{size:{w}px {h}px;margin:0}}html,body{{margin:0;padding:0}}img{{display:block;width:{w}px;height:{h}px}}</style></head><body><img src="{pathlib.Path(svg).resolve().as_uri()}"></body></html>"""
    with tempfile.NamedTemporaryFile('w', suffix='.html', delete=False) as f: f.write(html); hp = f.name
    subprocess.run([CH, '--headless', '--no-sandbox', '--disable-gpu', '--no-pdf-header-footer', '--print-to-pdf-no-header', f'--print-to-pdf={pdf}', 'file://' + hp], check=True, capture_output=True)
    os.unlink(hp)
def to_png(svg, png, scale=1.5):
    w, h = dims(svg)
    # Headless Chromium reserves part of the window height, so render a padded page and crop to the SVG box.
    html = f"""<!doctype html><html><head><meta charset="utf-8"><style>html,body{{margin:0;padding:0;background:white}}img{{display:block;width:{w}px;height:{h}px}}</style></head><body><img src="{pathlib.Path(svg).resolve().as_uri()}"></body></html>"""
    with tempfile.NamedTemporaryFile('w', suffix='.html', delete=False) as f: f.write(html); hp = f.name
    subprocess.run([CH, '--headless', '--no-sandbox', '--disable-gpu', '--hide-scrollbars', f'--force-device-scale-factor={scale}', f'--window-size={int(w)},{int(h) + 240}', f'--screenshot={png}', 'file://' + hp], check=True, capture_output=True)
    os.unlink(hp)
    try:  # Crop to the figure and reduce size for flat-color diagrams; skipped if Pillow is absent.
        from PIL import Image
        im = Image.open(png).convert('RGB').crop((0, 0, int(round(w * scale)), int(round(h * scale))))
        im.quantize(colors=256, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.NONE).save(png, optimize=True)
    except ImportError:
        pass
if __name__ == '__main__':
    for svg in sys.argv[1:]:
        p = pathlib.Path(svg)
        to_pdf(p, p.with_suffix('.pdf')); to_png(p, p.with_suffix('.png'))
        print(p.name, 'pdf+png')
