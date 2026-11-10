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

Delegated payment-credential leakage and theft (Shared Payment Tokens, Link Pay Tokens, agent virtual cards, authenticated wallet sessions exposed to other local processes).

Sources (recorded scope of each):
- stripe/link-cli README (2026; fact (public engineering artifact)). Vendor README for an agent payment-credential CLI: credential types, spend-request limits and validity, optional HTTP MCP endpoint bound to 127.0.0.1 by default with a stated local-session exposure warning; no incident or security evaluation. Limit: README statement; no incident.

### M02

Post-compromise persistence and privilege abuse (added users, linked or authorized accounts, cross-account permissions, lockout and deletion).

Sources (recorded scope of each):
- FBI and CISA Joint Cybersecurity Advisory AA23-320A, Scattered Spider (2023-11-16; revised 2023-11-21) (2023; fact (practitioner/incident) government). FBI and CISA advisory on one actor cluster (Scattered Spider), TTPs from FBI investigations to November 2023: help-desk social engineering to reset passwords or MFA tokens, MFA fatigue, SIM swap, actor-registered MFA tokens, federated identity provider added with automatic account linking, new identities, then data theft, extortion and ransomware; enterprise IT and SSO environments. The 2025-07-29 update (seven co-sealers, TTPs to June 2025) keeps these and calls the federated-IdP technique historical. Limit: one actor cluster's TTPs to November 2023; enterprise identity environment.
- Microsoft Threat Intelligence, From cookie theft to BEC: Attackers use AiTM phishing sites as entry point to further financial fraud (2022-07-12) (2022; fact (practitioner/incident) vendor). Vendor report of an AiTM phishing campaign against more than 10,000 organizations from Sept 2021: passwords and session cookies stolen through a proxy kit, MFA bypassed, stolen cookies replayed, inbox rules created, and follow-on payment fraud attempted as little as five minutes after theft. Reported minimum timing, not a distribution; no counts of fraud cases or losses; enterprise email.

### M03

Device and browser fingerprint spoofing, emulators and device farms.

Sources: none recorded for this mechanism.

### M04

Connected-account takeover via onboarding-link or embedded-session leakage.

Sources (recorded scope of each):
- Stripe Docs, Stripe-hosted onboarding (Account Links) (2026; fact (vendor documentation) illustrative platform). One-use, short-lived Account Link URLs that grant access to personal information; platforms must authenticate the account before redirecting and must not send links outside the application; tracking link issuance and use is a design inference. No incident evidence. Limit: public documentation; no incident evidence.
- Stripe public OpenAPI specification and API event map (2026; fact (public engineering artifact)). Public OpenAPI files (general availability, public preview and private preview) parsed in full, blob IDs and SHA-256 verified; capability premises only (objects, fields and events an account can create or change). Interface definitions, not complete event histories, private instrumentation or field population; searches for absent counterparts are bounded by the terms tried. Limit: public schema only.

### M05

Fake or cloned e-commerce sites collecting payments or card data.

Sources (recorded scope of each):
- Bitaab M., Karimi A., Lyu Z., Oest A., Kuchhal D., Saad M., Ahn G.-J., Wang R., Bao T., Shoshitaishvili Y., Doupé A. ScamMagnifier: Piercing the Veil of Fraudulent Shopping Website Campaigns (2025; peer-reviewed prior research). Newly registered domains, May 2023 to Jun 2024: 46,746 fraudulent shopping sites; a crawler extracted checkout merchant IDs and stopped before payment; one provider linked 14,394 domains to its merchant IDs (54.55% to 10 IDs); 20.17% of sites transacted within 10 days of registration. Externally visible processors only; provider linkage method undisclosed; no settlement observed; some internal count inconsistencies. Limit: three processors; lower bound.
- Stripe public OpenAPI specification and API event map (2026; fact (public engineering artifact)). Public OpenAPI files (general availability, public preview and private preview) parsed in full, blob IDs and SHA-256 verified; capability premises only (objects, fields and events an account can create or change). Interface definitions, not complete event histories, private instrumentation or field population; searches for absent counterparts are bounded by the terms tried. Limit: public schema only.

