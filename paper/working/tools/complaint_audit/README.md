# Audit of FTC payment-processor complaints

Protocol, fixed before any complaint is coded. Any later change is a new commit that states its reason.

## Question

In public FTC complaints against payment processors, how often is each tactic alleged that keeps abuse out of outcome monitoring, and does a record in the specification expose it?

The audit counts allegations. It does not measure how often these tactics occur on any platform, and it does not test detection.

## Cases

- Unit: one FTC complaint, as first filed in a federal court or as an administrative complaint, from 1 January 2019 to 16 November 2026. The window starts in the year of the earlier of the two complaints the paper replays and ends on the day this protocol was written.
- In scope: the complaint charges at least one defendant over payment acceptance it provided to other sellers: card or bank-debit processing, merchant accounts or access to them, as a processor, independent sales organization, sales agent, payment facilitator or merchant of record.
- Out of scope: defendants charged only over their own sales; money transfers sent by consumers; contempt, order-modification and subpoena filings; amended complaints, because the first filing is the unit.
- Two candidate sources, each searched in full:
  1. CourtListener's RECAP archive, full-text search: case name `Federal Trade Commission`; text `"credit card laundering" OR "payment processor" OR "merchant accounts"`; filed in the window. Run on 16 November 2026: 111 dockets.
  2. The FTC Legal Library's Cases and Proceedings list, Consumer Protection topic "Payments and Billing", dates in the window. The author runs it in a browser and saves the result pages, because the site does not allow automated access to filtered lists.
- Each candidate is marked in or out, with a reason, from its caption, its docket sheet and the FTC's press release or case summary only. The candidates, the decisions and the saved search results are committed as `CASES.csv` before any complaint is coded.
- Recall check: the three FTC complaints the paper cites (First Data, Allied Wallet and Paddle) and two 2026 actions reported in the press (Humboldt Merchant Services and Nuvei) must each appear among the candidates. A miss is reported, the search that would have found it is added, and both sources are run again.
- If more than 30 complaints are in scope, the window's start moves forward by whole years until 30 or fewer remain. That is decided from the count alone.

## Coding

- The sheet is [SHEET.md](SHEET.md): seven tactics, four context items and one open field.
- Each coder reads each complaint in full, from the filed PDF. Pages without a text layer are viewed as images. An unread page is recorded and the complaint is flagged.
- For each tactic the coder marks `alleged`, `not alleged` or `unclear`, and gives the paragraph numbers. Silence is `not alleged`.
- Two coders work separately: Claude (Anthropic) and ChatGPT (OpenAI). The second works from a packet committed first, in a session that cannot see the first coder's sheet. Both sheets are committed as received before either coder sees the other's.
- The author, a lawyer, rules on each disagreement against the complaint's text. His rulings are committed with their paragraph references.

## What each tactic means for the records, fixed in advance

Record names follow manuscript Section 8.5 and Supplement S10.

| Tactic | Bearing on the specification |
|---|---|
| T1 Split volume | Exposed by a view over recorded links between accounts, and only where a shared attribute is recorded |
| T2 Front accounts | The same; with no recorded shared attribute, nothing exposes it (a stated limit) |
| T3 Pooled account | Exposed only where each payment and report keeps its own seller |
| T4 Dilution | Not exposed: padded sales look like clean payments (a stated limit) |
| T5 Outcome suppression | Exposed by keeping the fraud report or alert as its own record, with the refund's effect on the chargeback channel (requirement C1) |
| T6 Changed identity | Exposed by per-payment descriptors and successor links |
| T7 Known and not acted on | Not a record gap: on the allegation, the defendant had the evidence |

The audit says nothing about requirements C2 and C3.

## Report, fixed in advance

- For each tactic: the number of complaints that allege it, out of all complaints coded. Counts only.
- The same counts in three groups: tactics a record exposes (T1, T2, T3, T5, T6), the tactic no record exposes (T4), and the one that is not a record gap (T7). Also the number of complaints that allege no tactic on the sheet.
- Of the complaints that allege T1 or T2, the number that also allege a shared attribute a platform could have recorded (context item X4).
- Tactics entered in the open field, listed and counted, and labelled as found after coding.
- Agreement between the two coders for each tactic, as counts, before the author's rulings.
- Every count with and without the three complaints read before this protocol was written.
- Negative results as prominently as positive ones.
- Results go into manuscript Section 8.5 and Supplement S10.

## Limits stated in advance

- A complaint is an allegation. Most of these cases settle without a finding.
- Enforced cases are a selected set. The counts describe these complaints, not processors in general.
- A complaint that is silent on a tactic does not show that the tactic was absent.
- FTC actions only, in the United States.
- The sheet was written after three in-scope complaints had been read in full for the paper (First Data, Allied Wallet and Paddle) and after press reports of the two 2026 actions had been seen. Their tactics shaped the sheet.
- Both coders are language models. The author's rulings are the only human check.

## Order of work

1. This protocol is merged.
2. `CASES.csv` and the saved searches are committed.
3. Each coder's sheet is committed.
4. The author's rulings are committed.
5. A script committed with the results computes the counts, and one pull request proposes the text.
