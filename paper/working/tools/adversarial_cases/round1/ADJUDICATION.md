# Round 1 adjudication (draft, 11 November 2026)

Tester: ChatGPT in a temporary chat, three replies of five cases each, from `PACKET_ROUND1.md` at commit `5dd4213`. The replies are stored unchanged as `reply_*.json`. Checker output: `RESULTS.md`.

This adjudication is Claude's. Claude wrote the rules being tested, so it is not independent. Each ruling should be checked by the author or by the tester.

## Counts

- 13 cases expected to be rejected: 3 caught (R05 and R14 by a rule, R12 by the schema); 10 pass.
- Of the 10 that pass: 7 are misses the rules could close, 2 fall under limits the supplement already states, 1 is a limit no record rule can close.
- 2 cases expected to be accepted: both rejected, as the tester predicted.
- Four of the seven misses need only a compromised agent (tier "agent").

## Rulings

| Case | Tier | Checker | Ruling | Reason | Proposed action |
|---|---|---|---|---|---|
| R01 | agent | passes | Miss | A current-conduct claim about 5 May rests on observations of 1 to 3 May. No rule compares a claim's interval with its support's event intervals. | Extend IR-09: a supporting observation's event interval overlaps the claim's interval. |
| R02 | other | passes | Stated limit | Ingestion watermark a month before the requested interval, status complete. S4.4 says the rules do not check ingestion lag. | Keep as a limit, or add a consistency check: a source's ingestion watermark is not earlier than its event watermark. |
| R03 | agent | passes | Miss | A human note linked to an agent output is cited as support and adds a second root. C3 says such a record "counts as dependent, not as independent corroboration". IR-10 excludes linked records; IR-09 does not. | Extend IR-09: a supporting record linked to an agent output adds no root except through an unlinked input. |
| R04 | agent | passes | Stated limit | The draft drops its context link to a released item the agent read in the same case. S4.4 says the rules do not check released-item links after a memory read. | Keep as a limit for now. Section 4.2 says interfaces attach these links, so a rule is the consistent end state. |
| R05 | other | IR-11 | Caught | Release dated before the draft existed. | None. |
| R06 | agent | passes | Miss, two parts | (a) The draft's content changes after release and its version hash does not; the rules treat the hash as a label. (b) A material presence claim with no supporting record passes every rule. Confirmed by a direct test. | (a) Define the hash as a digest of the draft's claims and recompute it in IR-11. (b) Extend IR-09: a material presence or current-conduct claim cites at least one supporting observation. |
| R07 | other | passes | Miss, minor | A source observation learned 17 days before its event. IR-07 orders learned times only for derived records. | Extend IR-07: a source observation is not learned before its event began. A fact recorded ahead of its effective date would need an exemption. |
| R08 | other | passes | Miss, needs a field | The store holds a matching record that a "complete" run did not return. The query-run record does not hold what was asked, so the rules cannot tell which stored records a run should have returned. | Add the query's predicate to QueryRun and a rule that a complete run returns every stored record that matches. |
| R09 | other | passes | Miss, needs a field | Release scope names another tenant; the item is read in a case outside it. Scope is free text and no rule reads it. | Give scope a structure (tenants, entities or case types) and add to IR-13: a read's case lies within the release scope. |
| R10 | other | IR-14 | Rules stand | A note written while a draft was open, with its link removed. The tester reads C3 as covering only records the output actually informed. The paper's rule is wider on purpose: interfaces link every record written while an output is open (Sections 2.3 and 4.2). | No rule change. Section 1's statement of C3 says "informed"; say there that exposure counts. |
| R11 | agent | passes | Miss, minor | A draft cites as contradicting a record learned 13 days after the draft was written. IR-09 checks learned time for support only. | Extend IR-09 or IR-02: every record a draft cites was learned or created by the draft's creation time. |
| R12 | other | schema | Caught | A run with no sources. | None. |
| R13 | other | passes | Limit no rule can close | The release record's free-text findings say nobody reviewed the draft. Rules can check that a person is named, not that the person reviewed. | State it in S4.4. |
| R14 | other | IR-10 | Caught | A source observation linked to an agent output as sole support for current conduct. | None. |
| R15 | agent | IR-08 | Judgment call | An absence claim cites one complete covering run and one partial run for another month. IR-08 as published requires every cited run to qualify. The tester says a supplementary run should not sink the claim. | Keep the strict rule and say so, or relax it to "at least one cited run qualifies and none returned a matching record". Author decides. |

## What this shows

- An outside tester, working from the published text only, got 10 of 13 violating histories past the rules.
- The most serious: a material presence claim that cites no evidence passes (R06b), and an agent-informed note counts as an independent root (R03).
- The rules were sound where the tester expected a gap in release timing (R05) and in current-conduct support (R14).
