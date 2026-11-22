#!/usr/bin/env python3
"""Check query-run and release records against their schema and rules IR-01 to IR-14 (Supplement S4.4),
and claims against outcome records under XR-01.

Usage:
  python3 tools/investigation_conformance.py                       run the conformance cases and necessity pairs
  python3 tools/investigation_conformance.py FILE.json [OUT.json]  check a file of the form {"records": [...]},
                                                                   with XR-01 if outcome records are given

Standard library only; the schema validator is the one in outcome_conformance.py. A schema and
passing synthetic cases do not establish operational effectiveness.
"""
import copy
import hashlib
import json
import re
from datetime import datetime
import sys
from datetime import timedelta
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import outcome_conformance as oc  # noqa: E402
from outcome_conformance import apply_patch, ts, validate  # noqa: E402

HERE = Path(__file__).resolve().parent.parent / 'SUPPLEMENT' / 'S4_INVESTIGATION_RECORDS'
SCHEMA = HERE / 'investigation_records.schema.json'
VALID = HERE / 'conformance_valid.json'
INVALID = HERE / 'conformance_invalid.json'
ACCEPT = HERE / 'conformance_accept.json'
JOINT = HERE / 'joint_case.json'
# Every reference one record makes to another, and the record types its target may have (the reference table of Supplement S4.4).
REFERENCES = {
    ('QueryRun', 'requested_by'): {'Actor'}, ('QueryRun', 'recorded_by'): {'Actor'}, ('QueryRun', 'returned'): {'Observation'},
    ('Observation', 'producer'): {'Actor'}, ('Observation', 'inputs'): {'Observation'}, ('Observation', 'root_ids'): {'Observation'},
    ('Observation', 'agent_output_links'): {'DraftOutput'}, ('DraftOutput', 'agent'): {'Actor'},
    ('claim', 'supporting'): {'Observation'}, ('claim', 'contradicting'): {'Observation'}, ('claim', 'query_runs'): {'QueryRun'},
    ('claim', 'context'): {'Observation', 'ReleasedItem'},
    ('OutputExposure', 'output_id'): {'DraftOutput'}, ('OutputExposure', 'viewer'): {'Actor'},
    ('ReleaseDecision', 'draft_id'): {'DraftOutput'}, ('ReleaseDecision', 'decided_by'): {'Actor'},
    ('ReleasedItem', 'release_id'): {'ReleaseDecision'}, ('ReleasedItem', 'draft_id'): {'DraftOutput'},
    ('MemoryRead', 'reader'): {'Actor'}, ('MemoryRead', 'item_id'): {'ReleasedItem'},
}
# The references whose target must be, or must not be, one kind of actor.
ACTOR_KINDS = {('QueryRun', 'requested_by'): ('not', 'gateway'), ('QueryRun', 'recorded_by'): ('is', 'gateway'),
               ('DraftOutput', 'agent'): ('is', 'agent'), ('OutputExposure', 'viewer'): ('is', 'human'),
               ('ReleaseDecision', 'decided_by'): ('is', 'human')}
C1_TYPES = ('ControlAction', 'ChannelStateTransition', 'ChannelStatusReading')
OBSERVED = {'source_observation', 'normalized_observation', 'derived_feature'}
RANK = {'low': 0, 'moderate': 1, 'high': 2}
COVERAGE_FIELDS = ('evaluated_entities', 'evaluated_interval', 'sources', 'access_filter_removed_rows',
                   'limits_reached', 'scope_limited', 'statuses', 'as_of')
DEPENDENCE_FIELDS = ('root_ids', 'inputs', 'agent_output_links', 'producer')


def ent(e):
    return (e['tenant'], e['namespace'], e['id'])


def within(inner, outer):
    return ts(outer['from']) <= ts(inner['from']) and ts(inner['to']) <= ts(outer['to'])


def overlaps(a, b):
    return ts(a['from']) <= ts(b['to']) and ts(b['from']) <= ts(a['to'])


