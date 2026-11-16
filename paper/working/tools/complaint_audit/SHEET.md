# Coding sheet

One row per complaint. Mark each tactic `alleged`, `not alleged` or `unclear`, and give the paragraph numbers that support the mark. Code what the complaint alleges about the sellers, the defendants or both. Do not infer a tactic from an outcome.

## Tactics

T1. Split volume. One seller's or scheme's sales are spread across several merchant accounts, entities or processors, so that each stays under a monitoring threshold. Often called load balancing.

T2. Front accounts. Merchant accounts are opened in the names of shell companies or straw owners, or with false statements about who the seller is.

T3. Pooled account. Several sellers' sales run through one merchant account, so that the acquirer or network cannot see each seller's own rates. Often called credit card laundering, factoring or aggregation.

T4. Dilution. Small or sham sales are added to raise the transaction count and lower a ratio. Often called microtransactions.

T5. Outcome suppression. Refunds, reversals or pre-dispute alerts are used so that chargebacks or fraud reports are not recorded against the account.

T6. Changed identity. A statement descriptor, business name or account is changed, or a closed account is replaced, so that reports and history do not follow the seller.

T7. Known and not acted on. A defendant is alleged to have seen chargeback or fraud-report levels, monitoring-program notices, complaints or warnings about a seller, and to have kept processing.

## Context

X1. The monitoring measure the complaint names: chargeback ratio, chargeback count, fraud-report ratio, return rate, other, none.

X2. The payment rail: card, bank debit, remotely created check or payment order, other.

X3. Does the complaint give rates or counts for any account? Yes or no, with paragraph numbers.

X4. Does the complaint allege an attribute shared across the accounts, such as an owner, address, phone number, bank account, website, device or call center? Yes or no, with paragraph numbers.

## Open field

O1. Any other tactic alleged to keep a seller out of monitoring, in the complaint's words, with paragraph numbers.

## Rules for close calls

- A tactic alleged of any seller the defendant served counts once for the complaint.
- `unclear` is for wording that could mean the tactic but does not say so. Quote the wording.
- T1 needs more than one account for the same seller or scheme, and a stated or plain link to thresholds or monitoring. Several accounts alone are not T1.
- T2 is about who the account is said to belong to. T3 is about whose sales run through it. Both can apply.
- T5 needs the refund, reversal or alert to be tied to avoiding chargebacks or reports. Ordinary refunds do not count.
- T6 needs a change over time.
- T7 needs the defendant to have had the information, as alleged.
- For each complaint, record the PDF's address, its page count and its SHA-256.
