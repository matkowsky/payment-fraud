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

Recorded by Claude (Anthropic), 22 November 2026.
