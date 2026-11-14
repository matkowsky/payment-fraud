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
- As run (see Changes, 14 November, second entry): reply 1 came from the first chat, which was then closed. Prompt 2 goes to a new temporary chat with the same settings and is `PROMPT_2.md`: the whole packet, then reply 1 as saved, then the same request. Prompt 3 was to be the same request in that second chat. That chat was closed after reply 2 (see Changes, 15 November), so prompt 3 goes to a third temporary chat with the same settings and is `PROMPT_3.md`: the whole packet, then replies 1 and 2 as saved, then the same request.

## Scoring

- `python3 tools/adversarial_cases/run_cases.py --sealed round2/CASES.json round2/RESULTS.md`, with CASES.json the three replies joined in order.
- Each disagreement between the tester's expectation and the checker is ruled against the paper's text. The author confirms every ruling.
- Reported, as counts and fractions: of the cases the tester meant to break a requirement, how many the frozen rules reject; of those that pass, how many are new failures and how many fall under stated limits; and, of the cases the tester meant to be legitimate, how many the rulings find falsely rejected.
- The tester's intent and the ruling on each case are reported separately. A case that is excluded or left unresolved is listed with its reason.
- No interval is reported. One tester writes the cases in sequence and is asked to vary them, so they are not a random sample from a defined population, and the coverage of a binomial interval would not be established. The results describe this suite of cases.
- Results go into Supplement S4.4 beside round 1, and the Section 1 sentence on the adversarial test is updated.

## Changes

- 13 November 2026, with no round 2 reply saved or scored: the report no longer promises an exact 95 percent interval. Reason: such an interval assumes independent draws from one population with one rejection rate, and this protocol does not establish that. The report now also keeps the tester's intent apart from the rulings and lists exclusions. The frozen rules, the tester, the prompts, the denominator and the scoring command are unchanged. From an independent review by ChatGPT, relayed by the author.
- 14 November 2026, with no round 2 reply saved or scored: a limit added to Supplement S4.4 after the freeze does not count as a stated limit here. A passing case that falls under it is reported as a new failure. Reason: one such limit was added on this date (the schema has no record for a later retraction, early expiry or withdrawal), and counting it would favor the rules. The frozen rules, the tester, the prompts and the scoring command are unchanged. From an independent review by ChatGPT, relayed by the author.
- 14 November 2026, second entry, with reply 1 saved and no case run through the checker: the first temporary chat was closed after reply 1, before prompt 2 was sent. Prompt 2 therefore goes to a new temporary chat with the same settings. It holds the whole packet, then reply 1 as saved, then the same request (`PROMPT_2.md`). Reason: the follow-up in the same chat is no longer possible, and a tester that had not seen reply 1 could not write cases different in kind from it. What differs from the plan as fixed: the fifteen cases come from two chats, not one, and the second tester reads the first tester's cases where it would have remembered its own. The prompt adds 402 bytes around the packet and the reply: a heading, three sentences saying that the earlier reply is copied unchanged and that none of its cases has been run, and the code fence. It says nothing about the checker or the rules beyond the packet. The reason for reporting no interval still holds: the cases are still written in sequence and asked to vary. The frozen rules, the packet, the request, the number of cases, the denominator and the scoring command are unchanged. The author asked for a complete prompt for the second reply (chat with Claude, 14 November 2026, 23:17 Asia/Jerusalem); Claude proposed this form.
- 15 November 2026 (00:18 Asia/Jerusalem), with replies 1 and 2 saved and no case run through the checker: the second temporary chat was closed after reply 2, before prompt 3 was sent. Prompt 3 therefore goes to a third temporary chat with the same settings. It holds the whole packet, then replies 1 and 2 as saved, then the same request (`PROMPT_3.md`). Reason: the same as for the second 14 November change. The follow-up in the same chat is no longer possible, and a tester that had not seen the earlier replies could not write cases different in kind from them. What differs from the plan as fixed: the fifteen cases come from three chats, not one, and each tester after the first reads the earlier cases where it would have remembered its own. The prompt adds 489 bytes around the packet and the replies: a heading, three sentences saying that the earlier replies are copied unchanged and that none of their cases has been run, two labels, and the code fences. It says nothing about the checker or the rules beyond the packet. The frozen rules, the packet, the request, the number of cases, the denominator and the scoring command are unchanged. The author asked for a new complete prompt because the chat had closed (chat with Claude, 15 November 2026, 00:18 Asia/Jerusalem); Claude built it in the form of `PROMPT_2.md`.
