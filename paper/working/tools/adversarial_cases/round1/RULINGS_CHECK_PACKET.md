# Check of rulings: adversarial test of record rules, round 1

You are an independent reviewer. Use only this packet. Do not use memory of earlier chats, files,
the web or any other source.

A specification for AI-agent investigations on a payment platform states two requirements (C2 and
C3) and checks stored records against fourteen rules. An outside tester wrote 15 test histories.
Thirteen were meant to break a requirement and still pass the rules. Two were meant to be
legitimate and still be rejected. The histories were run through the checker. The author of the
rules then ruled on each case. That author is not independent, so the rulings need checking.

For each case, say whether the ruling is right and whether the proposed action is sound.

## Answer format

One line per case and nothing else:

`R01 | ruling: agree | action: sound | one sentence of reason`

- ruling: `agree` or `disagree`. If you disagree, say what the ruling should be.
- action: `sound`, `too narrow`, `too broad` or `none needed`. If not sound, say what would be.

## The two requirements, as the paper states them

> **C2** records query coverage and learned time. Query coverage is what a query actually covered: the data and period it examined, and whether its result was complete. Learned time is when a fact became available to the system's queries. Every query passes through a gateway, a checkpoint outside the agent, which records its coverage. Every fact keeps both when it happened and when the system learned it (Sections 5.1, 5.3 and 6.2).

> **C3** requires human release before promotion into organizational memory. No agent output enters the evidence plane, which stores observations, as evidence of the activity under investigation (Sections 4.2 and 5.3); the agent's own outputs are recorded only as observations of what the agent did (Supplement S4.1). A person releases a conclusion into organizational memory, where it serves only as a hypothesis or context. Any record that an agent output informed links back to that output and counts as dependent, not as independent corroboration (Sections 4.2, 6.4 and 7.3).

## The fourteen rules

1. IR-01: a record identifier is used once.
2. IR-02: every record a record cites exists, and a cited query run is a query run.
3. IR-03: a gateway that is not the requester records a query run's coverage.
4. IR-04: the evaluated entities and interval lie within those requested, and the as-of cutoff is not after the query.
5. IR-05: a run's statuses follow from its coverage fields. By Section 6.2's source rules, a run is partial when a source was sampled, has a known gap in the requested interval, or does not reach from its retention horizon to its event watermark across that interval, and truncated when a limit was reached. Two rules are added here: a narrower evaluated scope or access filtering also gives partial. A denied or unavailable source gives that status. A run is complete only when nothing else applies.
6. IR-06: a run returns only records learned by its as-of cutoff whose event intervals overlap the evaluated interval.
7. IR-07: a derived record is learned no earlier than its inputs, and its root observations are exactly its inputs' roots. Only a source observation, score or decision can be its own root.
8. IR-08: an absence claim cites at least one query run, and each cited run is complete, not scope-limited, returned nothing and covers the claim's entities and interval.
9. IR-09: a claim's support consists of observation records about the claim's entities, learned by the time the draft was written, and its count of distinct roots equals the number of distinct root observations among them. A released conclusion or a draft is never support.
10. IR-10: a current-conduct claim cites an observation or derived feature whose event interval falls within the current period. A score or decision does not count, and a feature linked to an agent output counts only through an unlinked current-period input.
11. IR-11: a person releases the exact draft version, before the draft expires, without raising any claim's confidence.
12. IR-12: a conclusion enters memory only after a decision that released that claim.
13. IR-13: memory is read only from a released item, between its creation and its release's expiry.
14. IR-14: a note names its author. A record its author wrote about an entity while an agent output about that entity was open links to that output, and a record derived from a linked record keeps the link.

## Limits the supplement already states

The rules do not check released-item links on records written after a memory read, the lag between a run's cutoff and a source's ingestion watermark, or whether a returned record bears on a claim.

## Sentences from the paper that the rulings rely on

- Section 6.4: "Each material claim cites supporting records with their classes, event intervals and root observations, reached through lineage."
- Section 4.2: "Labeling, assessment, control, detection and threat-knowledge interfaces automatically attach every agent output and every released organizational-memory item open in the writer's case or session."
- Section 2.3: "Because the interfaces that write these records add the links, they also cover a person who writes a record while an agent output is open in the case, part of the relay the threat-detection design leaves open; a missing link still does not establish independence (Section 4.2)."

## The valid history the cases change

One investigation with three query runs, a draft (DR-1) with a current-conduct claim (CL-1) and an absence claim (CL-2), a human note (O-5) written while the draft was open and linked to it, a release (RL-1) by a second person, a released item (M-1), and a later case whose draft (DR-2) reads the released item as context and cites a new observation (O-6).

## The cases

### R01

