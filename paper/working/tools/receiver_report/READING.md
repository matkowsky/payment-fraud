# Reading record

Written 22 November 2026 (UTC), after the protocol (`README.md`) was committed. Revised the same day after the page images were viewed and two more documents were read; the revisions are marked.

Locators: `R 11:6-12` is Document 31, page 11 of 21, lines 6 to 12. `X15 61` is Document 31-3, page 61 of 182, which falls in Exhibit 15.

## Read

| Part | Pages | How |
|---|---|---|
| Report, Document 31 | 1 to 21, all | Extracted text. Every page has 109 to 411 words, so none is a scan |
| Exhibit 15, emails from one foreign processor | Document 31-3, 58 to 74, all | Extracted text. The fraud table appears three times in the thread with the same figures |
| Exhibit 19, the receiver's accountant's review, with its lists A and B and summary C | Document 31-3, 128 to 138 | Extracted text |
| The foreign processor's motion to dismiss, Document 104 (added) | 1 to 30, all | Extracted text. Every page has 113 to 415 words |
| Stipulated order between the Commission and that processor, Document 142 (added) | 1 to 30, all | Extracted text. Every page has 131 to 350 words |

Docket entry 123, the order denying the motion, was read only as its docket entry. The order is not in the archive.

## Page images viewed (added)

- Report: pages 11, 12, 13, 14, 16 and 17.
- Exhibit 15: Document 31-3 pages 59, 60, 61, 62, 63 and 69.
- Exhibit 19: Document 31-3 pages 130, 131 and 133.

What the images settled:

- Every value in `EXHIBIT15_FRAUD_TABLE.csv` matches the table on page 63, where no stamp covers a cell. On page 61 the exhibit stamp hides two cells, and on page 62 the header stamp hides one.
- The images show something the extracted text lacks: the fraud-amount and fraud-amount-percentage columns, and three of the four merchant names, are highlighted.
- The fraud table does not state its currency.
- Every value, row label and currency in `EXHIBIT19_INCOME.csv` matches pages 130 and 131. The parity note is footnote 1 on page 130 and the text above the second table on page 131.
- A correction. `FINDINGS.csv` first said the processor's list had 32 terminals. Pages 59 and 60 show 36: eight, eight, twelve and eight under the four companies. Four of the twelve are the terminals the processor says it acquires directly. The sheet now says 36.

`check_figures.py` checks both transcribed tables against themselves. In Exhibit 19, every column of every file sums to its total. In Exhibit 15, every percentage equals its amount or count ratio. So the transcribed totals and ratios reconcile internally, and the values, row labels, currencies and footnote were checked against the page images listed above.

## Not read

- Exhibit 19's attached statements, Document 31-3 pages 139 to 168: images with no extracted text. No figure used rests on them.
- Exhibit 14, call scripts: pages 54 to 57 seen; the rest not read.
- Exhibit 16, a chat: an image, not viewed. The report quotes it.
- Exhibit 18, a list of hosted domains, pages 81 to 127: a few rows seen.
- The appendix (Document 31-1), Exhibits 1 to 10 (Document 31-2), and Exhibits 11 to 13, 17 and 20 to 22: not opened.
- The declaration attached to the motion (Document 104-1): not read. The motion's facts rest on it.

## Figures from Exhibit 19 (revised)

Exhibit 19 keeps one file in pounds and two in dollars. The report (R 16, footnote 17) and the exhibit (X19 130 and 131) both assume one pound equals one dollar. Any figure here that pools the files uses that parity and says so. The exhibit notes that a pound was then about 1.27 dollars.

- At parity, the Refunds and Chargebacks rows of the three files sum to 14,782,397.84 of 62,294,426.00 in sales, 23.73 percent. For the two U.K. files they sum to 12,452,389.41 of 45,538,022.59, 27.35 percent. Pre-arbitration amounts and chargeback reversals are not netted.
- The report says refunds and chargebacks were "nearly $15 million, representing 20% of gross sales by the nominee entities" (R 17:12-14). The amount matches. The 20 percent cannot be reproduced from those rows, and its denominator is unresolved. The report's 27 percent for the U.K. entities does match. The paper uses the U.K. figure and not the 20 percent.
- The U.S. file's table (X19 131) shows 2,330,008.43 in its Refunds row and no figure in its Chargebacks row. The review's text (X19 133) calls the same amount refunds and chargebacks. The split is unknown. It is reported as a conflict, not as zero chargebacks and not as refunds only.

## The processor's own position (added)

From its motion to dismiss, Document 104. These are the motion's statements, not the court's and not findings about the Exhibit 15 emails, which the motion does not discuss.

- It is a licensed payment processor in Latvia. It processed for the U.K. companies through two Latvian banks, and all its conduct took place in Latvia (pages 8 to 11).
- It disputes the credit card laundering claim (page 17) and calls unfounded the claims that it helped lower chargeback ratios through microtransactions and volume increases (page 18). It says its staff in Latvia sent the commands for those microtransactions (pages 11 and 18) and does not concede their purpose.
- It says several merchant accounts for one client are "a common practice encouraged by Visa and Mastercard" (page 17).
- Its regulator investigated, issued preliminary findings on 23 April 2018 and signed an administrative agreement with it on 12 November 2018. The regulator also suggested that it terminate its negative-option accounts, and it says it did so as of November 2018 (pages 12 and 13).
- It disputes the chain from its conduct to harm in the United States (page 28).

The court denied the motion on 16 September 2019 (docket entry 123). On 15 January 2020 it entered a stipulated order (Document 142). In it the processor neither admits nor denies the complaint's allegations, and judgment of 3.5 million dollars is entered. The order requires chargeback rates to be calculated for each of a high-risk client's accounts and in the aggregate (Section VI.C), and chargeback and refund totals to be kept by amount and by number (Section XII.D).

## The three results fixed in advance as counting against the records (added)

1. A processor had the information and kept processing. Occurred, for the foreign processor: it held the fraud figures and the list tying the companies and terminals to one client, wrote that four terminals would keep working and later offered new accounts (X15 59-63, 69). The same emails show the bank stopping Visa and then Mastercard for the four companies.
2. No record named, or no attribute a processor could have seen across accounts. Partly met. For the front accounts the report names no shared attribute that a domestic processor held. It does show one on the seller's side, a single server hosting its websites (R 5:8-9), and does not say whether a processor could see it.
3. An account closed by ordinary monitoring, without the specified records. Not settled. The report says a spate of domestic accounts was cancelled for chargebacks (R 12:10-12) and that accounts closed for excessive chargebacks, "as they all were" (R 14:19-21). The same page says five newer domestic accounts were still processing (R 14:23-26). The report does not say what any processor monitored.

## Steps listed before any text went in the paper (closed)

1. Read Document 104 and give the foreign processor's position. Done, above.
2. View the page images of every page relied on. Done for the pages listed above. Exhibit 19's statements were not viewed; no figure rests on them.
3. Read Exhibit 14 in full if the scripts are used. Not needed: the supplement does not use the scripts.
4. Check the terminal websites of Exhibit 15 against Exhibit 18. Dropped; `README.md` gives the reason.
