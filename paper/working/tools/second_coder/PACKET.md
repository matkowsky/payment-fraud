# Second-coder packet: which signals does each mechanism need?

You are an independent rater. Use only this packet. Do not use memory of earlier chats, files, the web or any other source. If you recognize the project this comes from, say so and still answer only from the packet.

A "mechanism" is a way of abusing a multi-product payment platform. A "signal" is a kind of record the platform could keep. Your task is to decide, for each mechanism, which signals it should be linked to under the rule below.

## The rule

Link a mechanism to a signal when BOTH hold:

1. An investigator examining that mechanism would need the signal's record to test whether the
   mechanism occurred, or to tell it apart from legitimate activity.
2. At least one of the sources listed under the mechanism describes behaviour that the signal would
   record. If you link on reasoning alone, without such a source, mark the link "inference".

Do not link a signal only because it is generally useful. Most mechanisms link to between one and
six signals. Link every signal that meets the rule and no others.

For each mechanism also answer: is any record that rule 1 requires absent from the signal list?

## Answer format

One line per mechanism, nothing else before or after the lines:

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

Event-destination, webhook or data-destination hijack after compromise (attacker endpoint receives account events or data exports).

Sources (recorded scope of each):
- Stripe public OpenAPI specification and API event map (2026; fact (public engineering artifact)). Public OpenAPI files (general availability, public preview and private preview) parsed in full, blob IDs and SHA-256 verified; capability premises only (objects, fields and events an account can create or change). Interface definitions, not complete event histories, private instrumentation or field population; searches for absent counterparts are bounded by the terms tried. Limit: absence in the public schema is not evidence about internal telemetry.

### M02

Small-deposit verification abuse and bank-account reuse across accounts.

Sources: none recorded for this mechanism.

### M03

Bust-out (build history, then maximize payouts or financing before losses surface).

Sources (recorded scope of each):
- Stripe Docs, Best practices for risk management (2026; fact (vendor documentation) illustrative platform). Vendor guidance for Connect platforms: rejection reasons signalled by account.updated; account takeover prevention (two-factor authentication; monitoring changes to passwords, email and bank details from new devices); dispute activity above 0.75% generally excessive; delaying, holding, slowing or pausing payouts per account. Public practice only; no inference to private implementation. Limit: public documentation.
- Stripe Docs, Risk and liability management with Connect (2026; fact (vendor documentation) illustrative platform). Vendor explanation of negative-balance liability on Connect (direct versus indirect charges, platform reserves, 180-day rule) and of account risk: credit risk (refunds and chargebacks exceeding what an account can cover) and fraud risk (no intent to deliver; payment method cashing through a self-opened account). No dispute threshold, payout-hold guidance or bust-out description. Limit: public documentation.
- USAO District of New Jersey, Eighteen People Charged in International, $200 Million Credit Card Fraud Scam (2013-02-05) (2013; fact (practitioner/incident) government). Charging announcement (allegations, not findings): more than 7,000 fabricated identities with fabricated credit, loans run up and not repaid (bust-out), more than 1,800 drop addresses, sham companies whose merchant accounts were replaced by new companies and terminals after processors shut them for fraud, complicit merchants holding multiple processing accounts; 2013. Limit: allegations.
- FTC v. First Data Merchant Services LLC and Chi W. Ko, No. 1:20-cv-03867 (S.D.N.Y.), Complaint, ECF 1 (filed 2020-05-19) (2020; fact (practitioner/incident) government). Complaint (allegations, not findings): an ISO opened hundreds of merchant accounts for phony entities and shell corporations with false information; 40 pairs of identical applications approved (load balancing); an applicant approved two weeks after a prior account closed for excessive chargebacks; over 300,000 chargebacks in under a year. 2012 to 2014; the stipulated First Data order (ECF 15, read in full) does not adjudicate the allegations, and the Ko order (ECF 16) was not read. Limit: allegations.
- Stripe public OpenAPI specification and API event map (2026; fact (public engineering artifact)). Public OpenAPI files (general availability, public preview and private preview) parsed in full, blob IDs and SHA-256 verified; capability premises only (objects, fields and events an account can create or change). Interface definitions, not complete event histories, private instrumentation or field population; searches for absent counterparts are bounded by the terms tried. Limit: public schema only.

### M04

Session and token theft (infostealer cookies, session hijack).

