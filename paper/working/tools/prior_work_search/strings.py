"""Search strings for the prior-work database search. Standard library only.

  python3 tools/prior_work_search/strings.py          rewrite STRINGS.md and strings.json
  python3 tools/prior_work_search/strings.py --check  fail if either file is out of date

Every string comes from the term blocks below, so the databases are asked the same questions.
The blocks are fixed before the first run. A change after that is a new commit with its reason.
"""
import json, re, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
OR = ' OR '

PAY = ['fraud*', 'chargeback*', 'payment*', '"financial crime*"', '"money laundering"', '"transaction monitoring"']
LAB = ['"selective label*"', '"reject inference"', '"delayed feedback"', '"delayed label*"', '"label delay*"',
       '"verification latency"', '"censored label*"', '"censored feedback"', '"counterfactual evaluation"',
       '"off-policy evaluation"', '"bandit feedback"', '"sample selection bias"', '"label noise"', '"noisy label*"',
       '"friendly fraud"']
PAY2 = ['fraud*', 'chargeback*', 'dispute*', 'payment*']
REC = ['"decision log*"', '"decision record*"', '"decision provenance"', '"decision trace*"', '"audit trail*"',
       '"outcome record*"', '"label store"', '"feedback loop*"']
OUT = ['label*', 'outcome*', '"ground truth"', 'feedback']
AG = ['"language model*"', 'LLM*', '"AI agent*"', 'agentic', '"autonomous agent*"']
AGS = ['"AI agent*"', '"LLM agent*"', '"LLM-based agent*"', '"language agent*"', 'agentic', '"autonomous agent*"']
INV = ['investigat*', 'forensic*', '"incident response"', '"threat hunting"', '"security operations"',
       '"threat intelligence"', 'audit*', 'fraud*']
COV = ['"query completeness"', '"result completeness"', '"partial result*"', '"incomplete result*"',
       '"absence of evidence"', '"negative evidence"', '"data coverage"', '"search coverage"', 'bitemporal',
       '"valid time"', '"transaction time"', '"point-in-time"', '"temporal leakage"', '"data freshness"',
       '"execution trace*"', '"audit log*"', '"run record*"', '"provenance record*"']
MEM = ['memory', '"knowledge base*"']
GOV = ['"human-in-the-loop"', '"human approval"', '"human oversight"', '"human review"', 'provenance',
       '"memory poisoning"', '"belief revision"', '"truth maintenance"', '"circular reporting"',
       '"source independence"', '"write gate*"', 'governance']
FIN = ['fraud*', 'chargeback*', '"financial crime*"', '"money laundering"', 'payment*', '"threat intelligence"']
WRK = ['investigat*', 'triage', '"case management"', 'analyst*']
EVD = ['evidence', 'provenance', 'audit*', 'accountab*', 'oversight', 'governance', '"human-in-the-loop"']
TI = ['"threat intelligence"', '"intelligence analysis"', '"fraud intelligence"', '"intelligence product*"']
COR = ['"circular reporting"', '"source independence"', 'corroborat*', '"belief revision"', '"analytic standard*"',
       '"information provenance"', '"source reliability"']

# question id: (what it covers, term blocks joined by AND, first publication year or None)
QUESTIONS = {
    'Q1': ('C1: outcome labels shaped by decisions, in payments and fraud', [PAY, LAB], None),
    'Q2': ('C1: records that link outcomes to decisions', [PAY2, REC, OUT], None),
    'Q3': ('C2: query coverage and learned time in agent investigations', [AG, INV, COV], 2022),
    'Q4': ('C3: governed memory and reuse for agents', [AGS, MEM, GOV], 2022),
    'Q5': ('Setting: agents investigating fraud, financial crime or threats, with evidence controls', [AG, FIN, WRK, EVD], 2022),
    'Q6': ('C3: reused intelligence and independent corroboration, without agents', [TI, COR], None),
}