def exact_instant(value):
    """Equality key for validated aware timestamps; retain all fractional digits.

    This does not replace the datetime ordering used by other rules.
    """
    match = re.search(r'\.(\d+)', value)
    fraction = match.group(1).rstrip('0') if match else ''
    whole = value[:match.start()] + value[match.end():] if match else value
    parsed = datetime.fromisoformat(whole.replace('Z', '+00:00'))
    offset = parsed.utcoffset()
    if offset is None:
        raise ValueError('timestamp must include a UTC offset')
    seconds = ((parsed.toordinal() - 719163) * 86400
               + parsed.hour * 3600 + parsed.minute * 60 + parsed.second
               - (offset.days * 86400 + offset.seconds))
    return seconds, fraction


def same_interval(left, right):
    return all(exact_instant(left[end]) == exact_instant(right[end]) for end in ('from', 'to'))


def derive_statuses(run):
    """The fixed rules of Section 6.2: statuses follow from the coverage fields alone."""
    out = set()
    req = run['requested_interval']
    if {ent(e) for e in run['evaluated_entities']} != {ent(e) for e in run['requested_entities']} \
            or not same_interval(run['evaluated_interval'], req) or run['access_filter_removed_rows']:
        out.add('partial')
    for s in run['sources']:
        if s['access'] == 'denied':
            out.add('denied')
        elif s['access'] == 'unavailable':
            out.add('unavailable')
        elif (ts(req['to']) > ts(s['event_watermark']) or ts(req['to']) > ts(s['ingestion_watermark'])
              or ts(req['from']) < ts(s['retention_horizon']) or s['sampled']
              or any(overlaps(g, req) for g in s['known_gaps'])):
            out.add('partial')
    if run['limits_reached']:
        out.add('truncated')
    return sorted(out) or ['complete']


def supports_absence(runs, claim):
    """Cited runs support an absence claim if the claim names its sources and, for each named entity in each named
    source, the runs that are complete, not scope-limited and empty and that evaluated that entity in that source
    cover the claim's interval between them."""
    if not claim.get('sources'):
        return False
    start, end = ts(claim['interval']['from']), ts(claim['interval']['to'])
    for e in claim['entities']:
        for s in claim['sources']:
            spans = sorted((ts(q['evaluated_interval']['from']), ts(q['evaluated_interval']['to'])) for q in runs
                           if q['statuses'] == ['complete'] and not q['scope_limited'] and not q['returned']
                           and ent(e) in {ent(v) for v in q['evaluated_entities']}
                           and s in {x['source_id'] for x in q['sources']})
            reach = None
            for a, b in spans:
                if a > (start if reach is None else reach):
                    break
                reach = b if reach is None else max(reach, b)
            if reach is None or reach < end:
                return False
    return True


def claims_digest(claims):
    """A draft's version identifier: the first 16 hex digits of SHA-256 over its claims in canonical JSON."""
    text = json.dumps(claims, sort_keys=True, separators=(',', ':'), ensure_ascii=False)
    return hashlib.sha256(text.encode('utf-8')).hexdigest()[:16]


def seal(records):
    """Give each draft whose claims changed its new digest, and carry it to a release that named the old one.

    Used where a history is built on purpose with changed claims: the in-house invalid cases, so that a case
    meant to break one rule breaks only that rule, and the generated copies in investigation_cost.py.
    """
    for r in records:
        if r.get('record_type') != 'DraftOutput' or 'claims' not in r or 'version_hash' not in r:
            continue
        new = claims_digest(r['claims'])
        if new == r['version_hash']:
            continue
        for x in records:
            if x.get('record_type') == 'ReleaseDecision' and x.get('draft_id') == r['record_id'] \
                    and x.get('version_hash') == r['version_hash']:
                x['version_hash'] = new
        r['version_hash'] = new
    return records


def distinct_roots(ids, by):
    return {r for i in ids if i in by and by[i]['record_type'] == 'Observation' for r in by[i]['root_ids']}