Sources (recorded scope of each):
- Microsoft Threat Intelligence, From cookie theft to BEC: Attackers use AiTM phishing sites as entry point to further financial fraud (2022-07-12) (2022; fact (practitioner/incident) vendor). Vendor report of an AiTM phishing campaign against more than 10,000 organizations from Sept 2021: passwords and session cookies stolen through a proxy kit, MFA bypassed, stolen cookies replayed, inbox rules created, and follow-on payment fraud attempted as little as five minutes after theft. Reported minimum timing, not a distribution; no counts of fraud cases or losses; enterprise email. Limit: vendor.
- Ghasemisharif M., Ramesh A., Checkoway S., Kanich C., Polakis J. O Single Sign-Off, Where Art Thou? An Empirical Analysis of Single Sign-On Account Hijacking and Session Management on the Web (2018; peer-reviewed prior research). Consumer web and mobile SSO with Facebook as IdP: SSO on 6.30% of the Alexa top 1M (Sept 2017); Facebook session-cookie replay without alert (campus network, Jan to May 2017); manual audit of 95 relying parties showing long-term access via email or password change and IdP-account linking, and no user remediation at 71 of 95; proposed single sign-off revocation. Not enterprise SAML SSO or platform operator sessions; 2017 behavior, Facebook cookie exposure since fixed. Limit: Facebook SSO, 95 consumer relying parties, measured 2017 (published 2018); cookie exposure fixed after disclosure.
- Campobasso M., Allodi L. Impersonation-as-a-Service: Characterizing the Emerging Criminal Infrastructure for User Impersonation at Scale (2020; peer-reviewed prior research). One invite-only impersonation market, Dec 2017 to Mar 2020: about 262,000 listed profiles of malware-harvested cookies, saved credentials and browser fingerprints, sold with a custom browser and extension that load them; only 4.3% of profiles had a real fingerprint. Listings only; no profile bought, so profile quality and the impersonation software were not tested.

### M05

Merchant misrepresentation and transaction laundering (prohibited business behind a front).

Sources (recorded scope of each):
- McCoy D., Dharmdasani H., Kreibich C., Voelker G.M., Savage S. Priceless: The Role of Payments in Abuse-advertised Goods (2012; peer-reviewed prior research). Banking relationships of 40 spam- and search-advertised affiliate programs from 676 Visa test orders over about two years: 30 acquiring banks; terminals usually disappear within 30 days of a brand-holder complaint and programs move to other banks; almost 50%, later about 70%, of pharmaceutical transactions miscoded. Visa only, 2010 to 2012; transfer to onboarding is analogical. Limit: fetch-mediated; one network.
- Tian H., Gaffigan S.M., West D.S., McCoy D. Bullet-Proof Payment Processors (2018; peer-reviewed prior research). Two-year payment intervention with six luxury brands: 424 test purchases from counterfeit sites reported to Visa; processors shifted between acquiring banks, opened merchant accounts through shell companies that appeared to sell low-risk goods, and filtered test purchases. Six brands, Visa purchases, 2014 to 2017; failed attempts not tracked; not a prevalence ranking. Limit: fetch-mediated.
- FTC v. AlliedWallet, Inc., No. 2:19-cv-04355 (C.D. Cal.), Complaint, ECF 24 (unredacted, filed 2019-05-28; redacted twin ECF 1 filed 2019-05-20) (2019; fact (practitioner/incident) government). Complaint (allegations, not findings): a processor knowingly served fraudulent merchants, procured U.K. shell companies and nominees, submitted dummy websites, accepted plans to pad sales using stored-value card purchases and spread transaction volume across accounts, and kept processing after terminations; at least USD 110 million consumer loss alleged. Stipulated order; no merits adjudication. Limit: allegations.
- FTC v. First Data Merchant Services LLC and Chi W. Ko, No. 1:20-cv-03867 (S.D.N.Y.), Complaint, ECF 1 (filed 2020-05-19) (2020; fact (practitioner/incident) government). Complaint (allegations, not findings): an ISO opened hundreds of merchant accounts for phony entities and shell corporations with false information; 40 pairs of identical applications approved (load balancing); an applicant approved two weeks after a prior account closed for excessive chargebacks; over 300,000 chargebacks in under a year. 2012 to 2014; the stipulated First Data order (ECF 15, read in full) does not adjudicate the allegations, and the Ko order (ECF 16) was not read. Limit: allegations.
- FTC v. Paddle.com Market Limited, No. 1:25-cv-01886 (D.D.C.), Complaint, ECF 1 (filed 2025-06-16) (2025; fact (practitioner/incident) government). Complaint (allegations, not findings): a merchant of record processed for thousands of sellers under its own accounts, so networks and acquirers could not see seller-level chargeback rates; chargeback-prevention alerts (Ethoca, Verifi) and refunds kept disputes from being counted; descriptors changed to aggregate disputes. 2017 to 2023; stipulated order; figures not visible. Limit: allegations.
- Stripe Docs, Best practices for risk management (2026; fact (vendor documentation) illustrative platform). Vendor guidance for Connect platforms: rejection reasons signalled by account.updated; account takeover prevention (two-factor authentication; monitoring changes to passwords, email and bank details from new devices); dispute activity above 0.75% generally excessive; delaying, holding, slowing or pausing payouts per account. Public practice only; no inference to private implementation. Limit: public documentation.
- USAO Southern District of New York, CEO of Credit Card Processing Company Charged in $19 Million Credit Card Laundering Scheme (2019-10-11) (2019; fact (practitioner/incident) government). Charging announcement (allegations, not findings): about 26 sham merchant companies headed by paid nominee signers, false merchant applications concealing the true (prohibited telemarketing) merchant, closed accounts quickly replaced, and charges, refunds and chargebacks spread across accounts to evade bank, processor and ISO chargeback monitoring; 2012 to 2015. Limit: allegations.

