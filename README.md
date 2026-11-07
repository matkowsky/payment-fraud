# Evidence requirements for agent investigations across payment products

Open review space for the preprint **Threat Analytics Across Payment Products: Evidence Requirements for Agent Investigations** by Jonathan Matkowsky. Version 1.0, 29 October 2026. Not peer reviewed.

- Preprint, all versions: https://doi.org/10.5281/zenodo.23772005
- Version 1.0: https://doi.org/10.5281/zenodo.23772006
- Author ORCID: https://orcid.org/0009-0000-0708-5711

## What the paper says

When an AI agent investigates abuse across a payment platform's products, three kinds of record decide whether its conclusions can be trusted:

1. **Outcomes linked to the decisions that shaped them.** A blocked payment cannot produce a chargeback, so "no chargeback" can mean prevented, not yet reported, or never reported.
2. **What each search actually covered, and when the system learned each fact.** An incomplete search cannot establish absence.
3. **Human release before a conclusion is reused, with every record it informed linked back to it.** A reused conclusion cannot corroborate itself.

The paper is a synthesis and specification built from public sources: 71 signals, 24 responsibilities, two hypothetical investigations and an evaluation plan. It has not been built or evaluated, and no practitioner has reviewed it yet. That is what this repository is for.

## How to comment

You need a free GitHub account for the first three routes.

1. **Open an issue** and pick a form ([New issue](https://github.com/matkowsky/payment-Fraud/issues/new/choose)):
   - **Review comment**: anything about a passage, a section or the whole paper.
   - **Practitioner questions**: five short questions about how your team works. A two-line answer helps.
   - **Prior work I should cite**: a paper, standard, product or patent the paper misses or describes wrongly.
   - **Error report**: a factual, citation or arithmetic error.
2. **Comment line by line** on the manuscript in the [line-by-line review](https://github.com/matkowsky/payment-Fraud/pull/1). Open "Files changed", hover over a paragraph and click the plus sign. Each paragraph is one line.
3. **Start a conversation** in [Discussions](https://github.com/matkowsky/payment-Fraud/discussions) for open questions that are not about one passage.
4. **No GitHub account?** Comment on the LinkedIn post or email Jonathan@matkowsky.com.

Please refer to version 1.0 section numbers, and quote the sentence you mean when you can. Share only public or general information. Do not share confidential information from an employer or client, or personal data about anyone.

## What happens to comments

- Every comment gets a reply.
- When the author decides to propose a change, it follows the same public review routes offered to contributors. Submitted proposals are linked in the [version 1.1 revision tracker](https://github.com/matkowsky/payment-fraud/issues/2), with their evidence, discussion and disposition; actual manuscript edits use linked pull requests. Personal working notes remain private until selected for submission.
- Accepted changes go into version 1.1. The feedback window is planned to run until about 30 November 2026, with version 1.1 to follow on Zenodo and here.
- Contributors whose input changes the paper are credited in version 1.1, in the acknowledgments or, for substantial contributions, as co-authors, always with their permission. The terms are in [CONTRIBUTING.md](CONTRIBUTING.md).

## Proposed revisions and attribution

The [revision record](REVISIONS.md) explains proposed, accepted and published states and identifies human and AI contributions. The [working manuscript](paper/working/) has a [status record](paper/working/STATUS.md) that is synchronized automatically after merge. The changes proposed in PR #3 were jointly drafted by Jonathan Matkowsky and ChatGPT, based on Jonathan's notes and direction; review edits to them were drafted by Claude; checks are attributed separately. The version 1.0 text they revise carries its own declaration of AI use. Later contributions name the assistant actually used, and [STATUS.md](paper/working/STATUS.md) lists the drafting credit for each accepted change.

## What is in this repository

- [`paper/v1.0/`](paper/v1.0/): the contents of `PACKAGE_v1.0_2026-10-29.zip` as published on Zenodo, unchanged. `MANIFEST_SHA256_2026-10-29.txt` lists the SHA-256 hash of the other 54 files.
  - Start with the [manuscript](paper/v1.0/MANUSCRIPT_v1.0_2026-10-29.md) ([PDF](paper/v1.0/MANUSCRIPT_v1.0_2026-10-29.pdf)) and the [supplement](paper/v1.0/SUPPLEMENT.md) ([PDF](paper/v1.0/SUPPLEMENT.pdf)).
  - The supplement's 19 data files are in [`paper/v1.0/SUPPLEMENT/`](paper/v1.0/SUPPLEMENT/). [REPRODUCE.md](paper/v1.0/REPRODUCE.md) explains how to rebuild the documents and run the checks.
- [`paper/working/`](paper/working/): the version 1.1 working draft. Read the current [manuscript](paper/working/MANUSCRIPT.md) ([PDF](paper/working/MANUSCRIPT.pdf)) and [supplement](paper/working/SUPPLEMENT.md) ([PDF](paper/working/SUPPLEMENT.pdf)), and [what changed since version 1.0](paper/working/CHANGES_SINCE_v1.0.md), paragraph by paragraph. [STATUS.md](paper/working/STATUS.md) lists the accepted merges. Both documents and the change record are rebuilt automatically after each merge.
- [Version 1.1 revision tracker](https://github.com/matkowsky/payment-fraud/issues/2): submitted change proposals and their review status. Working notes and review recommendations are not automatically submitted proposals. The released version 1.0 package stays unchanged.

## How to cite

Matkowsky, J. (2026). *Threat Analytics Across Payment Products: Evidence Requirements for Agent Investigations* (Version 1.0) [Preprint]. Zenodo. https://doi.org/10.5281/zenodo.23772005

GitHub's "Cite this repository" button uses [CITATION.cff](CITATION.cff).

## License

- The author's text, figures and supplement tables: Creative Commons Attribution 4.0 International (CC BY 4.0), the same license as the Zenodo record. Full text in [LICENSE](LICENSE).
- Build and check scripts (the .py files): MIT License, see [LICENSE-SCRIPTS](LICENSE-SCRIPTS).
- The Stripe schema-derived components of two supplement tables: MIT License, as [THIRD_PARTY_NOTICES.md](paper/v1.0/THIRD_PARTY_NOTICES.md) states.
- Contributions: CC BY 4.0, as [CONTRIBUTING.md](CONTRIBUTING.md) states.