def check(records, schema):
    """Return findings as (rule, record_id, message)."""
    found = []
    seen = set()
    for r in records:
        for e in validate(r, schema, schema):
            found.append(('SCHEMA', r.get('record_id', '?'), e))
        if r.get('record_id') in seen:
            found.append(('IR-01', r['record_id'], 'identifier used more than once'))
        seen.add(r.get('record_id'))
    if found:
        return found
    by = {r['record_id']: r for r in records}
    kind = {r['record_id']: r['kind'] for r in records if r['record_type'] == 'Actor'}

    def agent_made(o):   # C3: what an agent produced is a record of what the agent did, not evidence of the activity
        return kind.get(o.get('producer')) == 'agent'

    def plain(o):   # names a producer that is not an agent, and carries no link to an agent output
        return 'producer' in o and not agent_made(o) and not o['agent_output_links']

    def refs(r):
        t = r['record_type']
        if t == 'QueryRun':
            return [r['requested_by'], r['recorded_by']] + r['returned']
        if t == 'Observation':
            return r['inputs'] + r['agent_output_links'] + r['root_ids'] + ([r['producer']] if 'producer' in r else [])
        if t == 'DraftOutput':
            out = [r['agent']]
            for c in r['claims']:
                out += c['supporting'] + c['contradicting'] + c['query_runs'] + c['context']
            return out
        if t == 'OutputExposure':
            return [r['output_id'], r['viewer']]
        if t == 'ReleaseDecision':
            return [r['draft_id'], r['decided_by']]
        if t == 'ReleasedItem':
            return [r['release_id'], r['draft_id']]
        if t == 'MemoryRead':
            return [r['reader'], r['item_id']]
        return []

    for r in records:
        for x in refs(r):
            if x not in by:
                found.append(('IR-02', r['record_id'], f'cites {x}, which does not exist'))
        for c in r.get('claims', []) if r['record_type'] == 'DraftOutput' else []:
            for q in c['query_runs']:
                if q in by and by[q]['record_type'] != 'QueryRun':
                    found.append(('IR-02', r['record_id'], f'cites {q} as a query run'))
        if r['record_type'] == 'Observation' and r.get('producer') in by and by[r['producer']]['record_type'] != 'Actor':
            found.append(('IR-02', r['record_id'], f'names {r["producer"]} as its producer'))
        # A reference whose target can be of one type only, or one kind of actor only, is checked here.
        t, rid = r['record_type'], r['record_id']
        if t == 'Observation':
            for x in r['agent_output_links']:
                if x in by and by[x]['record_type'] != 'DraftOutput':
                    found.append(('IR-02', rid, f'links to {x} as an agent output'))
        if t == 'DraftOutput' and r['agent'] in by and kind.get(r['agent']) != 'agent':
            found.append(('IR-02', rid, f'names {r["agent"]} as the agent that wrote it'))
        if t == 'OutputExposure':
            if r['output_id'] in by and by[r['output_id']]['record_type'] != 'DraftOutput':
                found.append(('IR-02', rid, f'names {r["output_id"]} as the agent output that was open'))
            if r['viewer'] in by and kind.get(r['viewer']) != 'human':
                found.append(('IR-02', rid, f'names {r["viewer"]} as the person who had the output open'))
        for f in {'QueryRun': ('requested_by', 'recorded_by'), 'MemoryRead': ('reader',)}.get(t, ()):
            if r[f] in by and r[f] not in kind:
                found.append(('IR-02', rid, f'names {r[f]} as an actor'))
    if found:
        return found

    for r in records:
        t, rid = r['record_type'], r['record_id']
        if t == 'QueryRun':
            if kind.get(r['recorded_by']) != 'gateway' or kind.get(r['requested_by']) == 'gateway':
                found.append(('IR-03', rid, 'coverage must be recorded by a gateway that is not the requester'))
            if not ({ent(e) for e in r['evaluated_entities']} <= {ent(e) for e in r['requested_entities']}
                    and within(r['evaluated_interval'], r['requested_interval']) and ts(r['as_of']) <= ts(r['issued_at'])):
                found.append(('IR-04', rid, 'evaluated scope exceeds the request, or the cutoff is after the query'))
            elif r['statuses'] != derive_statuses(r):
                found.append(('IR-05', rid, f'statuses {r["statuses"]} do not follow from coverage: {derive_statuses(r)}'))
            for x in r['returned']:
                o = by[x]
                if o['record_type'] != 'Observation' or ts(o['learned_at']) > ts(r['as_of']) \
                        or not overlaps(o['event_interval'], r['evaluated_interval']) \
                        or ent(o['entity']) not in {ent(e) for e in r['evaluated_entities']}:
                    found.append(('IR-06', rid, f'{x} was not learned by the cutoff, lies outside the evaluated interval '
                                                'or concerns an entity the run did not evaluate'))
        if t == 'Observation':
            ins = [by[i] for i in r['inputs']]
            if any(i['record_type'] != 'Observation' for i in ins):
                found.append(('IR-07', rid, 'an input is not an observation record'))
                continue
            if r['record_class'] == 'source_observation':
                roots_ok = r['root_ids'] == [rid] and not ins
            elif ins:
                roots_ok = set(r['root_ids']) == {x for i in ins for x in i['root_ids']}
            else:
                roots_ok = r['root_ids'] == [rid] and r['record_class'] in ('score', 'control_decision')
            if not roots_ok or any(ts(r['learned_at']) < ts(i['learned_at']) for i in ins):
                found.append(('IR-07', rid, 'roots or learned time do not follow from the inputs'))
            elif r['record_class'] == 'source_observation' and ts(r['learned_at']) < ts(r['event_interval']['from']):
                found.append(('IR-07', rid, 'a source observation cannot be learned before its event began'))
            owed = {x for i in ins for x in i['agent_output_links']}
            for x in records:   # whatever entity the record concerns (manuscript Section 4.2: the writer's session)
                if x['record_type'] == 'OutputExposure' and x['viewer'] == r.get('producer') \
                        and ts(x['opened_at']) <= ts(r['learned_at']) <= ts(x['closed_at']):
                    owed.add(x['output_id'])
            if not owed <= set(r['agent_output_links']):
                found.append(('IR-14', rid, f'missing link to agent output {sorted(owed - set(r["agent_output_links"]))}'))
            elif any(ts(by[x]['created_at']) > ts(r['learned_at']) for x in r['agent_output_links']):
                found.append(('IR-14', rid, 'a linked agent output was written after the record was learned'))
        if t == 'OutputExposure':
            if ts(r['opened_at']) < ts(by[r['output_id']]['created_at']) or ts(r['closed_at']) < ts(r['opened_at']):
                found.append(('IR-14', rid, 'an agent output is open only after it was written, and closes after it opens'))
        if t == 'DraftOutput':
            if r['version_hash'] != claims_digest(r['claims']):
                found.append(('IR-11', rid, "the draft's version identifier is not the digest of its claims"))
            for c in r['claims']:
                cid = f'{rid}/{c["claim_id"]}'
                named = {ent(e) for e in c['entities']}
                runs = [by[q] for q in c['query_runs']]

                def counter(x):   # an observation of a named entity inside the claim's interval
                    o = by[x]
                    return o['record_type'] == 'Observation' and ent(o['entity']) in named \
                        and overlaps(o['event_interval'], c['interval'])
                # A cited run over none of the claim's sources does not bear on it, for or against.
                bearing = [q for q in runs if set(c.get('sources', [])) & {s['source_id'] for s in q['sources']}]
                if c['claim_type'] == 'absence' and (
                        not supports_absence(runs, c) or any(counter(x) for q in bearing for x in q['returned'])
                        or any(counter(x) for x in c['supporting'] + c['contradicting'])):
                    found.append(('IR-08', cid, 'an absence claim names its sources and needs complete, empty runs that cover it '
                                                'in each, with no matching record returned by such a run or listed by the claim'))

                def existed(x):   # when a cited record came to exist
                    o = by[x]
                    return ts(o.get('learned_at') or o.get('issued_at') or o.get('created_at') or r['created_at'])
                sup = [by[x] for x in c['supporting']]
                # A record is dependent if it is linked to an agent output, names no producer, or, unless it is a
                # source observation, names no inputs: it may be cited, but it adds no root. The restriction runs
                # through the inputs, so a derived record adds only the roots reachable through records that are
                # not dependent.
                def countable(o, seen=()):
                    if o['record_type'] != 'Observation' or not plain(o) or o['record_id'] in seen:
                        return set()
                    if o['record_class'] == 'source_observation':
                        return set(o['root_ids'])
                    return set().union(*(countable(by[i], seen + (o['record_id'],)) for i in o['inputs'] if i in by))
                free = [o for o in sup if countable(o)]
                cited = c['supporting'] + c['contradicting'] + c['context'] + c['query_runs']
                if any(o['record_type'] != 'Observation' or ent(o['entity']) not in named for o in sup) \
                        or any(by[x]['record_type'] != 'Observation' for x in c['contradicting']) \
                        or any(by[x]['record_type'] not in ('Observation', 'ReleasedItem') for x in c['context']) \
                        or any(existed(x) > ts(r['created_at']) for x in cited) \
                        or c['distinct_roots'] != len(set().union(*(countable(o) for o in sup))) \
                        or (c['material'] and c['claim_type'] != 'absence' and not all(
                            any(ent(o['entity']) == e and overlaps(o['event_interval'], c['interval']) for o in free)
                            for e in named)):
                    found.append(('IR-09', cid, 'support and contradiction must be observations, support of the named entities; context an '
                                                'observation or a released item; all known by the draft; roots counted once among records that '
                                                'are not dependent, with one such record in the claim interval for each entity of a material claim'))
                elif c['claim_type'] == 'current_conduct':
                    def current(o):   # an observation of a named entity, within the current period
                        return o['record_class'] in OBSERVED and within(o['event_interval'], r['current_period']) \
                            and ent(o['entity']) in named
                    ok = False
                    for s in (by[x] for x in c['supporting']):
                        if not current(s):
                            continue
                        # A record that is linked to an agent output, was produced by an agent or names no producer
                        # counts only if its inputs hold, for each named entity, a current-period observation of that
                        # entity that is none of these (manuscript Section 6.4).
                        if not plain(s) and not all(any(
                                current(by[i]) and plain(by[i]) and ent(by[i]['entity']) == e
                                for i in s['inputs'] if i in by) for e in named):
                            continue
                        ok = True
                    if not ok:
                        found.append(('IR-10', cid, 'no current-period observation of a named entity is cited'))
                for x in c['context']:
                    if by[x]['record_type'] != 'ReleasedItem':
                        continue
                    release = by.get(by[x].get('release_id'), {})
                    if not any(m['record_type'] == 'MemoryRead' and m['item_id'] == x and m['case_id'] == r['case_id']
                               and ts(m['read_at']) <= ts(r['created_at']) for m in records) \
                            or ts(r['created_at']) >= ts(release.get('expires_at', r['created_at'])):
                        found.append(('IR-13', cid, f'cites released item {x} with no read of it in this case by the time of the draft, '
                                                    'or after its release expired'))
        if t == 'ReleaseDecision':
            d = by[r['draft_id']]
            claims = {c['claim_id']: c for c in d.get('claims', [])}
            if (d['record_type'] != 'DraftOutput' or kind.get(r['decided_by']) != 'human' or r['version_hash'] != d['version_hash']
                    or not ts(d['created_at']) <= ts(r['decided_at']) <= ts(d['expires_at'])
                    or any(c['claim_id'] not in claims or RANK[c['confidence']] > RANK[claims[c['claim_id']]['confidence']]
                           for c in r['claims'])):
                found.append(('IR-11', rid, 'release must be by a person, of the exact unexpired version, without raising confidence'))
        if t == 'ReleasedItem':
            rel = by[r['release_id']]
            if (rel['record_type'] != 'ReleaseDecision' or rel['decision'] != 'released' or rel['draft_id'] != r['draft_id']
                    or r['claim_id'] not in {c['claim_id'] for c in rel['claims']} or ts(r['created_at']) < ts(rel['decided_at'])):
                found.append(('IR-12', rid, 'a memory item needs a release decision that released its claim first'))
        if t == 'MemoryRead':
            item = by[r['item_id']]
            rel = by.get(item.get('release_id'), {})
            if item['record_type'] != 'ReleasedItem' or not (
                    ts(item['created_at']) <= ts(r['read_at']) < ts(rel.get('expires_at', item['created_at']))):
                found.append(('IR-13', rid, 'memory may be read only from a released, unexpired item'))
    return found


