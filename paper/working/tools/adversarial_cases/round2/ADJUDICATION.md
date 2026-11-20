# Round 2 adjudication

Tester: ChatGPT (GPT-6 Astra Pro) in three sessions, five cases each, from `PACKET_ROUND2.md`, `PROMPT_2.md` and `PROMPT_3.md`. The replies are stored unchanged as `reply_*.json`. The rules and the checker were frozen at main `58150e8` before the tester saw the packet, and are unchanged.

Files, in the order things happened:

1. `CASES.json`: the three replies joined, committed and pushed before the checker ran (`cb8e0d8`).
2. `RESULTS.md`: the frozen checker's output. Byte-identical when run at the freeze commit.
3. `FIRST_RULINGS_CLAUDE.md`: Claude's rulings on the thirteen disputed cases, pushed before the outside reply existed (`593b54c`).
4. `RULINGS_CHECK_PACKET.md` and `RULINGS_CHECK_REPLY.txt`: an outside session of the tester's model ruled on the same thirteen cases without seeing Claude's rulings. Stored as received.
5. This file: the rulings the author confirmed.

Claude wrote the rules, so its first rulings were not independent. The outside reviewer is independent of Claude but is the same model as the tester. The two gave the same ruling in 7 of 13 cases. Claude checked each of the six differences against the paper as it stood at the freeze and against the checker's code, and recommended a ruling for each. The author confirmed the recommended rulings at 23:28Z on 14 November 2026.

## Counts

What the frozen checker did:

- 12 histories meant to break a requirement: 2 rejected (R03 by the schema, R07 by IR-12), 10 passed.
- 3 histories meant to be legitimate: all 3 rejected (A01 by IR-14, A02 by IR-08, A03 by IR-11).

Confirmed rulings on the 10 that passed: 7 new failures (R01, R04, R05, R06, R08, R09, R12), 1 not a breach (R11), 2 unresolved (R02, R10). None falls under a limit stated before the freeze. Two of the seven need only a compromised agent (R05, R09).

Confirmed rulings on the 3 rejections: 2 false rejections (A01, A02), 1 intended (A03).

The same counts under each first set alone, for a reader who rules differently:

| Rulings | New failures | Not a breach | Unresolved or cannot tell | False rejections of 3 |
|---|---|---|---|---|
| Confirmed | 7 | 1 | 2 | 2 |
| Outside reviewer's | 5 | 2 | 3 | 2 |
| Claude's first | 10 | 0 | 0 | 1 |

At first exposure, round 1's rules rejected 3 of 13. The revised rules rejected 2 of 12 here. Round 1's nine of 13 was measured on the histories the rules had been revised on.

## Rulings