### M06

Signature and approval phishing and drainer-as-a-service against self-custodial and embedded wallets (incl. stablecoin allowance abuse).

Sources (recorded scope of each):
- Chen Z., Luo D., Hu Y., Wu L., He B., Zhou Y. Dissecting Payload-based Transaction Phishing on Ethereum (2025; peer-reviewed prior research). Payload-based transaction phishing on Ethereum, Dec 2022 to Oct 2023: 130,637 phishing transactions with about USD 342 million in losses; ice phishing through approve and permit accounted for 59.04% of losses; outstanding approvals let scammers drain assets later. Ethereum only; categories reflect the 2023 landscape. Limit: Ethereum.

### M07

Event-destination, webhook or data-destination hijack after compromise (attacker endpoint receives account events or data exports).

Sources (recorded scope of each):
- Stripe public OpenAPI specification and API event map (2026; fact (public engineering artifact)). Public OpenAPI files (general availability, public preview and private preview) parsed in full, blob IDs and SHA-256 verified; capability premises only (objects, fields and events an account can create or change). Interface definitions, not complete event histories, private instrumentation or field population; searches for absent counterparts are bounded by the terms tried. Limit: absence in the public schema is not evidence about internal telemetry.

### M08

Payout redirection after compromise (added bank accounts, payout schedule changes).

Sources (recorded scope of each):
- FBI IC3 PSA I-091818-PSA, Cybercriminals Utilize Social Engineering Techniques to Obtain Employee Credentials to Conduct Payroll Diversion (2018-09-18) (2018; fact (standard/guidance) government). FBI IC3 advisory based on complaints: phished employee credentials used to change payroll bank details, rules added to suppress alerts about direct-deposit changes, and deposits redirected, often to prepaid cards. No counts, losses, timing or platform payout incidents. Limit: no counts.
- Stripe Docs, Best practices for risk management (2026; fact (vendor documentation) illustrative platform). Vendor guidance for Connect platforms: rejection reasons signalled by account.updated; account takeover prevention (two-factor authentication; monitoring changes to passwords, email and bank details from new devices); dispute activity above 0.75% generally excessive; delaying, holding, slowing or pausing payouts per account. Public practice only; no inference to private implementation. Limit: public documentation.
- Stripe Docs, Account fraud prevention (Radar for platforms) (2026; fact (vendor documentation) illustrative platform). Vendor guidance for platform account risk: account risk scores and levels, risk metrics, agentic insights (matching bank account rejected for fraud; card-testing example), and reject reasons including card casher (buyer and seller), card tester and no intent to fulfill; no bank-account change guidance; no performance data. Limit: public documentation.
- Stripe public OpenAPI specification and API event map (2026; fact (public engineering artifact)). Public OpenAPI files (general availability, public preview and private preview) parsed in full, blob IDs and SHA-256 verified; capability premises only (objects, fields and events an account can create or change). Interface definitions, not complete event histories, private instrumentation or field population; searches for absent counterparts are bounded by the terms tried. Limit: public schema only.

### M09

Key theft from developer environments and agent tooling (infostealers, malicious packages, credentials in files; agent-tagged and restricted API keys exposed in model context, logs or tool configuration).

Sources (recorded scope of each):
- Chen Z., Zhang Y., Liu Y., Deng G., Li Y., Zhang Y., Ning J., Zhang L.Y., Ma L., Li Z. How Your Credentials Are Leaked by LLM Agent Skills: An Empirical Study (2026; preprint). One marketplace (SkillsMP), 10% random sample (17,022) of a 12 Feb 2026 snapshot of 170,226 skills; static extraction, sandboxed Claude Code runs with mock credentials, manual labeling; 520 affected skills, 1,708 issues; credentials exposed in skill code, docs and config files and at runtime through stdout fed into the model context; credentials persisted in forks after upstream removal. Generic credentials, not payment-platform keys; other marketplaces not measured. Limit: one marketplace (SkillsMP); sandbox with mock credentials.

### M10

