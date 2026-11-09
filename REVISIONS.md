# Revision status and contribution record

The [revision tracker](https://github.com/matkowsky/payment-fraud/issues/2) links public proposals, discussions and decisions. Each proposal identifies its baseline and exact commits.

| State | What it means | Where to verify |
|---|---|---|
| Proposed | Suggested text or edits committed on a proposal branch; not accepted merely because they have a commit. | Linked issue or open pull request, its source diff and candidate files. |
| Accepted | A maintainer explicitly accepts the changes and merges the pull request into main. | Recorded acceptance and merged pull request. |
| Published | Accepted work is included in a separately versioned release. | Release record, version tag and publication DOI. |
| Deferred or not adopted | A proposal is left for later or closed without adoption, with a reason. | Discussion and recorded disposition. |

Checks and reviews are separate evidence, not extra acceptance states. A successful build, an AI review or a human review does not itself accept or publish a change. Merging a proposal into main is the acceptance decision. The working-draft workflow then finds the merged pull request from the merge commit, records its number, merge account, time and commit, updates the document status labels, rebuilds both documents and the [change record](paper/working/CHANGES_SINCE_v1.0.md), and refreshes the checksum manifest. No manual relabeling is required. A failed automation run is visible in Actions; the merge record still establishes acceptance, while the files await synchronization. Preserve the prior proposed candidate in commit history. Published `paper/v1.0/` remains unchanged; review-only PR #1 is never merged.

## Who did what

GitHub may show Jonathan Matkowsky's account for actions carried out through an assistant. The account name alone does not explain the contribution. Each proposal, substantive review and acceptance record should state:

- Human contributor and account used.
- Assistant actually used: ChatGPT, Claude, another named assistant, or none.
- Contribution: joint drafting from the human contributor's notes and direction, editing, calculations, technical checks, or review, as applicable.
- Exact commit and files reviewed or checked, methods and limitations.
- Human acceptance decision, if made, with the accepted commit.

For this author's revisions drafted with AI from his notes and direction, use **“Jointly drafted by Jonathan Matkowsky and [named assistant], based on Jonathan's notes and direction.”** Record technical checks and reviews separately. This describes the drafting collaboration; it does not change the manuscript's author list or imply that Jonathan personally performed every check.

A later contribution may be jointly drafted with Claude. Name the assistant used for that contribution rather than copying an earlier assistant's attribution. Identify AI review as AI-assisted review; do not present it as independent human peer review. Do not claim that Claude or another reviewer has read a candidate until that review is recorded.

## Proposals

| Proposal | Drafting contribution | Checks performed | State |
|---|---|---|---|
| [Statistical evaluation revisions](paper/working/PROPOSAL.md) | Jointly drafted by Jonathan Matkowsky and ChatGPT (OpenAI), based on Jonathan's notes and direction. Review edits drafted by Claude (Anthropic) and applied at Jonathan's direction. | ChatGPT ran the build, package checks, numerical cross-checks and helper tests, and inspected rendered pages. Claude reviewed commit `4481a53`, updated the merge automation, then rebuilt both documents, reran the checks and inspected the changed pages. | Accepted: [PR #3](https://github.com/matkowsky/payment-fraud/pull/3) merged 7 November 2026 (`071f29c`). See [current status](paper/working/STATUS.md). |
| [Source-reading corrections and working-draft records](https://github.com/matkowsky/payment-fraud/pull/4) | Source-reading verification by ChatGPT (OpenAI), 29 October 2026; corrections applied by Claude (Anthropic) at Jonathan Matkowsky's direction; README, record and date updates drafted by Claude. | Claude matched the three corrected tables byte for byte to the SHA-256 values recorded on 29 October, and ran the tests and source checks. | Accepted: [PR #4](https://github.com/matkowsky/payment-fraud/pull/4) merged 7 November 2026 (`a27e314`). See [current status](paper/working/STATUS.md). |
| [Outcome-record refinements from Decision Event Schema review](https://github.com/matkowsky/payment-fraud/pull/5) | Drafted by Claude (Anthropic) at Jonathan Matkowsky's direction, from Oleg Solozobov's emailed comments of 8 November 2026 (credited by name with his permission). | Claude re-checked the DES passages against arXiv 2604.09296v1, ran the tests and source checks, and inspected the rebuilt pages. | Accepted: [PR #5](https://github.com/matkowsky/payment-fraud/pull/5) merged 8 November 2026 (`d1a4547`). See [current status](paper/working/STATUS.md). |
| [Stale data-availability sentence](https://github.com/matkowsky/payment-fraud/pull/6) | Drafted by Claude (Anthropic) at Jonathan Matkowsky's direction. | Claude ran the source checks on `9dbfa00`. | Proposed: [PR #6](https://github.com/matkowsky/payment-fraud/pull/6). |
| [Verified report links in E3](https://github.com/matkowsky/payment-fraud/pull/8) | Drafted by Claude (Anthropic) at Jonathan Matkowsky's direction. | Claude ran the tests and source checks on `8e34b51`. | Proposed: [PR #8](https://github.com/matkowsky/payment-fraud/pull/8). |
| [SR-Fraud's history-dependent gains and E5's matched analysis](https://github.com/matkowsky/payment-fraud/pull/9) | Drafted by Claude (Anthropic) at Jonathan Matkowsky's direction, from Xuwei Tan's emailed comments of 8 November 2026 (credited by name with his permission). Acknowledgments shortened to one line at Jonathan's direction, adding Jiahong Dai after his reply of 9 November 2026; each person named approves the final wording before publication. | Claude ran the tests and source checks on `4ca7134`. | Proposed: [PR #9](https://github.com/matkowsky/payment-fraud/pull/9). |
| [Section 3's audit counts moved to the supplement; one S1 depth label](https://github.com/matkowsky/payment-fraud/pull/12) | Drafted by Claude (Anthropic) at Jonathan Matkowsky's direction, from the 29 October editorial review. | Claude ran the source checks and a full build on `bb2cb39`. | Proposed: [PR #12](https://github.com/matkowsky/payment-fraud/pull/12). |

The working draft is in [paper/working/](paper/working/). Each proposal's pull request explains what it changes and is linked in the tracker; [what changed since version 1.0](paper/working/CHANGES_SINCE_v1.0.md) shows the accepted result.

## Suggested contribution record

```text
Human contributor:
Account used:
Assistant (or none):
Drafting contribution:
Checks/review performed by:
Commit examined:
Evidence and limitations:
Acceptance decision (pending, or person/date/commit):
```

Private notes remain private until their author selects a concrete public proposal. Contributors can comment on the pull request, suggest source-line edits, or open a focused issue linked to the tracker.

## Automatic synchronization

The workflow in `.github/workflows/working-draft.yml` has two jobs.

- **On a pull request** that changes `paper/working/`, it runs the tests and checks the sources and data only. Contributors edit `paper/working/SOURCE/` or the data files and do not rebuild PDFs, the change record or the manifest. The job has read-only repository access.
- **After a merge into main**, it finds the merged pull request from the merge commit and verifies that the pull request was merged into main and produced exactly the checked-out commit. It records the merge in `REVISION_STATUS.json` and `STATUS.md`, rebuilds both documents and the change record, runs the full checks, refreshes the manifest and commits the result. A push to `paper/working/` that did not come from a merged pull request fails visibly instead of being recorded.

Drafting credit for each merge comes from a `drafting_credit` entry in the merged branch's `REVISION_STATUS.json`, else a `Drafting contribution:` line in the pull request description, else a pointer to the pull request. Only the main-branch job can commit. It has no release step and never edits `paper/v1.0/`. If a run fails, fix the reported cause and rerun it from Actions; do not manually claim that regeneration succeeded. If a second merge lands before the first is synchronized, the first run stops rather than overwrite newer work, and the second run rebuilds the documents; the first merge then remains recorded in its pull request.
