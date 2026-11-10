# Second-coder packet: which signals does each mechanism need?

You are an independent rater. Use only this packet. Do not use memory of earlier chats, files, the web or any other source. If you recognize the project this comes from, say so and still answer only from the packet.

A "mechanism" is a way of abusing a multi-product payment platform. A "signal" is a kind of record the platform could keep. Your task is to decide, for each mechanism, which signals it should be linked to under the rule below.

## The rule

Link a mechanism to a signal when BOTH hold:

1. An investigator examining that mechanism would need the signal's record to test whether the
   mechanism occurred, or to tell it apart from legitimate activity.
2. At least one of the sources listed under the mechanism describes behaviour that the signal would
   record. If you link on reasoning alone, without such a source, mark the link "inference".

Do not link a signal only because it is generally useful. Link every signal that meets the rule and
no others.

How to apply the rule:

- A source from another setting (another platform, another industry) counts for rule 2 when it
  describes the same behaviour.
- Some sources are public interface schemas. Their scope says "capability premises": the schema shows
  that an account can create or change the thing the mechanism abuses. Such a source supports a
  signal that records that creation or change.
- Signals of any class may be linked: observations, derived features, model outputs, control
  outcomes and external knowledge.
- A derived feature and the observations it is computed from are separate signals. Link each one
  that meets the rule by itself. Do not link an observation only because a linked feature uses it.
- A mechanism with "Sources: none recorded" cannot meet rule 2. Apply rule 1 only and mark every
  link "inference".

For each mechanism also answer whether a record is missing. Answer "missing" only when the test in
rule 1 could not be made at all with the listed signals. A record that would merely help is not
missing.

## Answer format

One line per mechanism. If you recognize the project, say so in one sentence before the lines. Add nothing else:

`M01 | SIG-xx, SIG-yy (inference), SIG-zz | missing: none`

Write `missing: <the record that is absent>` if rule 1 needs a record the list lacks. Write `M01 | none | missing: none` if no signal meets the rule.

## Signals

