# Practitioner study

Protocol for Supplement S8, fixed before the first response. Any later change is a new commit that states its reason.

Changed before the first response, 12 November 2026: Part 3's added records now show stored fields without interpretation, because a referee noted that the earlier wording stated the answers. The questions and the answer key did not change.

Changed before the first response, 12 November 2026, at the author's direction: responses are kept for at most one year instead of two, and the eligibility, consent, Part 1 and case questions are now required, so that every participant answers each case question both before and after the records. Each case question still allows "Cannot tell". Parts 4 to 8 stay optional. The answer key did not change.

Changed before the first response, 13 November 2026: the report reads each requirement's counts beside the controls' counts, because an independent review noted that Part 3 always follows Part 2. The form, the questions and the answer key did not change.

Changed before the first response, 13 November 2026: the form opens when the recruitment post goes live, not at the merge, because the merge came two days before the form was ready. A single extension and the scoring of every eligible response are now fixed in advance. The form, the questions and the answer key did not change.

Changed before the first response, 13 November 2026, at the author's direction: the two volunteer human coders are dropped. They would only repeat checks a model already ran on the paper's own work, and they would draw on the same small pool of volunteers as the form. The paper states that agreement between human coders has not been measured. The form, the questions and the answer key did not change.

Changed before the first response, 14 November 2026, at the author's direction: no post carries the form link. A person asks for it, and the author checks that person's public profile against the criteria before sending it, because an open link lets anyone answer. The form, the questions and the answer key did not change.

Changed before the first response, 14 November 2026: the form opens on a fixed date, not when the post goes live. The posts went live on 14 November without the link, and the author opened the form the same day. The close date stays the one the posts state. The form, the questions and the answer key did not change.

Changed 14 November 2026, after the form opened; whether a response had arrived was not checked: the scoring script now refuses an export that lacks a required question's column, and it no longer reads a missing, blank or unlisted answer to E0, C0, P3 or P4 as an answer. It stops and names the row and the column, or with `--set-aside-invalid` scores the other rows and reports those set aside. Before, such a row could be counted as a participant who had not read Section 8, and E0 was not read at all. The live form requires these questions and offers fixed choices, so for every answer the form can produce the same responses are scored in the same groups; only the labels of the exclusion counts changed. Text typed under "other" in P1 or P2 is now counted as other and not copied, and quotes are taken from eligible rows only. From an independent review by ChatGPT. The form, the questions and the answer key did not change.

Changed 14 November 2026, after the form opened; whether a response had arrived was not checked: the report now states where each count of organizations comes from, because the same review noted that neither available count is the count among scored answers. The target of at least three organizations did not change. The form, the questions and the answer key did not change.

Changed 16 November 2026, after the form opened; whether a response had arrived was not checked: the protocol now says what happens if fewer than six eligible participants have answered when the extension ends, because it was silent on that. The study is reported either way. The form, the questions and the answer key did not change.

Changed 17 November 2026, after the form opened, at the author's direction; the author reports that no response had arrived: if no eligible response has arrived when the form closes on 30 November, the 14-day extension is not used, and the study is reported as having no responses. No response arrived in the first three days, and the author does not expect the extension to add one. In every other case the extension rule is unchanged. From this date the author sends no further invitations and no follow-up messages; a person who asks for the link is still sent it after the profile check. The form stays open until 30 November at 14:00 UTC, and every eligible response received by then is scored. The form, the questions and the answer key did not change.

Changed 18 November 2026, after the form opened; whether a response had arrived was not checked, and the private answer key was not read: the report no longer says that the controls show how often an answer changes on a second reading alone. Of the changes of answer between Part 2 and Part 3, the scoring script counts only a move between a supported answer and the item's counted error, in either direction. Because Part 3 always follows Part 2, reading each requirement's counts beside the controls' does not isolate the effect of the added records. Supplement S8 has said so since pull request #93, from the `codex/v1.1-e2-e8-e9-s8` branch, merged by the author on this date. The form, the questions, the answer key and the scoring script did not change.

Changed 19 November 2026, at the author's direction: the author closed the form early, between 20:28 and 20:33 UTC, with no responses. The form's linked workbook holds no response rows. The study is not reported in the paper, and Supplement S8 no longer describes it. This replaces the 16 and 17 November notes that the study is reported, the close on 30 November and the rule that there is no early stop. With no responses, the early close and the removal depend on no participant's answer. The form, the questions and the answer key did not change.

Changed 21 November 2026: Supplement S8 now says in one sentence that the cases, questions and key were written for this study, and that it opened on 14 November and closed on 19 November with no responses. This replaces "The study is not reported in the paper" in the 19 November note. Nothing else about the study is reported, and the form, the questions and the answer key did not change.

## Question

Do the records C1 to C3 require change the conclusions practitioners draw, how often do the failures they target occur in practice, and what does the field record today?

## Design

- One anonymous online form, about 35 minutes: [INSTRUMENT.md](INSTRUMENT.md).
- Two hypothetical cases from manuscript Section 8, each shown first as many systems show it (Part 2), then with the C1 to C3 records added (Part 3). The same eleven questions are asked both times: eight test a requirement and three are controls.
- Then: how often each failure has changed a real conclusion (Part 4), whether each record exists today and how hard it would be to add (Part 5), availability of the eleven signals the cases use (Part 6), who owns each of the 24 responsibilities (Part 7, optional), and open questions (Part 8).

## Participants

