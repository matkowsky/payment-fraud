"""Write RULINGS_CHECK_PACKET.md: an outside reviewer rules on the round 2 cases the checker and the tester disagree on.

  python3 tools/adversarial_cases/round2/build_check_packet.py     (from paper/working)

The reviewer rules blind: the packet holds no ruling by anyone. It holds the two requirements, the fourteen
rules, the limits stated before the freeze, the record fields and the valid history, all copied from
PACKET_ROUND2.md; further passages of the manuscript and supplement as they stood at the freeze commit; and each
disputed case with the tester's reason, its patch, what the frozen checker did (from RESULTS.md) and, for four
cases, a fact from diagnostics.py. Passages are taken whole, by line, so that the choice of sentences does not
steer the reviewer.
"""
import json, subprocess
from pathlib import Path

HERE = Path(__file__).resolve().parent
FREEZE = '58150e8'


def frozen(path):
    return subprocess.run(['git', 'show', f'{FREEZE}:paper/working/SOURCE/{path}'], capture_output=True, text=True,
                          check=True, cwd=HERE).stdout.split('\n')


def lines(text, first, last, starts):
    """Lines first..last (1-indexed) of a frozen file, after checking how the first one begins."""
    assert text[first - 1].startswith(starts), (first, text[first - 1][:60])
    return '\n'.join(text[first - 1:last]).strip()


HEAD = """# Independent rulings: adversarial test of record rules, round 2

You are an independent reviewer. Use only this packet. Do not use memory of earlier chats, files,
the web or any other source. If you recognize the project this comes from, say so in one sentence
before your answer and still work only from the packet.

A specification for AI-agent investigations on a payment platform states two requirements (C2 and
C3) and checks stored records against fourteen rules. An outside tester wrote 15 test histories.
Twelve were meant to break a requirement and still pass the rules. Three were meant to be
legitimate and still be rejected. The histories were run through the checker. Two were rejected,
as the tester did not expect, and need no ruling. The other thirteen are below.

The person who wrote the rules is not independent, so you rule on each case yourself. You are not
shown anyone else's ruling.

## How to rule

Judge each case against C2 and C3 as the paper states and explains them in this packet: the two
requirement statements and the passages under "Further passages from the paper". The fourteen
rules are the thing under test, so a rule's own wording does not settle what the paper requires.
Where two passages point different ways, say so in your reason.

For a case meant to break a requirement, which the checker passes, choose one:

- `new failure`: the history breaks C2 or C3, and no limit under "Stated limits" covers it.
- `stated limit`: the history only shows a limit listed under "Stated limits". Say which.
- `not a breach`: the history does not break C2 or C3.

For a case meant to be legitimate, which the checker rejects, choose one:

- `false rejection`: the history honours what the paper requires, and the rule asks for more than
  the paper's text does.
- `rules stand`: the paper's text requires what the rule enforces, so the history is not
  legitimate.

If the packet does not let you decide, answer `cannot tell` and say what is missing.

## Answer format

One line per case, thirteen lines, and nothing else:

`R01 | ruling: new failure | severity: serious | one or two sentences of reason, naming the passage or rule it rests on`

- ruling: one of the choices above.
- severity: `serious` or `minor` for a new failure or a false rejection, `none` otherwise.
"""

FACTS = {   # from diagnostics.py, run with the frozen checker
    'R05': 'The scoring ran the fourteen rules only. When the same history is also checked against the outcome records, '
           'the further rule XR-01 (quoted above) rejects it: "a cited reading does not exist or was taken after the draft".',
    'R06': 'The same note, written about ACC-1 where the case has ACC-2, is rejected by IR-14 for a missing link to DR-1.',
    'R10': 'The same claim citing only Q-6, without Q-2, is rejected by IR-08.',
    'R11': 'If a MemoryRead of M-2 is added, at any time after M-2 was created, IR-13 rejects that read.',
}
PATCH_KEYS = ('set_fields', 'remove_fields', 'remove_records', 'add_records')


def main():
    packet = (HERE.parent / 'PACKET_ROUND2.md').read_text(encoding='utf-8')
    reqs = packet[packet.index('## The two requirements'):packet.index('## Answer format')].strip()
    fields = packet[packet.index('## Record fields'):].strip()
    ms, sp = frozen('manuscript.md'), frozen('supplement.md')
    passages = [
        ('Manuscript, Section 2.3', lines(ms, 75, 75, 'C3 adopts human release')),
        ('Manuscript, Section 4.2', lines(ms, 123, 125, '- The **evidence plane**') + '\n\n' + lines(ms, 131, 135, 'For example, two accounts')),
        ('Manuscript, Section 5.3', lines(ms, 193, 193, '**Write authority follows')),
        ('Manuscript, Section 6.2', lines(ms, 233, 244, 'A complete result with no rows')),
        ('Manuscript, Section 6.4', lines(ms, 272, 282, 'A draft separates material claims')),
        ('Supplement, S4.1, storage requirements: assessment store', lines(sp, 254, 257, '- Retain the model or reviewer identity')),
        ('Supplement, S4.1, storage requirements: organizational-memory store', lines(sp, 281, 284, '- Keep released items only')),
        ('Supplement, S4.4: a further rule, outside the fourteen', lines(sp, 440, 442, '**Requirements together.**') + '\n\n'
         + 'The rules cannot tell whether a claim relies on an unreported outcome it does not list, or which channels it should cite.'),
    ]
    assert passages[-1][1].split('\n\n')[-1] in sp[450]
    cases = {c['case_id']: c for c in json.loads((HERE / 'CASES.json').read_text(encoding='utf-8'))}
    rows = [[x.strip() for x in r.strip().strip('|').split('|')] for r in (HERE / 'RESULTS.md').read_text(encoding='utf-8').split('\n')
            if r.startswith('| ') and not r.startswith('| Case')]
    out = [HEAD, reqs, '', '## Further passages from the paper', '',
           'Copied whole from the manuscript and supplement as they stood when the rules were frozen.', '']
    for title, text in passages:
        out += [f'### {title}', '', text, '']
    out += [fields, '', '## The thirteen cases', '',
            'Each case is a patch to the valid history above. `set_fields` replaces whole top-level fields, `remove_fields` '
            'removes them and `add_records` adds records. Where a case changed a draft\'s claims, the draft was given its new '
            'digest before checking, so the version identifier in the patch does not matter.', '']
    n = 0
    for case_id, tier, expect, result, outcome, why, detail in rows:
        if not outcome.startswith('ADJUDICATE'):
            continue
        n += 1
        c = cases[case_id]
        meant = (f'to break {c["breaks"]} and still pass the rules' if expect == 'reject'
                 else 'to be legitimate and still be rejected')
        did = 'passes all fourteen rules.' if result == 'passes' else f'{result}: "{detail}".'
        out += [f'### {case_id}', '', f'- Meant {meant}. Tier: {tier}.', f'- The tester\'s reason: {c["why"]}',
                f'- The checker: {did}']
        if case_id in FACTS:
            out.append(f'- A further fact: {FACTS[case_id]}')
        out += ['- Patch:', '', '```json', json.dumps({k: c[k] for k in PATCH_KEYS if k in c}), '```', '']
    assert n == 13
    (HERE / 'RULINGS_CHECK_PACKET.md').write_text('\n'.join(out).rstrip() + '\n', encoding='utf-8')
    print(f'wrote RULINGS_CHECK_PACKET.md: {n} cases')


if __name__ == '__main__':
    main()
