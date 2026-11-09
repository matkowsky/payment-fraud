"""Finite integrity and hypothetical-arithmetic checks for a proposed version 1.1 revision. No network or real activity.

Run from the extracted package directory: python3 CHECK_CANDIDATE.py
Pull-request checks run python3 CHECK_CANDIDATE.py --sources, which skips the comparison with
generated bibliographies because generated files are rebuilt only after merge.
These checks establish artifact consistency and the arithmetic of stipulated examples only.
They do not prove source claims, novelty, implementation or system performance.
"""
from pathlib import Path
import csv, json, re, collections, subprocess, sys
SOURCES_ONLY = '--sources' in sys.argv[1:]
B = Path(__file__).resolve().parent; S = B / 'SUPPLEMENT'
MS = 'MANUSCRIPT.md'; REFJ = 'REFERENCES.json'; REFB = 'REFERENCES.bib'
def rows(n): return list(csv.DictReader((S / n).open(encoding='utf-8')))
s = rows('S3_SIGNALS.csv'); p = rows('S3_MECHANISM_SIGNAL_PAIRS.csv'); d = rows('S3_SOURCE_DIRECTORY.csv')
j = rows('S3_MAPPING_SOURCE_JOINS.csv'); a = rows('S2_MECHANISM_ALLOCATION.csv'); f = rows('S4_FUNCTIONS.csv')
c = rows('S6_SYNTHETIC_COHORT.csv'); r = json.loads((B / REFJ).read_text(encoding='utf-8'))
t = (B / MS).read_text(encoding='utf-8'); body = (B / 'SOURCE/manuscript.md').read_text(encoding='utf-8')
ts = (B / 'SUPPLEMENT.md').read_text(encoding='utf-8'); sbody = (B / 'SOURCE/supplement.md').read_text(encoding='utf-8')

# Inventory, mappings and lineage
assert len(s) == len({x['signal_id'] for x in s}) == 71
assert len({x['family'] for x in s}) == 12
assert len(p) == len({(x['mechanism'], x['signal_id']) for x in p}) == 163
assert sum(x['support_class'] == 'inference' for x in p) == 9
assert len(d) == len({x['source_id'] for x in d}) == 61
assert len(j) == len({x['row_id'] for x in j}) == len({(x['mechanism_id'], x['source_id']) for x in j}) == 126
sid = {x['signal_id'] for x in s}; src = {x['source_id'] for x in d}; joins = {(x['mechanism_id'], x['source_id']) for x in j}
assert {x['source_id'] for x in j} == src, 'every directory source is joined and every joined source is in the directory'
for x in p:
    assert x['signal_id'] in sid
    for k in re.findall(r'L\d+', x['source_ids']): assert (k in src and (x['mechanism'], k) in joins), (x, k)
g = {x['signal_id']: re.findall(r'SIG-\d+', x['lineage_inputs']) for x in s}
def visit(k, stack):
    assert k not in stack, 'Lineage cycle ' + str(stack + [k])
    for dep in g[k]: assert dep in sid; visit(dep, stack + [k])
for k in g: visit(k, [])
assert sid - {x['signal_id'] for x in p} == {'SIG-44', 'SIG-45', 'SIG-46'}
assert len(a) == len({x['ID'] for x in a}) == 99
counts = collections.Counter(x['disposition'] for x in a)
assert dict(counts) == {'dedicated': 53, 'targeted': 8, 'unreviewed': 20, 'covered': 13, 'screened gap': 4, 'adjacent logged': 1}, counts
# Job-posting topics in the priority basis (Supplement S2): 24 candidates, 23 of the 26 Tier 1, all mapped, 65 links.
posting = {x['ID'] for x in a if re.search(r'(?<![\w:])r:', x['Priority (basis)'])}
tier1 = {x['ID'] for x in a if x['Depth'] == 'Tier 1'}; mapped = {x['mechanism'] for x in p}
assert len(posting) == 24 and len(tier1) == 26 and len(posting & tier1) == 23, (len(posting), len(tier1))
assert posting & tier1 <= mapped and sum(x['mechanism'] in posting & tier1 for x in p) == 65
assert posting - tier1 == {'EC-06'} and 'EC-06' not in mapped
assert len(f) == 24 and {int(x['component']) for x in f} == set(range(1, 25))
assert collections.Counter(x['class'] for x in f) == {'DI': 17, 'AGV': 1, 'INH': 6}
public = collections.Counter('partial' if x['public_representation_label'].startswith('FACT') else 'na' if x['public_representation_label'].startswith('n/a') else 'unlocated' for x in s)
assert public == {'partial': 32, 'na': 32, 'unlocated': 7}, public

