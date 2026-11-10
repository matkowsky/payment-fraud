"""Build a self-contained packet asking an outside reviewer to check Claude's round 1 rulings.

  python3 tools/adversarial_cases/round1/build_check_packet.py     writes RULINGS_CHECK_PACKET.md

The reviewer needs no earlier chat: the packet carries the requirements, the rules, the paper's
relevant sentences, and for each case the tester's reason, the checker's result and Claude's ruling.
"""
import json, re
from pathlib import Path

HERE = Path(__file__).resolve().parent
W = HERE.parents[2]

RULINGS = {  # case: (checker result, ruling, reason, proposed action)
 'R01': ('passes', 'Miss', 'No rule compares a claim\'s interval with the event intervals of its supporting records.',
         'Extend IR-09: each supporting observation\'s event interval overlaps the claim\'s interval.'),
 'R02': ('passes', 'Stated limit', 'The supplement says the rules do not check ingestion-watermark lag.',
         'Keep as a limit, or add a consistency check: a source\'s ingestion watermark is not earlier than its event watermark.'),
 'R03': ('passes', 'Miss', 'C3 says a record an agent output informed "counts as dependent, not as independent corroboration". IR-10 excludes linked records; IR-09 still counts their roots.',
         'Extend IR-09: a supporting record linked to an agent output adds no root except through an unlinked input.'),
 'R04': ('passes', 'Stated limit', 'The supplement says the rules do not check released-item links on records written after a memory read.',
         'Keep as a limit for now; a rule would match Section 4.2.'),
 'R05': ('rejected by IR-11', 'Caught', 'The checker rejects a release dated before the draft existed.', 'None.'),
 'R06': ('passes', 'Miss, two parts', '(a) The rules treat the version hash as a label and never recompute it. (b) A material presence claim with no supporting record passes every rule.',
         '(a) Define the hash as a digest of the draft\'s claims and recompute it in IR-11. (b) Extend IR-09: a material presence or current-conduct claim cites at least one supporting observation.'),
 'R07': ('passes', 'Miss, minor', 'IR-07 orders learned times only for derived records.',
         'Extend IR-07: a source observation is not learned before its event began, with an exemption for a fact recorded ahead of its effective date.'),
 'R08': ('passes', 'Miss, needs a field', 'The query-run record does not hold what was asked, so the rules cannot tell which stored records a complete run should have returned.',
         'Add the query\'s predicate to QueryRun and a rule that a complete run returns every stored record that matches.'),
 'R09': ('passes', 'Miss, needs a field', 'Release scope is free text and no rule reads it.',
         'Give scope a structure and add to IR-13: a read\'s case lies within the release scope.'),
 'R10': ('rejected by IR-14', 'Rules stand', 'The paper links by exposure on purpose: every record written while an agent output is open is linked (Sections 2.3 and 4.2, quoted below). The tester read C3 as covering only records the output actually informed.',
         'No rule change. Make Section 1\'s statement of C3 say that exposure counts.'),
 'R11': ('passes', 'Miss, minor', 'IR-09 checks learned time for supporting records only.',
         'Every record a draft cites was learned or created by the draft\'s creation time.'),
 'R12': ('rejected by the schema', 'Caught', 'The schema rejects a run with no sources.', 'None.'),
 'R13': ('passes', 'Limit no rule can close', 'Rules can check that a person is named, not that the person reviewed. Free text is not read.',
         'State this limit in the supplement.'),
 'R14': ('rejected by IR-10', 'Caught', 'The checker excludes a linked source observation as sole support for current conduct.', 'None.'),
 'R15': ('rejected by IR-08', 'Judgment call', 'IR-08 as published requires every cited run to be complete, empty and covering. The tester says a supplementary partial run should not sink the claim.',
         'Either keep the strict rule and say so, or relax it to "at least one cited run qualifies and none returned a matching record".'),
}

BRIEF = """# Check of rulings: adversarial test of record rules, round 1

You are an independent reviewer. Use only this packet. Do not use memory of earlier chats, files,
the web or any other source.

A specification for AI-agent investigations on a payment platform states two requirements (C2 and
C3) and checks stored records against fourteen rules. An outside tester wrote 15 test histories.
Thirteen were meant to break a requirement and still pass the rules. Two were meant to be
legitimate and still be rejected. The histories were run through the checker. The author of the
rules then ruled on each case. That author is not independent, so the rulings need checking.

For each case, say whether the ruling is right and whether the proposed action is sound.

## Answer format

One line per case and nothing else:

`R01 | ruling: agree | action: sound | one sentence of reason`

- ruling: `agree` or `disagree`. If you disagree, say what the ruling should be.
- action: `sound`, `too narrow`, `too broad` or `none needed`. If not sound, say what would be.
"""

QUOTES = """## Sentences from the paper that the rulings rely on

- Section 6.4: "Each material claim cites supporting records with their classes, event intervals and root observations, reached through lineage."
- Section 4.2: "Labeling, assessment, control, detection and threat-knowledge interfaces automatically attach every agent output and every released organizational-memory item open in the writer's case or session."
- Section 2.3: "Because the interfaces that write these records add the links, they also cover a person who writes a record while an agent output is open in the case, part of the relay the threat-detection design leaves open; a missing link still does not establish independence (Section 4.2)."
"""


def section(text, start, end):
    a = text.index(start)
    return text[a:text.index(end, a)]


def main():
    ms = (W / 'SOURCE' / 'manuscript.md').read_text(encoding='utf-8')
    sup = (W / 'SOURCE' / 'supplement.md').read_text(encoding='utf-8')
    reqs = [p for p in ms.split('\n\n') if p.startswith(('**C2**', '**C3**'))]
    s44 = section(sup, '### S4.4 ', '\n## S5.')
    rules = section(s44, '1. IR-01', '\nThe [valid conformance case]')
    limits = re.search(r'The rules do not check[^.]*\.', s44).group(0)
    cases = json.loads((HERE / 'CASES.json').read_text(encoding='utf-8'))
    assert [c['case_id'] for c in cases] == list(RULINGS)
    out = [BRIEF, '## The two requirements, as the paper states them', '', *['> ' + r + '\n' for r in reqs],
           '## The fourteen rules', '', rules.strip(), '', '## Limits the supplement already states', '', limits, '', QUOTES,
           '## The valid history the cases change', '',
           'One investigation with three query runs, a draft (DR-1) with a current-conduct claim (CL-1) and an absence '
           'claim (CL-2), a human note (O-5) written while the draft was open and linked to it, a release (RL-1) by a '
           'second person, a released item (M-1), and a later case whose draft (DR-2) reads the released item as context '
           'and cites a new observation (O-6).', '', '## The cases', '']
    for c in cases:
        result, ruling, reason, action = RULINGS[c['case_id']]
        out += [f"### {c['case_id']}", '',
                (f"- The tester says this history should be **rejected** because it breaks {c['breaks']}, and predicted the rules would pass it. Tier: {c['tier']}."
                 if c['expect'] == 'reject' else
                 f"- The tester says this history is **legitimate** and predicted the rules would wrongly reject it. Tier: {c['tier']}."),
                f"- Tester's reason: {c['why']}", f"- Checker: {result}.", f"- Ruling: **{ruling}**. {reason}",
                f"- Proposed action: {action}", '']
    text = '\n'.join(out)
    (HERE / 'RULINGS_CHECK_PACKET.md').write_text(text, encoding='utf-8')
    print(f'{len(text)} characters, {len(text.split())} words')


if __name__ == '__main__':
    main()