Credential stuffing and password spraying against operator (Dashboard) accounts.

Sources (recorded scope of each):
- Thomas K., Pullman J., Yeo K., Raghunathan A., Kelley P.G., Invernizzi L., Benko B., Pietraszek T., Patel S., Boneh D., Bursztein E. Protecting accounts from credential stuffing with password breach alerting (2019; peer-reviewed prior research). Privacy-preserving breach-alerting protocol and Chrome extension checking exact username and password pairs at login against 4 billion breached credentials; 667,716 opt-in users, 21.2 million logins on 746,853 domains, Feb to Mar 2019; 1.5% of logins used breached credentials (lower bound); 26% of warnings led to resets. Users' own logins, not observed attacker attempts; desktop Chrome only; not specific to payment or wallet accounts. Limit: opt-in extension users.
- Doerfler P., Marincenko M., Ranieri J., Jiang Y., Moscicki A., McCoy D., Thomas K. Evaluating Login Challenges as a Defense Against Account Takeover (2019; peer-reviewed prior research). Google login and recovery challenges, 2017 to 2018: device-based challenges blocked nearly all bot and most phishing hijack attempts; 47.8% of challenged sign-ins from an unfamiliar device and network succeeded in the same session; the one-week access figure uses users who failed a challenge as its denominator. Google only; the unfamiliar-device sample may include hijackers. Limit: one provider.

### M11

Stablecoin rails for layering, cash-out and sanctions evasion (rapid conversion, unhosted-wallet P2P, chain hopping).

Sources (recorded scope of each):
- FATF, Targeted Report on Stablecoins and Unhosted Wallets: Peer-to-Peer Transactions (2026-03-03) (2026; fact (standard/guidance) intergovernmental). FATF targeted report: stablecoins in ML/TF/PF (84 percent of USD 154 billion illicit VA volume in 2025, citing Chainalysis), P2P transfers via unhosted wallets outside AML/CFT obligations, layering, cash-out and chain hopping, near-instant cross-border settlement, issuer blacklist, freeze and burn controls, blockchain analytics and their limits, case studies and risk indicators; non-binding guidance and case material, not measurement. Limit: figure vendor-sourced.

### M12

Webhook forgery and replay against merchant endpoints lacking signature or timestamp checks.

Sources: none recorded for this mechanism.

### M13

Synthetic-identity onboarding of merchant or connected accounts.

Sources (recorded scope of each):
- Federal Reserve, Payments Fraud Insights: Detecting Synthetic Identity Fraud in the U.S. Payment System (October 2019) (2019; fact (standard/guidance) government). Federal Reserve Banks white paper on detecting synthetic identity fraud in consumer credit: definition (fictitious and sometimes real elements), contributing factors, relationship indicators (same SSN, address, phone, IP address or device; unrelated authorized users), false-positive caution on single traits, sleeper synthetics and bust-out tactics; loss figures are vendor estimates; guidance, not measurement. Limit: consumer credit focus; fetch-mediated.
- USAO District of New Jersey, Eighteen People Charged in International, $200 Million Credit Card Fraud Scam (2013-02-05) (2013; fact (practitioner/incident) government). Charging announcement (allegations, not findings): more than 7,000 fabricated identities with fabricated credit, loans run up and not repaid (bust-out), more than 1,800 drop addresses, sham companies whose merchant accounts were replaced by new companies and terminals after processors shut them for fraud, complicit merchants holding multiple processing accounts; 2013. Limit: allegations; 2013.

### M14

Post-compromise API key misuse (connected accounts, payout destinations, refunds, card testing, data export).

