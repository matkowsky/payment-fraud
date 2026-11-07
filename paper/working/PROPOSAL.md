# Statistical evaluation revisions proposed for version 1.1

**Status at submission: proposed for review.** See [STATUS.md](STATUS.md) and the linked PR for the current state. The rationale and drafting/checking attribution below describe the submitted proposal.

Human author and submitter: **Jonathan Matkowsky**. **Jointly drafted by Jonathan Matkowsky and ChatGPT (OpenAI), based on Jonathan's notes and direction.** ChatGPT implemented the repository edits, rebuilt the documents and performed the recorded checks. Drafting collaboration, technical checking, review and acceptance are distinct contributions. The statistical review prompting this proposal was also AI-assisted. These are not independent human peer reviews. At submission, Claude had not been recorded as reviewing this candidate; a later review should identify the reviewer or assistant and the exact commit reviewed. Claude's later review and its follow-up edits are recorded in the Review record section below.

## Baseline and scope

The candidate starts from the [published version 1.0 package](https://github.com/matkowsky/payment-fraud/tree/98f5c0e787756c2251fa70927407efb4107699a4/paper/v1.0), not a private version 1.1 working copy. The published package SHA-256 is `2614b465e53dce9e724739ceb99c21579c6d23e15f8bd82ee39c48c800192e46`; every extracted file was checked against the GitHub blob identity. Previously documented private source-reading corrections and unrelated planning notes are outside this proposal and remain separate work.

The first proposal-branch commit copies the unchanged baseline to `paper/working/`. Subsequent commits contain the proposed edits. Review the source diffs between that baseline-copy commit and the candidate head for a focused comparison; the pull request links it. Reader-facing Markdown and PDFs are regenerated from the citation-key sources.

## Proposed changes

| Item | Location | Before | Proposed behavior and reason |
|---|---|---|---|
| E9 endpoint | Manuscript 9.1; Supplement S7 and S7.1 | A realized comparison with a noisy holdout reference is called reduction in absolute bias. | Define reduction in absolute error against the same mature holdout reference, with joint uncertainty. Specify a reported-outcome target, not all underlying fraud. A statistical bias claim would require a separate explicit sampling expectation and identified target. |
| E3 harm guardrail | Manuscript 9.1; Supplement S7.1 | An observed false-flag increase of at most five percentage points passes. | Require the prespecified one-sided 95% upper bound to be below the margin, preserving business pairing and additional clustering. Size the complete rule. This strengthens the proposed test rather than correcting arithmetic. |
| E8 sizing | Supplement S7.1 | Correct 299/628 examples appear within a clustered study design without a local qualification. | Label them independent-trial, single-endpoint illustrations. Keep the values and existing requirement to size the complete clustered study. |
| Decision-rule clarity | Supplement S7.1, introduction and E1 | Non-support can be confused with evidence against a requirement; E1 differs at exact equality with its margin. | Distinguish support, evidence against and inconclusive/unidentified results. Make equality fail to establish E1 support, matching the manuscript. |
| Reproduction count | REPRODUCE.md | One sentence says 120 cited works despite the 122-work package. | Correct the stale count to 122. |
| Optional helper | tools/iterate.sh | Obsolete output stem and pipelines can mask build/check failure. | Use the candidate filename, propagate build/check exit status, and tolerate only the ordinary diff status indicating changes. |
| Result-state rules (review) | Supplement S7.1, introduction | Three result states were named, but only support had a rule. | Give each state a rule: evidence against when the bound at the same confidence level, taken from the other side, lies on the failing side of the threshold; inconclusive when neither holds or the target is unidentified. |
| E9 interval method (review) | Supplement S7.1, E9 | The joint uncertainty procedure for D was left open. | Note that D is not smooth where C1 succeeds, so standard intervals can miss their coverage there. Name the method in advance and size part (b) by simulating it. |
| E3 margin (review) | Supplement S7.1 | The false-flag margin was fixed at 5 points and missing from the named parameters. | Name it with E1's and E8's parameters and keep 5 points as the proposed default. |
| Attribution scope (review) | README.md; paper/working/README.md and STATUS.md | The drafting credit read as covering the whole working manuscript. | Scope it to this proposal's changes and record the review edits separately. |

The five-percentage-point margin remains a proposed default to fix and justify before collection. This revision does not establish that it is appropriate for every platform. No evaluation has been run on platform data and no system effectiveness is claimed.

## Questions for reviewers

1. Does E9 now state an interpretable reference-error target and its limits? Would the intended use instead require a fully specified bias estimator?
2. Is E3's stronger inferential guardrail appropriate for its confirmatory role, and are its pairing, clustering and full-rule power requirements clear?
3. Are E8's illustration and the three result states clear without obscuring the unchanged substantive requirements?
4. Do the source and generated-document changes agree, and are the supporting-file repairs sufficient?

Comment on the pull request's source lines, or link a focused issue from the [revision tracker](https://github.com/matkowsky/payment-fraud/issues/2). Further commits on this branch remain proposals. Maintainer acceptance is recorded by merge; a published version requires a separate release record.

## Validation

Build environment: Pandoc 3.1.3; XeLaTeX from TeX Live 2023/Debian. The manuscript and supplement rebuilt successfully (45 and 31 pages). The existing package consistency checks passed, including 122 cited works, joins, lineage and hypothetical arithmetic; the five helper success/failure tests passed. ChatGPT inspected page overview renders and the changed evaluation passages. Citation sequences, reference sources, CSV data and SVG figure sources remain unchanged. Figure PDF/PNG exports were regenerated by the build. These are technical checks, not independent human review.

Run `python3 CHECK_CANDIDATE.py` for the existing package consistency and hypothetical-arithmetic checks. Run `python3 tools/test_iterate.py` for the helper's success and failure paths. `MANIFEST_SHA256.txt` identifies this proposed package. None of these checks proves source claims, novelty or operational effectiveness.

For a statistical cross-check: in the review's simple binary paired example, five additional false flags among 100 businesses has a one-sided exact 95% upper bound of 10.2253%; at a true six-percentage-point increase the old descriptive rule passes with probability 44.0693%. These are stipulated examples, not observed platform results. E8's independent-trial arithmetic retains the original values; its power at n=628 and true release probability .001 is approximately 97.4101%, exceeding the stated 93% target.

## Automatic status after merge

The working manuscript now uses stable `MANUSCRIPT.md` and `MANUSCRIPT.pdf` filenames. After GitHub confirms that the proposal configured in `REVISION_STATUS.json` was merged into `main`, the workflow records the merge account/time/commit, changes the labels to accepted working draft, rebuilds both documents, runs the checks and refreshes `MANIFEST_SHA256.txt`. It commits those generated updates as `github-actions[bot]`. It never creates a published release or changes `paper/v1.0/`. Failure stops the update and is visible in Actions. The setup and local transition tests are separate from an actual post-merge run, which remains pending until the PR is merged.

Local validation of the automation: eight merge/status tests and the five helper tests pass. Both the proposed state and an isolated accepted-state fixture rebuild to 45 manuscript pages and 31 supplement pages and pass the existing package checker and 61-file checksum verification. The first-page status labels were visually inspected in both states. The accepted-state fixture is test data only; it has not been uploaded as an accepted manuscript. The GitHub post-merge job remains unrun until an actual merge.

## Review record

- Reviewer: Claude (Anthropic), Claude Opus 5.5, at Jonathan Matkowsky's request. This is AI-assisted review, not independent human peer review.
- Commit reviewed: `4481a53`, compared with the baseline copy `52d599c`. The review is posted on the pull request.
- Findings: the statistical cross-checks above reproduce exactly (10.2253%, 44.0693%, 299, 628, 97.4101% and the 72% union bound). 628 is the smallest count with at least 93% power; below it the best power is 91.79%. The review requested the four edits marked "(review)" in the table above.
- Follow-up edits: drafted by Claude and applied at Jonathan's direction in one commit on this branch. Only the supplement source, its generated files and the attribution and status records changed. The manuscript source, CSV data, references and figure sources did not change, so the manuscript PDF and figure exports from `4481a53` were kept.
- Checks after the edits: rebuilt with Pandoc 3.1.3 and TeX Live 2023/Debian to 45 manuscript pages and 31 supplement pages. The package checker, the five helper tests, the eight merge/status tests and 61-file manifest verification pass. Supplement pages 17, 19 and 22, which carry the edits, and the Table S9.1 float pages were inspected.
- Open, not blocking this proposal: a contributor pull request that edits `paper/working/` fails the proposal check unless it names its own PR number in `REVISION_STATUS.json` and includes a full rebuild; after this proposal is accepted, later merges are not rebuilt unless their PR resets the status; `accept()` has no direct test.
