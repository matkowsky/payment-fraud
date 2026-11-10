#!/usr/bin/env python3
"""Check query-run and release records against their schema and rules IR-01 to IR-14 (Supplement S4.4).

Usage:
  python3 tools/investigation_conformance.py              run the conformance cases and necessity pairs
  python3 tools/investigation_conformance.py FILE.json    check a file of the form {"records": [...]}

Standard library only; the schema validator is the one in outcome_conformance.py. A schema and
passing synthetic cases do not establish operational effectiveness.
"""
import copy
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from outcome_conformance import apply_patch, ts, validate  # noqa: E402

HERE = Path(__file__).resolve().parent.parent / 'SUPPLEMENT' / 'S4_INVESTIGATION_RECORDS'
SCHEMA = HERE / 'investigation_records.schema.json'
VALID = HERE / 'conformance_valid.json'
INVALID = HERE / 'conformance_invalid.json'
OBSERVED = {'source_observation', 'normalized_observation', 'derived_feature'}
RANK = {'low': 0, 'moderate': 1, 'high': 2}
COVERAGE_FIELDS = ('evaluated_entities', 'evaluated_interval', 'sources', 'access_filter_removed_rows',
                   'limits_reached', 'scope_limited', 'statuses', 'as_of')
DEPENDENCE_FIELDS = ('root_ids', 'inputs', 'agent_output_links', 'author')


def ent(e):
    return (e['tenant'], e['namespace'], e['id'])


def within(inner, outer):
    return ts(outer['from']) <= ts(inner['from']) and ts(inner['to']) <= ts(outer['to'])


def overlaps(a, b):
    return ts(a['from']) <= ts(b['to']) and ts(b['from']) <= ts(a['to'])


def derive_statuses(run):
    """The fixed rules of Section 6.2: statuses follow from the coverage fields alone."""
    out = set()
    req = run['requested_interval']
    if {ent(e) for e in run['evaluated_entities']} != {ent(e) for e in run['requested_entities']} \
            or run['evaluated_interval'] != req or run['access_filter_removed_rows']:
        out.add('partial')
    for s in run['sources']:
        if s['access'] == 'denied':
            out.add('denied')
        elif s['access'] == 'unavailable':
            out.add('unavailable')
        elif (ts(req['to']) > ts(s['event_watermark']) or ts(req['from']) < ts(s['retention_horizon']) or s['sampled']
              or any(overlaps(g, req) for g in s['known_gaps'])):
            out.add('partial')
    if run['limits_reached']:
        out.add('truncated')
    return sorted(out) or ['complete']


def supports_absence(run, claim):
    """A run supports an absence claim only if it is complete, unfiltered, returned nothing and covers the claim."""
    return (run['statuses'] == ['complete'] and not run['scope_limited'] and not run['returned']
            and {ent(e) for e in claim['entities']} <= {ent(e) for e in run['evaluated_entities']}
            and within(claim['interval'], run['evaluated_interval']))


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

    def refs(r):
        t = r['record_type']
        if t == 'QueryRun':
            return [r['requested_by'], r['recorded_by']] + r['returned']
        if t == 'Observation':
            return r['inputs'] + r['agent_output_links'] + r['root_ids'] + ([r['author']] if 'author' in r else [])
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
                        or not overlaps(o['event_interval'], r['evaluated_interval']):
                    found.append(('IR-06', rid, f'{x} was not learned by the cutoff or lies outside the evaluated interval'))
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
            owed = {x for i in ins for x in i['agent_output_links']}
            for x in records:
                if x['record_type'] == 'OutputExposure' and x['viewer'] == r.get('author') and ent(x['entity']) == ent(r['entity']) \
                        and ts(x['opened_at']) <= ts(r['learned_at']) <= ts(x['closed_at']):
                    owed.add(x['output_id'])
            if r['record_class'] == 'human_note' and 'author' not in r:
                found.append(('IR-14', rid, 'a note must name its author'))
            elif not owed <= set(r['agent_output_links']):
                found.append(('IR-14', rid, f'missing link to agent output {sorted(owed - set(r["agent_output_links"]))}'))
        if t == 'DraftOutput':
            for c in r['claims']:
                cid = f'{rid}/{c["claim_id"]}'
                if c['claim_type'] == 'absence' and not (c['query_runs'] and all(
                        by[q]['record_type'] == 'QueryRun' and supports_absence(by[q], c) for q in c['query_runs'])):
                    found.append(('IR-08', cid, 'an absence claim needs complete query runs that cover it'))
                named = {ent(e) for e in c['entities']}
                if any(by[s]['record_type'] != 'Observation' or ent(by[s]['entity']) not in named
                       or ts(by[s]['learned_at']) > ts(r['created_at']) for s in c['supporting']) \
                        or c['distinct_roots'] != len(distinct_roots(c['supporting'], by)):
                    found.append(('IR-09', cid, 'support must be observations of the named entities, learned by the draft, counted once per root'))
                elif c['claim_type'] == 'current_conduct':
                    def current(o):
                        return o['record_class'] in OBSERVED and within(o['event_interval'], r['current_period'])
                    ok = False
                    for s in (by[x] for x in c['supporting']):
                        if not current(s):
                            continue
                        if s['agent_output_links'] and not any(
                                current(by[i]) and not by[i]['agent_output_links'] for i in s['inputs']):
                            continue
                        ok = True
                    if not ok:
                        found.append(('IR-10', cid, 'no current-period observation of the conduct is cited'))
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
    assert supports_absence(a, claim) and not supports_absence(b, claim)
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
    assert strip([item], ('release_id',)) == strip([orphan], ('release_id',))
    assert not check(valid, schema)
    without = [orphan if r is item else r for r in valid if r['record_type'] != 'ReleaseDecision']
    assert {f[0] for f in check(without, schema)} == {'IR-02'}
    out['C3 release'] = 'reuse permitted in one history only'
    return out


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
    expected = {'SCHEMA'} | {f'IR-{n:02d}' for n in range(1, 15)}
    assert rules == expected, ('rules without a failing case', sorted(expected - rules))
    pairs = necessity_pairs(valid, schema)
    return {'valid_records': len(valid), 'invalid_cases': len(cases), 'rules_exercised': len(rules), 'necessity_pairs': len(pairs)}


if __name__ == '__main__':
    if len(sys.argv) > 1:
        schema = json.loads(SCHEMA.read_text(encoding='utf-8'))
        found = check(json.loads(Path(sys.argv[1]).read_text(encoding='utf-8'))['records'], schema)
        for f in found:
            print(*f, sep='\t')
        sys.exit(1 if found else 0)
    print(json.dumps(run_conformance()))