### M06

Credential stuffing against consumer-wallet and merchant end-customer accounts.

Sources (recorded scope of each):
- Thomas K., Pullman J., Yeo K., Raghunathan A., Kelley P.G., Invernizzi L., Benko B., Pietraszek T., Patel S., Boneh D., Bursztein E. Protecting accounts from credential stuffing with password breach alerting (2019; peer-reviewed prior research). Privacy-preserving breach-alerting protocol and Chrome extension checking exact username and password pairs at login against 4 billion breached credentials; 667,716 opt-in users, 21.2 million logins on 746,853 domains, Feb to Mar 2019; 1.5% of logins used breached credentials (lower bound); 26% of warnings led to resets. Users' own logins, not observed attacker attempts; desktop Chrome only; not specific to payment or wallet accounts. Limit: opt-in Chrome extension users, Feb to Mar 2019; logins on 746,853 web domains, not wallet- or merchant-specific.

### M07

Layering through shell companies, transfers and scheduled movements across accounts.

Sources (recorded scope of each):
- FinCEN Advisory FIN-2014-A005, Update on U.S. Currency Restrictions in Mexico: Funnel Accounts and TBML (2014-05-28) (2014; fact (standard/guidance) government). FinCEN advisory: funnel accounts receive multiple cash deposits in one area, often below the reporting threshold, and are drained elsewhere with little elapsed time; multiple funnel accounts consolidate funds into one account; red flags and SAR terms. Bank cash-deposit and trade-based laundering setting; no time or concentration thresholds; no payment-platform evidence. Limit: cash rail; analog.

### M08

Credential, session and key markets fed by infostealers and leaks.

Sources (recorded scope of each):
- Campobasso M., Allodi L. Impersonation-as-a-Service: Characterizing the Emerging Criminal Infrastructure for User Impersonation at Scale (2020; peer-reviewed prior research). One invite-only impersonation market, Dec 2017 to Mar 2020: about 262,000 listed profiles of malware-harvested cookies, saved credentials and browser fingerprints, sold with a custom browser and extension that load them; only 4.3% of profiles had a real fingerprint. Listings only; no profile bought, so profile quality and the impersonation software were not tested. Limit: one market.

### M09

AI token and compute theft for resale.

Sources: none recorded for this mechanism.

### M10

Account farming and aged-account preparation for later abuse.

Sources (recorded scope of each):
- Thomas K., McCoy D., Grier C., Kolcz A., Paxson V. Trafficking Fraudulent Accounts: The Role of the Underground Market in Twitter Spam and Abuse (2013; peer-reviewed prior research). 121,027 fraudulent Twitter accounts bought from 27 merchants, Jun 2012 to Apr 2013: registration from unique IPs (79%), email confirmation, solved CAPTCHAs and naming patterns; accounts stockpiled a median of 31 days and sold as 'pre-aged' to evade heuristics on new accounts. Twitter only; classifier applied retroactively; not payment accounts. Limit: Twitter; retroactive; adversary adaptation noted.