# Citations, references and numbering
# All 122 works are cited across the manuscript and supplement pair; each generated bibliography lists the works its text cites.
mkeys = set(re.findall(r'(?<!\w)@([\w]+)', body)); skeys = set(re.findall(r'(?<!\w)@([\w]+)', sbody)); refkeys = {x['id'] for x in r}
keys = mkeys | skeys
assert len(keys) == 122 and keys == refkeys, sorted(refkeys ^ keys)
if not SOURCES_ONLY:
    assert set(re.findall(r'<div id="ref-([^"]+)"', t)) == mkeys
    assert set(re.findall(r'<div id="ref-([^"]+)"', ts)) == skeys
assert {x['citation_key'] for x in rows('S1_CITED_SOURCE_NOTES.csv')} == refkeys
assert set(re.findall(r'\*\*Table (\d+)\.', body)) == set(map(str, range(1, 7)))
assert set(re.findall(r'\*\*Figure (\d+)\.', body)) == set(map(str, range(1, 5)))
for path in re.findall(r'!\[[^]]*\]\(([^)]+)\)', body):
    assert (B / 'SOURCE' / path).is_file(), path
    for ext in ('.pdf', '.png'): assert (B / 'SOURCE' / path).with_suffix(ext).is_file(), (path, ext)

# Synthetic cohort (Trace B): disjoint cohorts, deduplication and attribution
assert len(c) == len({x['transaction_id'] for x in c}) == 400
cb = {x['transaction_id'] for x in c if int(x['chargeback_report'])}
alerts = {x['transaction_id'] for x in c if int(x['pre_dispute_resolution'])}
assert (len(cb), len(alerts), len(cb & alerts), len(cb | alerts)) == (8, 14, 2, 20)
for ac in 'ABCD':
    z = [x for x in c if x['account_id'] == ac]
    assert len(z) == 100 and sum(int(x['chargeback_report']) for x in z) == 2
    assert sum(1 for x in z if int(x['chargeback_report']) or int(x['pre_dispute_resolution'])) == (8 if ac in 'AB' else 2)
assert len(cb) / len(c) == .02 and len(cb | alerts) / len(c) == .05 and (len(cb) + len(alerts)) / len(c) == .055
assert {x['transaction_id'] for x in c if x['chargeback_recorded_at_account'] == 'account-X'} == {'D001', 'D002'}
# Counting where a chargeback is recorded hides D's two reports; transaction attribution restores them.
recorded = collections.Counter(x['chargeback_recorded_at_account'] for x in c if int(x['chargeback_report']))
assert dict(recorded) == {'A': 2, 'B': 2, 'C': 2, 'account-X': 2}, recorded
by_recording = {ac: recorded.get(ac, 0) / 100 for ac in 'ABCD'}; by_attribution = {ac: 2 / 100 for ac in 'ABCD'}
assert by_recording['D'] == 0 and by_attribution['D'] == .02
# Pooled ratio is the transaction-weighted mean of account ratios for disjoint cohorts.
T = {ac: 100 for ac in 'ABCD'}; D = {ac: 2 for ac in 'ABCD'}
pooled = sum(D.values()) / sum(T.values()); weighted = sum((T[k] / sum(T.values())) * (D[k] / T[k]) for k in T)
assert abs(pooled - weighted) < 1e-12 and min(D[k] / T[k] for k in T) <= pooled <= max(D[k] / T[k] for k in T)

# Section 8.2 uncertainty: exact (Clopper-Pearson) 95 percent intervals and Fisher's two-sided exact test, standard library only.
from math import comb
def binom_cdf(k, n, p): return sum(comb(n, i) * p**i * (1 - p)**(n - i) for i in range(k + 1))
def clopper_pearson(k, n, a=0.05):
    def solve(f):
        lo, hi = 0.0, 1.0
        for _ in range(200):
            mid = (lo + hi) / 2
            lo, hi = (mid, hi) if f(mid) else (lo, mid)
        return (lo + hi) / 2
    lower = 0.0 if k == 0 else solve(lambda q: 1 - binom_cdf(k - 1, n, q) < a / 2)
    upper = 1.0 if k == n else solve(lambda q: binom_cdf(k, n, q) > a / 2)
    return lower, upper
