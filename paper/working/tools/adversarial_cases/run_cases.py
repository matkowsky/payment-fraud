"""Run an outside tester's adversarial cases against the query-run and release rules.

  python3 tools/adversarial_cases/run_cases.py CASES.json [RESULTS.md]
  python3 tools/adversarial_cases/run_cases.py --sealed CASES.json [RESULTS.md]
  python3 tools/adversarial_cases/run_cases.py --sealed --joint CASES.json [RESULTS.md]     round 3

With --sealed, a draft whose claims a case changed is first given its new digest, and a release that
named the old digest is updated to match. That models a draft written that way and then released.
Without it, a changed draft keeps its old version identifier, which models a draft altered after
release. Since the rules began to recompute the digest, every altered draft fails IR-11 as written,
so the sealed run is the one that shows what else the rules catch.

CASES.json is the tester's JSON array (code fences are stripped). Each case patches the valid history;
the patched history is checked against the schema and rules IR-01 to IR-14. The table says, for each
case, what the tester expected and what the checker did. A case the tester expected to be rejected
that passes, or expected to pass that is rejected, is marked for adjudication: a person decides
whether the tester or the rules are right. This script decides nothing.

Rounds 1 and 2 were written before a claim held its sentence (claim_text), before an absence claim named its
sources and before a claim that lists outcome items said how it uses them (outcome_use). To rerun those
histories under the present rules, upgrade() gives each claim that lacks them a placeholder sentence, the
sources of every run it cites, and the negative reading. The saved cases are not changed. If such a claim
lists outcome items, XR-01 is run against the valid outcome records, which the round 2 command did not do.

With --joint (round 3), the history a case patches is the joint case: the valid investigation records, the
four records of the later case K-3, and the valid outcome records. A case may patch either store, under the
keys "investigation" and "outcome", and every history is checked against all 29 rules. Nothing is upgraded.
"""
import json, re, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
import outcome_conformance as oc                              # noqa: E402
from investigation_conformance import SCHEMA, VALID, check, check_both, check_joint, joint_history, seal   # noqa: E402
from outcome_conformance import apply_patch                   # noqa: E402

PATCH_KEYS = ('set_fields', 'remove_fields', 'remove_records', 'add_records')
LEGACY_TEXT = 'Not recorded: this history was written before a claim held its sentence.'


def upgrade(records):
    """Give claims written before three fields existed the values described above. Returns the same list."""
    by = {r.get('record_id'): r for r in records}
    for r in records:
        for c in r.get('claims', []) if r.get('record_type') == 'DraftOutput' else []:
            c.setdefault('claim_text', LEGACY_TEXT)
            if c.get('claim_type') == 'absence' and 'sources' not in c:
                c['sources'] = sorted({s['source_id'] for q in c.get('query_runs', [])
                                       if by.get(q, {}).get('record_type') == 'QueryRun' for s in by[q]['sources']})
            if c.get('outcome_items') and 'outcome_use' not in c:
                c['outcome_use'] = 'negative'
    return records


def findings(case, sealed=True, joint=False):
    """Apply one case and return the checker's findings. Raises if the patch cannot be applied."""
    schema = json.loads(SCHEMA.read_text(encoding='utf-8'))
    if joint:
        records, outcomes, _ = joint_history()
        inv = case.get('investigation', {k: case[k] for k in PATCH_KEYS if k in case})
        records = apply_patch(records, inv)
        outcomes = apply_patch(outcomes, case.get('outcome', {}))
        return check_both(seal(records) if sealed else records, outcomes, schema, json.loads(oc.SCHEMA.read_text(encoding='utf-8')))
    valid = json.loads(VALID.read_text(encoding='utf-8'))['records']
    records = upgrade(apply_patch(valid, case))
    found = check(seal(records) if sealed else records, schema)
    if any(c.get('outcome_items') for r in records if r.get('record_type') == 'DraftOutput' for c in r.get('claims', [])):
        found = found + check_joint(records, json.loads(oc.VALID.read_text(encoding='utf-8'))['records'])
    return found