- Six to ten people with at least two years investigating fraud or abuse, or building systems for it, at payment companies, banks, fintechs, marketplaces or vendors.
- Recruited through the author's LinkedIn posts and direct invitations. People whose work the paper cites may take part.
- No post carries the form link. A person asks for it by a private message or by a like on the post, and the author checks that person's public profile against the criteria above before sending it. The post says that a like is public and a message is private.
- At least three organizations. The form does not ask for the employer, so the count among scored answers cannot be checked. Two counts are reported, each with its source: organizations among the people sent the link, from their public profiles, and organizations among participants who email the author separately for credit. Those emails are never linked to answers.

## Consent and ethics

The study is not run through any institution and has no funding; the author knows of no local requirement for ethics-board review. ACM's policy on research involving human participants then requires authors to "be prepared to show compliance" with its principles. The study does so as follows:

- Adults only, with consent recorded on the form's first page.
- Minimal risk: professional judgment on hypothetical cases; no personal, employer or confidential information; only the eligibility, consent, Part 1 and case questions are required, each case question allows "Cannot tell", and participants may stop at any time.
- The form records no name or email address. The author knows who received the link, not who answered. Results are reported in aggregate. Quotes need the participant's permission and carry no identifying detail.
- No published figure or quote may show which organization lacks a record or signal.
- Responses are deleted at journal publication or after one year, whichever comes first, with every export of them. The consent text, the date of each export and the scored counts are kept as evidence.

## Scoring, fixed in advance

- The answer key was fixed before the first response and is kept private until the form closes, so participants cannot see it. SHA-256 of the key file: `3438ef22c7491a0adbe01b3702515b2b7699dc2b6675c405e70500f081b3f8f0`. It is published with the results.
- [score_responses.py](score_responses.py) scores the form's export. It refuses a key whose hash differs and an export without a required question's column, stops at a row whose E0, C0, P3 or P4 is not one of the question's choices, excludes responses that answer No to E0 or C0 or report under two years of experience, and copies no free text except answers whose author allowed quoting, for review before any use. Each question title and grid row in the form starts with its code from the instrument; Part 3 repeats use `A1-R` to `B6-R`, and Part 5's second grid uses `R1-H` to `R5-H`.
- Each item has one error the records are meant to prevent. For each item, report how many participants made that error in Part 2 and in Part 3, and how many moved from the error to a supported answer.
- Report items by requirement, controls separately, and participants who had read Section 8 or Supplement S6 separately.
- Read each requirement's error counts and scored transitions beside the controls'. No added record bears on the three controls. A scored transition is a move between a supported answer and the item's counted error; other changes of answer are not counted. Part 3 always follows Part 2, so this comparison does not isolate the effect of the added records.
- Report counts only. With six to ten people there is no significance test.
- Parts 4 to 7: counts per answer. Part 8: themes, with quotes only where permitted.
- Report negative results as prominently as positive ones: items where the records changed nothing, records the field already keeps, and records rated hard or not feasible.

## Limits stated in advance

- Within-person design: Part 3 follows Part 2, so a changed answer may reflect the reveal, not the record.
- The cases are hypothetical and come from the paper. Practitioners who read it may know the answers (P4 separates them).
- A small, self-selected sample. Results describe these participants, not the field.
- Eligibility rests on a public profile and the participant's own confirmation. The form is anonymous, so the author cannot confirm who answered, that a link was not passed on, or that no one answered twice.
- Stated 14 November 2026: for the same reason, the number of organizations among the scored answers cannot be verified.

## Human coders

None. The mechanism-link check (S3) and the rulings on the adversarial histories (S4.4) are reported as model checks. Their packets stay in the package for anyone who wants to repeat them: `../second_coder/PACKET.md` and `../adversarial_cases/round1/RULINGS_CHECK_PACKET.md`.

## Timeline

The form opens on 14 November 2026 at 17:30 UTC and closes on 30 November at 14:00 UTC. If fewer than six eligible participants who have not read Section 8 or Supplement S6 have answered by then, it stays open once for 14 more days. From 17 November 2026: if no eligible response at all has arrived by then, it closes then, and the study is reported as having no responses. Every eligible response received before it closes is scored; there is no early stop. If fewer than six have answered when the extension ends, the study is still reported, with the shortfall stated as a limit. Results go into a new subsection of manuscript Section 9 and into S8.

Before opening, the author checked the scorer on one test response. It was deleted from the form and from the form's linked workbook, and it is not data.

## Scoring correction, 12 November 2026

The reverse transition, **Supported to counted error (Part 2 → Part 3)**, counts only an earlier answer supported by the key (including an explicitly permitted Part 2 “Cannot tell”) followed by that item's counted error. Skipped, missing and unsupported earlier answers do not qualify. They remain in the answer distributions and any later counted error remains in the Part 3 total. The forward transition retains the Part 3 support definition.

This corrects the scorer introduced in PR #49, whose reverse predicate counted every earlier answer other than the designated error under a “Supported to error” label. The README originally specified counted errors and the forward transition, but did not separately define the reverse metric. This dated correction preserves that history; it is not represented as part of the originally frozen scorer. It was developed using synthetic responses and the public made-up test key only, without access to the private key or participant data. Actual collection/analysis timing was not verified in this correction; any affected results must identify their scorer version and disclose rescoring. The answer-key hash and instrument are unchanged.

Requirement-level `answers` counts eligible participant–item slots, including skips; it is not a count of nonblank answers or a transition-rate denominator. These outputs report counts only.

Drafting contribution: jointly Jonathan Matkowsky and ChatGPT/Codex, from Jonathan's direction; implementation and synthetic checks by ChatGPT/Codex. Independent AI review is recorded in the linked correction PR; it is not human peer review or empirical study validation.