### M11

Inbound transfer fraud on financial accounts (fund, withdraw, return).

Sources: none recorded for this mechanism.

### M12

Payout redirection after compromise (added bank accounts, payout schedule changes).

Sources (recorded scope of each):
- FBI IC3 PSA I-091818-PSA, Cybercriminals Utilize Social Engineering Techniques to Obtain Employee Credentials to Conduct Payroll Diversion (2018-09-18) (2018; fact (standard/guidance) government). FBI IC3 advisory based on complaints: phished employee credentials used to change payroll bank details, rules added to suppress alerts about direct-deposit changes, and deposits redirected, often to prepaid cards. No counts, losses, timing or platform payout incidents. Limit: no counts.
- Stripe Docs, Best practices for risk management (2026; fact (vendor documentation) illustrative platform). Vendor guidance for Connect platforms: rejection reasons signalled by account.updated; account takeover prevention (two-factor authentication; monitoring changes to passwords, email and bank details from new devices); dispute activity above 0.75% generally excessive; delaying, holding, slowing or pausing payouts per account. Public practice only; no inference to private implementation. Limit: public documentation.
- Stripe Docs, Account fraud prevention (Radar for platforms) (2026; fact (vendor documentation) illustrative platform). Vendor guidance for platform account risk: account risk scores and levels, risk metrics, agentic insights (matching bank account rejected for fraud; card-testing example), and reject reasons including card casher (buyer and seller), card tester and no intent to fulfill; no bank-account change guidance; no performance data. Limit: public documentation.
- Stripe public OpenAPI specification and API event map (2026; fact (public engineering artifact)). Public OpenAPI files (general availability, public preview and private preview) parsed in full, blob IDs and SHA-256 verified; capability premises only (objects, fields and events an account can create or change). Interface definitions, not complete event histories, private instrumentation or field population; searches for absent counterparts are bounded by the terms tried. Limit: public schema only.

### M13

Business email compromise and invoice fraud using hosted invoices or payment redirection.

Sources (recorded scope of each):
- FBI IC3 Public Service Announcement, Business Email Compromise: The $55 Billion Scam (2024-09-11) (2024; fact (standard/guidance) government). FBI IC3 PSA: BEC definition (compromised email, unauthorized transfers), USD 55.5 billion exposed losses in 305,033 incidents, October 2013 to December 2023 (IC3, law-enforcement and financial-institution data), recipient counts, 2023 growth in funds sent to custodial accounts at third-party and P2P payment processors and crypto exchanges, UK and Hong Kong banks as intermediary stops; advice incl. verifying account-information change requests; no invoice-redirection, mule or timing detail. Limit: IC3 complaints, law-enforcement and financial-institution filings; exposed losses, October 2013 to December 2023.

### M14

Merchant-side dispute evasion (dispute avoidance, churning, fabricated evidence, threshold gaming).