def check_joint(records, outcomes):
    """XR-01: a claim that states or relies on items' outcomes not being reported lists the items, says which of the
    two it does, and cites for each item a channel reading taken by the time of the draft. Every cited reading of a
    listed item was made with full access and shows that no report had arrived. Where the claim reads the absence as
    a negative, every cited reading also shows a matured absence, and a cited complete run evaluated the item from
    its clock start through the end of its reporting window and returned nothing about it."""
    found = []
    by = {r['record_id']: r for r in records}
    out = {r['record_id']: r for r in outcomes}
    windows = {(r['channel_id'], r['reporting_window'].get('rule_version')): r['reporting_window']
               for r in outcomes if r['record_type'] == 'OutcomeChannel'}
    for d in records:
        for c in d['claims'] if d['record_type'] == 'DraftOutput' else []:
            cid = f'{d["record_id"]}/{c["claim_id"]}'
            if not c.get('outcome_items'):
                if c.get('outcome_readings') or 'outcome_use' in c:
                    found.append(('XR-01', cid, 'cites readings or names a use but lists no outcome item'))
                continue
            if c.get('outcome_use') not in ('status', 'negative'):
                found.append(('XR-01', cid, 'does not say whether it states that no report arrived or reads that as a negative'))
                continue
            readings = [out.get(x) for x in c.get('outcome_readings', [])]
            if any(x is None or x['record_type'] != 'ChannelStatusReading' or ts(x['read_time']) > ts(d['created_at'])
                   for x in readings):
                found.append(('XR-01', cid, 'a cited reading does not exist or was taken after the draft'))
                continue
            runs = [by[q] for q in c['query_runs'] if by.get(q, {}).get('record_type') == 'QueryRun']
            for e in c['outcome_items']:
                mine = [x for x in readings if (x['item']['item_type'], x['item']['item_id']) == (e['namespace'], e['id'])]
                if not mine or any(x['report_presence'] != 'none_arrived' or x['query_access'] != 'full' for x in mine):
                    found.append(('XR-01', cid, f'{e["id"]}: no cited reading, or one that does not show with full access that no report arrived'))
                    continue
                if c['outcome_use'] == 'status':   # the statement is true whatever the channel's state; no negative is read
                    continue
                if any(x['no_report_status'] != 'matured_absent' for x in mine):
                    found.append(('XR-01', cid, f'{e["id"]}: a cited reading is not a matured absence'))
                    continue
                for x in mine:
                    w = windows.get((x['channel_id'], x.get('matured_under_rule_version')), {})
                    start = ts(x['clock_start']['value'])
                    end = start + timedelta(days=w.get('days', 0))
                    if not any(q['statuses'] == ['complete'] and not q['scope_limited']
                               and ent(e) in {ent(v) for v in q['evaluated_entities']}
                               and ts(q['evaluated_interval']['from']) <= start <= end <= ts(q['evaluated_interval']['to'])
                               and not any(ent(by[i]['entity']) == ent(e) for i in q['returned'] if i in by)
                               for q in runs):
                        found.append(('XR-01', cid, f'{e["id"]}: no cited complete run covers its reporting window'))
    return found


