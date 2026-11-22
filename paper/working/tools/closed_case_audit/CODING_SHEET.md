# Coding sheet

One row per sampled case, per auditor. Code from the records the case cited and from what the source systems held when the case closed. Use later information only to establish what the systems held then.

## For each case

Record the case's main conclusion in one line, for your own use. It is not shared.

Then answer F1 to F3. For each, the code is `occurred`, `did not occur` or `cannot settle`.

**F1. Absence on partial coverage.**
Did the conclusion rest on a claim that something was absent, such as no report, no link or no earlier activity? If so, look at the query or search behind the claim.
- `occurred`: the query was partial, truncated or limited in scope, so it did not cover the whole population or period that the claim needs.
- `did not occur`: there was no such claim, or the query covered what the claim needs.
- `cannot settle`: the records do not show what the query covered.

**F2. Missing report read as a negative.**
Did the conclusion treat the lack of a report, such as a chargeback or a fraud report, as evidence that nothing was wrong? If so, look at the payment's control decision and the channel's reporting window.
- `occurred`: a decision had closed that channel for the payment, for example a block or a refund, or the channel's window had not ended when the case closed.
- `did not occur`: there was no such reading, or the channel was open and its window had ended.
- `cannot settle`: the records do not show the decision or the window.

**F3. Corroboration from one root.**
Did the conclusion cite two or more records as agreeing with each other? If so, trace each to its origin.
- `occurred`: the records trace to one root observation, or one of them is an earlier conclusion, or was written by someone with that conclusion in front of them.
- `did not occur`: there was no such corroboration, or the records have separate origins.
- `cannot settle`: the origins cannot be traced.

**For each failure coded `occurred`:** would the conclusion change if the failure were corrected? `yes`, `no` or `cannot tell`. Count only `yes` as changed.

**I1. Missing from the inventory.**
Did the conclusion need a record that the paper's signal inventory (Supplement S3) does not list? `yes` or `no`. If yes, name the kind of record in a few words, with no case detail.

## Rules

- A case that the records cannot settle is coded so. That share is itself a result.
- Do not infer a failure from the outcome of the case.
- Code alone. Agreement is counted on the first codes, before any discussion.
- After discussion, each case gets one final code for each failure. Where the auditors still differ, the final code is `cannot settle`.
