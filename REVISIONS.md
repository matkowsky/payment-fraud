# Revision status and contribution record

The [revision tracker](https://github.com/matkowsky/payment-fraud/issues/2) links public proposals, discussions and decisions. Each proposal identifies its baseline and exact commits.

| State | What it means | Where to verify |
|---|---|---|
| Proposed | Suggested text or edits committed on a proposal branch; not accepted merely because they have a commit. | Linked issue or open pull request, its source diff and candidate files. |
| Accepted | A maintainer explicitly accepts the changes and merges the pull request into main. | Recorded acceptance and merged pull request. |
| Published | Accepted work is included in a separately versioned release. | Release record, version tag and publication DOI. |
| Deferred or not adopted | A proposal is left for later or closed without adoption, with a reason. | Discussion and recorded disposition. |

Checks and reviews are separate evidence, not extra acceptance states. A successful build, an AI review or a human review does not itself accept or publish a change. Merging a proposal into main is the acceptance decision. The working-draft workflow then records the merge account, time and commit, updates the document status labels, rebuilds both documents and refreshes the checksum manifest. No manual relabeling is required. A failed automation run is visible in Actions; the merge record still establishes acceptance, while the files await synchronization. Preserve the prior proposed candidate in commit history. Published `paper/v1.0/` remains unchanged; review-only PR #1 is never merged.

## Who did what

GitHub may show Jonathan Matkowsky's account for actions carried out through an assistant. The account name alone does not explain the contribution. Each proposal, substantive review and acceptance record should state:

- Human contributor and account used.
- Assistant actually used: ChatGPT, Claude, another named assistant, or none.
- Contribution: joint drafting from the human contributor's notes and direction, editing, calculations, technical checks, or review, as applicable.
- Exact commit and files reviewed or checked, methods and limitations.
- Human acceptance decision, if made, with the accepted commit.

For this author's revisions drafted with AI from his notes and direction, use **“Jointly drafted by Jonathan Matkowsky and [named assistant], based on Jonathan's notes and direction.”** Record technical checks and reviews separately. This describes the drafting collaboration; it does not change the manuscript's author list or imply that Jonathan personally performed every check.

A later contribution may be jointly drafted with Claude. Name the assistant used for that contribution rather than copying an earlier assistant's attribution. Identify AI review as AI-assisted review; do not present it as independent human peer review. Do not claim that Claude or another reviewer has read a candidate until that review is recorded.

## Current proposal

| Proposal | Drafting contribution | Checks performed | State |
|---|---|---|---|
| [Statistical evaluation revisions](paper/working/PROPOSAL.md) | Jointly drafted by Jonathan Matkowsky and ChatGPT (OpenAI), based on Jonathan's notes and direction. | ChatGPT ran the build, package checks, numerical cross-checks and helper tests, and inspected rendered pages. | See [current status](paper/working/STATUS.md) and the linked PR merge record. Subsequent reviews must be recorded separately. |

The candidate is in [paper/working/](paper/working/). The proposal explains what changed and what remains outside its scope. Its pull request is linked in the tracker.

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

The workflow in `.github/workflows/working-draft.yml` validates the configured proposal against GitHub and the exact merge commit before accepting any labels. Pull-request checks have read-only repository access. Only the main-branch synchronization job can commit generated updates. It has no release step and never edits `paper/v1.0/`. If a run fails, fix the reported cause and rerun it from Actions; do not manually claim that regeneration succeeded. A new proposal should set `REVISION_STATUS.json` to `proposed` with its own PR number and run `python3 tools/revision_status.py sync` before rebuilding.
