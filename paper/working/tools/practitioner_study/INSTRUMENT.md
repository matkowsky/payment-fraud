# Practitioner study: the form, item by item

This is the full text of the online form (Supplement S8). It was fixed before the first response; any later change is a new commit with its reason. About 35 minutes; Part 7 is optional.

## Consent

This study tests a published specification of the records an AI agent needs to investigate payment abuse under human authority. It asks for your professional judgment on two short hypothetical cases and on what your field records today.

- It takes about 35 minutes. You may stop at any time.
- Questions marked with an asterisk (*) are required: eligibility, consent, Part 1 and the case questions in Parts 2 and 3. Each case question allows "Cannot tell". You may skip any other question.
- The form does not record your name or email. Do not name your employer, and do not share anything confidential or anything that would identify an organization or a person.
- Answers are reported only in aggregate. A free-text answer is quoted only if you allow it below, and only without identifying detail.
- Responses are kept until the paper is published in a journal, or for one year, whichever comes first, and then deleted. Aggregated results stay in the paper.
- You must be 18 or older and have at least two years of experience investigating fraud or abuse, or building systems for it.
- To be credited by name, email the author separately after you finish. That email is never linked to your answers.
- Please do not read Section 8 of the paper or Supplement S6 before you finish. The cases come from them.

C0. I have read the above and agree to take part. (Yes / No; No ends the form)

## Part 1: about you

P1. Your main role: investigator or analyst / fraud or risk data science / threat intelligence / trust and safety / engineering for fraud or risk systems / manager of one of these / other

P2. The organization whose practice you know best: payment processor or acquirer / card issuer or bank / marketplace or platform / fintech / vendor or consultancy / other

P3. Years of experience in fraud, abuse or risk: under 2 / 2 to 5 / 6 to 10 / more than 10

P4. Have you read Section 8 of the paper or Supplement S6? Yes / No

## Part 2: two cases, as many systems show them

Answer from what is shown. "Cannot tell" is a valid answer.

### Case A: a published key

A scan finds an API key that was published in a public code repository. You are asked whether it was misused.

- Earlier requests with this key came from one cloud region with a stable client fingerprint. A search of the key's requests over the past seven days returned only those.
- Nineteen minutes after publication, requests arrived through a residential proxy with a different fingerprint. In the same burst, someone created a webhook endpoint, changed the account's payout destination and moved payouts to a faster schedule. Assume the key allows these changes.
- The account's record shows that the new payout destination is also attached to two other accounts, from before the key was published.
- The platform's automated compromise check scored the account 30 minutes after publication and did not flag it.
- Payouts went out after the change. Thirty days later, no victim report or incident finding has been recorded for them.

A1. Was the request burst at 19 minutes the first misuse of this key? Yes / No / Cannot tell

A2. Did the compromise check miss evidence that was available to it when it scored the account? Yes / No / Cannot tell

A3. Does the shared payout destination show that the three accounts have one owner? Yes / No, not by itself / Cannot tell

A4. Does the absence of reports after 30 days indicate that the payouts were legitimate? Yes, weakly / No / Cannot tell

A5. Does the request burst at 19 minutes warrant investigation? Yes / No / Cannot tell

### Case B: linked storefronts

A risk model and a rejected application point to similar storefronts. You are asked whether four new merchant accounts, A to D, form one operation built to avoid dispute monitoring.

- Eleven storefronts share two templates and a statement-descriptor pattern, and settle through accounts A to D. A person who controls A also appears on a closed account and on the rejected application.
- Each account has 100 completed transactions in the period.
- Chargebacks recorded at each account: A 2, B 2, C 2, D 0.
- A combined chargeback-or-alert measure across the four accounts is 5 percent.
- A search for the controlling person across all merchant accounts found no accounts beyond A and the closed account.
- Two analyst notes, written by different analysts on different days, each say the four accounts look like one operation.
- Account C also had a payment blocked as suspected fraud. That payment has no chargeback.

B1. Is account D's chargeback rate lower than the others'? Yes / No / Cannot tell

B2. Does the combined 5 percent show that no account is above 5 percent on that measure? Yes / No / Cannot tell

B3. Does the search show that the controlling person has no other merchant accounts? Yes / No / Cannot tell

B4. Do the two analyst notes count as two independent confirmations? Yes / No / Cannot tell

B5. Should C's blocked payment count as a non-fraud transaction because it has no chargeback? Yes / No / Cannot tell

B6. Do the shared templates and descriptor pattern justify investigating the four accounts together? Yes / No / Cannot tell

## Part 3: the same cases, with the records added

The cases are unchanged. These records are now also available. Answer the same questions again; changing an answer is fine.

### Case A: added records

Each record is shown as the system stores it.