Sources (recorded scope of each):
- FTC v. AlliedWallet, Inc., No. 2:19-cv-04355 (C.D. Cal.), Complaint, ECF 24 (unredacted, filed 2019-05-28; redacted twin ECF 1 filed 2019-05-20) (2019; fact (practitioner/incident) government). Complaint (allegations, not findings): a processor knowingly served fraudulent merchants, procured U.K. shell companies and nominees, submitted dummy websites, accepted plans to pad sales using stored-value card purchases and spread transaction volume across accounts, and kept processing after terminations; at least USD 110 million consumer loss alleged. Stipulated order; no merits adjudication. Limit: allegations.
- FTC v. First Data Merchant Services LLC and Chi W. Ko, No. 1:20-cv-03867 (S.D.N.Y.), Complaint, ECF 1 (filed 2020-05-19) (2020; fact (practitioner/incident) government). Complaint (allegations, not findings): an ISO opened hundreds of merchant accounts for phony entities and shell corporations with false information; 40 pairs of identical applications approved (load balancing); an applicant approved two weeks after a prior account closed for excessive chargebacks; over 300,000 chargebacks in under a year. 2012 to 2014; the stipulated First Data order (ECF 15, read in full) does not adjudicate the allegations, and the Ko order (ECF 16) was not read. Limit: allegations.
- FTC v. Paddle.com Market Limited, No. 1:25-cv-01886 (D.D.C.), Complaint, ECF 1 (filed 2025-06-16) (2025; fact (practitioner/incident) government). Complaint (allegations, not findings): a merchant of record processed for thousands of sellers under its own accounts, so networks and acquirers could not see seller-level chargeback rates; chargeback-prevention alerts (Ethoca, Verifi) and refunds kept disputes from being counted; descriptors changed to aggregate disputes. 2017 to 2023; stipulated order; figures not visible. Limit: allegations; confounder noted.
- Stripe Docs, Best practices for risk management (2026; fact (vendor documentation) illustrative platform). Vendor guidance for Connect platforms: rejection reasons signalled by account.updated; account takeover prevention (two-factor authentication; monitoring changes to passwords, email and bank details from new devices); dispute activity above 0.75% generally excessive; delaying, holding, slowing or pausing payouts per account. Public practice only; no inference to private implementation. Limit: public documentation.
- Zhang S., He E., Zhan X., He S., Xiao R., Yi X., Li H. Generative AI-Enabled Refund Fraud in Chinese E-Commerce: Investigation on Merchants and Platform Workers (2026; preprint). Interview study with 17 merchants and 13 platform workers in Chinese e-commerce: GenAI-fabricated defect images and records used in refund claims, one manipulated photo reused to claim from four shops at once, chatbots misclassifying generated images. Self-reported accounts; no measurement of prevalence; Chinese platforms only; participant tables inconsistent. Limit: Chinese e-commerce; interviews.
- USAO Southern District of New York, CEO of Credit Card Processing Company Charged in $19 Million Credit Card Laundering Scheme (2019-10-11) (2019; fact (practitioner/incident) government). Charging announcement (allegations, not findings): about 26 sham merchant companies headed by paid nominee signers, false merchant applications concealing the true (prohibited telemarketing) merchant, closed accounts quickly replaced, and charges, refunds and chargebacks spread across accounts to evade bank, processor and ISO chargeback monitoring; 2012 to 2015. Limit: allegations.

### M15

Post-compromise persistence through automation objects (workflows, hosted custom-object methods, event destinations, connected apps, assistant skills).

Sources (recorded scope of each):
- Microsoft Threat Intelligence, Threat actors misuse OAuth applications to automate financially driven attacks, 2023-12-12 (2023; fact (practitioner/incident) vendor). Vendor report of three attack sets in which compromised accounts created or modified OAuth applications: secrets and credentials added and cloud compute provisioned for cryptomining (fees 10,000 to 1.5 million USD), BEC persistence and phishing through Microsoft Graph, inbox rules, and spam through Mail.Send. Microsoft tenant setting; no changes to authentication factors or event destinations described; no prevalence estimates. Limit: vendor.
- FBI and CISA Joint Cybersecurity Advisory AA23-320A, Scattered Spider (2023-11-16; revised 2023-11-21) (2023; fact (practitioner/incident) government). FBI and CISA advisory on one actor cluster (Scattered Spider), TTPs from FBI investigations to November 2023: help-desk social engineering to reset passwords or MFA tokens, MFA fatigue, SIM swap, actor-registered MFA tokens, federated identity provider added with automatic account linking, new identities, then data theft, extortion and ransomware; enterprise IT and SSO environments. The 2025-07-29 update (seven co-sealers, TTPs to June 2025) keeps these and calls the federated-IdP technique historical. Limit: one actor cluster's TTPs to November 2023; enterprise identity environment.

### M16

Client-side e-skimming and payment-page tampering on merchant checkouts.

Sources: none recorded for this mechanism.

### M17

Abuse of support and escalation workflows (policy and procedure abuse).

Sources (recorded scope of each):
- FBI and CISA Joint Cybersecurity Advisory AA23-320A, Scattered Spider (2023-11-16; revised 2023-11-21) (2023; fact (practitioner/incident) government). FBI and CISA advisory on one actor cluster (Scattered Spider), TTPs from FBI investigations to November 2023: help-desk social engineering to reset passwords or MFA tokens, MFA fatigue, SIM swap, actor-registered MFA tokens, federated identity provider added with automatic account linking, new identities, then data theft, extortion and ransomware; enterprise IT and SSO environments. The 2025-07-29 update (seven co-sealers, TTPs to June 2025) keeps these and calls the federated-IdP technique historical. Limit: one actor cluster's TTPs to November 2023; enterprise IT help desk, applied to platform support workflows by analogy.

### M18

No-intent-to-deliver merchant (non-delivery, partial or wrong goods, fabricated shipping evidence).

