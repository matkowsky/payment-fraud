# Round 2: held-out test of the frozen rules

Fixed before the tester sees the packet. Any change to this plan is a new commit with its reason.

## Why

A referee noted that round 1 is in-sample: the rules were revised on the same 15 histories that then scored nine of 13 rejected. Round 2 tests the revised rules on histories they were not tuned on.

## Frozen rules

- Rules IR-01 to IR-14 as stated in Supplement S4.4 and implemented in `tools/investigation_conformance.py` at main `58150e8`.
- No rule or checker change until every round 2 case is scored and adjudicated. A fix found in round 2 is reported as a round 2 miss first.

## Tester

- ChatGPT, a fresh temporary chat, memory off, no project, no web, as in round 1. The model name shown is recorded.
- The tester gets `../PACKET_ROUND2.md` only: not the round 1 cases, results or rulings.
- Prompt 1: the whole packet. Prompts 2 and 3: "Write 5 more cases in the same format, different in kind from your earlier ones." Fifteen cases in all.
- Replies are saved unchanged as `reply_1.json`, `reply_2.json` and `reply_3.json`, with the date in `RUN_RECORD.md`.

## Scoring

- `python3 tools/adversarial_cases/run_cases.py --sealed round2/CASES.json round2/RESULTS.md`, with CASES.json the three replies joined in order.
- Each disagreement between the tester's expectation and the checker is ruled against the paper's text. The author confirms every ruling; a human coder from the practitioner post rechecks them if one is available.
- Reported: of the cases meant to break a requirement, how many the frozen rules reject, with an exact 95 percent interval; how many pass as new failures and how many as stated limits; and false rejections among the cases meant to be legitimate.
- Results go into Supplement S4.4 beside round 1, and the Section 1 sentence on the adversarial test is updated.
