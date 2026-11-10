"""Score a second rater's answers against the paper's mechanism-to-signal links.

  python3 tools/second_coder/score.py ANSWERS.txt [KEY.json]

ANSWERS.txt holds the rater's lines: `M01 | SIG-xx, SIG-yy (inference) | missing: none`.
Prints agreement over every mechanism-signal cell of the mapped sample (Cohen's kappa, and the share
of the paper's links the rater also made and of the rater's links the paper also made), then each
disagreement, then the rater's "missing" answers.
"""
import csv, json, re, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SUP = HERE.parents[1] / 'SUPPLEMENT'
CROSS_CUTTING = {'SIG-44', 'SIG-45', 'SIG-46'}

def rows(name):
    with open(SUP / name, newline='', encoding='utf-8') as f:
        return list(csv.DictReader(f))

def parse(text, labels):
    got = {}
    for line in text.splitlines():
        m = re.match(r'^\W*(M\d\d)\s*\|(.*?)\|\s*missing:\s*(.*?)\W*$', line.strip(), re.I)
        if not m or m.group(1) not in labels: continue
        got[m.group(1)] = (set(re.findall(r'SIG-\d\d', m.group(2))),
                           set(re.findall(r'(SIG-\d\d)\s*\(inference\)', m.group(2), re.I)), m.group(3).strip())
    missing = sorted(set(labels) - set(got))
    if missing: sys.exit('No answer line for: ' + ', '.join(missing))
    return got

def kappa(a, b, c, d):
    """a both link, b paper only, c rater only, d neither."""
    n = a + b + c + d
    po = (a + d) / n
    pe = ((a + b) * (a + c) + (c + d) * (b + d)) / (n * n)
    return (po - pe) / (1 - pe) if pe < 1 else 1.0

def tally(answers=None, key=None):
    """Counts for the mapped mechanisms of a run: (both, paper only, rater only, neither, identical sets, detail, got, labels)."""
    labels = json.loads(Path(key or HERE / 'KEY.json').read_text())['labels']
    got = parse(Path(answers or HERE / 'real_run' / 'ANSWERS.txt').read_text(encoding='utf-8'), labels)
    sig = [s['signal_id'] for s in rows('S3_SIGNALS.csv') if s['signal_id'] not in CROSS_CUTTING]
    paper = {}
    for p in rows('S3_MECHANISM_SIGNAL_PAIRS.csv'):
        paper.setdefault(p['mechanism'], set()).add(p['signal_id'])
    a = b = c = d = 0
    detail = []
    for label, mid in labels.items():
        rater = got[label][0] & set(sig)
        if mid not in paper:
            continue
        truth = paper[mid] - CROSS_CUTTING
        a += len(truth & rater); b += len(truth - rater); c += len(rater - truth)
        d += len(sig) - len(truth | rater)
        detail.append((label, mid, sorted(truth & rater), sorted(truth - rater), sorted(rater - truth)))
    return a, b, c, d, detail, got, labels, paper


def main():
    a, b, c, d, detail, got, labels, paper = tally(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else None)
    names = {s['signal_id']: s['signal'] for s in rows('S3_SIGNALS.csv')}
    n_map = len(detail)
    print(f'Mapped mechanisms scored: {n_map}; cells: {a + b + c + d}')
    print(f'Both link: {a}; paper only: {b}; rater only: {c}; neither: {d}')
    print(f"Cohen's kappa: {kappa(a, b, c, d):.2f}")
    print(f"Paper's links the rater also made: {a}/{a + b} ({100 * a / (a + b):.0f} percent)")
    if a + c: print(f"Rater's links the paper also made: {a}/{a + c} ({100 * a / (a + c):.0f} percent)")
    print(f'Mechanisms with identical link sets: {sum(1 for x in detail if not x[3] and not x[4])}/{n_map}')
    print('\nDisagreements:')
    for label, mid, both, ponly, ronly in detail:
        if ponly or ronly:
            print(f'- {label} ({mid}): paper only ' + (', '.join(f'{s} {names[s]}' for s in ponly) or 'none')
                  + '; rater only ' + (', '.join(f'{s} {names[s]}' for s in ronly) or 'none'))
    print('\nMechanisms the paper judged covered by existing records:')
    for label, mid in labels.items():
        if mid not in paper:
            print(f'- {label} ({mid}): rater linked {sorted(got[label][0]) or "none"}; missing: {got[label][2]}')
    print('\n"Missing record" answers for mapped mechanisms:')
    for label, mid in labels.items():
        if mid in paper and got[label][2].lower() not in ('none', 'none.'):
            print(f'- {label} ({mid}): {got[label][2]}')


if __name__ == '__main__':
    main()
