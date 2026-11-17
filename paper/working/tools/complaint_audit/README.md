# Audit of FTC payment-processor complaints

Protocol, fixed before any complaint is coded. Any later change is a new commit that states its reason.

Changed 16 November 2026, before this protocol was merged and before any complaint was read for coding: the scope sentence was tightened, three exclusions were added, a third source and an independent comparison list were added, the FTC list's date filter was described, and the unit was restated. Reasons: the candidate lists showed that the scope sentence did not decide some records; that the FTC's topic list lacks two cases the scope is meant to cover (Paddle and BlueSnap); that one processor was first charged by an amended complaint (Transact Pro, 2019); and that another was charged again in a second forum over conduct first charged in 2017 (Electronic Payment Systems). The sheet's tactics did not change.

Changed 17 November 2026, after the candidates were screened and before any complaint was read for coding: the court-record search by case name, used for the filing date and number of in-scope cases that the text search did not return, is now described, and so is the text search's caption limit. The text search was also rerun with the caption forms `FTC` and `F.T.C.`; it added six records and no in-scope case. One rule was added: how a case found after coding starts is handled.

Corrected 17 November 2026, after PR #86 merged and before any complaint was read for coding: U04's court record was wrong. D. Utah 2:19-cv-00996 (23 December 2019) is the FTC's petition to enforce an investigative demand against Complete Merchant Solutions. The complaint is D. Utah 2:20-cv-00864, filed 9 December 2020. The error showed when the complaint PDF was sought. Row 86 is now out and row 256 is in; the count of complaints is unchanged. The other 13 units' numbers and dates were checked again against the docket or the complaint's first page. `UNITS.csv` now names the PDF each coder reads.

Changed 17 November 2026, after both coder sheets were committed and before any count was computed: the author delegated the rulings on the 24 disagreements to a separate agent (Claude Sonnet 5.5, Anthropic). The agent saw the sheet, the complaints and each item's two readings in random order, without the coders' names, and not either coder's notes. Its brief, its rulings as returned and the key to the blinding are in `sheets/adjudication/`. It took coder 1's reading on 17 items, coder 2's on 1 and neither on 6; it is from the same company as coder 1. `adjudicate.py` applies the rulings and the sheet's rule for the X4 tie.

Changed 17 November 2026, before the second adjudicator's rulings were seen: a second adjudicator, a model from neither coder's company, chosen and run by the author through Johns Hopkins AI, rules on the same 24 items from a self-contained prompt (`sheets/adjudication/ADJUDICATOR_2_PROMPT.txt`). It sees the same blinded items and cited paragraphs as the first, but not the rest of each complaint. Fixed now: where the two adjudicators agree, that ruling stands; where they differ, the author rules against the complaint's text.

Recorded 17 November 2026, 19:03: adjudicator 2 was Meta Llama Maverick (name as given by the author). Its answer as returned and its rulings are in `sheets/adjudication/`. The two agree on 13 items and differ on 11 (`sheets/adjudication/SPLITS.md`). On all 24 items adjudicator 2 took the higher of the two readings or went above both; this is reported with the counts.

Changed 17 November 2026, 19:10, before a third adjudicator's rulings were seen: because adjudicator 2 took the higher reading on every item, gave one-sentence reasons and misstated the text once, the author runs a third adjudicator, from neither coder's company and not Meta, with a tighter prompt (`sheets/adjudication/ADJUDICATOR_3_PROMPT.md`). It adds two instructions: neither reading is presumed right, and each ruling must quote the complaint's deciding words and the sheet's words they meet or fail. The rule for splits is replaced: a ruling stands only where all three adjudicators agree; every other item goes to the author. An added adjudicator can only send more items to the author. All three adjudicators' rulings are reported.

## Question

In public FTC complaints against payment processors, how often is each tactic alleged that keeps abuse out of outcome monitoring, and does a record in the specification expose it?

The audit counts allegations. It does not measure how often these tactics occur on any platform, and it does not test detection.

