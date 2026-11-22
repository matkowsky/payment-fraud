"""Facts from the frozen checker about four round 3 cases. They are observations, not rulings.

  python3 tools/adversarial_cases/round3/diagnostics.py     (from paper/working)

Each line says what the checker does with a history. The rulings packet quotes these lines.
"""
import copy, json, sys, traceback
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1]))
sys.path.insert(0, str(HERE.parent))
import outcome_conformance as oc                                                    # noqa: E402
from investigation_conformance import SCHEMA, check, check_both, joint_history, seal   # noqa: E402
from outcome_conformance import apply_patch                                           # noqa: E402

schema = json.loads(SCHEMA.read_text(encoding='utf-8'))
outcome_schema = json.loads(oc.SCHEMA.read_text(encoding='utf-8'))
cases = {c['case_id']: c for c in json.loads((HERE / 'CASES.json').read_text(encoding='utf-8'))}


def history(case):
    records, outcomes, _ = joint_history()
    return seal(apply_patch(records, case.get('investigation', {}))), apply_patch(outcomes, case.get('outcome', {}))


def rules(found):
    return sorted({f[0] for f in found}) or 'nothing'


# R14: the plan's command reported an error. What do the fourteen rules alone say, and where does the error arise?
records, outcomes = history(cases['R14'])
print('R14, rules IR-01 to IR-14 alone:', rules(check(records, schema)))
try:
    check_both(records, outcomes, schema, outcome_schema)
    print('R14, all 29 rules: no error')
except KeyError as e:
    frames = [f.name for f in traceback.extract_tb(sys.exc_info()[2])]
    assert 'check_joint' in frames, frames   # check_joint is the code for XR-01
    print(f'R14, all 29 rules: the checker raises KeyError {e} in check_joint, the code for XR-01, before it reports anything')

# R05: the claim is marked as a status and its sentence is changed. Does any rule read the sentence?
records, outcomes = history(cases['R05'])
print('R05, as written:', rules(check_both(records, outcomes, schema, outcome_schema)))
other = copy.deepcopy(cases['R05'])
other['investigation']['set_fields']['DR-3']['claims'][0]['claim_text'] = 'Any other sentence.'
records, outcomes = history(other)
print('R05, with any other sentence:', rules(check_both(records, outcomes, schema, outcome_schema)))

# R02 and R13: which rules reject them.
for cid in ('R02', 'R13'):
    records, outcomes = history(cases[cid])
    print(f'{cid}:', rules(check_both(records, outcomes, schema, outcome_schema)))
# R13 with the claim's entity restored and only the outcome item changed, and the reverse.
for label, entity, item in (('entity PA-3, outcome item PA-4', 'PA-3', 'PA-4'), ('entity PA-4, outcome item PA-3', 'PA-4', 'PA-3')):
    c = copy.deepcopy(cases['R13']); claim = c['investigation']['set_fields']['DR-3']['claims'][0]
    claim['entities'][0]['id'] = entity; claim['outcome_items'][0]['id'] = item
    records, outcomes = history(c)
    print(f'R13 with {label}:', rules(check_both(records, outcomes, schema, outcome_schema)))