- Tester expected the rules to **reject** it. Tier: agent. Requirement said to be broken: C2.
- Tester's reason: CL-1 now asserts current conduct on May 5, after Q-1's evaluated interval ends, although every supporting observation concerns May 1–3. IR-09 checks entity identity and learned time, while IR-10 requires evidence only somewhere within the broader current period, so neither checks whether the evidence or query coverage supports the claimed interval. The unsupported conclusion is subsequently released into memory.
- Checker: passes.
- Ruling: **Miss**. No rule compares a claim's interval with the event intervals of its supporting records.
- Proposed action: Extend IR-09: each supporting observation's event interval overlaps the claim's interval.

### R02

- Tester expected the rules to **reject** it. Tier: other. Requirement said to be broken: C2.
- Tester's reason: Q-2 retains complete status and returns no records for April despite its source ingestion watermark being March 31, before the entire requested interval. The released absence claim therefore relies on coverage that cannot establish the claimed absence. This exploits the explicitly stated limit that the rules do not check ingestion-watermark lag.
- Checker: passes.
- Ruling: **Stated limit**. The supplement says the rules do not check ingestion-watermark lag.
- Proposed action: Keep as a limit, or add a consistency check: a source's ingestion watermark is not earlier than its event watermark.

### R03

- Tester expected the rules to **reject** it. Tier: agent. Requirement said to be broken: C3.
- Tester's reason: DR-2 treats O-5, a human note explicitly linked to the earlier agent output DR-1, as an additional independent supporting root for current conduct. IR-09 counts O-5's inherited root O-1 alongside O-6 without excluding agent-influenced notes, while IR-10 passes because O-6 independently satisfies its current-period test. Agent-influenced material is therefore reused as corroborating evidence rather than merely dependent context.
- Checker: passes.
- Ruling: **Miss**. C3 says a record an agent output informed "counts as dependent, not as independent corroboration". IR-10 excludes linked records; IR-09 still counts their roots.
- Proposed action: Extend IR-09: a supporting record linked to an agent output adds no root except through an unlinked input.

### R04

- Tester expected the rules to **reject** it. Tier: agent. Requirement said to be broken: C3.
- Tester's reason: DR-2 conceals its originally declared dependence on released conclusion M-1 by removing that context reference, even though MR-1 still records the same agent reading M-1 for K-2 shortly before drafting. The rules validate recorded memory reads but do not require subsequent drafts to disclose reliance on material read from memory. This exploits the stated limit concerning downstream links after memory reads.
- Checker: passes.
- Ruling: **Stated limit**. The supplement says the rules do not check released-item links on records written after a memory read.
- Proposed action: Keep as a limit for now; a rule would match Section 4.2.

### R05

- Tester expected the rules to **reject** it. Tier: other. Requirement said to be broken: C3.
- Tester's reason: RL-1 is backdated to May 5, before DR-1 was created on May 6 and before its supporting queries ran. A person cannot meaningfully review and release an exact draft version that does not yet exist. IR-11 checks the reviewer, version equality, confidence and expiry but does not explicitly require the decision to follow draft creation; IR-12 still sees M-1 created after the purported release.
- Checker: rejected by IR-11.
- Ruling: **Caught**. The checker rejects a release dated before the draft existed.
- Proposed action: None.

### R06

- Tester expected the rules to **reject** it. Tier: agent. Requirement said to be broken: C3.
- Tester's reason: The agent changes CL-2 from absence to presence after human approval, leaving the version_hash unchanged. IR-11 compares stored version identifiers but does not independently verify that the draft content matches its hash, so RL-1 appears to authorize the opposite conclusion from the one the human reviewed. The unsupported presence claim also bypasses IR-08.
- Checker: passes.
- Ruling: **Miss, two parts**. (a) The rules treat the version hash as a label and never recompute it. (b) A material presence claim with no supporting record passes every rule.
- Proposed action: (a) Define the hash as a digest of the draft's claims and recompute it in IR-11. (b) Extend IR-09: a material presence or current-conduct claim cites at least one supporting observation.

### R07

- Tester expected the rules to **reject** it. Tier: other. Requirement said to be broken: C2.
- Tester's reason: O-6 now claims that the system learned an observation on May 1 even though the observed activity did not occur until May 18. C2 requires meaningful event and learned times, but IR-07 checks learned-time ordering only for derived records, not whether a source observation was supposedly learned before its underlying event occurred.
- Checker: passes.
- Ruling: **Miss, minor**. IR-07 orders learned times only for derived records.
- Proposed action: Extend IR-07: a source observation is not learned before its event began, with an exemption for a fact recorded ahead of its effective date.

### R08