| ID | Signal | Family | Class |
|---|---|---|---|
| SIG-01 | Onboarding identity and business submissions (stored as claims with source and time) | Identity and onboarding | source observation |
| SIG-02 | Identity-verification decision and reason codes | Identity and onboarding | control outcome |
| SIG-03 | Capture-session context (device, camera pipeline, emulator or injection indicators) | Identity and onboarding | source observation |
| SIG-04 | Cross-account reuse of onboarding attributes (hard versus soft identifiers, with confounders) | Identity and onboarding | derived feature |
| SIG-05 | Declared versus observed business category mismatch | Identity and onboarding | derived feature |
| SIG-06 | Evidence-supported links between closed and newly opened accounts | Identity and onboarding | derived feature |
| SIG-50 | Account age at first sensitive use; dormancy-to-activation and ownership-change patterns | Identity and onboarding | derived feature |
| SIG-07 | Login attempt (network, ASN, user agent, TLS client fingerprint, outcome) | Authentication, session and operator administration | source observation |
| SIG-08 | Breached-credential match at login (feature, secrets not stored) | Authentication, session and operator administration | derived feature |
| SIG-09 | Challenge and MFA decision; reviewed outcome if available | Authentication, session and operator administration | control outcome |
| SIG-10 | MFA, recovery and support-initiated resets with acting staff identity | Authentication, session and operator administration | source observation |
| SIG-11 | Session or link issuance context versus use context | Authentication, session and operator administration | derived feature |
| SIG-12 | Device or browser fingerprint match (weak evidence; cloneable) | Authentication, session and operator administration | derived feature |
| SIG-13 | SSO and identity-provider configuration change | Authentication, session and operator administration | source observation |
| SIG-14 | User, role and invite changes | Authentication, session and operator administration | source observation |
| SIG-15 | Key exposure observation (repository, package, image, page, log) | Credentials, API keys and request context | external threat knowledge |
| SIG-16 | Per-key behavioral baseline and first use after exposure | Credentials, API keys and request context | derived feature |
| SIG-17 | OAuth application and automation-object creation events | Credentials, API keys and request context | source observation |
| SIG-18 | Payout-destination lifecycle (added or changed, first-seen, validation, ownership match) | Funds movement and payout destinations | source observation |
| SIG-19 | Payout-schedule and notification-setting changes | Funds movement and payout destinations | source observation |
| SIG-20 | Destination reuse across accounts | Funds movement and payout destinations | derived feature |
| SIG-21 | Inbound-to-outbound dwell time per account | Funds movement and payout destinations | derived feature |
| SIG-22 | Recipient first-seen and recipient change before outbound payment | Funds movement and payout destinations | source observation |
| SIG-23 | Per-account temporal baseline with explicit label-delay fields (volume, ticket size, refunds, disputes, payout acceleration) | Funds movement and payout destinations | derived feature |
| SIG-24 | Dispute and refund metrics at beneficial-owner or cluster level | Funds movement and payout destinations | derived feature |
| SIG-25 | Pre-dispute alert resolutions recorded separately from disputes | Funds movement and payout destinations | control outcome |
| SIG-26 | Inbound-credit concentration and onward-transfer timing per connected account, with any linked scam reports | Funds movement and payout destinations | derived feature |
| SIG-27 | Authorization attempt (decline and response code, BIN, card fingerprint, merchant, acquiring bank, static statement descriptor, device, amount); 3-D Secure result and separately reported liability-shift status; transaction identifier and completion/capture state | Payment attempts, authorization and payment controls | source observation |
| SIG-28 | Enumeration features over windows at merchant, BIN and platform level (includes probing of inconsistent field checks) | Payment attempts, authorization and payment controls | derived feature |
| SIG-29 | Merchant-level charge profile (small, repeated, failing charges; billing-address churn) | Payment attempts, authorization and payment controls | derived feature |
| SIG-30 | Buyer-seller identity overlap | Payment attempts, authorization and payment controls | derived feature |
| SIG-31 | Storefront and domain observations (age, registration, template fingerprint, referral channel) | Merchant storefront and business claims | external threat knowledge |
| SIG-32 | Storefront-to-merchant identifier relation with namespace and why the identifier is believed to belong to the entity | Merchant storefront and business claims | derived feature |
| SIG-33 | Platform risk assessments (fraudulent merchant or website signals with risk level and indicators) | Platform outputs and labels | model or risk output |
| SIG-51 | Account rejection action with reason (request parameter supplied by the rejecting platform) and resulting disabled reason | Platform outputs and labels | control outcome |
| SIG-34 | Agent tool call with provenance of every input that reached the model | Agents, tools and approvals | source observation |
| SIG-35 | Tool-manifest version and hash change | Agents, tools and approvals | source observation |
| SIG-36 | Approval event with approved payload hash (including the tool-manifest version and hash in force at approval), token issued, executed payload hash, and the tool-manifest version and hash in force at execution | Agents, tools and approvals | control outcome |
| SIG-37 | OAuth client registration, consent and session lifecycle for agent integrations | Agents, tools and approvals | source observation |
| SIG-38 | Agent identity assertion and verification outcome (signed requests) | Agents, tools and approvals | control outcome |
| SIG-39 | Memory or skill write from untrusted input | Agents, tools and approvals | source observation |
| SIG-40 | Egress decision for assistant and tool traffic (allowlist, post-resolution checks) | Agents, tools and approvals | control outcome |
| SIG-47 | Delegated payment credential issuance, scope and use (amount, merchant, expiry; local session exposure) | Agents, tools and approvals | source observation |
| SIG-48 | Event-destination and webhook-endpoint creation and change events | Credentials, API keys and request context | source observation |
| SIG-49 | Lookalike-domain and phishing-infrastructure observations, including reported network addresses, targeting the platform brand | External threat knowledge | external threat knowledge |
| SIG-41 | Compromised-card intelligence with validity windows (including issuer flags after testing) | External threat knowledge | external threat knowledge |
| SIG-42 | On-chain exposure of destination wallets and cross-ledger links | External threat knowledge | external threat knowledge |
| SIG-43 | Onramp session (payment method, KYC tier, destination wallet, delivery time) | Payment attempts, authorization and payment controls | source observation |
| SIG-52 | Post-access change sequence: new application or application secret, automation object, MFA factor, user, identity provider, notification or inbox rule, or event destination created after an access event, and the actions that follow | Authentication, session and operator administration | derived feature |
| SIG-53 | Stealer-log and credential-market observations (credentials, cookies, session tokens, fingerprints; theft time; source) | External threat knowledge | external threat knowledge |
| SIG-54 | Account registration attempt context (email, network, user agent, device session, form timing, signup-flow completeness) for platform and end-customer accounts | Identity and onboarding | source observation |
| SIG-55 | Session and link lifecycle: issuance, redemption and use (session or link identifier, network, device, action) | Authentication, session and operator administration | source observation |
| SIG-56 | API or web request context (credential or session identifier where present, endpoint, network, HTTP and TLS fingerprint, user agent, request signature, result) | Credentials, API keys and request context | source observation |
| SIG-57 | Funds movement event (inbound credit, outbound transfer or payment, payout, on-chain transfer where applicable; amount, counterparty, time) | Funds movement and payout destinations | source observation |
| SIG-58 | Label event with provenance (dispute, early fraud warning, refund, payout return or recall, charge-off, complaint, victim report, incident finding, investigator or platform abuse label, business-reported outcome): source, label type, attribution level, gate passed, arrival time and lag, channel clock-start and reporting-window reference, report-status history, and links to evaluation maturity settings and any assessment that the report may be mistaken or deliberately false | Platform outputs and labels | source observation |
| SIG-59 | Compromised-card match per attempt (card present in compromised-card intelligence within its validity window) | Payment attempts, authorization and payment controls | derived feature |
| SIG-60 | End-customer login activity reported by the business (device session or IP, user agent, referrer) | End-customer lifecycle and entitlement | source observation |
| SIG-61 | Billing lifecycle per end customer (trial start with saved payment method, conversion, cancellation, discount or promotion applied, usage accrued, upcoming invoice, invoice paid, failed or uncollectible) | End-customer lifecycle and entitlement | source observation |
| SIG-62 | End-customer identifier reuse and clustering (email, IP, device, payment instrument; hard versus soft; reuse window and scope recorded) | End-customer lifecycle and entitlement | derived feature |
| SIG-63 | Concurrent-location use of one end-customer account | End-customer lifecycle and entitlement | derived feature |
| SIG-64 | Refund and dispute history per end customer, by label type | End-customer lifecycle and entitlement | derived feature |
| SIG-65 | Unpaid accrued exposure per end customer (usage accrued since the last successful payment versus projected invoice) | End-customer lifecycle and entitlement | derived feature |
| SIG-66 | Platform risk outputs for payments and end customers (payment risk level or score; fraudulent_payment, fraudulent_dispute and early_fraud_warning likelihoods; user_multi_accounting; user_account_sharing; non_payment_abuse; account_farming_risk_level) with model identity and version | Platform outputs and labels | model or risk output |
| SIG-67 | Business decision on end-customer activity/exposure: allow, restrict, block, trial gate, early invoice, prepayment or pause | End-customer lifecycle and entitlement | control outcome |
| SIG-68 | Decoded signing request and linked execution/allowance observations (request as displayed versus decoded intent: method, spender, token, amount or unlimited, deadline; execution outcome and observed allowance state) | Wallet signing and token allowances | source observation |
| SIG-69 | Outstanding token allowance exposure per wallet and spender (granted, used, revoked) | Wallet signing and token allowances | derived feature |
| SIG-70 | Payment-level control decision (platform block, review, challenge or allow; issuer decline; merchant block) with rule or model identity and decision time; recorded with its effect on each outcome channel | Payment attempts, authorization and payment controls | control outcome |
| SIG-71 | Account-level protective action (payout block or cancellation, hold, pause or schedule extension, API-key restriction or rotation, token freeze), with authority, reason and time | Funds movement and payout destinations | control outcome |

## Mechanisms

### M01

Small-deposit verification abuse and bank-account reuse across accounts.

Sources: none recorded for this mechanism.

### M02

OAuth and third-party app abuse (malicious or over-permissioned apps, consent phishing, token theft).

Sources: none recorded for this mechanism.

### M03

Supply-chain compromise of commerce plugins and SDK-impersonating packages.

Sources: none recorded for this mechanism.

### M04

Unauthorized bank-debit fraud using stolen bank credentials or accounts.

Sources: none recorded for this mechanism.

### M05

Client-side e-skimming and payment-page tampering on merchant checkouts.

Sources: none recorded for this mechanism.

### M06

Inbound transfer fraud on financial accounts (fund, withdraw, return).

Sources: none recorded for this mechanism.

### M07

Business stablecoin issuance abuse (issuer controls, reserve misrepresentation, issuance used to evade sanctions).

Sources: none recorded for this mechanism.

### M08

Embedded-wallet authentication and recovery takeover (OTP, social login, key-share recovery).

Sources: none recorded for this mechanism.