def load_cases(path):
    text = Path(path).read_text(encoding='utf-8')
    m = re.search(r'\[.*\]', text, re.S)
    if not m: sys.exit('No JSON array found')
    return json.loads(m.group(0))


def touched_types(case, base_types):
    kinds = set()
    for key in ('set_fields', 'remove_fields'):
        kinds |= {base_types.get(rid, 'unknown record') for rid in case.get(key, {})}
    kinds |= {base_types.get(rid, 'unknown record') for rid in case.get('remove_records', [])}
    kinds |= {r.get('record_type', 'untyped record') for r in case.get('add_records', [])}
    return kinds


def rules_hit(case, sealed=True, joint=False):
    """The set of checks a case fails: empty if it passes, {'MALFORMED'} if the patch cannot be applied."""
    try:
        return {f[0] for f in findings(case, sealed, joint)}
    except (KeyError, TypeError, ValueError, AttributeError):
        return {'MALFORMED'}


def main():
    args = [a for a in sys.argv[1:] if a not in ('--sealed', '--joint')]
    sealed = '--sealed' in sys.argv[1:]
    joint = '--joint' in sys.argv[1:]
    sys.argv = [sys.argv[0]] + args
    cases = load_cases(sys.argv[1])
    schema = json.loads(SCHEMA.read_text(encoding='utf-8'))
    valid = json.loads(VALID.read_text(encoding='utf-8'))['records']
    assert not check(valid, schema), 'the valid history must pass'
    base_types = {r['record_id']: r['record_type'] for r in (joint_history()[0] if joint else valid)}
    rows, tally = [], {}
    for c in cases:
        cid, expect = c.get('case_id', '?'), c.get('expect', '?')
        inv = c.get('investigation', c) if joint else c
        kinds = touched_types(inv, base_types) | ({'outcome record'} if joint and c.get('outcome') else set())
        tier = 'agent' if kinds <= {'DraftOutput'} else 'other'
        if not any(inv.get(k) for k in PATCH_KEYS) and not (joint and c.get('outcome')):
            result, detail = 'malformed', 'the case changes nothing'
        else:
            try:
                found = findings(c, sealed, joint)
            except (KeyError, TypeError, ValueError, AttributeError) as e:
                found, result, detail = None, 'malformed', f'patch or record could not be applied: {type(e).__name__} {e}'
            if found is not None:
                rules = sorted({f[0] for f in found})
                if not found:
                    result, detail = 'passes', ''
                elif rules == ['SCHEMA']:
                    result, detail = 'rejected by the schema', '; '.join(sorted({f[2] for f in found}))[:160]
                else:
                    result, detail = 'rejected by ' + ', '.join(rules), '; '.join(sorted({f[2] for f in found}))[:160]
        if result == 'malformed':
            outcome = 'not a test: malformed'
        elif expect == 'reject':
            if result == 'passes':
                outcome = 'ADJUDICATE: passes, tester says it breaks ' + str(c.get('breaks'))
            else:
                outcome = 'caught by the schema' if result == 'rejected by the schema' else 'caught by a rule'
        elif expect == 'accept':
            outcome = 'accepted, as the tester expected' if result == 'passes' else 'ADJUDICATE: rejected, tester says it is legitimate'
        else:
            outcome = 'not a test: no expectation given'
        key = outcome.split(':')[0]
        tally[key] = tally.get(key, 0) + 1
        note = '' if c.get('tier') == tier else f" (tester said {c.get('tier')})"
        rows.append(f"| {cid} | {tier}{note} | {expect} | {result} | {outcome} | {str(c.get('why', '')).replace('|', '/')} | {detail.replace('|', '/')} |")
    out = [('Sealed run. ' if sealed else '') + f'Cases: {len(cases)}. ' + '; '.join(f'{k}: {v}' for k, v in sorted(tally.items())) + '.', '',
           '| Case | Tier | Tester expects | Checker | Outcome | Tester\'s reason | Checker detail |', '|---|---|---|---|---|---|---|', *rows, '']
    text = '\n'.join(out)
    if len(sys.argv) > 2: Path(sys.argv[2]).write_text(text, encoding='utf-8')
    print(text)


if __name__ == '__main__':
    main()