def check_both(records, outcomes, schema, outcome_schema):
    """Each store's own rules, then XR-01 across them."""
    return check(records, schema) + oc.check(outcomes, outcome_schema) + check_joint(records, outcomes)


def joint_history():
    """The joint case: the valid investigation records plus case K-3, and the valid outcome records."""
    joint = json.loads(JOINT.read_text(encoding='utf-8'))
    records = json.loads(VALID.read_text(encoding='utf-8'))['records'] + joint['records']
    outcomes = json.loads(oc.VALID.read_text(encoding='utf-8'))['records']
    return records, outcomes, joint['cases']


def strip(records, fields):
    return [{k: v for k, v in r.items() if k not in fields} for r in records]


def necessity_pairs(valid, schema):
    """For each requirement, two histories that differ in what may be concluded but are identical without its fields."""
    by = {r['record_id']: r for r in valid}
    out = {}
    # C2 coverage: the same empty result, once complete and once reaching past the source's event watermark.
    a = copy.deepcopy(by['Q-2'])
    b = copy.deepcopy(a)
    b['sources'][0]['event_watermark'] = '2026-04-15T00:00:00Z'
    b['statuses'] = derive_statuses(b)
    claim = next(c for c in by['DR-1']['claims'] if c['claim_type'] == 'absence')
    assert strip([a], COVERAGE_FIELDS) == strip([b], COVERAGE_FIELDS) and a['returned'] == b['returned'] == []
    assert supports_absence([a], claim) and not supports_absence([b], claim)
    out['C2 coverage'] = 'absence supported in one history only'
    # C2 learned time: the same observation, learned before the cutoff in one history and after it in the other.
    run = by['Q-1']
    early = copy.deepcopy(by['O-2'])
    late = dict(copy.deepcopy(early), learned_at='2026-05-09T00:00:00Z')
    assert strip([early], ('learned_at',)) == strip([late], ('learned_at',))
    assert ts(early['learned_at']) <= ts(run['as_of']) < ts(late['learned_at'])
    out['C2 learned time'] = 'known at the cutoff in one history only'
    # C3 dependence: a second supporting record derived from a different observation, or derived from the first.
    base = dict(copy.deepcopy(by['O-3']), record_id='N-1', learned_at='2026-05-05T00:00:00Z')
    indep = dict(copy.deepcopy(base), inputs=['O-2'], root_ids=['O-2'])
    echo = dict(copy.deepcopy(base), inputs=['O-1'], root_ids=['O-1'], agent_output_links=[])
    assert strip([indep], DEPENDENCE_FIELDS) == strip([echo], DEPENDENCE_FIELDS)
    assert not check(valid + [indep], schema) and not check(valid + [echo], schema)
    roots_a = len(distinct_roots(['O-1', 'N-1'], dict(by, **{'N-1': indep})))
    roots_b = len(distinct_roots(['O-1', 'N-1'], dict(by, **{'N-1': echo})))
    assert (roots_a, roots_b) == (2, 1)
    out['C3 dependence'] = 'two root observations in one history, one in the other'
    # C3 release: the same stored conclusion, released by a person in one history and never released in the other.
    item = next(r for r in valid if r['record_type'] == 'ReleasedItem')
    orphan = dict(copy.deepcopy(item), release_id='RL-NONE')
    without = [orphan if r is item else r for r in valid if r['record_id'] != item['release_id']]
    assert not check(valid, schema)
    assert {f[0] for f in check(without, schema)} == {'IR-02'}

    def hide_release_evidence(history):
        remaining = [r.copy() for r in history if r['record_id'] != item['release_id']]
        stored = next(r for r in remaining if r['record_id'] == item['record_id'])
        del stored['release_id']
        return remaining

    assert hide_release_evidence(valid) == hide_release_evidence(without)
    out['C3 release'] = 'reuse permitted in one history only'
    return out


