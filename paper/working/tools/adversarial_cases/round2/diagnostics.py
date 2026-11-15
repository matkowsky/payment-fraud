"""Four facts used in RULINGS_CHECK_PACKET.md, from the frozen checker. Changes no rule and no file.

  python3 tools/adversarial_cases/round2/diagnostics.py     (from paper/working)
"""
import copy, json, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent.parent))
import investigation_conformance as ic   # noqa: E402
import outcome_conformance as oc         # noqa: E402

schema = json.loads(ic.SCHEMA.read_text(encoding='utf-8'))
valid = json.loads(ic.VALID.read_text(encoding='utf-8'))['records']
outcomes = json.loads(oc.VALID.read_text(encoding='utf-8'))['records']
cases = {c['case_id']: c for c in json.loads((HERE / 'CASES.json').read_text(encoding='utf-8'))}


def history(case):
    return ic.seal(oc.apply_patch(valid, case))


def hit(found):
    return sorted({f[0] for f in found})


# R05: the fourteen rules pass it; XR-01 rejects it once the outcome records are checked too.
r05 = history(cases['R05'])
assert hit(ic.check(r05, schema)) == [] and hit(ic.check_joint(valid, outcomes)) == []
assert hit(ic.check_joint(r05, outcomes)) == ['XR-01']
# R06: the same note about ACC-1 is rejected by IR-14.
c = copy.deepcopy(cases['R06'])
c['add_records'][0]['entity']['id'] = 'ACC-1'
assert hit(ic.check(history(cases['R06']), schema)) == [] and hit(ic.check(history(c), schema)) == ['IR-14']
# R10: the same claim citing only the unavailable run is rejected by IR-08.
c = copy.deepcopy(cases['R10'])
c['set_fields']['DR-2']['claims'][0]['query_runs'] = ['Q-6']
assert hit(ic.check(history(cases['R10']), schema)) == [] and hit(ic.check(history(c), schema)) == ['IR-08']
# R11: any read of the late item is rejected by IR-13.
r11 = history(cases['R11'])
assert hit(ic.check(r11, schema)) == []
for when in ('2026-08-08T09:05:00Z', '2026-08-08T10:00:00Z', '2026-09-01T00:00:00Z', '2027-01-01T00:00:00Z'):
    read = {'record_type': 'MemoryRead', 'record_id': 'MR-X', 'case_id': 'K-9', 'reader': 'AG-1', 'item_id': 'M-2', 'read_at': when}
    assert hit(ic.check(r11 + [read], schema)) == ['IR-13'], when
print('The four facts hold: R05 (XR-01), R06 (IR-14 for ACC-1), R10 (IR-08 for Q-6 alone), R11 (IR-13 on any read).')
