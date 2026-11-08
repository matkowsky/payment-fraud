#!/usr/bin/env python3
"""Check outcome records against the field-level schema and rules OR-01 to OR-12 (Supplement S4.2).

Usage:
  python3 tools/outcome_conformance.py              run the conformance cases
  python3 tools/outcome_conformance.py FILE.json    check a file of the form {"records": [...]}

Standard library only. The schema validator supports the JSON Schema keywords the schema uses:
$ref, oneOf, const, enum, type, required, properties, additionalProperties, items, minItems,
minLength, pattern, minimum and format date-time. A schema and passing synthetic cases do not
establish operational effectiveness.
"""
import copy
import json
import re
import sys
from datetime import datetime, timedelta
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent / 'SUPPLEMENT' / 'S4_OUTCOME_RECORDS'
SCHEMA = HERE / 'outcome_records.schema.json'
VALID = HERE / 'conformance_valid.json'
INVALID = HERE / 'conformance_invalid.json'
DATE_TIME = re.compile(r'^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}(:\d{2}(\.\d+)?)?(Z|[+-]\d{2}:\d{2})$')
OPEN_STATES = {'open', 'reopened_or_extended'}


def ts(value):
    return datetime.fromisoformat(value.replace('Z', '+00:00'))


def json_type(value):
    if isinstance(value, bool): return 'boolean'
    if isinstance(value, int): return 'integer'
    if isinstance(value, float): return 'number'
    if isinstance(value, str): return 'string'
    if isinstance(value, list): return 'array'
    if isinstance(value, dict): return 'object'
    return 'null'


def validate(inst, schema, root, path='$'):
    """Return schema errors for inst; empty when valid."""
    if '$ref' in schema:
        name = schema['$ref'].split('/')[-1]
        return validate(inst, root['$defs'][name], root, path)
    errors = []
    if 'oneOf' in schema:
        matches = sum(1 for s in schema['oneOf'] if not validate(inst, s, root, path))
        if matches != 1:
            errors.append(f'{path}: matches {matches} alternatives, expected exactly one')
        return errors
    if 'const' in schema and inst != schema['const']:
        return [f'{path}: expected {schema["const"]!r}']
    if 'enum' in schema and inst not in schema['enum']:
        return [f'{path}: {inst!r} not in {schema["enum"]}']
    if 'type' in schema:
        actual = json_type(inst)
        if actual != schema['type'] and not (schema['type'] == 'number' and actual == 'integer'):
            return [f'{path}: expected {schema["type"]}, found {actual}']
    if isinstance(inst, dict):
        for key in schema.get('required', []):
            if key not in inst:
                errors.append(f'{path}: missing {key}')
        props = schema.get('properties', {})
        for key, value in inst.items():
            if key in props:
                errors += validate(value, props[key], root, f'{path}.{key}')
            elif schema.get('additionalProperties') is False:
                errors.append(f'{path}: unexpected field {key}')
    if isinstance(inst, list):
        if len(inst) < schema.get('minItems', 0):
            errors.append(f'{path}: fewer than {schema["minItems"]} items')
        if 'items' in schema:
            for i, value in enumerate(inst):
                errors += validate(value, schema['items'], root, f'{path}[{i}]')
    if isinstance(inst, str):
        if len(inst) < schema.get('minLength', 0):
            errors.append(f'{path}: empty')
        if 'pattern' in schema and not re.search(schema['pattern'], inst):
            errors.append(f'{path}: does not match {schema["pattern"]}')
        if schema.get('format') == 'date-time':
            try:
                assert DATE_TIME.match(inst); ts(inst)
            except Exception:
                errors.append(f'{path}: not an RFC 3339 date-time')
    if isinstance(inst, int) and not isinstance(inst, bool) and inst < schema.get('minimum', inst):
        errors.append(f'{path}: below minimum')
    return errors


def bounds(estimate):
    """(earliest, latest) of a time estimate, or (None, None) when unknown."""
    if estimate['status'] == 'exact':
        t = ts(estimate['value']); return t, t
    if estimate['status'] == 'interval':
        return ts(estimate['earliest']), ts(estimate['latest'])
    return None, None


def key(item):
    return (item['item_type'], item['item_id'])