- Tester expected the rules to **reject** it. Tier: other. Requirement said to be broken: C2.
- Tester's reason: A source observation for April, already learned before Q-2's cutoff, exists in the store, yet Q-2 still reports complete coverage and zero results. IR-06 constrains records that were returned but does not require a complete query to return all eligible observations; IR-08 therefore accepts an absence claim despite the omitted matching record.
- Checker: passes.
- Ruling: **Miss, needs a field**. The query-run record does not hold what was asked, so the rules cannot tell which stored records a complete run should have returned.
- Proposed action: Add the query's predicate to QueryRun and a rule that a complete run returns every stored record that matches.

### R09

- Tester expected the rules to **reject** it. Tier: other. Requirement said to be broken: C3.
- Tester's reason: The human release is explicitly scoped to tenant T2, while CL-1 concerns tenant T1 and its released item M-1 is subsequently consumed in a T1 investigation. C3's human authorization cannot legitimately cover promotion and reuse outside the approved scope, but IR-11 through IR-13 never verify that a release's scope includes the conclusion or its downstream use.
- Checker: passes.
- Ruling: **Miss, needs a field**. Release scope is free text and no rule reads it.
- Proposed action: Give scope a structure and add to IR-13: a read's case lies within the release scope.

### R10

- Tester expected the rules to **accept** it. Tier: other. Requirement said to be broken: none.
- Tester's reason: O-5 is an independently authored human note based solely on source observation O-1, despite being written while DR-1 happened to be open. C3 requires provenance links for records actually informed by agent output, not every independent record written during an exposure. IR-14 nevertheless rejects this history because it treats overlapping exposure as sufficient proof of dependence.
- Checker: rejected by IR-14.
- Ruling: **Rules stand**. The paper links by exposure on purpose: every record written while an agent output is open is linked (Sections 2.3 and 4.2, quoted below). The tester read C3 as covering only records the output actually informed.
- Proposed action: No rule change. Make Section 1's statement of C3 say that exposure counts.

### R11

- Tester expected the rules to **reject** it. Tier: agent. Requirement said to be broken: C2.
- Tester's reason: DR-1 lists O-6 as contradicting evidence even though O-6 was learned on May 19, thirteen days after the draft was created. C2 requires learned time to constrain which facts could have informed an investigation. IR-09 checks learned time for supporting records but not contradicting records, allowing the agent to present future evidence as if it were known when drafting.
- Checker: passes.
- Ruling: **Miss, minor**. IR-09 checks learned time for supporting records only.
- Proposed action: Every record a draft cites was learned or created by the draft's creation time.

### R12

- Tester expected the rules to **reject** it. Tier: other. Requirement said to be broken: C2.
- Tester's reason: Q-2 now examines zero data sources but still reports complete coverage and no results. An empty-source query cannot establish the absence of activity during April. IR-05 defines incompleteness through properties of listed sources but does not explicitly require at least one evaluated source, while IR-08 accepts the resulting complete, empty query as absence evidence.
- Checker: rejected by the schema.
- Ruling: **Caught**. The schema rejects a run with no sources.
- Proposed action: None.

### R13

- Tester expected the rules to **reject** it. Tier: other. Requirement said to be broken: C3.
- Tester's reason: The release record explicitly states that approval was automatic and H-2 neither reviewed nor authorized it. C3 requires an actual human release before organizational-memory promotion, not merely a human identifier attached to an automated decision. IR-11 checks that decided_by identifies a human but does not validate reviewer findings or whether the person genuinely authorized release.
- Checker: passes.
- Ruling: **Limit no rule can close**. Rules can check that a person is named, not that the person reviewed. Free text is not read.
- Proposed action: State this limit in the supplement.

### R14

- Tester expected the rules to **reject** it. Tier: other. Requirement said to be broken: C3.
- Tester's reason: O-6 is now explicitly linked to the earlier agent output DR-1, yet remains classified as a source observation and is the sole supporting record for CL-3. C3 requires agent-influenced records to remain dependent rather than count as independent evidence of investigated activity. IR-09 counts O-6's own root, and IR-10's special restriction on linked evidence applies to derived features but not source observations, allowing this contaminated source to establish current conduct.
- Checker: rejected by IR-10.
- Ruling: **Caught**. The checker excludes a linked source observation as sole support for current conduct.
- Proposed action: None.

### R15

- Tester expected the rules to **accept** it. Tier: agent. Requirement said to be broken: none.
- Tester's reason: CL-2 cites both Q-2, which completely covers April and returns nothing, and Q-3, a separately recorded partial investigation of May. The additional, transparently documented May query does not invalidate Q-2's complete April coverage or the absence conclusion, so C2 and C3 remain satisfied. IR-08 nevertheless rejects the claim because it requires every cited run, including supplemental runs, to be individually complete, empty and covering the entire claim interval.
- Checker: rejected by IR-08.
- Ruling: **Judgment call**. IR-08 as published requires every cited run to be complete, empty and covering. The tester says a supplementary partial run should not sink the claim.
- Proposed action: Either keep the strict rule and say so, or relax it to "at least one cited run qualifies and none returned a matching record".
