# Prior-work database search

A structured search for sources the paper misses. The strings were fixed on 14 November 2026, before the first run. Any later change is a new commit that states its reason.

Changed 14 November 2026, with no run recorded in this folder: the export limit, the top-up and the databases each question runs in are now stated in full, because an independent review found them ambiguous. No string changed.

## Question

Does a published source state a requirement equivalent to C1, C2 or C3 (manuscript Section 1), combine two of them, contradict a claim the paper makes, or measure something the paper says is unmeasured?

## Strings

[strings.py](strings.py) holds the term blocks and writes every string to [STRINGS.md](STRINGS.md) and [strings.json](strings.json). `python3 tools/prior_work_search/strings.py --check` fails if either file is out of date.

- Six questions. Q1 and Q2 cover C1. Q3 covers C2. Q4 and Q6 cover C3. Q5 covers the setting.
- Q1 to Q5 run in all four databases. Q6 runs in Scopus and Web of Science only.
- Q3, Q4 and Q5 are limited to 2022 onward, because they concern language-model agents.
- Eight cited-by searches start from sources the paper already cites.

## Who runs what

- Scopus, Web of Science, IEEE Xplore and the ACM Digital Library: the author runs these by hand. No AI agent searches them. Elsevier's terms for Scopus and IEEE's terms for its digital library restrict automated searching, and the same caution is applied to the other two.
- An AI assistant (Claude) screens what the author sends and records each decision in a file named `SCREENING.md` in this folder.

## Rules

- Each run records the date (UTC), the string as run, the number of hits and the number exported.
- When a run returns more than 300 hits, export the first 300 by relevance and record the full count. This holds for every run. CB4 and CB7 have no terms to search within: export every citing document, up to that limit.
- Screen by title, then by abstract. A source is critical if it meets the question above, or if it is the peer-reviewed version of a preprint the paper cites.
- A critical source is read in full before the paper cites it or changes because of it.

## Top-up, just before submission

- Rerun every string for works the database added since the baseline run date. The baseline strings and exports stay as they are; the top-up strings are a new commit.
- Raise the last year to the year of the top-up in the Web of Science strings and in the IEEE and ACM year filters, which stop at 2026. The Scopus strings have no last year.
- Where a database can filter by the date it added a record, use that filter from the baseline run date on. Where it cannot, limit the run to publication years from the baseline year on.
- Export every hit of a top-up run, in batches if there are more than 300, and record the count.
- Remove records the baseline exported, by DOI or, without one, by the database's record number. Screen the rest.

## Limits

- Title, abstract and keyword searches miss a source whose abstract uses other words.
- The ACM string is untested. The IEEE strings use no wildcard and at most 25 words in a clause, so they carry fewer terms. Those two limits are this protocol's cautious choices; they were not tested on the site.
- A baseline run above 300 hits is cut at 300 by relevance, so a relevant source ranked lower is missed.
- Where a top-up run is limited by publication year, a work published earlier and added late is missed.
- One screener. No second person checks the screening.