Sources (recorded scope of each):
- Gamazo W., Quist N. (Palo Alto Networks Unit 42). CloudKeys in the Air: Tracking Malicious Operations of Exposed IAM Keys, 2023-10-30 (2023; fact (practitioner/incident) vendor). Vendor honeypot: overly permissive AWS IAM keys leaked in past commits of public GitHub repositories; reconnaissance began about four minutes after AWS applied its quarantine policy; after the researchers removed the quarantine, more than 400 API calls in seven minutes launched mining instances. One actor in a researcher-controlled environment; the five-minute figures conflict with the article's own timeline; no population timing distribution. Limit: vendor; one cloud provider; honeypot-style exposure.
- Stripe public OpenAPI specification and API event map (2026; fact (public engineering artifact)). Public OpenAPI files (general availability, public preview and private preview) parsed in full, blob IDs and SHA-256 verified; capability premises only (objects, fields and events an account can create or change). Interface definitions, not complete event histories, private instrumentation or field population; searches for absent counterparts are bounded by the terms tried. Limit: public schema; internal telemetry not established.

### M15

Abuse of agent authorization flows (MCP OAuth consent phishing, approval fatigue, stolen approval tokens).

Sources (recorded scope of each):
- Kumar A.A. Loopjacking: Hijacking Human-in-the-Loop Approval (2026; preprint). Approval of one operation used to release a different one (representation mismatch or post-approval state substitution), reproduced in a purposive set of agent-framework releases; a canonical approval record with a digest, compared with the operation at use time, blocked the tested attacks. One operator; no independent reproduction; not a prevalence estimate. Limit: single author.
- Stripe Docs, Model Context Protocol (MCP) (2026; fact (vendor documentation) illustrative platform). Vendor documentation of the remote MCP server: tools (generic API read and write, Treasury money movement), OAuth consent and revocable sessions, agent API keys (non-agent keys rejected from December 2026), a prompt-injection caution, client tool approval, and Stripe human confirmation with an approval token for certain writes; no incident or effectiveness data. Limit: public documentation.

### M16

Platform-brand impersonation phishing targeting merchants and developers.

Sources (recorded scope of each):
- Kondracki B., Azad B.A., Starov O., Nikiforakis N. Catching Transparent Phish: Analyzing and Detecting MITM Phishing Toolkits (2021; peer-reviewed prior research). Three open-source MITM phishing toolkits (13 versions) fingerprinted by client-side RTT and TLS-library features (99.9% lab accuracy); 1,220 in-the-wild sites found mainly via Certificate Transparency, Mar 2020 to Mar 2021, targeting 19 consumer, financial and enterprise brands (22 trademarks monitored, no merchant payment platform); 43.7% of domains and 18.9% of IPs on blocklists; target-side detection by unique JA3 TLS client fingerprints. Not the platform brand; RTT method applies to probing the phishing server, not to login requests at the target. Limit: 22 monitored consumer, financial and enterprise brands (PayPal, banks, card issuers; no merchant payment platform); not merchant- or developer-targeted; Mar 2020 to Mar 2021.

### M17

Injected unauthorized actions and memory or skill poisoning in operator-facing AI assistants (refunds, coupons, subscription changes).

Sources (recorded scope of each):
- Dash P., Ge T., Jain A., Shah T., Shang Z. From Untrusted Input to Trusted Memory: A Systematic Study of Memory Poisoning Attacks in LLM Agents (2026; preprint). Memory poisoning in LLM agents: four long-term memory write channels and no robust provenance for stored entries; on synthetic benchmark cases, writes from untrusted input succeeded in 34% and 67% of cases on two agents and were retrieved in later sessions. Two agents, one model, LLM-generated test cases and an LLM judge. Limit: benchmark (MPBench).
- Kumar A.A. Loopjacking: Hijacking Human-in-the-Loop Approval (2026; preprint). Approval of one operation used to release a different one (representation mismatch or post-approval state substitution), reproduced in a purposive set of agent-framework releases; a canonical approval record with a digest, compared with the operation at use time, blocked the tested attacks. One operator; no independent reproduction; not a prevalence estimate.

### M18

Stolen or rented identity for onboarding (identity theft, straw owners, account rental).

Sources (recorded scope of each):
- USAO Southern District of New York, CEO of Credit Card Processing Company Charged in $19 Million Credit Card Laundering Scheme (2019-10-11) (2019; fact (practitioner/incident) government). Charging announcement (allegations, not findings): about 26 sham merchant companies headed by paid nominee signers, false merchant applications concealing the true (prohibited telemarketing) merchant, closed accounts quickly replaced, and charges, refunds and chargebacks spread across accounts to evade bank, processor and ISO chargeback monitoring; 2012 to 2015. Limit: allegations.