def check(records, schema):
    """Return a sorted list of (rule, record_id, message) findings."""
    findings = []
    add = lambda rule, rid, msg: findings.append((rule, rid, msg))
    for r in records:
        for e in validate(r, schema, schema):
            add('SCHEMA', r.get('record_id', '?'), e)
    if findings:
        return sorted(findings)

    by_type = {}
    for r in records:
        by_type.setdefault(r['record_type'], []).append(r)
    seen = {}
    for r in records:  # OR-01 records are never edited in place
        if r['record_id'] in seen:
            add('OR-01', r['record_id'], 'record identifier used twice; a change must be a new record')
        seen[r['record_id']] = r
    channels = {c['channel_id']: c for c in by_type.get('OutcomeChannel', [])}
    decisions = {d['decision_id']: d for d in by_type.get('ControlAction', [])}
    labels = by_type.get('LabelEvent', [])
    reports = {}
    for le in labels:
        reports.setdefault(le['report_id'], []).append(le)
    learned = lambda r: ts(r['learned_at']) if 'learned_at' in r else ts(r['read_time'])

    for r in records:  # OR-02 corrections and revisions point back to an earlier record
        ref = r.get('corrects') or r.get('revision_of')
        if r['record_type'] == 'LabelEvent' and (r['revision_kind'] == 'initial') == ('revision_of' in r):
            add('OR-02', r['record_id'], 'an initial report has no revision_of; every revision has one')
        if ref:
            prior = seen.get(ref)
            if (prior is None or prior['record_type'] != r['record_type'] or learned(prior) >= learned(r)
                    or (r['record_type'] == 'LabelEvent' and prior.get('report_id') != r['report_id'])):
                add('OR-02', r['record_id'], f'{ref} is not an earlier record of the same type and report')

    for r in records:  # OR-03 references resolve
        if 'channel_id' in r and r['record_type'] != 'OutcomeChannel' and r['channel_id'] not in channels:
            add('OR-03', r['record_id'], f'unknown channel {r["channel_id"]}')
        for eff in r.get('channel_effects', []):
            if eff['channel_id'] not in channels:
                add('OR-03', r['record_id'], f'unknown channel {eff["channel_id"]}')
        cause = r.get('cause') or r.get('read_under_change') or {}
        if cause.get('kind') == 'decision' and cause['decision_id'] not in decisions:
            add('OR-03', r['record_id'], f'unknown decision {cause["decision_id"]}')
        if r['record_type'] == 'LabelEventDecisionLink':
            if r['decision_id'] not in decisions:
                add('OR-03', r['record_id'], f'unknown decision {r["decision_id"]}')
            if r['report_id'] not in reports:
                add('OR-03', r['record_id'], f'unknown report {r["report_id"]}')

    for le in labels:  # OR-04 occurred <= reported <= arrived <= learned, where known
        occ_lo, _ = bounds(le['occurred_at'])
        rep_lo, rep_hi = bounds(le['reported_at'])
        arr, lrn = ts(le['arrived_at']), ts(le['learned_at'])
        if (occ_lo and rep_hi and occ_lo > rep_hi) or (rep_lo and rep_lo > arr) or arr > lrn:
            add('OR-04', le['record_id'], 'report times out of order')
        if le['status'] in ('won', 'lost') and le['adjudicated'] == 'not_applicable':  # OR-05
            add('OR-05', le['record_id'], 'a won or lost status must state whether it followed adjudication')

    for d in decisions.values():  # OR-06 channel effects are complete
        chans = [e['channel_id'] for e in d['channel_effects']]
        if len(chans) != len(set(chans)):
            add('OR-06', d['record_id'], 'a channel appears more than once')
        for e in d['channel_effects']:
            if e['effect'] == 'delayed' and 'expected_clock_start' not in e:
                add('OR-06', d['record_id'], 'a delayed effect needs expected_clock_start')
            if e['effect'] == 'changed_meaning' and 'meaning_change' not in e:
                add('OR-06', d['record_id'], 'a changed-meaning effect needs meaning_change')

    transitions = by_type.get('ChannelStateTransition', [])
    for t in transitions:  # OR-07 the cause matches the state
        c = t['cause']
        if 'effective_to' in t and ts(t['effective_to']) <= ts(t['effective_from']):
            add('OR-07', t['record_id'], 'effective interval ends before it starts')
        if t['state'] == 'closed' and c['kind'] != 'decision':
            add('OR-07', t['record_id'], 'a permanent closure must cite the decision that caused it')
        if t['state'] == 'reopened_or_extended' and c['kind'] != 'rule_event':
            add('OR-07', t['record_id'], 'a reopening or extension must cite the rule event that caused it')
        if c['kind'] == 'decision' and c['decision_id'] in decisions:
            d = decisions[c['decision_id']]
            effect = {e['channel_id']: e['effect'] for e in d['channel_effects']}.get(t['channel_id'])
            need = {'closed': 'closed', 'delayed_or_not_opened': 'delayed'}.get(t['state'])
            if key(t['item']) not in {key(x) for x in d['targets']}:
                add('OR-07', t['record_id'], 'the item is not a target of the cited decision')
            if need and effect != need:
                add('OR-07', t['record_id'], f'cited decision records effect {effect!r} on this channel')
            if ts(t['effective_from']) < ts(d['decided_at']):
                add('OR-07', t['record_id'], 'transition takes effect before the decision')

    corrected = {r['corrects'] for r in records if 'corrects' in r}
    live = [t for t in transitions if t['record_id'] not in corrected]
    for le in labels:  # OR-08 no report through a channel a decision closed for that item
        for t in live:
            if (t['state'] == 'closed' and key(t['item']) == key(le['item'])
                    and t['channel_id'] == le['channel_id']):
                add('OR-08', le['record_id'], f'channel closed for this item by {t["cause"]["decision_id"]}; '
                    'correct the item link or the closure')

    pairs = set()
    for k in by_type.get('LabelEventDecisionLink', []):  # OR-09 link roles are consistent
        if (k['report_id'], k['decision_id']) in pairs:
            add('OR-09', k['record_id'], 'duplicate link for the same report and decision')
        pairs.add((k['report_id'], k['decision_id']))
        d, rep = decisions.get(k['decision_id']), reports.get(k['report_id'])
        if not d or not rep:
            continue
        item = key(rep[0]['item'])
        targets = {key(x) for x in d['targets']}
        if k['role'] == 'decision_on_reported_item' and item not in targets:
            add('OR-09', k['record_id'], 'the reported item is not a target of the decision')
        if k['role'] == 'decision_on_earlier_related_attempt' and (
                item in targets or not any(x['item_type'] == 'payment_attempt' for x in d['targets'])):
            add('OR-09', k['record_id'], 'the decision must concern a different payment attempt')
        if k['role'] == 'decision_on_containing_entity' and not any(
                x['item_type'] in ('account', 'payout') for x in d['targets']):
            add('OR-09', k['record_id'], 'the decision must concern an account or payout')
        if k['role'] == 'other' and 'role_note' not in k:
            add('OR-09', k['record_id'], 'role other needs role_note')

    def known_transitions(item, channel, at):
        return [t for t in live if key(t['item']) == item and t['channel_id'] == channel and ts(t['learned_at']) <= at]

    def state_at(ts_list, when):
        active = [t for t in ts_list if ts(t['effective_from']) <= when
                  and ('effective_to' not in t or when < ts(t['effective_to']))]
        return max(active, key=lambda t: ts(t['effective_from']))['state'] if active else 'unknown'

    for rd in by_type.get('ChannelStatusReading', []):
        at, item, ch = ts(rd['read_time']), key(rd['item']), rd['channel_id']
        known = known_transitions(item, ch, at)
        if rd['channel_state'] != state_at(known, at):  # OR-10 as-of reading
            add('OR-10', rd['record_id'], f'state as of read time is {state_at(known, at)!r}')
        arrived = any(key(le['item']) == item and le['channel_id'] == ch and ts(le['learned_at']) <= at
                      for le in labels)
        presence = rd['report_presence']  # OR-11 report presence and query access
        if presence == 'unavailable' and rd['query_access'] not in ('denied', 'unavailable'):
            add('OR-11', rd['record_id'], 'unavailable presence requires denied or unavailable access')
        if presence != 'unavailable' and (presence == 'present') != arrived:
            add('OR-11', rd['record_id'], 'presence does not match reports learned by read time')
        channel = channels.get(ch)  # OR-12 no-report status
        if channel is None:
            continue
        window = channel['reporting_window']
        cs_lo, cs_hi = bounds(rd['clock_start'])
        if presence == 'present':
            expected = 'not_applicable'
        elif presence == 'unavailable' or rd['query_access'] != 'full' and rd['channel_state'] != 'closed':
            expected = {'pending', 'unknown'}
        elif rd['channel_state'] == 'closed':
            expected = 'channel_closed'
        elif window['status'] == 'none_defined':
            expected = 'no_defined_window'
        elif window['status'] == 'unknown' or cs_lo is None or cs_lo != cs_hi:
            expected = 'unknown'
        else:
            end = cs_lo + timedelta(days=window['days'])
            for t in known:
                if t['state'] == 'reopened_or_extended' and 'effective_to' in t:
                    end = max(end, ts(t['effective_to']))
            if at < end:
                expected = 'pending'
            else:
                covering = [t for t in known if ts(t['effective_from']) < end
                            and ('effective_to' not in t or ts(t['effective_to']) > cs_lo)]
                starts = any(ts(t['effective_from']) <= cs_lo and t['state'] in OPEN_STATES for t in covering)
                open_all = starts and all(t['state'] in OPEN_STATES for t in covering)
                expected = 'matured_absent' if open_all else 'unknown'
                if open_all and rd.get('matured_under_rule_version') != window['rule_version']:
                    add('OR-12', rd['record_id'], 'a matured absence records the rule version it matured under')
        ok = rd['no_report_status'] in expected if isinstance(expected, set) else rd['no_report_status'] == expected
        if not ok:
            add('OR-12', rd['record_id'], f'no-report status should be {expected!r}')
        changed = {d['decision_id'] for d in decisions.values() if item in {key(x) for x in d['targets']}
                   and ts(d['decided_at']) <= at and any(e['channel_id'] == ch and e['effect'] == 'changed_meaning'
                                                         for e in d['channel_effects'])}
        if rd['no_report_status'] == 'matured_absent' and changed and \
                rd.get('read_under_change', {}).get('decision_id') not in changed:
            add('OR-12', rd['record_id'], 'a matured absence on a channel whose meaning a decision changed cites it')
        if rd['no_report_status'] != 'matured_absent' and 'matured_under_rule_version' in rd:
            add('OR-12', rd['record_id'], 'only a matured absence records a maturity rule version')
    return sorted(set(findings))


