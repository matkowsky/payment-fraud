# Round 1 adjudication

Tester: ChatGPT (model shown: GPT-6) in a temporary chat, three replies of five cases each, from `PACKET_ROUND1.md` at commit `5dd4213`. The replies are stored unchanged as `reply_*.json`.

Three files record what happened, in order:
1. `RESULTS.md`: the checker's output on the rules as they stood before any change.
2. `RULINGS_CHECK_REPLY.txt`: a separate session's check of Claude's first rulings, from `RULINGS_CHECK_PACKET.md`, stored as received. Same model and environment as the tester (author, 11 November): ChatGPT, model shown GPT-6, temporary chat, memory off.
3. `RESULTS_AFTER_FIX.md`: the checker's output on the revised rules, with each changed draft given its new digest.

Claude wrote the rules and the first rulings, so the first rulings were not independent. The outside check agreed with 12 of 15 rulings and disagreed with 3 (R13, R14, R15). Claude checked each disagreement against the paper and the checker's code and accepted all three. The check also showed that Claude's first fix for R03 would not have closed the gap, and tightened the fixes for R01, R02 and R09.

## Counts

Before any change:
- 13 histories meant to break a requirement: 3 rejected (R05, R12, R14), 10 passed.
- 2 histories meant to be legitimate: both rejected.

Final rulings on the 10 that passed: 8 gaps in the rules (R01, R03, R06, R07, R08, R09, R11, R13) and 2 under limits the supplement already stated (R02, R04). Four of the eight need only a compromised agent (R01, R03, R06, R11).

After the rule changes: 9 of the 13 rejected; R04, R08, R09 and R13 still pass and are stated as limits; R15 is accepted; R10 is rejected by design.

## Rulings

| Case | Tier | Before | Final ruling | What was done | After |
|---|---|---|---|---|---|
| R01 | agent | passes | Gap | IR-09: a material presence or current-conduct claim needs an unlinked supporting observation whose event interval overlaps the claim's interval. The first proposal, every supporting observation, was too broad. | IR-09 |
| R02 | other | passes | Stated limit, now closed | IR-05: a run is partial when a source's ingestion watermark is earlier than the end of the requested interval. | IR-05 |
| R03 | agent | passes | Gap | IR-09: a supporting record linked to an agent output adds no root. The first proposal kept an exception that would have let this case through. | IR-09 |
| R04 | agent | passes | Stated limit | None. Section 4.2 says interfaces attach these links, so a rule is the consistent end state. | passes |
| R05 | other | IR-11 | Caught | None. | IR-11 |
| R06 | agent | passes | Gap, two parts | (a) IR-11: the version identifier is the digest of the draft's claims and is recomputed. (b) IR-09: a material presence or current-conduct claim needs an unlinked supporting observation. | IR-09; IR-11 as written |
| R07 | other | passes | Gap, minor | IR-07: a source observation is not learned before its event began. The schema has no class for a fact recorded ahead of its effective date; stated as a limit. | IR-07 |
| R08 | other | passes | Gap, needs a field | Stated as a limit: a query run does not record what was asked. | passes |
| R09 | other | passes | Gap, needs a field | Stated as a limit: release scope is free text. A fix must hold both the release and later reads to the scope. | passes |
| R10 | other | IR-14 | Rules stand | The design links by exposure (Sections 2.3 and 4.2). Section 1's statement of C3 now says that a record written while an agent output is open counts as informed. | IR-14 |
| R11 | agent | passes | Gap, minor | IR-09: every record a claim cites exists by the time the draft was written. | IR-09 |
| R12 | other | schema | Caught | None. | schema |
| R13 | other | passes | Gap, needs a field | Stated as two limits: a release carries no authenticated approval tied to the draft, and no record rule can show that the person read it. The first ruling called the whole case beyond any rule. | passes |
| R14 | other | IR-10 | Caught; rule text was wrong | The published IR-10 named linked features only, while the checker also excluded linked source observations. The text now says "a record linked to an agent output". | IR-09 |
| R15 | agent | IR-08 | False rejection | IR-08: one qualifying run is enough, and no cited run may have returned a matching record. The first ruling called this a judgment call. | passes |

## Not yet done

- Fields for the query's predicate, a structured release scope and an authenticated approval, with their rules.
- Round 2: a fresh tester against the revised rules.