def joint_pairs(records, outcomes, schema, outcome_schema):
    """Two requirements hold in both histories of a pair; only the third tells them apart."""
    out = {}
    blocked = next(c for c in joint_history()[2] if c['case_id'] == 'J01')
    # C1 with C2 and C3 holding: a complete, empty run and a release, over an attempt that matured or was blocked.
    b_out = apply_patch(outcomes, blocked['outcome'])
    keep = [r for r in outcomes if r['record_type'] not in C1_TYPES]
    assert keep == [r for r in b_out if r['record_type'] not in C1_TYPES]
    assert not check(records, schema) and not oc.check(outcomes, outcome_schema) and not oc.check(b_out, outcome_schema)
    assert not check_joint(records, outcomes) and {f[0] for f in check_joint(records, b_out)} == {'XR-01'}
    out['C1 with C2 and C3'] = 'the same released absence is a negative in one history only'
    # C2 with C1 and C3 holding: the same matured reading, read through a complete run or a stalled label feed.
    stalled = copy.deepcopy(records)
    q = next(r for r in stalled if r['record_id'] == 'Q-5')
    q['sources'][0]['ingestion_watermark'] = '2026-05-20T00:00:00Z'
    q['statuses'] = derive_statuses(q)
    assert strip(records, COVERAGE_FIELDS) == strip(stalled, COVERAGE_FIELDS) and q['statuses'] == ['partial']
    assert {f[0] for f in check_both(stalled, outcomes, schema, outcome_schema)} == {'IR-08', 'XR-01'}
    out['C2 with C1 and C3'] = 'the same matured reading supports a negative in one history only'
    return out


