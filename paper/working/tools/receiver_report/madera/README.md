# Second documented case: a receiver's reports from inside a processor

Protocol note, fixed 22 November 2026 (UTC), before any page of the three files was read. The protocol in `../README.md` applies unchanged: the same reading rules, the same sheet, and the same three results fixed in advance as counting against the records. Any later change is a new commit that states its reason.

## Source

- FTC and State of Ohio v. Madera Merchant Services, LLC et al., W.D. Tex., No. 3:19-cv-00195. Its complaint is unit U03 of the count (`../../complaint_audit/UNITS.csv`).
- Document 34, filed 23 March 2020, 42 pages. The docket describes it as a notice of the receiver's interim report.
- Document 43, filed 21 April 2021, 27 pages. The docket describes it as an unopposed motion to approve the receiver's final report, accounting, payment and discharge. Document 43-1, 4 pages, is its proposed order.
- `../DOCKET_CHECK.md` listed Documents 34 and 43 as filed and not held by the public archive. The author obtained the three files from PACER on 22 November 2026. They are public court filings and are not copied into this repository. SHA-256 of each file as received:
  - Document 34: `5055b4a555b01b1f84a226b680b27815b0e6b14a10cc2683e45ecd0ee1d0cdaf`
  - Document 43: `2d4161e5c29f45010864089752852400db05dc32ca1c435273f9fc5ee7f8dc2d`
  - Document 43-1: `633357a04e51da2607aaf53b371df7063198c5d6f51a064758403c5b183c8437`

## Why this case

The docket check found it. Of the 14 dockets it is the only other one that lists a receiver's report. It was not chosen for what it says.

## Seen before this note

- The complaint for U03, coded for the count in Supplement S10.1.
- The docket's entry descriptions that the docket check returned.
- Search excerpts of the FTC's posted orders and press pages in this case. They say the court appointed a temporary receiver over the two processor companies, that the companies processed remotely created payment orders, and that the case ended in stipulated orders. None of those documents was read in full.
- The three files' names, sizes, page counts and creation dates. No page had been read.

## What differs from the first case, fixed now

- The receivership is over a processor, not a seller. `held_by` and `processor_knew` record what the report says this processor's own staff, files or systems held.
- The sheet's tactics were written with card payments in mind, and this processor used remotely created payment orders. A tactic is marked as stated only if the report states it in substance for that payment type: returned items in place of chargebacks, bank accounts in place of merchant accounts. Each such reading is noted in the row.
- Beyond the sheet, one more thing is recorded: what the report says the processor recorded about returned payments, by merchant and by bank account, and what was done with those records. If the report shows the processor tracked returns by merchant and kept processing, that counts against the records, under the first of the three fixed results.
- A report that deals only with assets, bank accounts and the receiver's administration states no tactic. If so, that is the result, and it is reported.

## What the case cannot show

- How often any tactic occurs. It is one case, and the docket ended in stipulated orders.
- A court's findings. A receiver reports to the court.
- That a specified record would have exposed the conduct.

## Reader and fairness

- Read and coded by Claude (Anthropic), which was also one of the two coders of the complaint for U03. There is no second reader and no human check, unless a later note says so.
- No individual is named in the paper. Roles only.
- Every recorded statement carries its page and line. Every page is checked for extracted text, and a page with little or none is viewed as an image.

Recorded by Claude (Anthropic), 22 November 2026.