# IEEE Xplore: no wildcards and at most 25 words in a clause (a phrase counts each word).
IEEE = {
    'Q1': [['fraud', 'chargeback', 'payment'],
           ['"selective labels"', '"reject inference"', '"delayed feedback"', '"delayed labels"', '"verification latency"',
            '"censored feedback"', '"counterfactual evaluation"', '"off-policy evaluation"', '"bandit feedback"',
            '"label noise"', '"friendly fraud"']],
    'Q2': [['fraud', 'chargeback', 'dispute', 'payment'],
           ['"decision log"', '"decision record"', '"decision provenance"', '"decision trace"', '"audit trail"',
            '"outcome record"', '"feedback loop"'],
           ['label', 'outcome', '"ground truth"', 'feedback']],
    'Q3': [['"language model"', 'LLM', '"AI agent"', 'agentic', '"autonomous agent"'],
           ['investigation', 'forensic', '"incident response"', '"threat hunting"', '"security operations"',
            '"threat intelligence"', 'audit', 'fraud'],
           ['"query completeness"', '"partial results"', '"incomplete results"', '"absence of evidence"',
            '"negative evidence"', '"data coverage"', 'bitemporal', '"valid time"', '"point-in-time"',
            '"execution trace"', '"audit log"']],
    'Q4': [['"AI agent"', '"LLM agent"', '"language agent"', 'agentic', '"autonomous agent"'],
           ['memory', '"knowledge base"'],
           ['"human-in-the-loop"', '"human approval"', '"human oversight"', '"human review"', 'provenance',
            '"memory poisoning"', '"belief revision"', '"truth maintenance"', '"circular reporting"', 'governance']],
    'Q5': [['"language model"', 'LLM', '"AI agent"', 'agentic', '"autonomous agent"'],
           ['fraud', 'chargeback', '"financial crime"', '"money laundering"', 'payment', '"threat intelligence"'],
           ['investigation', 'triage', '"case management"', 'analyst'],
           ['evidence', 'provenance', 'audit', 'accountability', 'oversight', 'governance', '"human-in-the-loop"']],
}

# Forward-citation searches in Scopus: anchor paper, DOI, terms to search within the citing documents.
ANCHORS = [
    ('CB1', 'Lakkaraju et al. 2017, The Selective Labels Problem', '10.1145/3097983.3098066',
     'fraud* OR payment* OR chargeback* OR credit'),
    ('CB2', 'Dal Pozzolo et al. 2018, Credit Card Fraud Detection: A Realistic Modeling and a Novel Learning Strategy',
     '10.1109/TNNLS.2017.2736643', 'delay* OR latency OR "selection bias" OR counterfactual OR censor*'),
    ('CB3', 'Chapelle 2014, Modeling Delayed Feedback in Display Advertising', '10.1145/2623330.2623634',
     'fraud* OR payment* OR chargeback*'),
    ('CB4', 'Ehrhardt et al. 2021, Reject Inference Methods in Credit Scoring', '10.1080/02664763.2021.1929090',
     '(none: export every citing document)'),
    ('CB5', 'Razniewski and Nutt 2011, Completeness of Queries over Incomplete Databases', '10.14778/3402707.3402715',
     'agent* OR investigat* OR audit* OR provenance OR "language model*"'),
    ('CB6', 'Singh et al. 2019, Decision Provenance: Harnessing Data Flow for Accountable Systems',
     '10.1109/ACCESS.2018.2887201', 'agent* OR "language model*" OR fraud* OR payment*'),
    ('CB7', 'Sakellariou et al. 2022, A Reference Model for Cyber Threat Intelligence (CTI) Systems',
     '10.3390/electronics11091401', '(none: export every citing document)'),
    ('CB8', 'Zhao et al. 2024, ExpeL: LLM Agents Are Experiential Learners', '10.1609/aaai.v38i17.29936',
     'provenance OR governance OR poisoning OR "human-in-the-loop" OR audit*'),
]


