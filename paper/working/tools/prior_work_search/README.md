# Prior-work database search

A structured search for sources the paper misses. The strings were fixed on 14 November 2026, before the first run. Any later change is a new commit that states its reason.

## Question

Does a published source state a requirement equivalent to C1, C2 or C3 (manuscript Section 1), combine two of them, contradict a claim the paper makes, or measure something the paper says is unmeasured?

## Strings

[strings.py](strings.py) holds the term blocks and writes every string to [STRINGS.md](STRINGS.md) and [strings.json](strings.json). `python3 tools/prior_work_search/strings.py --check` fails if either file is out of date.

- Six questions. Q1 and Q2 cover C1. Q3 covers C2. Q4 and Q6 cover C3. Q5 covers the setting.
- Q3, Q4 and Q5 are limited to 2022 onward, because they concern language-model agents.
- Eight cited-by searches start from sources the paper already cites.

## Who runs what

- Scopus, Web of Science, IEEE Xplore and the ACM Digital Library: the author runs these by hand. No AI agent searches them. Elsevier's terms for Scopus and IEEE's terms for its digital library restrict automated searching, and the same caution is applied to the other two.
- An AI assistant (Claude) screens what the author sends and records each decision in a file named `SCREENING.md` in this folder.

## Rules

- Each run records the date (UTC), the string as run and the number of hits.
- When a string returns more than 300 hits, export the first 300 by relevance and record the full count.
- Screen by title, then by abstract. A source is critical if it meets the question above, or if it is the peer-reviewed version of a preprint the paper cites.
- A critical source is read in full before the paper cites it or changes because of it.
- Top-up: just before submission, rerun every string for works added since the run date.

## Limits

- Title, abstract and keyword searches miss a source whose abstract uses other words.
- The ACM string is untested. IEEE Xplore allows no wildcard inside a phrase and at most 25 words in a clause, so its strings carry fewer terms.
- One screener. No second person checks the screening.
