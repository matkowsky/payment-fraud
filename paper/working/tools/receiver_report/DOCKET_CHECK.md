# Docket check: which of the 14 cases hold a filed record beyond the complaint

Protocol, fixed 22 November 2026 (UTC), before the search below was run on any docket but one. Any later change is a new commit that states its reason.

## Question

For each of the 14 dockets in `../complaint_audit/UNITS.csv`: does CourtListener's RECAP archive hold, in full, either of these?

- (a) A report to the court by a receiver or a monitor.
- (b) A decision in which the court states facts: findings of fact, a decision on summary judgment, a decision on a contested preliminary injunction, a magistrate judge's report and recommendation, or an opinion.

## Why

`README.md` says two of the 14 dockets were checked and the case read is not a sample. This check puts the same search to all 14, so that which cases are read does not depend on what was already known.

## Seen before this protocol

- U02 (Apex): the receiver's report was read under `README.md`. U04 (Complete Merchant Solutions): four searches found only the judgment in the archive.
- The complaints of all 14 were coded for Supplement S10.1.
- The search's form was tried once on U02, whose result was known, to see that it finds the receiver's report. The search fixed below is narrower than that trial.
- For the other 12 dockets, no entry was looked at for this check before the protocol was fixed.

## Search

One search for each docket, by court and docket number, over CourtListener's index of docket entries (search type `rd`), oldest first:

```
(short_description:report AND description:(receiver OR monitor))
OR short_description:(opinion OR memorandum OR "findings of fact"
   OR "order on motion for summary judgment"
   OR "order on motion for partial summary judgment"
   OR "order on motion for preliminary injunction"
   OR "report and recommendations")
OR description:("findings of fact" OR "memorandum opinion" OR "memorandum decision"
   OR "opinion and order" OR "report and recommendation")
```

If the search returns nothing, a second search confirms that the archive has the docket at all.

## What counts

- Counted: an entry of kind (a) or (b) whose document the archive holds in full.
- Listed, not counted: an entry of kind (a) or (b) that the archive does not hold. It may exist on PACER.
- Not counted: stipulated orders, consent judgments and default judgments, which state no contested facts; a party's motion, brief, declaration or exhibit; a receiver's fee application, bond or status report on administration.
- An entry's kind is judged from its description. Where the description does not settle it, the document's first page does.

## What follows

- Every docket's result is recorded in `DOCKET_CHECK.csv`, including "nothing found".
- Every counted document is read under `README.md`, unchanged: the same sheet, the same three results fixed in advance as counting against the records, roles only. They are read in unit order. A document that cannot be read in full is listed as not read.
- The supplement reports how many dockets held a counted document and what each reading found, with results against the records given the same prominence as results for them.

## Limits

- The archive holds what its users have bought from PACER. "Nothing found" means nothing in this archive under this search, not that nothing was filed.
- The search reads entry descriptions. A decision entered under another label can be missed.
- Party exhibits are not searched. Some hold a processor's own records, as in Supplement S10.2.
- Three of the 14 cases were filed in 2025 or 2026 and may have no decision yet.

## Changes after the protocol

22 November 2026, 16:29Z, after the fixed search had run on all 14 dockets and before any second search. The text above is unchanged.

- Result of the fixed search: it returned entries for one docket, U02, and nothing for the other 13.
- A second search is added and put to all 14 dockets. Reason: the fixed search asks for particular entry labels, and courts label entries differently, so a report or decision under another label would be missed. The second search reads entry descriptions alone:

```
description:(receiver OR monitor OR "special master" OR "summary judgment"
   OR "motion to dismiss" OR "preliminary injunction" OR findings OR opinion)
```

- What counts, what is only listed and what follows are unchanged. Both searches' results are recorded for every docket.

## Result

Searches run 22 November 2026, 16:22Z to 16:39Z. `DOCKET_CHECK.csv` has one row for each docket.

- Counted: one document, in one docket of 14. It is the receiver's preliminary report in U02, which Supplement S10.3 already reads.
- Listed, not counted, because the archive does not hold them:
  - U03: a notice of the receiver's interim report (Document 34, 23 March 2020) and a motion to approve the receiver's final report (Document 43, 21 April 2021).
  - U02: six later status reports by the receiver, and a court of appeals memorandum of 14 December 2023. CourtListener's opinion search does not hold that memorandum either.
- The other 12 dockets: no entry of kind (a) or (b) under either search. Their latest entries are judgments, injunctions, consent or stipulated orders, or orders on motions.
- Neither search returned a decision on summary judgment, a decision on a contested preliminary injunction, findings after trial or a magistrate judge's report in any docket.

## Judgments made in applying the protocol

- An ex parte restraining order is not counted, though it has a section headed findings. It rests on one party's showing. U02's is held (Document 16).
- An order on a motion to dismiss is not counted. It takes the complaint's allegations as true and states no facts. U02 lists two, neither held.
- U01's receiver was a liquidating receiver. Its filings concern the sale of real property and a final accounting, which the protocol does not count.
- For U02 the second search was run with an added filter on entry labels, to limit output. Every other docket got the search as fixed.
- For U13 and U14 every entry the archive lists was also read, four and six entries.

## What was not done

- Nothing was bought from PACER. The two U03 filings may be there. The U03 complaint charges the two companies as payment processors. The FTC's posted copy of the stipulated preliminary injunction says the court appointed a temporary receiver over them; that was seen as a search excerpt and the order was not read in full. If so, these would be a receiver's account from inside a processor, which the one report read is not.
- Party exhibits were not searched.
- The count of documents the archive indexes was not taken for U02 and U06.

Corrected in this commit: the time of the change above read 16:30Z; the commit that recorded it was made at 16:29Z.

Recorded by Claude (Anthropic), 22 November 2026.
