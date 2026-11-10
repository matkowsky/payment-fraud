# Adversarial test of the query-run and release rules

Purpose: find histories that break requirement C2 or C3 as the paper states them and still pass the schema and rules IR-01 to IR-14, and legitimate histories the rules wrongly reject.

Why an outside tester: the 35 invalid cases in `SUPPLEMENT/S4_INVESTIGATION_RECORDS/` were written by the same hand as the rules, so each fails the check it was built to fail. Here the cases come from a tester who sees the published requirements, rules, schema and valid history, and never the checker's code.

Threat model: worst case. A case of tier "agent" changes only DraftOutput records, which is all a fully compromised agent can write. A case of tier "other" changes any record, as a compromised gateway, store or insider could. No live model is involved, so the test says nothing about how often an agent is hijacked.

## Files

- `build_packet.py` writes `PACKET_ROUND1.md`: the tester's brief, the two requirements quoted from the manuscript, the record types, rules and stated limits quoted from Supplement S4.4, the schema and the valid history.
- `run_cases.py CASES.json [RESULTS.md]` applies each case as a patch to the valid history, runs the checker, and prints what the tester expected and what the checker did. It marks disagreements for adjudication and decides nothing itself.

## Procedure

1. Round 1: the tester gets `PACKET_ROUND1.md` in a temporary chat with memory off, outside any project, with no web access, and returns a JSON array of 5 cases. The tester is then asked twice for 5 more, different in kind, for 15 in all. The first version of the packet asked for 16 cases at once and carried the full JSON schema; the tester's session timed out and returned no cases, so it was replaced before any answer was received.
2. The cases are saved unchanged and run. Each disagreement is adjudicated against the paper's text: the rules are wrong, or the tester is.
3. Round 2: the tester gets the round 1 results and writes new cases that adapt to them.
4. Every case and outcome is kept in this folder. Each confirmed miss is either fixed by a rule change or stated as a limit in Supplement S4.4.