def reference_sweep(records, schema):
    """Point every reference in a passing history at a record of each type it may not have, and at an actor of each
    kind it may not have. The rules must reject every such history. Returns the two counts."""
    assert not check(records, schema)
    first = {}
    for r in records:
        first.setdefault(r['record_type'], r['record_id'])
    actors = {}
    for r in records:
        if r['record_type'] == 'Actor':
            actors.setdefault(r['kind'], r['record_id'])
    spare = {'record_type': 'Actor', 'record_id': 'SWEEP-RULE', 'kind': 'rule'}
    actors.setdefault('rule', spare['record_id'])

    def holders(history):   # (record type or 'claim', the object that holds the field)
        for r in history:
            yield r['record_type'], r
            for c in r['claims'] if r['record_type'] == 'DraftOutput' else []:
                yield 'claim', c

    def mutated(index, field, target):
        history = copy.deepcopy(records) + [copy.deepcopy(spare)]
        holder = list(holders(history))[index][1]
        holder[field] = holder[field] + [target] if isinstance(holder[field], list) else target
        return seal(history)

    wrong_type = wrong_kind = 0
    for index, (where, holder) in enumerate(holders(records)):
        for (kind_of_holder, field), allowed in REFERENCES.items():
            if kind_of_holder != where or field not in holder:
                continue
            for record_type, target in first.items():
                if record_type not in allowed:
                    assert check(mutated(index, field, target), schema), (holder.get('record_id', holder.get('claim_id')), field, target)
                    wrong_type += 1
            if (where, field) in ACTOR_KINDS:
                sense, named = ACTOR_KINDS[(where, field)]
                for actor_kind, target in actors.items():
                    if (actor_kind == named) != (sense == 'is'):
                        assert check(mutated(index, field, target), schema), (holder['record_id'], field, target)
                        wrong_kind += 1
    return wrong_type, wrong_kind