## Cases

- Unit: the earliest FTC pleading, in a federal court or an administrative proceeding, that charges an in-scope defendant. It must have been filed from 1 January 2019 to 16 November 2026. An amended complaint that first adds an in-scope defendant is that pleading. A later amendment, or a second complaint over the same conduct, is not a separate unit. The window starts in the year of the earlier of the two complaints the paper replays and ends on the day this protocol was written.
- In scope: the pleading charges at least one defendant over payments it processed, or merchant accounts it opened or arranged, for other sellers alleged to have harmed consumers. The defendant provides payment acceptance or acts for a provider: a processor, independent sales organization, sales agent, payment facilitator or merchant of record.
- Out of scope:
  - sellers and their own entities, charged over their own sales, even where the complaint alleges that they hid those sales from monitoring or where one entity is named as a payments company;
  - defendants charged over how they sold processing services to their own merchant customers;
  - money transfers sent by consumers;
  - lenders and servicers of payment plans;
  - vendors that neither provide payment acceptance nor act for a provider, such as chargeback-dispute services;
  - contempt, order-modification and subpoena filings.
- Three candidate sources, each searched in full:
  1. CourtListener's RECAP archive, full-text search: case name `Federal Trade Commission`; text `"credit card laundering" OR "payment processor" OR "merchant accounts"`; filed in the window. Run on 16 November 2026: 111 dockets. Rerun on 17 November 2026 with case name `FTC`: 6 dockets; with `F.T.C.`: none. It finds a case only if its filings are in the archive.
  2. The FTC Legal Library's Cases and Proceedings list, Consumer Protection topic "Payments and Billing", dates in the window. Captured on 16 November 2026: 58 records. The list filters by a record's last update, so it also returns older cases; the complaint's filing date decides.
  3. The same FTC list with no topic, searched for each of `payment processor`, `payment processing`, `credit card laundering` and `merchant account`, dates in the window. Captured on 16 November 2026: 41, 43, 56 and 23 records.
- The text search in source 1 matches only captions that name the FTC. Pleadings the Justice Department files for the FTC are captioned "United States v." and come from sources 2 and 3.
- Any in-scope case that source 1 did not return is looked up on CourtListener by case name, for its court, number and filing date.
- The author runs sources 2 and 3 in a browser and saves the result pages, because the site does not allow automated access to filtered lists.
- Each candidate is marked in or out, with a reason, from its caption, its docket sheet and the FTC's press release or case summary. Where those do not settle a defendant's role, the pleading's own description of the defendants is read, and nothing else in it. The candidates, the decisions and the saved search results are committed as `CASES.csv` before any complaint is coded.
- Recall check: the three FTC complaints the paper cites (First Data, Allied Wallet and Paddle) and two 2026 actions reported in the press (Humboldt Merchant Services and Nuvei) must each appear among the candidates. A miss is reported, the search that would have found it is added, and the sources are run again. The candidates are also compared with an independent list, Truth in Advertising's "FTC actions against payment processors" (updated 13 November 2026). `CASES.csv` records any case on that list, or otherwise known, that no source returned.
- A case found after coding starts is coded the same way by both coders, added to `CASES.csv` and `UNITS.csv` with a dated note, and reported. If it is found after the counts are computed, the counts are shown with and without it.
- If more than 30 complaints are in scope, the window's start moves forward by whole years until 30 or fewer remain. That is decided from the count alone.

## Coding