Sources (recorded scope of each):
- Stripe Docs, Risk and liability management with Connect (2026; fact (vendor documentation) illustrative platform). Vendor explanation of negative-balance liability on Connect (direct versus indirect charges, platform reserves, 180-day rule) and of account risk: credit risk (refunds and chargebacks exceeding what an account can cover) and fraud risk (no intent to deliver; payment method cashing through a self-opened account). No dispute threshold, payout-hold guidance or bust-out description. Limit: public documentation.
- Stripe Docs, Account fraud prevention (Radar for platforms) (2026; fact (vendor documentation) illustrative platform). Vendor guidance for platform account risk: account risk scores and levels, risk metrics, agentic insights (matching bank account rejected for fraud; card-testing example), and reject reasons including card casher (buyer and seller), card tester and no intent to fulfill; no bank-account change guidance; no performance data. Limit: public documentation.
- Stripe public OpenAPI specification and API event map (2026; fact (public engineering artifact)). Public OpenAPI files (general availability, public preview and private preview) parsed in full, blob IDs and SHA-256 verified; capability premises only (objects, fields and events an account can create or change). Interface definitions, not complete event histories, private instrumentation or field population; searches for absent counterparts are bounded by the terms tried. Limit: public schema only.
- Bitaab M., Karimi A., Lyu Z., Oest A., Kuchhal D., Saad M., Ahn G.-J., Wang R., Bao T., Shoshitaishvili Y., Doupé A. ScamMagnifier: Piercing the Veil of Fraudulent Shopping Website Campaigns (2025; peer-reviewed prior research). Newly registered domains, May 2023 to Jun 2024: 46,746 fraudulent shopping sites; a crawler extracted checkout merchant IDs and stopped before payment; one provider linked 14,394 domains to its merchant IDs (54.55% to 10 IDs); 20.17% of sites transacted within 10 days of registration. Externally visible processors only; provider linkage method undisclosed; no settlement observed; some internal count inconsistencies. Limit: three payment processors; collaborator-limited data.
- Stripe Docs, Best practices for risk management (2026; fact (vendor documentation) illustrative platform). Vendor guidance for Connect platforms: rejection reasons signalled by account.updated; account takeover prevention (two-factor authentication; monitoring changes to passwords, email and bank details from new devices); dispute activity above 0.75% generally excessive; delaying, holding, slowing or pausing payouts per account. Public practice only; no inference to private implementation. Limit: public documentation.

### M19

Mule and pass-through accounts receiving and rapidly moving proceeds.

Sources (recorded scope of each):
- Stripe Docs, Manage fraud (Treasury and Issuing for Connect platforms) (2026; fact (vendor documentation) illustrative platform). Vendor fraud guide for platforms liable for Treasury and Issuing losses: default defense layer, inbound transfer fraud and return windows, bank-account linking abuse, APP fraud (including BEC and fake invoices) and mule activity (rapid outflow to new or changed recipients), and private-preview rules; guidance, not measurement. Limit: public documentation.
- UK Payment Systems Regulator, APP fraud performance data (web page, undated; data for 1 January to 6 October 2024 from the February 2026 report) (2026; fact (standard/guidance) government). UK PSR APP scam performance data, payments before 7 October 2024 (cases closed in 2024): Metric C ranks the 20 firms receiving the highest value and volume of APP scams per £ million and per million transactions received, from scams sent by the 14 largest banking groups over Faster Payments; smaller firms included as disproportionate receivers (report: non-directed PSPs 34 percent of fraud value, 19 percent of payment value); firm-level, not account-level. Limit: firm-level, not account-level; UK Faster Payments; scams sent from the 14 largest banking groups, payments before 7 October 2024.
- FinCEN Advisory FIN-2014-A005, Update on U.S. Currency Restrictions in Mexico: Funnel Accounts and TBML (2014-05-28) (2014; fact (standard/guidance) government). FinCEN advisory: funnel accounts receive multiple cash deposits in one area, often below the reporting threshold, and are drained elsewhere with little elapsed time; multiple funnel accounts consolidate funds into one account; red flags and SAR terms. Bank cash-deposit and trade-based laundering setting; no time or concentration thresholds; no payment-platform evidence. Limit: bank cash deposits (funnel accounts); analog; no time or concentration thresholds.

### M20

Free-trial abuse (repeat trials, virtual or prepaid cards, disposable emails).

