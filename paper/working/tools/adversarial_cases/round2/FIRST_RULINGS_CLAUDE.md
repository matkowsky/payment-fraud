# Round 2: Claude's proposed rulings on the thirteen disputed cases

Prepared by Claude, 15 November 2026 (Asia/Jerusalem). PROPOSED, not confirmed. The plan says the author confirms every ruling.

Claude wrote the rules, so these rulings are not independent. In round 1 an outside check corrected three of Claude's fifteen first rulings, each time toward the tester. Where a case is a close call, the ruling below goes against the rules and the other reading is stated.

Texts used: manuscript and supplement as they stood at the freeze commit `58150e8`. Checker output: `round2/RESULTS.md` (PR #82), identical at the freeze commit. Diagnostics named below were run with the frozen checker and changed no file.

## What the frozen checker did (fact, not a ruling)

- Meant to break a requirement: 12. Rejected: 2 (R03 by the schema, R07 by IR-12). Pass: 10.
- Meant to be legitimate: 3. Rejected: 3 (A01 by IR-14, A02 by IR-08, A03 by IR-11).

## Proposed counts

- Of the 10 that pass: 10 new failures, 0 under limits stated before the freeze.
  - Three need only a compromised agent: R02, R05, R09.
  - Three are minor: R02, R08, R11. One is caught by the fifteenth rule, XR-01, which the plan's command does not run: R05.
- Of the 3 legitimate cases: 1 falsely rejected (A02). Two rejections stand (A01, A03).

## Range if the close calls go the other way

| Reading | Rejected of 12 | New failures | Not a breach | False rejections of 3 |
|---|---|---|---|---|
| Proposed (strict on the rules) | 2 | 10 | 0 | 1 |
| Most favourable to the rules | 2, or 3 with XR-01 | 6 | 3 (R02, R08, R11) | 1 |
| Least favourable | 2 | 10 | 0 | 2 (A01 added) |

Under every reading the frozen rules reject at most 3 of the 12, and at least 6 cases are new failures.

## Cases meant to break a requirement that pass

| Case | Tier | Proposed ruling | Basis in the paper's text | The other reading |
|---|---|---|---|---|
| R01 | other | New failure | C3: no agent output enters the evidence plane as evidence of the activity. Section 5.3: agent proposals "cannot support current-conduct claims without their underlying observations". The checker never looks at the kind of a record's producer, so an observation produced by the agent counts as an independent root. | None found. |
| R02 | agent | New failure, minor | C3: a released conclusion serves "only as a hypothesis or context". Section 6.4: the checker "rejects substitution of organizational memory for observations", and a claim lists "the retrieved records that count against it". IR-09 bars a released item from support only. Nothing checks what a claim cites against itself. | Not a breach: a record listed against a claim cannot raise its support, so nothing is corroborated. |
| R04 | other | New failure | C2: coverage is "what a query actually covered". Section 6.2: the gateway records the evaluated entities. A run that says it evaluated only ACC-2 returns records about ACC-1. IR-06 checks returned records for time only. The stated limit about whether a returned record "bears on a claim" is a different matter: here the run contradicts itself. | None found. |
| R05 | agent | New failure of the fourteen rules; caught by XR-01 | Section 6.4: a claim that relies on an unreported outcome cites the channel state "at the read time". IR-09 lists support, contradiction, context and query runs, not outcome readings, and the checker's fourteen rules never read the two outcome fields. Diagnostic: the joint check rejects this history under XR-01 ("a cited reading does not exist or was taken after the draft"). XR-01 is stated in S4.4 and was in the frozen file, but it is outside the fourteen rules the tester was given and outside the plan's command. | Count it as rejected by the specification, since XR-01 existed at the freeze. The plan freezes IR-01 to IR-14 and one command, so the proposed ruling does not. |
| R06 | other | New failure; an exact fix needs a field | C3 as stated in Section 1 has no entity condition: a record written while an agent output is open to its writer counts as informed. Section 4.2 and S4.1 scope the link by "the writer's case or session". IR-14 scopes it by entity, which the paper does not say. Diagnostic: the same note about ACC-1 is rejected by IR-14. The schema has no case or session on a note or an exposure. | Not shown to be a breach: the records do not say the note was written in the case where the draft was open. |
| R08 | other | New failure, minor | A record learned on 19 May carries a link to a draft written on 20 May. One of the two is false, so the history does not keep a true learned time or a true dependence. IR-07 orders a record after its inputs; nothing orders it after a linked output. | Not a breach: a false link only makes a record dependent, which is the safe direction for C3. |
| R09 | agent | New failure | Section 6.4 speaks of support "for each named entity" and of claims "about named entities". The claim names ACC-2 with no observation and no query coverage of ACC-2. IR-09 asks only that each supporting record be about some named entity. Related to item 29 of the 14 November review (IR-10 and entities), which is held until this round is ruled. | None found. |
| R10 | other | New failure; the fix needs a decision | Abstract: "an incomplete search cannot establish absence". Section 6.2: "An unavailable dataset means the intended test did not occur." The claim cites a run over the same account, interval and cutoff whose source was unavailable. IR-08 counts a cited run against a claim only if it returned a record. Diagnostic: citing the unavailable run alone is rejected. | A claim names no sources, so the unavailable source may not bear on it. Then the schema lacks a field, and by the plan's 14 November change a limit stated after the freeze still counts as a new failure. |
| R11 | other | New failure, minor | Section 5.3: only a person releasing a reviewed draft adds a claim to organizational memory. The item enters memory a day after its release expired. IR-12 has no upper bound in time. Diagnostic: any read of the item is rejected by IR-13, so it cannot be used. | Not a breach: release did come before promotion, and expiry governs use, which IR-13 enforces. |
| R12 | other | New failure | The draft of 20 May claims absence in April and itself lists, against the claim, an observation of the same account in that interval learned on 19 May. Its only run has a 6 May cutoff. IR-08 looks only at records the cited runs returned. | None found. |

No case falls under a limit stated before the freeze. Checked against each: links after a memory read; whether a returned record bears on a claim; ingestion watermark against the cutoff; what a query asked; free-text release scope; unauthenticated approval; whether the person read the draft; a fact recorded ahead of its effective date; an unreported outcome a claim does not list.

## Cases meant to be legitimate that are rejected

| Case | Rule | Proposed ruling | Basis in the paper's text | The other reading |
|---|---|---|---|---|
| A01 | IR-14 | Rules stand | S4.1, assessment store: "Retain the model or reviewer identity and version", and record "the writer's case or session". Section 4.2 attaches links by what is open to the writer. A note with no writer cannot be tested against that clause of C3 at all. | False rejection: Section 6.4 says a record without a producer "counts as dependent and adds no root", and this note keeps its link, so nothing C3 protects is lost in this history. This is the closest call of the three. |
| A02 | IR-08 | False rejection | Section 6.4: an absence claim cites "the query runs whose coverage records support it", in the plural. Two complete, empty runs with the same cutoff, source and account cover the interval together. IR-08 asks for one run that covers all of it. | The single-run condition is a deliberate simplification. It still rejects a history the paper's text supports. |
| A03 | IR-11 | Rules stand | Section 6.4: "Release preserves the assessment's uncertainty." Raising a claim's confidence at release does not. The tester saw only the Section 1 statement of C3, which does not say this. | False rejection, if the Section 1 statement alone is the test. Then the gap is in that statement, not in the rule. |

## What this means for the paper, if the rulings are confirmed

- Round 1's nine of 13 was in-sample. On held-out cases the revised rules reject 2 of 12, and every case that passes is a new failure.
- The Section 1 sentence on the adversarial test and S4.4 would have to say so. No text has been changed.
- Fixes and new stated limits come after the rulings. Each is first reported as a round 2 miss, as the plan requires.

## Not done

- No outside check of these rulings. Round 1 had one, in a separate ChatGPT session. The round 2 plan does not require it.
- No rule, checker or paper text changed. No `ADJUDICATION.md` committed.