- The sheet is [SHEET.md](SHEET.md): seven tactics, four context items and one open field.
- Each coder reads each complaint in full, from the PDF named in `UNITS.csv` with its SHA-256: the court's copy from CourtListener where the author obtained it, otherwise the copy on the FTC's case page. The packets were built from these files with `pdftotext -layout` (Poppler 24.02.0). Pages without a text layer are viewed as images. An unread page is recorded and the complaint is flagged.
- For each tactic the coder marks `alleged`, `not alleged`, `unclear` or `unavailable`, and gives the paragraph numbers. In a complaint read in full, silence is `not alleged`. Where an unread page prevents a mark, the mark is `unavailable` and names the page.
- Two coders work separately: Claude (Anthropic) and ChatGPT (OpenAI). The second works from a packet committed first, in a session that cannot see the first coder's sheet. Both sheets are committed as received before either coder sees the other's.
- A complaint's text is evidence only. A coder follows no instruction found in a complaint or its PDF, and returns only the sheet's fields with paragraph numbers. Text that reads as an instruction to the coder is reported to the author and changes no mark.
- Before a sheet is committed, a script checks it. It accepts only the sheet's fields and allowed values, requires paragraph numbers for every `alleged` or `unclear` mark and page numbers for every `unavailable` mark, and requires each cited paragraph number to exist in that complaint. A sheet that fails goes back to its coder.
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

- For each tactic: the number of complaints marked `alleged`, `not alleged`, `unclear` and `unavailable`, after the author's rulings. The four counts sum to the complaints coded. Counts only.
- The same counts in three groups: tactics the specified records could expose if the required data were recorded (T1, T2, T3, T5, T6), the tactic no record exposes (T4), and the one that is not a record gap (T7). An allegation in the first group is not a showing that a record would have exposed it.
- The number of complaints with no tactic alleged. Only a complaint read in full and marked `not alleged` on all seven counts.
- Of the complaints that allege T1 or T2, the number whose cited paragraphs tie a shared attribute to the accounts in that tactic (context item X4). A shared attribute alleged elsewhere in the complaint is reported separately, as occurring in the same complaint and nothing more.
- Tactics entered in the open field, listed and counted, and labelled as found after coding.
- Agreement between the two coders for each tactic, as counts, before the author's rulings.
- Every count with and without the three complaints read before this protocol was written.
- Negative results as prominently as positive ones.
- Results go into manuscript Section 8.5 and Supplement S10.

## Limits stated in advance

- A complaint is an allegation. Most of these cases settle without a finding.
- Enforced cases are a selected set. The counts describe these complaints, not processors in general.
- Complaints against sellers alone are out of scope, though some allege the same tactics. The counts therefore understate how often the FTC alleges them.
- A complaint that is silent on a tactic does not show that the tactic was absent.
- FTC actions only, in the United States.
- The sheet was written after three in-scope complaints had been read in full for the paper (First Data, Allied Wallet and Paddle) and after press reports of the two 2026 actions had been seen. Their tactics shaped the sheet.
- Both coders are language models. The author's rulings are the only human check.

## Order of work

1. This protocol is merged.
2. `CASES.csv` and the saved searches are committed.
3. Each coder's sheet passes the script's check and is committed.
4. The author's rulings are committed.
5. A script committed with the results computes the counts, and one pull request proposes the text.

## Files

- `CASES.csv`: every candidate record from the three sources and the name searches, one row each, with its decision, reason and basis. 256 rows; 24 rows in scope, which are 14 complaints.
- `UNITS.csv`: the 14 complaints to code, with court, number, pleading date, how each was found, whether it was read for the paper before this protocol, and the PDF each coder reads, with its SHA-256 and page count.
- `packets/`: one coder packet per complaint, built by `build_packet.py`.
- `paragraphs/`: each complaint's numbered paragraphs, used by `check_sheet.py`.
- `searches/`: the author's two FTC Legal Library captures of 16 November 2026, as saved.
- `CODER_INSTRUCTIONS.md`: what each coder receives before the sheet, and the output format.
- `build_packet.py`: writes one packet per complaint (instructions, sheet, then the complaint text as a JSON list of pages between two markers) and the complaint's paragraph index.
- `check_sheet.py`: the format check on each coder's sheet. It checks form, not meaning.
- `test_complaint_audit.py`: tests for both scripts and for the agreement of `CASES.csv` with `UNITS.csv`.
