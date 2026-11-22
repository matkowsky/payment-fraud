# One documented case: a receiver's report read against the tactic sheet

Protocol, fixed 22 November 2026 (UTC), before the report was read in full. Any later change is a new commit that states its reason.

## Question

The count in Supplement S10.1 covers allegations. Does a court-appointed receiver's report, written from one operation's own books, files and staff interviews, state any of the seven tactics as fact? For each tactic it states: on what basis, who held the information, and which specified record bears on it.

## Source

- FTC v. Apex Capital Group, LLC et al., C.D. Cal., No. 2:18-cv-09573. Its first amended complaint is unit U02 of the count (`../complaint_audit/UNITS.csv`).
- Preliminary Report of Temporary Receiver, Document 31, filed 28 November 2018: the report (21 pages), an appendix (3 pages), Exhibits 1 to 10 (29 pages) and Exhibits 11 to 22 (182 pages). Read from the copies in CourtListener's RECAP archive.
- How the case was chosen: two of the 14 dockets were checked for filed records beyond the complaint. This one holds a receiver's report. The other, Complete Merchant Solutions, has only the judgment available. The other 12 dockets were not checked. The case is not a sample.

## Seen before this protocol

Keyword searches of the report's text for "chargeback" and "merchant account" returned snippets. They showed refunds issued on vendors' alerts to avoid account cancellations, accounts opened through nominee companies and paid signers, and totals for the nominee companies' sales, refunds and chargebacks. The report had not been read in full and no exhibit had been opened. The complaint for U02 had been coded for the count.

## Reading

- The report is read in full. Every page is checked for extracted text. A page with little or none is viewed as an image.
- An exhibit is read only if a statement used here rests on it. Every exhibit not read is listed as not read.
- Every recorded statement carries its page and line.

## Sheet

`FINDINGS.csv`, one row per tactic T1 to T7 as `../complaint_audit/SHEET.md` defines them:

- `stated`: yes, no or unclear. Whether the report states the tactic as fact, not whether the complaint alleges it.
- `basis`: staff statement, books or files, exhibit, or the receiver's own inference, with any words the report uses about reliability.
- `held_by`: who had the information, as the report tells it: seller, processor, bank or vendor.
- `processor_knew`: what the report says a processor or bank knew or did, if anything.
- `record`: the record that Table S10.1 names for the tactic, and whether the report's facts fit that reading, cut against it or do not bear on it.
- `locator`: page and line.

Figures are recorded only as the report states them, with its own qualifiers, in `FIGURES.csv`.

## Fixed before reading: what counts against the records

- A stated tactic where a processor or bank had the information and kept processing. The gap is then not a record.
- A stated tactic for which Table S10.1 names no record, or where the report shows no attribute a processor could have seen across accounts.
- An account closed by ordinary monitoring, without the specified records.

Such findings are reported with the same weight as the others.

## What the case cannot show

- How often any tactic occurs. It is one case, chosen because its record is rich.
- What a processor's own systems recorded. The report is written from the seller's side.
- That a specified record would have exposed the conduct. It can show the conduct and who held which information.
- A court's findings. A receiver reports to the court, this report is preliminary, and the docket shows stipulated orders.

## Reader and fairness

- Read and coded by Claude (Anthropic), which also coded the complaint for U02. There is no second reader and no human check, unless a later note says so.
- No individual is named in the paper. Roles only.
- If the paper repeats what the report says about a named processor's conduct, that processor's own filing is read, where the docket has one, and its position is given in a sentence.

## Report

Whatever the sheet shows goes in the supplement. Results against the records are given the same prominence as results for them.

## Changes after the protocol

22 November 2026 (UTC), after the reading. The text above is unchanged.

- Figures are in `EXHIBIT15_FRAUD_TABLE.csv` and `EXHIBIT19_INCOME.csv`. No `FIGURES.csv` was made. Reason: every figure used comes from one of two exhibit tables, and each table is kept whole as transcribed.
- A check of the terminal websites in Exhibit 15 against the domain list in Exhibit 18 was planned in `READING.md` and dropped. Reason: the processor's own list already ties the terminals to one client, so the check could change no finding. Exhibit 18 stays unread and is not cited.
- The stipulated order between the Commission and the processor (Document 142) was read in full. Reason: the supplement gives the processor's position, so it also gives how the claims against it ended.

22 November 2026 (UTC), later. The text above is unchanged.

- All 14 dockets were then searched the same way, under `DOCKET_CHECK.md`. "The other 12 dockets were not checked" describes how the case was chosen, not the present state. Result: this docket is the only one of the 14 in which the archive holds a receiver's report or a decision in which the court states facts.

22 November 2026, 22:01Z. The text above is unchanged.

- A second case was read: the receiver's reports in U03, which the archive lists and does not hold. Its protocol note, sheet and reading record are in `madera/`. The protocol above applies to it unchanged; `madera/README.md` fixes what differs.