def scopus(blocks, year):
    s = ' AND '.join('TITLE-ABS-KEY ( ' + OR.join(b) + ' )' for b in blocks)
    return s + (f' AND PUBYEAR > {year - 1}' if year else '')


def wos(blocks, year):
    s = ' AND '.join('TS=(' + OR.join(b) + ')' for b in blocks)
    return s + (f' AND PY=({year}-2026)' if year else '')


def _both_numbers(term):
    # ACM: a phrase takes no wildcard, so give its singular and plural.
    if term.startswith('"') and '*' in term:
        base = term.strip('"').replace('*', '')
        return [f'"{base}"', f'"{base}s"']
    return [term]


def acm(blocks):
    return ' AND '.join('Abstract:(' + OR.join(x for t in b for x in _both_numbers(t)) + ')' for b in blocks)


def ieee(blocks):
    return ' AND '.join('(' + OR.join('"All Metadata":' + t for t in b) + ')' for b in blocks)


def _words(clause):
    return sum(len(re.findall(r'[A-Za-z0-9]+', t)) for t in clause)


def runs():
    out = []
    for q, (topic, blocks, year) in QUESTIONS.items():
        out.append({'run': q + '-SC', 'question': q, 'database': 'Scopus', 'string': scopus(blocks, year),
                    'year_limit': 'In the string' if year else 'None'})
        out.append({'run': q + '-WS', 'question': q, 'database': 'Web of Science', 'string': wos(blocks, year),
                    'year_limit': 'In the string' if year else 'None'})
        if q in IEEE:
            out.append({'run': q + '-IE', 'question': q, 'database': 'IEEE Xplore', 'string': ieee(IEEE[q]),
                        'year_limit': f'Set {year} to 2026 in the year filter' if year else 'None'})
            out.append({'run': q + '-AC', 'question': q, 'database': 'ACM Digital Library', 'string': acm(blocks),
                        'year_limit': f'Set {year} to 2026 in Publication Date' if year else 'None'})
    return out


def build():
    for q, clauses in IEEE.items():
        for c in clauses:
            assert _words(c) <= 25 and not any('*' in t for t in c), (q, c)
    data = {'questions': {q: {'covers': v[0], 'from_year': v[2]} for q, v in QUESTIONS.items()},
            'runs': runs(),
            'cited_by': [{'run': a[0], 'anchor': a[1], 'doi': a[2], 'search_within': a[3]} for a in ANCHORS]}
    md = ['# Search strings', '', 'Generated by `strings.py`. Do not edit by hand.', '']
    for q, (topic, _, year) in QUESTIONS.items():
        md += [f'## {q}. {topic}', '', f'From year: {year}.' if year else 'No year limit.', '']
        for r in data['runs']:
            if r['question'] == q:
                md += [f"**{r['run']}, {r['database']}.** Year limit: {r['year_limit']}.", '', '```', r['string'], '```', '']
    md += ['## Cited by', '', 'In Scopus: open the anchor by its DOI, open its citing documents and search within them.', '']
    for a in ANCHORS:
        md += [f'**{a[0]}. {a[1]}.** DOI {a[2]}.', '', '```', a[3], '```', '']
    return json.dumps(data, indent=1, ensure_ascii=False) + '\n', '\n'.join(md)


if __name__ == '__main__':
    js, md = build()
    targets = {HERE / 'strings.json': js, HERE / 'STRINGS.md': md}
    if '--check' in sys.argv[1:]:
        stale = [p.name for p, text in targets.items() if not p.is_file() or p.read_text(encoding='utf-8') != text]
        sys.exit(f'out of date: {stale}' if stale else 0)
    for p, text in targets.items():
        p.write_text(text, encoding='utf-8')
    d = json.loads(js)
    print(f"{len(d['runs'])} database strings, {len(d['cited_by'])} cited-by anchors")