def fisher_two_sided(a, b, c, d):
    r1, c1, n = a + b, a + c, a + b + c + d
    pmf = lambda x: comb(c1, x) * comb(n - c1, r1 - x) / comb(n, r1)
    obs = pmf(a)
    return sum(pmf(x) for x in range(max(0, r1 + c1 - n), min(r1, c1) + 1) if pmf(x) <= obs * (1 + 1e-9))
intervals = {(2, 100): (0.24, 7.04), (0, 100): (0.0, 3.62), (8, 400): (0.87, 3.90), (8, 100): (3.52, 15.16)}
for (k, n), (lo, hi) in intervals.items():
    l, u = clopper_pearson(k, n)
    assert (round(100 * l, 2), round(100 * u, 2)) == (lo, hi), (k, n, l, u)
fisher_p = fisher_two_sided(8, 92, 2, 98)
assert round(fisher_p, 2) == 0.10 and abs(fisher_p - 0.1005) < 5e-4, fisher_p

# Supplement S7.1 sizing arithmetic: nine evaluations, four confirmatory at 93 percent power each (union bound);
# the planted false exonerations E8 needs at least to show a release rate below 1 percent with none released;
# and the number it needs for 93 percent power when the true release rate is 0.1 percent, with the implied
# drafts and days if planted false exonerations are 5 percent of drafts and 20 drafts arrive a day.
assert round(1 - 4 * 0.07, 2) == 0.72 and 'all four pass with probability at least 72 percent' in sbody and '79 percent' not in sbody
assert 'E1, E3, E8 and E9 are confirmatory' in sbody and 'E1, E3, E8 and E9 are confirmatory' in body
assert set(re.findall(r'^#### E(\d) \(', sbody, re.M)) == set(map(str, range(1, 10)))
n_fe = next(n for n in range(1, 1000) if 1 - 0.05 ** (1 / n) < 0.01)
assert n_fe == 299 and 'needs at least 299' in sbody and 'at least 150' not in sbody
def e8_power(n, true, tol=0.01, a=0.05):
    # Pass when the exact one-sided 95 percent upper bound is at or below tol, i.e. at most c releases,
    # where c is the largest count with P(X <= c; n, tol) <= a.
    c = -1
    while c + 1 <= n and binom_cdf(c + 1, n, tol) <= a: c += 1
    return 0.0 if c < 0 else binom_cdf(c, n, true)
n_pow = next(n for n in range(1, 2000) if e8_power(n, 0.001) >= 0.93)
assert n_pow == 628 and all(e8_power(m, 0.001) >= 0.93 for m in range(n_pow, n_pow + 60)) and e8_power(299, 0.001) < 0.93
e8_drafts = round(n_pow / 0.05); e8_days = e8_drafts // 20
assert e8_drafts == 12560 and e8_days == 628 and 'needs 628' in sbody and '12,560 drafts, about 628 days' in sbody
assert round(100 * binom_cdf(2, 628, 0.01), 2) == 4.98 and binom_cdf(3, 628, 0.01) > 0.05 and round(100 * binom_cdf(2, 628, 0.001), 1) == 97.4
assert 'two or fewer releases show it' in sbody and 'probability 4.98 percent' in sbody and 'probability 97.4 percent' in sbody
assert round(100 * 0.93 ** 4) == 75 and 'about 75 percent if their results are independent' in sbody
m59 = next(m for m in range(1, 1000) if 1 - 0.95 ** m >= 0.95)  # Section 6.4: sample finding a 5 percent contrary share
assert m59 == 59 and '59 records give 95 percent when $q$ is 5 percent' in body

# Trace A timing: the same edge is effective earlier but unavailable to the frozen assessment.
edge = {'effective_minute': -1440, 'known_minute': 1440}; cutoff = 30
assert edge['effective_minute'] <= cutoff < edge['known_minute']
assert not (edge['effective_minute'] <= cutoff and edge['known_minute'] <= cutoff)
assert 2 < 7 * 24  # two available hours cannot establish seven-day absence

# Relative links resolve, including from directly opened source Markdown.
checked_links = 0
for md in [*B.glob('*.md'), *(B / 'SOURCE').glob('*.md')]:
    for target in re.findall(r'!?\[[^\]]*\]\(([^)]+)\)', md.read_text(encoding='utf-8')):
        if target.startswith(('http://', 'https://', '#', 'mailto:')): continue
        target = target.split('#')[0]
        assert (md.parent / target).is_file(), (md.name, target)
        checked_links += 1

