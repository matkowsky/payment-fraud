"""Run an outside tester's adversarial cases against the query-run and release rules.

  python3 tools/adversarial_cases/run_cases.py CASES.json [RESULTS.md]
  python3 tools/adversarial_cases/run_cases.py --sealed CASES.json [RESULTS.md]

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
"""
import json, re, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from investigation_conformance import SCHEMA, VALID, check, seal   # noqa: E402
from outcome_conformance import apply_patch                   # noqa: E402

PATCH_KEYS = ('set_fields', 'remove_fields', 'remove_records', 'add_records')


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


def rules_hit(case, sealed=True):
    """The set of checks a case fails: empty if it passes, {'MALFORMED'} if the patch cannot be applied."""
    schema = json.loads(SCHEMA.read_text(encoding='utf-8'))
    valid = json.loads(VALID.read_text(encoding='utf-8'))['records']
    try:
        records = apply_patch(valid, case)
        return {f[0] for f in check(seal(records) if sealed else records, schema)}
    except (KeyError, TypeError, ValueError, AttributeError):
        return {'MALFORMED'}


def main():
    args = [a for a in sys.argv[1:] if a != '--sealed']
    sealed = '--sealed' in sys.argv[1:]
    sys.argv = [sys.argv[0]] + args
    cases = load_cases(sys.argv[1])
    schema = json.loads(SCHEMA.read_text(encoding='utf-8'))
    valid = json.loads(VALID.read_text(encoding='utf-8'))['records']
    assert not check(valid, schema), 'the valid history must pass'
    base_types = {r['record_id']: r['record_type'] for r in valid}
    rows, tally = [], {}
    for c in cases:
        cid, expect = c.get('case_id', '?'), c.get('expect', '?')
        kinds = touched_types(c, base_types)
        tier = 'agent' if kinds <= {'DraftOutput'} else 'other'
        if not any(c.get(k) for k in PATCH_KEYS):
            result, detail = 'malformed', 'the case changes nothing'
        else:
            try:
                found = check(seal(apply_patch(valid, c)) if sealed else apply_patch(valid, c), schema)
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