def run_conformance():
    schema = json.loads(SCHEMA.read_text(encoding='utf-8'))
    valid = json.loads(VALID.read_text(encoding='utf-8'))['records']
    cases = json.loads(INVALID.read_text(encoding='utf-8'))['cases']
    base = check(valid, schema)
    assert not base, ('valid case fails', base)
    rules = set()
    for case in cases:
        got = {f[0] for f in check(seal(apply_patch(valid, case)), schema)}
        assert got == {case['rule']}, (case['case_id'], case['rule'], sorted(got))
        rules.add(case['rule'])
    expected = {'SCHEMA'} | {f'IR-{n:02d}' for n in range(1, 15)}
    assert rules == expected, ('rules without a failing case', sorted(expected - rules))
    pairs = necessity_pairs(valid, schema)
    records, outcomes, joint_cases = joint_history()
    outcome_schema = json.loads(oc.SCHEMA.read_text(encoding='utf-8'))
    assert not check_both(records, outcomes, schema, outcome_schema), check_both(records, outcomes, schema, outcome_schema)
    for case in joint_cases:
        got = {f[0] for f in check_both(seal(apply_patch(records, case.get('investigation', {}))),
                                        apply_patch(outcomes, case.get('outcome', {})), schema, outcome_schema)}
        assert got == {case['rule']}, (case['case_id'], case['rule'], sorted(got))
    joint = joint_pairs(records, outcomes, schema, outcome_schema)
    accept = json.loads(ACCEPT.read_text(encoding='utf-8'))['cases']
    for case in accept:   # changes the requirements allow must still pass
        if 'investigation' in case or 'outcome' in case:
            got = check_both(seal(apply_patch(records, case.get('investigation', {}))),
                             apply_patch(outcomes, case.get('outcome', {})), schema, outcome_schema)
        else:
            got = check(seal(apply_patch(valid, case)), schema)
        assert not got, (case['case_id'], got)
    wrong_type, wrong_kind = reference_sweep(records, schema)
    return {'valid_records': len(valid), 'invalid_cases': len(cases), 'rules_exercised': len(rules), 'necessity_pairs': len(pairs),
            'joint_records': len(records) - len(valid), 'joint_cases': len(joint_cases), 'joint_pairs': len(joint),
            'accept_cases': len(accept), 'wrong_type_references': wrong_type, 'wrong_kind_references': wrong_kind}


if __name__ == '__main__':
    if len(sys.argv) > 1:
        schema = json.loads(SCHEMA.read_text(encoding='utf-8'))
        records = json.loads(Path(sys.argv[1]).read_text(encoding='utf-8'))['records']
        found = check(records, schema)
        if len(sys.argv) > 2:
            found += check_joint(records, json.loads(Path(sys.argv[2]).read_text(encoding='utf-8'))['records'])
        elif any(c.get('outcome_items') or c.get('outcome_readings') or 'outcome_use' in c
                 for r in records if r.get('record_type') == 'DraftOutput' for c in r.get('claims', [])):
            found.append(('XR-01', '-', 'a claim lists outcome items: give the outcome records as a second file'))
        for f in found:
            print(*f, sep='\t')
        sys.exit(1 if found else 0)
    print(json.dumps(run_conformance()))
