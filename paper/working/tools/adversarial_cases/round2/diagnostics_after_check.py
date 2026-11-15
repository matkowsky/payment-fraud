"""Two facts used in ADJUDICATION.md, found after the outside check, from the frozen checker. Changes no rule and no file.

  python3 tools/adversarial_cases/round2/diagnostics_after_check.py     (from paper/working)
"""
import copy, json, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent.parent))
import investigation_conformance as ic   # noqa: E402
import outcome_conformance as oc         # noqa: E402

schema = json.loads(ic.SCHEMA.read_text(encoding='utf-8'))
valid = json.loads(ic.VALID.read_text(encoding='utf-8'))['records']
cases = {c['case_id']: c for c in json.loads((HERE / 'CASES.json').read_text(encoding='utf-8'))}


def hit(case):
    return sorted({f[0] for f in ic.check(ic.seal(oc.apply_patch(valid, case)), schema)})


# R09: the claim passes when it names ACC-1 and ACC-2, and is rejected by IR-09 when it names only ACC-2.
only = copy.deepcopy(cases['R09'])
only['set_fields']['DR-2']['claims'][0]['entities'] = [{'tenant': 'T1', 'namespace': 'account', 'id': 'ACC-2'}]
assert hit(cases['R09']) == [] and hit(only) == ['IR-09']
# R12: the same counter-record defeats the absence claim under IR-08 once a later cited run returns it.
later = copy.deepcopy(cases['R12'])
run = copy.deepcopy(next(r for r in valid if r['record_id'] == 'Q-2'))
run.update(record_id='Q-7', case_id='K-2', issued_at='2026-05-20T10:40:00Z', as_of='2026-05-20T10:00:00Z', returned=['O-9'])
for source in run['sources']:
    source['event_watermark'] = source['ingestion_watermark'] = '2026-05-20T00:00:00Z'
later['add_records'].append(run)
later['set_fields']['DR-2']['claims'][0]['query_runs'] = ['Q-2', 'Q-7']
assert hit(cases['R12']) == [] and hit(later) == ['IR-08']
print('The two facts hold: R09 (IR-09 when only ACC-2 is named), R12 (IR-08 when a later cited run returns O-9).')
