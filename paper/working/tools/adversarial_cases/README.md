# Adversarial test of the query-run and release rules

Purpose: find histories that break requirement C2 or C3 as the paper states them and still pass the schema and rules IR-01 to IR-14, and legitimate histories the rules wrongly reject.

Why an outside tester: the invalid cases in `SUPPLEMENT/S4_INVESTIGATION_RECORDS/` were written by the same hand as the rules, so each fails the check it was built to fail. Here the cases come from a tester who sees the published requirements, rules, schema and valid history, and never the checker's code.

Threat model: worst case. A case of tier "agent" changes only DraftOutput records, which is all a fully compromised agent can write. A case of tier "other" changes any record, as a compromised gateway, store or insider could. No live model is involved, so the test says nothing about how often an agent is hijacked.

## Files

- `build_packet.py` writes `PACKET_ROUND1.md`: the tester's brief, the two requirements quoted from the manuscript, the record types, rules and stated limits quoted from Supplement S4.4, the schema and the valid history.
- `run_cases.py CASES.json [RESULTS.md]` applies each case as a patch to the valid history, runs the checker, and prints what the tester expected and what the checker did. It marks disagreements for adjudication and decides nothing itself.

## Procedure

1. Round 1: the tester gets `PACKET_ROUND1.md` in a new session with memory off, outside any project, with no web access, and returns a JSON array of 5 cases. The tester is then asked twice for 5 more, different in kind, for 15 in all. The first version of the packet asked for 16 cases at once and carried the full JSON schema; the tester's session timed out and returned no cases, so it was replaced before any answer was received.
2. The cases are saved unchanged and run. Each disagreement is adjudicated against the paper's text: the rules are wrong, or the tester is.
3. Round 2, held out: a fresh tester gets `PACKET_ROUND2.md` (the revised rules and every stated limit, not the round 1 cases) and writes 15 cases against rules frozen until they are scored. `round2/PLAN.md` fixes the procedure.
4. Every case and outcome is kept in this folder. Each confirmed miss is either fixed by a rule change or stated as a limit in Supplement S4.4.

## State after round 1

- `PACKET_ROUND1.md` shows the rules as they stood before round 1 (commit `5dd4213`). Do not rebuild it: the builder reads the current supplement, which now holds the revised rules.
- `round1/` holds the tester's replies, the results before and after the rule changes, the outside check of the rulings and the final rulings (`ADJUDICATION.md`).
- `run_cases.py --sealed` gives each changed draft its new digest first. `CHECK_CANDIDATE.py` reruns the fifteen cases that way and checks the outcomes.

## State after round 2

- `round2/PLAN.md` fixed the procedure before the tester saw the packet and lists every change made to it, with its reason. The rules and the checker were frozen at main `58150e8` for the round.
- `round2/` holds the tester's three replies and the two later prompts, the joined cases, the checker's output, Claude's first rulings, the packet and reply of the outside check of those rulings, and the rulings the author confirmed (`ADJUDICATION.md`). `RUN_RECORD.md` gives the order of events and what was not captured.
- Result: of 12 histories meant to break a requirement, the frozen rules rejected two. Of the 10 that passed, seven are new failures, one does not break a requirement and two are unresolved. Two of three legitimate histories were falsely rejected.
- One rule was changed after round 2: IR-10, on 19 November 2026, because a review had raised the point before the round. It changes no outcome in either round. The failures are stated as gaps in Supplement S4.4, because a fix would be tested only on the histories that prompted it. No third round is planned.
- `CHECK_CANDIDATE.py` reruns the round 2 cases and checks that the outcomes are those recorded. If a rule is changed later, those outcomes and the text of S4.4 change with it.