Sources (recorded scope of each):
- Stripe Docs, Free trial abuse prevention (2026; fact (vendor documentation) illustrative platform). Vendor documentation: free-trial abuse patterns (prepaid or virtual cards; the same card across accounts) and a Radar control that blocks high-risk trial starts, recorded as a rule decision. No performance figures; no inference to how risk is scored. Limit: public documentation.
- Stripe Docs, Pay-as-you-go abuse evaluation (2026; fact (vendor documentation) illustrative platform). Vendor documentation of a preview billing evaluation: non-payment risk for post-paid usage, evaluated mid-cycle against the expected invoice amount, with levels including not_assessed and unknown; suggested actions (review, early invoice, prepayment, limits, pause); the endpoint fails open. No performance figures. Limit: public documentation.
- Stripe public OpenAPI specification and API event map (2026; fact (public engineering artifact)). Public OpenAPI files (general availability, public preview and private preview) parsed in full, blob IDs and SHA-256 verified; capability premises only (objects, fields and events an account can create or change). Interface definitions, not complete event histories, private instrumentation or field population; searches for absent counterparts are bounded by the terms tried. Limit: public schema only.

### M21

Authorized push payment scams using platform accounts as sender or receiver.

Sources (recorded scope of each):
- Stripe Docs, Manage fraud (Treasury and Issuing for Connect platforms) (2026; fact (vendor documentation) illustrative platform). Vendor fraud guide for platforms liable for Treasury and Issuing losses: default defense layer, inbound transfer fraud and return windows, bank-account linking abuse, APP fraud (including BEC and fake invoices) and mule activity (rapid outflow to new or changed recipients), and private-preview rules; guidance, not measurement. Limit: public documentation.
- UK Payment Systems Regulator, APP fraud performance data (web page, undated; data for 1 January to 6 October 2024 from the February 2026 report) (2026; fact (standard/guidance) government). UK PSR APP scam performance data, payments before 7 October 2024 (cases closed in 2024): Metric C ranks the 20 firms receiving the highest value and volume of APP scams per £ million and per million transactions received, from scams sent by the 14 largest banking groups over Faster Payments; smaller firms included as disproportionate receivers (report: non-directed PSPs 34 percent of fraud value, 19 percent of payment value); firm-level, not account-level. Limit: firm-level, not account-level; UK Faster Payments; scams sent from the 14 largest banking groups, payments before 7 October 2024.

### M22

Stablecoin rails for layering, cash-out and sanctions evasion (rapid conversion, unhosted-wallet P2P, chain hopping).

Sources (recorded scope of each):
- FATF, Targeted Report on Stablecoins and Unhosted Wallets: Peer-to-Peer Transactions (2026-03-03) (2026; fact (standard/guidance) intergovernmental). FATF targeted report: stablecoins in ML/TF/PF (84 percent of USD 154 billion illicit VA volume in 2025, citing Chainalysis), P2P transfers via unhosted wallets outside AML/CFT obligations, layering, cash-out and chain hopping, near-instant cross-border settlement, issuer blacklist, freeze and burn controls, blockchain analytics and their limits, case studies and risk indicators; non-binding guidance and case material, not measurement. Limit: figure vendor-sourced.

### M23

Stolen or rented identity for onboarding (identity theft, straw owners, account rental).

Sources (recorded scope of each):
- USAO Southern District of New York, CEO of Credit Card Processing Company Charged in $19 Million Credit Card Laundering Scheme (2019-10-11) (2019; fact (practitioner/incident) government). Charging announcement (allegations, not findings): about 26 sham merchant companies headed by paid nominee signers, false merchant applications concealing the true (prohibited telemarketing) merchant, closed accounts quickly replaced, and charges, refunds and chargebacks spread across accounts to evade bank, processor and ISO chargeback monitoring; 2012 to 2015. Limit: allegations.

### M24

Card testing through attacker-controlled merchant or connected accounts.

Sources (recorded scope of each):
- Stripe Docs, Account fraud prevention (Radar for platforms) (2026; fact (vendor documentation) illustrative platform). Vendor guidance for platform account risk: account risk scores and levels, risk metrics, agentic insights (matching bank account rejected for fraud; card-testing example), and reject reasons including card casher (buyer and seller), card tester and no intent to fulfill; no bank-account change guidance; no performance data. Limit: public documentation.

### M25

Merchant financing fraud using fabricated volume or synthetic or stolen business identity, then default.

Sources: none recorded for this mechanism.
