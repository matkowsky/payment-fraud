#!/usr/bin/env python3
"""Check two intervals for E9's reduction in reference error on the worked example of Supplement S7.1.

Usage:
  python3 tools/e9_interval_check.py                 the recorded run, results to stdout
  python3 tools/e9_interval_check.py --out FILE.json  also write the results
  python3 tools/e9_interval_check.py --replications N --resamples B --attempts n --seed S

The model is the worked example. Each completed flagged attempt falls, independently, in one of four classes:
  early    a fraud chargeback by the read time                          0.24
  late     window open at the read time, a fraud chargeback afterwards  lam
  never    window open at the read time, no fraud chargeback            0.20 - lam
  closed   window closed at the read time, no fraud chargeback          0.56
The pass comparator reads every attempt without a chargeback as a negative: q0 = early / n.
C1 leaves late and never unlabeled, and the plan excludes them: q1 = early / (n - late - never).
The reference is read after every window has closed: r = (early + late) / n.
D = |q0 - r| - |q1 - r|. At lam = 0.06 the reference equals q1 (D = 0.06). At lam = 0.03, D = 0.

Two intervals are checked, both from the same paired bootstrap that resamples attempts.
  percentile  the 2.5th and 97.5th percentiles of the resampled D.
  parts       D = max(min(L, W), -W) with L = 2r - q0 - q1 and W = q1 - q0, both smooth. Each part gets the
              1.25th and 98.75th percentiles of its own resampled values, and the interval for D is the range
              of D over that box. The two parts together hold with at least 95 percent confidence.

No truth review, clustering or strata are modelled. Standard library only. Every random draw comes from
random.Random(seed).random(), so a run repeats exactly.
"""
import argparse
import json
import math
import random
import sys

EARLY, UNLABELED, CLOSED = 0.24, 0.20, 0.56
CONDITIONS = (('reference_equals_c1', 0.06), ('d_is_zero', 0.03))
RECORDED = {'attempts': 1000, 'replications': 10000, 'resamples': 999, 'seed': 20261113}
REDUCED = {'attempts': 1000, 'replications': 100, 'resamples': 199, 'seed': 20261113}


def binomial(rng, n, p):
    """One binomial draw by inversion outward from the mode, using one uniform number."""
    if n <= 0 or p <= 0.0:
        return 0
    if p >= 1.0:
        return n
    q = 1.0 - p
    m = min(n, int((n + 1) * p))
    pm = math.exp(math.lgamma(n + 1) - math.lgamma(m + 1) - math.lgamma(n - m + 1) + m * math.log(p) + (n - m) * math.log(q))
    u = rng.random() - pm
    if u <= 0.0:
        return m
    ratio = p / q
    lo = hi = m
    plo = phi = pm
    while lo > 0 or hi < n:
        if hi < n:
            hi += 1
            phi *= (n - hi + 1) / hi * ratio
            u -= phi
            if u <= 0.0:
                return hi
        if lo > 0:
            plo *= lo / (n - lo + 1) / ratio
            lo -= 1
            u -= plo
            if u <= 0.0:
                return lo
    return m  # rounding left a sliver of probability unassigned


def draw(rng, n, p_early, p_late, p_never):
    """Counts of early, late and never among n attempts; the rest are closed."""
    early = binomial(rng, n, p_early)
    rest = n - early
    left = 1.0 - p_early
    late = binomial(rng, rest, p_late / left) if rest and left > 0.0 else 0
    rest -= late
    left -= p_late
    never = binomial(rng, rest, min(1.0, p_never / left)) if rest and left > 0.0 else 0
    return early, late, never


def parts(n, early, late, never):
    """L and W for one set of counts. D = clamp(L, -W, W)."""
    q0 = early / n
    q1 = early / (n - late - never)
    r = (early + late) / n
    return 2 * r - q0 - q1, q1 - q0


def clamp(length, width):
    return max(min(length, width), -width)


def truth(lam):
    q0, q1, r = EARLY, EARLY / (1.0 - UNLABELED), EARLY + lam
    return {'q0': q0, 'q1': q1, 'r': r, 'D': abs(q0 - r) - abs(q1 - r)}


def box(l_lo, l_hi, w_lo, w_hi):
    """Range of clamp(L, -W, W) over a box. W is never negative in this model."""
    low = min(l_lo, w_lo) if l_lo >= 0 else max(l_lo, -w_hi)
    high = min(l_hi, w_hi) if l_hi >= 0 else max(l_hi, -w_lo)
    return low, high


