"""Check a closed-case audit form and compute its shares, exact intervals and ranges.

Usage: python3 summarize.py RESULTS_FORM.csv
Standard library only. The form holds counts; no case data is read.
"""
import csv
import json
import sys
from math import comb

FAILURES = ('F1', 'F2', 'F3')


def binom_cdf(k, n, p):
    return sum(comb(n, i) * p**i * (1 - p)**(n - i) for i in range(k + 1))


def exact_interval(k, n, alpha=0.05):
    """Clopper-Pearson interval for k of n."""
    def solve(test):
        lo, hi = 0.0, 1.0
        for _ in range(200):
            mid = (lo + hi) / 2
            lo, hi = (mid, hi) if test(mid) else (lo, mid)
        return (lo + hi) / 2
    lower = 0.0 if k == 0 else solve(lambda q: 1 - binom_cdf(k - 1, n, q) < alpha / 2)
    upper = 1.0 if k == n else solve(lambda q: binom_cdf(k, n, q) > alpha / 2)
    return lower, upper


def read_form(path):
    with open(path, encoding='utf-8', newline='') as f:
        return {r['item']: r['value'].strip() for r in csv.DictReader(f)}


def count(form, item):
    value = form.get(item, '')
    if not value.isdigit():
        raise SystemExit(f'{item}: enter a whole number, found {value!r}')
    return int(value)


def share(k, n):
    lo, hi = exact_interval(k, n)
    return {'count': k, 'of': n, 'percent': round(100 * k / n, 1), 'interval_95': [round(100 * lo, 1), round(100 * hi, 1)]}


def summarize(form):
    total = count(form, 'cases_sampled')
    if total == 0:
        raise SystemExit('cases_sampled: no cases')
    out = {'identified_as': form.get('identified_as', ''), 'sampling_frame': form.get('sampling_frame', ''),
           'period': form.get('period', ''), 'fixed_in_advance': form.get('fixed_in_advance', ''), 'cases_sampled': total}
    for f in FAILURES:
        occurred, absent, unsettled, changed, agree = (count(form, f'{f}_{k}') for k in
                                                       ('occurred', 'not_occurred', 'unsettled', 'changed', 'first_codes_agree'))
        if occurred + absent + unsettled != total:
            raise SystemExit(f'{f}: occurred, not occurred and unsettled sum to {occurred + absent + unsettled}, not {total}')
        if changed > occurred:
            raise SystemExit(f'{f}: more cases changed ({changed}) than occurred ({occurred})')
        if agree > total:
            raise SystemExit(f'{f}: more agreeing cases ({agree}) than cases ({total})')
        settled = occurred + absent
        row = {'settled': settled, 'unsettled': unsettled,
               'first_codes_agree_percent': round(100 * agree / total, 1)}
        if settled:
            row['occurred_of_settled'] = share(occurred, settled)
            row['changed_conclusion_of_settled'] = share(changed, settled)
        # Every sampled case, with the unsettled ones counted first as none and then as occurrences.
        row['occurred_of_all_range_percent'] = [round(100 * occurred / total, 1), round(100 * (occurred + unsettled) / total, 1)]
        row['changed_of_all_range_percent'] = [round(100 * changed / total, 1), round(100 * (changed + unsettled) / total, 1)]
        out[f] = row
    out['inventory_gap'] = {'count': count(form, 'I1_yes'), 'of': total, 'kinds': form.get('I1_kinds', '')}
    if out['inventory_gap']['count'] > total:
        raise SystemExit('I1_yes: more cases than were sampled')
    return out


if __name__ == '__main__':
    if len(sys.argv) != 2:
        raise SystemExit(__doc__)
    print(json.dumps(summarize(read_form(sys.argv[1])), indent=2))