# Reader-facing tables cannot retain chat identifiers, repair directions or internal project identifiers.
residue = r'turn\d+(?:view|search|fetch|academia)|manuscript lines?|replace with|sub.agent|\bGate [0-9]|\bWorkstream\b|\bG2-\d|\bRQ-[A-Z]\d|engineering ledger'
for csvpath in S.glob('*.csv'):
    content = csvpath.read_text(encoding='utf-8')
    assert not re.search(residue, content, re.I), csvpath.name

# BibLaTeX identity roundtrip, if Pandoc is available.
try:
    parsed = json.loads(subprocess.check_output(['pandoc', str(B / REFB), '-f', 'biblatex', '-t', 'csljson'], text=True))
    assert {x['id'] for x in parsed} == refkeys
except FileNotFoundError:
    parsed = None

# Public bundle screening: private locations, review records, credentials and em dashes.
private = r'jonathanmatkowsky|jonathan_matkowsky|sharepoint\.com|onedrive|REVIEW_REPORT|PURPOSE_CONTEXT|PRIVATE_RECORDS|supervisory|job search|job application|interview prep|sk-[A-Za-z0-9]{20,}'
screened = 0
for path in [B / MS, B / 'SUPPLEMENT.md', B / 'README.md', B / 'REPRODUCE.md', B / REFB, B / REFJ,
             *[p for p in [B / 'CHANGES_SINCE_v1.0.md'] if p.is_file()],
             *(B / 'SOURCE').glob('*.md'), *(B / 'FIGURES').rglob('*.svg'), *(B / 'SUPPLEMENT').rglob('*.csv'),
             *(B / 'SUPPLEMENT').rglob('*.json')]:
    z = path.read_text(encoding='utf-8')
    assert not re.search(private, z, re.I), path
    assert '—' not in z, ('em dash', path.name)
    screened += 1

# Outcome-record schema (Supplement S4.2): the synthetic valid case passes and each invalid case fails exactly its rule.
sys.path.insert(0, str(B / 'tools'))
from outcome_conformance import run_conformance
outcome = run_conformance()
assert outcome == {'valid_records': 27, 'invalid_cases': 22, 'rules_exercised': 15}, outcome

result = {'signals': 71, 'families': 12, 'pairs': 163, 'explicit_inference_pairs': 9, 'lineage': 'valid and acyclic',
          'source_directory': 61, 'source_join_rows': 126, 'allocation': dict(counts),
          'posting_priority': {'candidates': 24, 'tier1': 26, 'tier1_with_posting_topic': 23, 'their_links': 65}, 'functions': 24,
          'public_counterparts': dict(public), 'cited_works': 122, 'cited_in_manuscript': len(mkeys), 'cited_in_supplement': len(skeys), 'tables': 6, 'figures': 4,
          'synthetic': {'transactions': 400, 'chargebacks': 8, 'alerts': 14, 'overlap': 2, 'union': 20,
                        'chargeback_ratio': .02, 'broader_report_ratio': .05, 'undeduplicated_sum_rejected': .055,
                        'D_by_recording_account': by_recording['D'], 'D_by_transaction_attribution': by_attribution['D'],
                        'clopper_pearson_and_fisher': f'intervals match Section 8.2; Fisher two-sided p = {fisher_p:.4f}'},
          'bib_parser_checked': parsed is not None, 'private_content_and_dash_screen': f'passed ({screened} files)',
          'relative_links_checked': checked_links, 'outcome_record_conformance': outcome,
          'as_of_example': 'later-known edge excluded; earlier onset unresolved',
          'evaluation_sizing': {'evaluations': 9, 'confirmatory': 4, 'all_confirmatory_pass_at_least': 0.72, 'e8_false_exonerations_for_1_percent': n_fe,
                                'e8_for_93_percent_power_at_0.1_percent': n_pow, 'e8_drafts_at_5_percent': e8_drafts, 'e8_days_at_20_a_day': e8_days},
          'mode': 'sources only; generated bibliographies not compared' if SOURCES_ONLY else 'full',
          'scope': 'Artifact integrity and hypothetical arithmetic only; not source proof or system evaluation.'}
print(json.dumps(result, indent=2))