def run_condition(lam, attempts, replications, resamples, seed):
    rng = random.Random(seed)
    target = truth(lam)['D']
    tally = {m: {'covered': 0, 'lower_above_truth': 0, 'upper_below_truth': 0} for m in ('percentile', 'parts')}
    bias = 0.0
    rank95, rank_part = max(1, int(0.025 * (resamples + 1))), max(1, int(0.0125 * (resamples + 1)))
    lo95, hi95 = rank95 - 1, resamples - rank95          # the rank95-th smallest and rank95-th largest
    lo_part, hi_part = rank_part - 1, resamples - rank_part
    eps = 1e-12
    for _ in range(replications):
        early, late, never = draw(rng, attempts, EARLY, lam, UNLABELED - lam)
        bias += clamp(*parts(attempts, early, late, never)) - target
        pe, pl, pn = early / attempts, late / attempts, never / attempts
        ds, ls, ws = [], [], []
        for _ in range(resamples):
            length, width = parts(attempts, *draw(rng, attempts, pe, pl, pn))
            ls.append(length)
            ws.append(width)
            ds.append(clamp(length, width))
        ds.sort()
        ls.sort()
        ws.sort()
        intervals = {'percentile': (ds[lo95], ds[hi95]), 'parts': box(ls[lo_part], ls[hi_part], ws[lo_part], ws[hi_part])}
        for method, (low, high) in intervals.items():
            if low > target + eps:
                tally[method]['lower_above_truth'] += 1
            elif high < target - eps:
                tally[method]['upper_below_truth'] += 1
            else:
                tally[method]['covered'] += 1
    return {'lam': lam, 'truth': {key: round(value, 6) for key, value in truth(lam).items()},
            'mean_estimate_minus_truth': round(bias / replications, 6), 'intervals': tally}


def run(attempts, replications, resamples, seed):
    return {'settings': {'attempts': attempts, 'replications': replications, 'resamples': resamples, 'seed': seed},
            'conditions': {name: run_condition(lam, attempts, replications, resamples, seed + index)
                           for index, (name, lam) in enumerate(CONDITIONS)}}


def self_check():
    """The sampler against the exact binomial distribution, and the identity D = clamp(L, -W, W)."""
    rng = random.Random(1)
    n, p, draws = 12, 0.3, 40000
    counts = [0] * (n + 1)
    for _ in range(draws):
        counts[binomial(rng, n, p)] += 1
    for k in range(n + 1):
        exact = math.comb(n, k) * p ** k * (1 - p) ** (n - k)
        assert abs(counts[k] / draws - exact) < 4 * math.sqrt(exact * (1 - exact) / draws) + 1e-4, (k, counts[k] / draws, exact)
    assert binomial(rng, 0, 0.5) == 0 and binomial(rng, 7, 0.0) == 0 and binomial(rng, 7, 1.0) == 7
    for early, late, never in ((240, 40, 160), (240, 5, 195), (240, 0, 200), (240, 200, 0), (100, 150, 50)):
        q0, q1, r = early / 1000, early / (1000 - late - never), (early + late) / 1000
        assert abs(clamp(*parts(1000, early, late, never)) - (abs(q0 - r) - abs(q1 - r))) < 1e-12
    assert abs(truth(0.06)['D'] - 0.06) < 1e-12 and abs(truth(0.06)['q1'] - truth(0.06)['r']) < 1e-12 and abs(truth(0.03)['D']) < 1e-12
    assert box(0.01, 0.05, 0.02, 0.04) == (0.01, 0.04) and box(-0.03, 0.05, 0.02, 0.04) == (-0.03, 0.04) and box(-0.09, -0.01, 0.02, 0.04) == (-0.04, -0.01)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    parser.add_argument('--attempts', type=int, default=RECORDED['attempts'])
    parser.add_argument('--replications', type=int, default=RECORDED['replications'])
    parser.add_argument('--resamples', type=int, default=RECORDED['resamples'])
    parser.add_argument('--seed', type=int, default=RECORDED['seed'])
    parser.add_argument('--out')
    args = parser.parse_args(argv)
    self_check()
    result = {'recorded': run(args.attempts, args.replications, args.resamples, args.seed), 'reduced': run(**REDUCED)}
    text = json.dumps(result, indent=1) + '\n'
    if args.out:
        with open(args.out, 'w', encoding='utf-8') as handle:
            handle.write(text)
    sys.stdout.write(text)


if __name__ == '__main__':
    main()