### M19

Card testing by validating stolen card data through card setup and small payments.

Sources (recorded scope of each):
- Meltzer J., Chadalapaka V. (Stripe), How Stripe Radar responded to a new wave of card testing (2025-01-15) (2025; fact (public engineering publication) illustrative platform). Vendor engineering post: card testers shifted from enumeration to verification attacks using dumps of stolen cards, raising issuer authorization rates; the platform responded by ingesting dumps to block those cards, monitoring the internet for stolen numbers and adding stolen-card models. Its figures have no stated period, source or baseline. Limit: platform statement.
- Stripe Docs, Protect yourself from card testing (2026; fact (vendor documentation) illustrative platform). Vendor guidance defining card testing (setup and small payments, harvesting 3DS or issuer responses, publishable-key reuse, stolen secret keys), its symptoms and recommended controls; no prevalence or effectiveness data.

### M20

Fake review and reputation fraud supporting merchant legitimacy.

Sources: none recorded for this mechanism.

### M21

Merchant financing fraud using fabricated volume or synthetic or stolen business identity, then default.

Sources: none recorded for this mechanism.

### M22

AI token and compute theft for resale.

Sources: none recorded for this mechanism.

### M23

Pay-as-you-go non-payment (run up usage, never pay).

Sources (recorded scope of each):
- Stripe Docs, Pay-as-you-go abuse evaluation (2026; fact (vendor documentation) illustrative platform). Vendor documentation of a preview billing evaluation: non-payment risk for post-paid usage, evaluated mid-cycle against the expected invoice amount, with levels including not_assessed and unknown; suggested actions (review, early invoice, prepayment, limits, pause); the endpoint fails open. No performance figures. Limit: public documentation; preview API.
- Stripe public OpenAPI specification and API event map (2026; fact (public engineering artifact)). Public OpenAPI files (general availability, public preview and private preview) parsed in full, blob IDs and SHA-256 verified; capability premises only (objects, fields and events an account can create or change). Interface definitions, not complete event histories, private instrumentation or field population; searches for absent counterparts are bounded by the terms tried. Limit: public schema only.

### M24

Business email compromise and invoice fraud using hosted invoices or payment redirection.

Sources (recorded scope of each):
- FBI IC3 Public Service Announcement, Business Email Compromise: The $55 Billion Scam (2024-09-11) (2024; fact (standard/guidance) government). FBI IC3 PSA: BEC definition (compromised email, unauthorized transfers), USD 55.5 billion exposed losses in 305,033 incidents, October 2013 to December 2023 (IC3, law-enforcement and financial-institution data), recipient counts, 2023 growth in funds sent to custodial accounts at third-party and P2P payment processors and crypto exchanges, UK and Hong Kong banks as intermediary stops; advice incl. verifying account-information change requests; no invoice-redirection, mule or timing detail. Limit: IC3 complaints, law-enforcement and financial-institution filings; exposed losses, October 2013 to December 2023.

### M25

Account sharing (one account used concurrently from several places).

Sources (recorded scope of each):
- Stripe Docs, Customer account evaluations (2026; fact (vendor documentation) illustrative platform). Vendor documentation of a preview API: registration and login evaluations (user_multi_accounting, user_account_sharing) with scores and risk levels from device session or IP, user agent and referrer, and reported allowed, restricted or blocked outcomes; abuse reasons (email, IP and device reuse within the business over seven days) do not alone confirm abuse. No inference to internal implementation or data used. Limit: public documentation; preview API.
- Stripe public OpenAPI specification and API event map (2026; fact (public engineering artifact)). Public OpenAPI files (general availability, public preview and private preview) parsed in full, blob IDs and SHA-256 verified; capability premises only (objects, fields and events an account can create or change). Interface definitions, not complete event histories, private instrumentation or field population; searches for absent counterparts are bounded by the terms tried. Limit: public schema only; public preview.
