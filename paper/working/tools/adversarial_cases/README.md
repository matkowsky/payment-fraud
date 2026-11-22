# Adversarial test of the query-run and release rules

Purpose: find histories that break requirement C2 or C3 as the paper states them and still pass the schema and rules IR-01 to IR-14, and legitimate histories the rules wrongly reject. Round 3 adds rule XR-01 and the negative that C1 bars.

Why an outside tester: the invalid cases in `SUPPLEMENT/S4_INVESTIGATION_RECORDS/` were written by the same hand as the rules, so each fails the check it was built to fail. Here the cases come from a tester who sees the published requirements, rules, schema and valid history, and never the checker's code.

Threat model: worst case. A case of tier "agent" changes only DraftOutput records, which is all a fully compromised agent can write. A case of tier "other" changes any record, as a compromised gateway, store or insider could. No live model is involved, so the test says nothing about how often an agent is hijacked.

## Files

- `build_packet.py 3` writes `PACKET_ROUND3.md`: the tester's brief, the requirements quoted from the manuscript, the record types, rules and stated limits quoted from Supplement S4.4, the field guides and the joint history of both stores. `PACKET_ROUND1.md` and `PACKET_ROUND2.md` are kept as sent and are not rebuilt.
- `run_cases.py CASES.json [RESULTS.md]` applies each case as a patch to the valid history, runs the checker, and prints what the tester expected and what the checker did. It marks disagreements for adjudication and decides nothing itself. With `--joint` (round 3) a case may patch either store, and every history is checked against all 29 rules. For rounds 1 and 2 the script first gives each claim the three fields added on 22 November 2026; its header says how.

## Procedure

1. Round 1: the tester gets `PACKET_ROUND1.md` in a new session with memory off, outside any project, with no web access, and returns a JSON array of 5 cases. The tester is then asked twice for 5 more, different in kind, for 15 in all. The first version of the packet asked for 16 cases at once and carried the full JSON schema; the tester's session timed out and returned no cases, so it was replaced before any answer was received.
2. The cases are saved unchanged and run. Each disagreement is adjudicated against the paper's text: the rules are wrong, or the tester is.
3. Round 2, held out: a fresh tester gets `PACKET_ROUND2.md` (the revised rules and every stated limit, not the round 1 cases) and writes 15 cases against rules frozen until they are scored. `round2/PLAN.md` fixes the procedure.
4. Every case and outcome is kept in this folder. Each confirmed miss is either fixed by a rule change or stated as a limit in Supplement S4.4.
5. Round 3, held out: a tester from outside the two model families used so far writes cases against the rules as revised after round 2. `round3/PLAN.md` fixes the procedure.

## State after round 1

- `PACKET_ROUND1.md` shows the rules as they stood before round 1 (commit `5dd4213`). Do not rebuild it: the builder reads the current supplement, which now holds the revised rules.
- `round1/` holds the tester's replies, the results before and after the rule changes, the outside check of the rulings and the final rulings (`ADJUDICATION.md`).
- `run_cases.py --sealed` gives each changed draft its new digest first. `CHECK_CANDIDATE.py` reruns the fifteen cases that way and checks the outcomes.

## State after round 2

- `round2/PLAN.md` fixed the procedure before the tester saw the packet and lists every change made to it, with its reason. The rules and the checker were frozen at main `58150e8` for the round.
- `round2/` holds the tester's three replies and the two later prompts, the joined cases, the checker's output, Claude's first rulings, the packet and reply of the outside check of those rulings, and the rulings the author confirmed (`ADJUDICATION.md`). `RUN_RECORD.md` gives the order of events and what was not captured.
- Result: of 12 histories meant to break a requirement, the frozen rules rejected two. Of the 10 that passed, seven are new failures, one does not break a requirement and two are unresolved. Two of three legitimate histories were falsely rejected.
- Until 22 November 2026 the failures were stated as gaps in Supplement S4.4 and not fixed, because a fix would be tested only on the histories that prompted it, and no third round was planned. One rule had been changed: IR-10, on 19 November 2026, because a review had raised the point before the round. It changes no outcome in either round.
- `round2/RESULTS.md` is what the frozen rules did. It is a saved record and is not regenerated.

## Revision of 22 November 2026

- The rules were revised from a table of every reference between records and four attributes of its target: type, kind of actor, entity and time (the reference table of Supplement S4.4). `investigation_conformance.py` holds the table and generates a test from it.
- Three claim fields are new: the sentence (`claim_text`), which the version digest now covers; the sources an absence claim speaks for (`sources`); and whether a claim that lists outcome items states their status or reads a negative (`outcome_use`).
- Two questions the text had left open are settled by decision: a released conclusion is cited as context only, and an absence claim speaks for the sources it names.
- In sample, under the revised rules: 11 of round 2's 12 histories meant to break a requirement are rejected, and the twelfth was ruled not a breach. Both false rejections are gone. Round 1 is unchanged at nine of 13. `CHECK_CANDIDATE.py` reruns both rounds and checks these outcomes.
- These counts say nothing about new histories. Round 3 was the test.

## Round 3

- `round3/PLAN.md` fixes the tester, the packet, the scoring, the rulings and what is reported. `PACKET_ROUND3.md` is the packet as sent and is not rebuilt.
- Run on 22 November 2026. The tester was Llama 4 Maverick (Meta), as the author states. It wrote 16 cases; the plan asked for 15, and all are scored. `round3/RUN_RECORD.md` gives the order of events and what was not recorded.
- The rules, the checkers, the runner, the schemas and the histories were frozen from the merge of the plan until every case was ruled on.
- What the frozen checkers did (`round3/RESULTS.md`): of 13 histories meant to break a requirement, 11 rejected, one passes, and one stopped the checker with an error. Seven were rejected by the investigation rules or XR-01, two by the schema and two only by outcome rules, which the round did not test. Of three meant to be legitimate, one passes and two are rejected.
- Rulings (`round3/ADJUDICATION.md`): Claude ruled first on four cases, an outside reviewer (GPT-6 Astra Pro) ruled on each without seeing those rulings, the two agreed on all four, and the author confirmed them. The pass is a stated limit. Both rejections stand. The rules as stated reject the history that stopped the checker, so that case is one fault in the checker's code.
- After the round the fault was fixed: the code for XR-01 reads an entity only from a returned observation. The generated reference test now runs all 29 rules. `run_cases.py` reports an error raised by the checker as a checker error, not as a malformed case. `CHECK_CANDIDATE.py` reruns the 16 cases.
- The round is weak support. Its tester differs from the tester of rounds 1 and 2, and 13 of its 16 cases change one record.
