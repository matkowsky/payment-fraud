# Practitioner study

Protocol for Supplement S8, fixed before the first response. Any later change is a new commit that states its reason.

Changed before the first response, 12 November 2026: Part 3's added records now show stored fields without interpretation, because a referee noted that the earlier wording stated the answers. The questions and the answer key did not change.

## Question

Do the records C1 to C3 require change the conclusions practitioners draw, how often do the failures they target occur in practice, and what does the field record today?

## Design

- One anonymous online form, about 35 minutes: [INSTRUMENT.md](INSTRUMENT.md).
- Two hypothetical cases from manuscript Section 8, each shown first as many systems show it (Part 2), then with the C1 to C3 records added (Part 3). The same eleven questions are asked both times: eight test a requirement and three are controls.
- Then: how often each failure has changed a real conclusion (Part 4), whether each record exists today and how hard it would be to add (Part 5), availability of the eleven signals the cases use (Part 6), who owns each of the 24 responsibilities (Part 7, optional), and open questions (Part 8).

## Participants

- Six to ten people with at least two years investigating fraud or abuse, or building systems for it, at payment companies, banks, fintechs, marketplaces or vendors.
- Recruited through the author's LinkedIn post and direct invitations. People whose work the paper cites may take part.
- At least three organizations. The form does not ask for the employer. Participants who want credit email the author separately; those emails, never linked to answers, give the count of organizations.

## Consent and ethics

The study is not run through any institution and has no funding; the author knows of no local requirement for ethics-board review. ACM's policy on research involving human participants then requires authors to "be prepared to show compliance" with its principles. The study does so as follows:

- Adults only, with consent recorded on the form's first page.
- Minimal risk: professional judgment on hypothetical cases; no personal, employer or confidential information; any question may be skipped.
- The form records no name or email address. Results are reported in aggregate. Quotes need the participant's permission and carry no identifying detail.
- No published figure or quote may show which organization lacks a record or signal.
- Responses are deleted at journal publication or after two years, whichever comes first. The consent text and the response export with its date are kept as evidence.

## Scoring, fixed in advance

- The answer key was fixed before the first response and is kept private until the form closes, so participants cannot see it. SHA-256 of the key file: `3438ef22c7491a0adbe01b3702515b2b7699dc2b6675c405e70500f081b3f8f0`. It is published with the results.
- [score_responses.py](score_responses.py) scores the form's export. It refuses a key whose hash differs, excludes responses without consent or with under two years of experience, and copies no free text except answers whose author allowed quoting, for review before any use. Each question title and grid row in the form starts with its code from the instrument; Part 3 repeats use `A1-R` to `B6-R`, and Part 5's second grid uses `R1-H` to `R5-H`.
- Each item has one error the records are meant to prevent. For each item, report how many participants made that error in Part 2 and in Part 3, and how many moved from the error to a supported answer.
- Report items by requirement, controls separately, and participants who had read Section 8 or Supplement S6 separately.
- Report counts only. With six to ten people there is no significance test.
- Parts 4 to 7: counts per answer. Part 8: themes, with quotes only where permitted.
- Report negative results as prominently as positive ones: items where the records changed nothing, records the field already keeps, and records rated hard or not feasible.

## Limits stated in advance

- Within-person design: Part 3 follows Part 2, so a changed answer may reflect the reveal, not the record.
- The cases are hypothetical and come from the paper. Practitioners who read it may know the answers (P4 separates them).
- A small, self-selected sample. Results describe these participants, not the field.

## Independent human coders

Two further volunteers, who do not take the form, repeat checks that a model performed:

- The 52-link mechanism check: `../second_coder/PACKET.md`, about one to two hours, scored with `../second_coder/score.py`.
- The rulings on the 15 adversarial histories: `../adversarial_cases/round1/RULINGS_CHECK_PACKET.md`, about one hour.

Both are reported beside the model results, with agreement between them.

## Timeline

The form opens when this protocol is merged and closes two weeks later. Results go into a new subsection of manuscript Section 9 and into S8.

## Scoring correction, 12 November 2026

The reverse transition, **Supported to counted error (Part 2 → Part 3)**, counts only an earlier answer supported by the key (including an explicitly permitted Part 2 “Cannot tell”) followed by that item's counted error. Skipped, missing and unsupported earlier answers do not qualify. They remain in the answer distributions and any later counted error remains in the Part 3 total. The forward transition retains the Part 3 support definition.

This corrects the scorer introduced in PR #49, whose reverse predicate counted every earlier answer other than the designated error under a “Supported to error” label. The README originally specified counted errors and the forward transition, but did not separately define the reverse metric. This dated correction preserves that history; it is not represented as part of the originally frozen scorer. It was developed using synthetic responses and the public made-up test key only, without access to the private key or participant data. Actual collection/analysis timing was not verified in this correction; any affected results must identify their scorer version and disclose rescoring. The answer-key hash and instrument are unchanged.

Requirement-level `answers` counts eligible participant–item slots, including skips; it is not a count of nonblank answers or a transition-rate denominator. These outputs report counts only.

Drafting contribution: jointly Jonathan Matkowsky and ChatGPT/Codex, from Jonathan's direction; implementation and synthetic checks by ChatGPT/Codex. Independent AI review is recorded in the linked correction PR; it is not human peer review or empirical study validation.