def apply_patch(records, case):
    out = copy.deepcopy(records)
    by_id = {r['record_id']: r for r in out}
    for rid, fields in case.get('remove_fields', {}).items():
        for f in fields:
            by_id[rid].pop(f)
    for rid, fields in case.get('set_fields', {}).items():
        by_id[rid].update(copy.deepcopy(fields))
    out = [r for r in out if r['record_id'] not in set(case.get('remove_records', []))]
    return out + copy.deepcopy(case.get('add_records', []))


def run_conformance():
    schema = json.loads(SCHEMA.read_text(encoding='utf-8'))
    valid = json.loads(VALID.read_text(encoding='utf-8'))['records']
    cases = json.loads(INVALID.read_text(encoding='utf-8'))['cases']
    base = check(valid, schema)
    assert not base, ('valid case fails', base)
    rules = set()
    for case in cases:
        got = {f[0] for f in check(apply_patch(valid, case), schema)}
        assert got == {case['rule']}, (case['case_id'], case['rule'], sorted(got))
        rules.add(case['rule'])
    expected_rules = {'SCHEMA'} | {f'OR-{n:02d}' for n in range(1, 13)}
    assert rules == expected_rules, ('rules without a failing case', sorted(expected_rules - rules))
    return {'valid_records': len(valid), 'invalid_cases': len(cases), 'rules_exercised': len(rules)}


if __name__ == '__main__':
    if len(sys.argv) > 1:
        schema = json.loads(SCHEMA.read_text(encoding='utf-8'))
        found = check(json.loads(Path(sys.argv[1]).read_text(encoding='utf-8'))['records'], schema)
        for f in found:
            print(*f, sep='\t')
        sys.exit(1 if found else 0)
    print(json.dumps(run_conformance()))
