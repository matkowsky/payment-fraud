# Closed-case audit kit

A way for a payment platform, processor or bank to measure, on its own closed investigation cases, how often the three failures occur that the paper's requirements target. It carries out "A first study within a quarter" in Supplement S7.1.

No case data leaves the organization. The only thing shared, if the organization chooses to share, is a form of counts.

## What the audit measures

For a random sample of closed cases, how often each of these occurred, and how often it would have changed the case's conclusion:

- F1. An absence claim rested on a query that was partial, truncated or limited in scope (requirement C2).
- F2. A missing report was read as a negative on a channel that a decision had closed, or whose reporting window had not ended (requirement C1).
- F3. Corroboration rested on records that trace to one root observation or to an earlier conclusion (requirement C3).

It also records whether the conclusion needed a record that the paper's signal inventory lacks.

## What it cannot show

- Whether the specified records would have prevented a failure. It measures how often the failures occur.
- Anything about cases outside the sampling frame.

A result of no failures is a result. It would count against the need for the records and is reported with the same prominence as any other.

## Before you start

- The audit reviews identifiable staff's work on real case records. Get your organization's ethics and privacy review first.
- Fix the sampling frame, the sample size and the two auditors before any case is opened. Write them in the form.
- Sample size: with 200 settled cases an exact 95 percent interval on any share is at most 14.3 points wide; with 160, at most 16.0.

## Steps

1. Draw the sample at random from the frame.
2. Two auditors code every case separately with [CODING_SHEET.md](CODING_SHEET.md). They do not confer until both have coded all cases.
3. Count agreement before any discussion. Then settle differences and record the final code for each case.
4. Fill in [RESULTS_FORM.csv](RESULTS_FORM.csv).
5. Run `python3 summarize.py RESULTS_FORM.csv`. It checks that the counts add up and prints each share with its exact 95 percent interval, and the range each share could take if the unsettled cases were all occurrences or all none.

[EXAMPLE_FORM.csv](EXAMPLE_FORM.csv) shows a filled form. Its counts are invented.

## Sharing the form

Sharing is optional. If you share:

- Send the form only. It holds counts and four descriptive lines. Do not send case, account, customer or staff data.
- Choose how you are identified: by name, by a description you write, such as "a European acquirer", or not at all.
- The form is added to this folder as received, and the paper's next version reports its counts. Results against the records get the same prominence as results for them.
- You may withdraw the form at any time before that version is released.
- Send it to the corresponding author, whose address is on the paper's first page.

## Files

- `CODING_SHEET.md`: what the auditors record for each case.
- `RESULTS_FORM.csv`: the blank form.
- `EXAMPLE_FORM.csv`: a filled form with invented counts.
- `summarize.py`: checks a form and computes the shares, intervals and ranges. Standard library only; Python 3.9 or later.