| Case | Tier | Checker | Claude first | Outside reviewer | Confirmed ruling | Basis |
|---|---|---|---|---|---|---|
| R01 | other | passes | New failure | New failure, serious | New failure | C3: no agent output enters the evidence plane as evidence of the activity. The checker never reads the kind of a record's producer, so an observation the agent produced counts as an independent root. |
| R02 | agent | passes | New failure, minor | Cannot tell | Unresolved | C3 lets a released conclusion serve as a hypothesis or context. Section 6.4 says a claim lists the retrieved records that count against it. The paper does not say whether a released conclusion listed against a claim is a contrary hypothesis or evidence. |
| R03 | other | schema | | | Caught | No ruling needed. |
| R04 | other | passes | New failure | New failure, serious | New failure | C2: coverage is what a query actually covered. A run that records only ACC-2 as evaluated returns records about ACC-1. IR-06 checks returned records for time only. Not the stated limit about whether a returned record bears on a claim. |
| R05 | agent | passes | New failure; caught by XR-01 | New failure, minor | New failure of the fourteen rules | IR-09 names four kinds of citation and not outcome readings, and the fourteen rules never read a claim's outcome fields. The fifteenth rule, XR-01, rejects this history when the outcome records are checked (`diagnostics.py`). The plan's command does not run XR-01. |
| R06 | other | passes | New failure | New failure, serious | New failure | C3 has no entity condition on a record written while an agent output is open to its writer. Section 4.2 and S4.1 scope the link by the writer's case or session. IR-14 scopes it by entity. The schema has no case or session on a note or an exposure. |
| R07 | other | IR-12 | | | Caught | No ruling needed. |
| R08 | other | passes | New failure, minor | New failure, minor | New failure, minor | A record learned on 19 May links to a draft written on 20 May. IR-07 orders a record after its inputs; nothing orders it after a linked output. |
| R09 | agent | passes | New failure | Not a breach | New failure | The claim names ACC-2 with no observation and no coverage of ACC-2. The reviewer is right that the sentence "for each named entity" in Section 6.4 covers linked features only. The ruling rests on two other grounds. Round 1's R01, confirmed after its outside check, ruled a claim whose evidence did not cover its interval a gap; this is that defect for one of two named entities. And the frozen checker rejects the same claim when it names only ACC-2 (`diagnostics_after_check.py`). |
| R10 | other | passes | New failure | Cannot tell | Unresolved | A claim records no sources. The text cannot say whether an unavailable run on a refunds source bears on a claim that a complete payments run supports. Round 1's ruling on its R15 already let a claim cite an extra run that does not support it. |
| R11 | other | passes | New failure, minor | Not a breach | Not a breach | C3 asks for release before promotion, and the release came first. Nothing in C3 or S4.1 makes expiry a deadline for storing a released claim. The frozen checker rejects every read of the item under IR-13 (`diagnostics.py`). |
| R12 | other | passes | New failure | Cannot tell | New failure | The draft claims absence and lists, against the claim, an observation of the same account in the claim's interval, learned before the draft. An absence claim in this schema is its entities and interval, and IR-08 treats any record about them as defeating it when a cited run returns it. With a later cited run that returns the same record, IR-08 rejects the history (`diagnostics_after_check.py`). The reviewer asked for claim wording and an as-of qualifier, which the schema does not have. |
| A01 | other | IR-14 | Rules stand | False rejection, minor | False rejection, minor | Section 6.4 gives a record without a producer a treatment: it counts as dependent and adds no root. It does not reject it. The note keeps its link. |
| A02 | other | IR-08 | False rejection | False rejection, minor | False rejection | Section 6.4: an absence claim cites the query runs whose coverage records support it. Two complete, empty runs with the same cutoff, source and account cover the interval together. IR-08 asks for one run that covers all of it. |
| A03 | other | IR-11 | Rules stand | Rules stand | Rules stand | Section 6.4: release preserves the assessment's uncertainty. Raising a claim's confidence at release does not. |

In R09 and R12 the confirmed ruling is Claude's, against the outside reviewer's. Both go against Claude's own rules. The reviewer did not have round 1's rulings or the two later diagnostics.

## What was decided, and what was not done

- No rule and no checker code is changed. The seven failures and the two false rejections are stated in Supplement S4.4 as known gaps. A fix would be tested only on the histories that prompted it, which is the fault a referee found in round 1.
- No third rater and no third round (author, 15 November 2026). The headline counts do not depend on the six disputed rulings.
- What the failures have in common is given in S4.4 as an inference from the cases, not as a tested result.

## Limits of this round

- The fifteen histories came from three sessions, where the plan fixed one. Each later session was given the earlier histories (`PLAN.md`, changes of 14 and 15 November).
- The model name and the settings were recorded after the sessions, not while they were open. Text outside the replies' arrays was not captured.
- The tester and the outside reviewer are the same model. ChatGPT models also assisted with other parts of the paper.
- The rulings are judgment. The two first sets agreed in 7 of 13 cases.
- The histories are not a sample from a defined population, and the tester read the rules and aimed at their gaps. The counts describe these histories. No interval is given.