- Coverage of the seven-day search, written by the query service: requested 7 days before publication to now; evaluated 2 hours before publication to now; status partial.
- Learned times: link of the new payout destination to the two other accounts, effective before publication, learned 1 day after publication.
- Compromise check: scored 30 minutes after publication; inputs as of 30 minutes after publication.
- Outcome channels for these payouts: victim report, reporting window none defined; incident finding, reporting window none defined.

A1 to A5 again.

### Case B: added records

Each record is shown as the system stores it.

- Report-to-transaction links: 2 chargebacks recorded at a fifth account, X, linked to transactions of account D; link verified by transaction identifier.
- Chargeback-or-alert measure by account, each transaction counted once: A 8 of 100, B 8 of 100, C 2 of 100, D 2 of 100.
- Coverage of the search for the controlling person, written by the query service: 3 account sources; 1 source sampled at 10 percent; row limit reached; status partial and truncated.
- Exposure links: analyst note 1 and analyst note 2 each link to the agent's cluster assessment of accounts A to D, open in the case when the note was written.
- Decision record for C's blocked payment: decision block; effect on the chargeback channel closed.

B1 to B6 again.

## Part 4: how often these failures matter

In the last two years, how often have you seen each of these change a conclusion or a decision? Never / once / two to five times / more than five times / cannot say

F1. An outcome read as "no fraud" when a decision had blocked, refunded or reversed the item, or when the reporting window had not closed.

F2. "Nothing found" taken from a search that was incomplete, truncated, sampled or not yet loaded.

F3. A fact treated as known at a time before the system had actually learned it.

F4. Two notes, labels or reports counted as independent when one rested on the other or on the same tool output.

F5. Optional: one example, in general terms only.

## Part 5: what your field records today

For the organization whose practice you know best. Skip any item that would disclose something confidential.

For each record: is it recorded today? Yes / partly / no / don't know. How hard would it be to add? Easy / moderate / hard / not feasible / don't know.

R1. For each protective decision (block, refund, hold, reversal), its effect on each later outcome channel, such as "chargebacks no longer possible" or "reports delayed".

R2. For each search or query, what it actually covered (sources, time range, gaps, sampling, truncation), written by the system rather than the analyst.

R3. For each fact, when the system learned it, kept separately from when it happened.

R4. A person's release decision before an automated or agent conclusion is reused in later cases.

R5. Links from each label or analyst note to the automated or agent outputs open when it was written.

## Part 6: signals the cases use

Is this typically available to an investigator at decision time? Yes / partly / no / don't know

S1. Reuse of onboarding attributes across accounts, with hard and soft identifiers kept apart.
S2. Observation that a key was exposed (repository, package, image, page or log).
S3. Each key's normal behavior, and its first use after exposure.
S4. Payout-destination history: added or changed, first seen, validation, ownership match.
S5. The same payout destination on several accounts.
S6. Dispute and refund measures for a beneficial owner or cluster of accounts.
S7. Pre-dispute alert resolutions kept separately from disputes.
S8. The link from a storefront to a merchant identifier, and why the identifier is believed to belong to it.
S9. Request context: credential or session, endpoint, network, fingerprints, user agent.
S10. Each label event with its source: dispute, early fraud warning, refund, payout return, charge-off, complaint, victim report or incident finding.
S11. Account-level protective actions: payout block, hold, pause or schedule change, key restriction or rotation, token freeze.

## Part 7 (optional, about 5 minutes): who does this work

In the organization whose practice you know best, which team usually does each? Fraud or abuse operations / risk data science / threat intelligence / trust and safety / engineering / compliance / no one / don't know

O1. Tasking and scoping investigations.
O2. Routing work to tools and specialists.
O3. Searching earlier released intelligence.
O4. Specialist analysis.
O5. Learning what data exists and what it means.
O6. Controlling which tools and queries an investigator or agent may use.
O7. Keeping the evidence store.
O8. Testing hypotheses against data.
O9. Extracting and matching entities.
O10. Correlating related accounts and activity.
O11. Tracking actors and activity groups.
O12. Describing techniques, tools and infrastructure.
O13. Tracking vulnerabilities and abusable conditions.
O14. Keeping a structured store of threat knowledge.
O15. Hunting for undetected abuse.
O16. Building and validating detections.
O17. Feeding threats into threat models.
O18. Writing recommendations for product or customer action.
O19. Writing finished intelligence.
O20. Keeping evidence lineage.
O21. Independent quality review before release.
O22. Releasing conclusions for reuse.
O23. Testing lessons before they are reused.
O24. Securing the investigation tools themselves.

## Part 8: your view

V1. What record or step is missing?
V2. What would be hardest to adopt, or not feasible, and why?
V3. Is anything in the cases or records wrong or unrealistic?
V4. May your free-text answers be quoted without identifying detail? Yes / No
