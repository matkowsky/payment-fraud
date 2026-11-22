#!/usr/bin/env python3
"""Checks the two transcribed tables against their own totals and prints the ratios the notes use.

Run from paper/working: python3 tools/receiver_report/check_figures.py
"""
import csv
from collections import defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
YEARS = ('y2015', 'y2016', 'y2017', 'y2018')


def income():
    files = defaultdict(dict)
    for r in csv.DictReader(open(HERE / 'EXHIBIT19_INCOME.csv', encoding='utf-8')):
        files[r['file']][r['line']] = {k: float(r[k]) for k in YEARS + ('total',)}
    return files


def check_income(files):
    for name, lines in files.items():
        parts = [v for k, v in lines.items() if k != 'Total']
        for col in YEARS + ('total',):
            assert abs(sum(p[col] for p in parts) - lines['Total'][col]) < 0.015, (name, col)
        for k, v in lines.items():
            assert abs(sum(v[y] for y in YEARS) - v['total']) < 0.015, (name, k)


def fraud_rows():
    return list(csv.DictReader(open(HERE / 'EXHIBIT15_FRAUD_TABLE.csv', encoding='utf-8')))


def check_fraud(rows):
    for r in rows:
        amt = 100 * float(r['fa_amt_vs']) / float(r['trn_amt_vs'])
        cnt = 100 * float(r['fa_cnt_vs']) / float(r['trn_cnt_vs'])
        assert abs(amt - float(r['fa_amt_pct_vs'])) < 0.006, r
        assert abs(cnt - float(r['fa_cnt_pct_vs'])) < 0.006, r


def report():
    files = income()
    check_income(files)
    rows = fraud_rows()
    check_fraud(rows)
    out = []
    gross = both = 0.0
    for name, lines in files.items():
        s = lines['Sales']['total']
        cb = -lines.get('Chargebacks', {'total': 0.0})['total']
        rf = -lines['Refunds']['total']
        gross += s
        both += cb + rf
        if cb:
            out.append(f'{name}: chargebacks {100 * cb / s:.1f}% of sales, refunds {100 * rf / s:.1f}%, both {100 * (cb + rf) / s:.1f}%')
        else:
            out.append(f'{name}: no chargeback line; refunds and chargebacks together {100 * rf / s:.1f}% of sales')
        if cb:
            out.append('  chargebacks by year: ' + ', '.join(
                f"{y[1:]} {100 * -lines['Chargebacks'][y] / lines['Sales'][y]:.1f}%" for y in YEARS))
    uk = [files['5 UK LTD USD'], files['UK LTD']]
    uk_s = sum(f['Sales']['total'] for f in uk)
    uk_b = sum(-f['Chargebacks']['total'] - f['Refunds']['total'] for f in uk)
    uk_cb = sum(-f['Chargebacks']['total'] for f in uk)
    out.append(f'U.K. files, pounds counted as dollars: refunds and chargebacks {uk_b:,.2f} of {uk_s:,.2f} sales, {100 * uk_b / uk_s:.1f}%; chargebacks alone {100 * uk_cb / uk_s:.1f}%')
    out.append(f'All three files: refunds and chargebacks {both:,.2f} of {gross:,.2f} sales, {100 * both / gross:.1f}%')
    net = sum(f['Total']['total'] for f in files.values())
    out.append(f'Net sales, three files: {net:,.2f}')
    for month in sorted({r['month'] for r in rows}):
        m = [r for r in rows if r['month'] == month]
        ta, tc = sum(float(r['trn_amt_vs']) for r in m), sum(int(r['trn_cnt_vs']) for r in m)
        fa, fc = sum(float(r['fa_amt_vs']) for r in m), sum(int(r['fa_cnt_vs']) for r in m)
        out.append(f'{month}, four merchants pooled: fraud {100 * fa / ta:.2f}% by amount, {100 * fc / tc:.2f}% by count; '
                   f'average payment {ta / tc:.2f}, average reported payment {fa / fc:.2f}')
    return out


if __name__ == '__main__':
    print('\n'.join(report()))
