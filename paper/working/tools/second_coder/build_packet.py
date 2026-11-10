"""Build the blind packet for the second-coder check of the mechanism-to-signal links.

  python3 tools/second_coder/build_packet.py [SEED]        writes PACKET.md and KEY.json beside this file
                                                          (PACKET_SEED.md and KEY_SEED.json for another seed)
  python3 tools/second_coder/build_packet.py covered-rest  writes PACKET_COVERED_REST.md and KEY_COVERED_REST.json:
                                                          the covered mechanisms the first sample left out

The packet gives a second rater the linking rule, the signals, and a seeded random sample of mechanisms
with the recorded scope of each mechanism's sources. It contains none of the paper's links. Mechanism
IDs are replaced by M01, M02, ... so the rater cannot look the answers up; KEY.json maps them back.
Sample: 20 of the 61 mapped mechanisms and 5 of the 13 judged covered by existing records.
"""
import csv, json, random, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SUP = HERE.parents[1] / 'SUPPLEMENT'
SEED = 20261111          # the sample for the real run; 20261110 was used for the dry run
N_MAPPED, N_COVERED = 20, 5
CROSS_CUTTING = {'SIG-44', 'SIG-45', 'SIG-46'}   # apply to every mechanism; not coded

RULE = """## The rule

Link a mechanism to a signal when BOTH hold:

1. An investigator examining that mechanism would need the signal's record to test whether the
   mechanism occurred, or to tell it apart from legitimate activity.
2. At least one of the sources listed under the mechanism describes behaviour that the signal would
   record. If you link on reasoning alone, without such a source, mark the link "inference".

Do not link a signal only because it is generally useful. Link every signal that meets the rule and
no others.

How to apply the rule:

- A source from another setting (another platform, another industry) counts for rule 2 when it
  describes the same behaviour.
- Some sources are public interface schemas. Their scope says "capability premises": the schema shows
  that an account can create or change the thing the mechanism abuses. Such a source supports a
  signal that records that creation or change.
- Signals of any class may be linked: observations, derived features, model outputs, control
  outcomes and external knowledge.
- A derived feature and the observations it is computed from are separate signals. Link each one
  that meets the rule by itself. Do not link an observation only because a linked feature uses it.
- A mechanism with "Sources: none recorded" cannot meet rule 2. Apply rule 1 only and mark every
  link "inference".

For each mechanism also answer whether a record is missing. Answer "missing" only when the test in
rule 1 could not be made at all with the listed signals. A record that would merely help is not
missing.
"""

def rows(name):
    with open(SUP / name, newline='', encoding='utf-8') as f:
        return list(csv.DictReader(f))

def main():
    rest = len(sys.argv) > 1 and sys.argv[1] == 'covered-rest'
    seed = SEED if rest else int(sys.argv[1]) if len(sys.argv) > 1 else SEED
    suffix = '_COVERED_REST' if rest else '' if seed == SEED else f'_{seed}'
    alloc = {r['ID']: r for r in rows('S2_MECHANISM_ALLOCATION.csv')}
    pairs = rows('S3_MECHANISM_SIGNAL_PAIRS.csv')
    signals = [s for s in rows('S3_SIGNALS.csv') if s['signal_id'] not in CROSS_CUTTING]
    sources = {s['source_id']: s for s in rows('S3_SOURCE_DIRECTORY.csv')}
    joins = {}
    for j in rows('S3_MAPPING_SOURCE_JOINS.csv'):
        joins.setdefault(j['mechanism_id'], []).append(j)
    mapped = sorted({p['mechanism'] for p in pairs})
    covered = sorted(i for i, r in alloc.items() if r['disposition'] == 'covered')
    rng = random.Random(seed)
    sample = rng.sample(mapped, N_MAPPED) + rng.sample(covered, N_COVERED)
    rng.shuffle(sample)
    if rest:   # the covered mechanisms the first sample left out, in a seeded order
        sample = sorted(set(covered) - set(sample))
        random.Random(SEED + 1).shuffle(sample)
    key = {f'M{n:02d}': mid for n, mid in enumerate(sample, 1)}

    out = ['# Second-coder packet: which signals does each mechanism need?', '',
           'You are an independent rater. Use only this packet. Do not use memory of earlier chats, '
           'files, the web or any other source. If you recognize the project this comes from, say so '
           'and still answer only from the packet.', '',
           'A "mechanism" is a way of abusing a multi-product payment platform. A "signal" is a kind '
           'of record the platform could keep. Your task is to decide, for each mechanism, which '
           'signals it should be linked to under the rule below.', '', RULE,
           '## Answer format', '',
           'One line per mechanism. If you recognize the project, say so in one sentence before the lines. Add nothing else:', '',
           '`M01 | SIG-xx, SIG-yy (inference), SIG-zz | missing: none`', '',
           'Write `missing: <the record that is absent>` if rule 1 needs a record the list lacks. '
           'Write `M01 | none | missing: none` if no signal meets the rule.', '',
           '## Signals', '', '| ID | Signal | Family | Class |', '|---|---|---|---|']
    for s in signals:
        out.append(f"| {s['signal_id']} | {s['signal']} | {s['family']} | {s['chain_level']} |")
    out += ['', '## Mechanisms', '']
    for label, mid in key.items():
        out += [f"### {label}", '', alloc[mid]['Mechanism'] + '.', '']
        js = joins.get(mid, [])
        if not js:
            out += ['Sources: none recorded for this mechanism.', '']
            continue
        out.append('Sources (recorded scope of each):')
        for j in js:
            src = sources[j['source_id']]
            limit = f" Limit: {j['recorded_scope_limit']}." if j['recorded_scope_limit'].strip('. ') else ''
            out.append(f"- {src['citation']} ({src['year']}; {src['source_type'].lower()}). {src['scope']}{limit}")
        out.append('')
    (HERE / f'PACKET{suffix}.md').write_text('\n'.join(out), encoding='utf-8')
    (HERE / f'KEY{suffix}.json').write_text(json.dumps({'seed': seed, 'labels': key}, indent=1) + '\n', encoding='utf-8')
    print(f'{len(key)} mechanisms, {len(signals)} signals, {len(" ".join(out).split())} words')

if __name__ == '__main__':
    main()
