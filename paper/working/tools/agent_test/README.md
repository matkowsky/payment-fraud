# Agent test of the practitioner study's cases

Protocol, fixed before any model is run. Any later change is a new commit that states its reason.

Changed 19 November 2026, before any run: the author runs the script through a GitHub Actions workflow in a private repository of his, so that a run can be started from a phone. The workflow checks out this repository at a stated commit and runs `agent_test.py` unchanged. The API keys are that repository's secrets. The raw replies and the results are kept in that private repository, not in OneDrive, until the practitioner study's form closes. Claude wrote the workflow file. Each run is started by the author, or by Claude at his direction. The models, prompts, session counts, seed, scoring and cost cap did not change.

## Question

When AI models answer the two cases of the practitioner study, do they give the counted error without the records, and does adding the records remove it? Filler records, matched in number and form but bearing on no question, separate the effect of the records' content from the effect of more text.

This is a separate study from the practitioner study, which closed with no responses and is not in the paper (`../practitioner_study/README.md`).

## Material

- The case text, questions and choices of Part 2 of `../practitioner_study/INSTRUMENT.md`, and the records of its Part 3, read verbatim from the file by `agent_test.py`.
- Part 3's lead-in reads "These records are now also available. Answer the same questions again". Each session here reads the cases once, so the lead-in is "These records are also available." The sentence "Each record is shown as the system stores it." is kept.
- `FILLER.md`: filler records for each case, the same number as the records (four for Case A, five for Case B), in the same form. They were written without reading the answer key.
- `PILOT_CASE.md`: a throwaway case for the pilot. It is never used in the main run. Its key is a separate file, kept private with the study's key; `PILOT_CASE.md` records its SHA-256.
- The instructions around the cases are fixed in `agent_test.py` (`HEAD` and `TAIL`). Each model must end its reply with one line: `RESULT <run id> | A1: <answer> | ... | B6: <answer>`.

## Conditions

Three, assigned between sessions:

1. Case only: Part 2 as written.
2. With records: each case followed by its Part 3 records.
3. With filler: each case followed by its filler records.

Each session shows both cases, Case A first, in one condition. A session is a new conversation with no earlier turns, no tools, no web access and no memory.

## Models

Two vendors, three sizes each, through their APIs, run by the author's script with his keys:

- OpenAI: `gpt-6.1-sol`, `gpt-6.1-terra`, `gpt-6-luna`. `store` off.
- Anthropic: `claude-opus-5-5`, `claude-sonnet-5-5`, `claude-haiku-5-5`.

Added 19 November 2026, at the author's direction, after the main results of these six models were read: `gpt-6.2-astra` and `claude-fable-5-2`, each vendor's most capable API model that day. The list above had left out OpenAI's most capable model (then GPT-6 Astra) to save cost, and had missed Claude Fable 5.2, released on 9 November. GPT-6.2 Astra was released on 17 November. The two run the main phase only, with the same prompts, conditions and 30 sessions per condition; their rows are appended to `RUN_SHEET.csv` and no earlier row changed. They are reported apart from the six, and the report compares all eight model by model, with nothing pooled. The author allows spending past the earlier budget, so the cap is raised to 40 dollars per vendor, above the worst case for the two added models.

Default settings for each; no tools; at most 6,000 output tokens per reply. Each request carries only its prompt. The model name the API returns is recorded with each reply. Reasoning or thinking settings stay at each vendor's default, which may differ between vendors. The prompt lets every model reason in its reply.

Both vendors' tools were used in the research (manuscript Section 3). Claude drafted the cases and the filler records; ChatGPT reviewed the paper and the study. So no model here is a fully independent subject. Each model is reported apart, and the paper states which vendor's tools did what.

Each model's stated training cutoff is recorded. A model whose cutoff falls after 11 November 2026, when `INSTRUMENT.md` became public, is reported as possibly exposed to the cases.

Recorded 19 November 2026, from each vendor's model page: OpenAI lists a knowledge cutoff of 30 April 2026 for `gpt-6.1-sol`, 1 June 2026 for `gpt-6.1-terra`, and 18 May 2026 for `gpt-6-luna` and `gpt-6.2-astra`. Anthropic lists a training data cutoff of June 2026 for `claude-opus-5-5`, `claude-sonnet-5-5`, `claude-haiku-5-5` and `claude-fable-5-2`. Every cutoff falls before 11 November 2026, so no model is reported as possibly exposed to the cases.

## Sessions, fixed now

| Phase | Each of the six models |
|---|---|
| Pilot (case P) | 10 per condition, 30 in all |
| Main (Cases A and B) | 30 per condition, 90 in all |

`RUN_SHEET.csv` lists every session: run id, phase, model, condition, order and the SHA-256 of its prompt. The order is random from seed 20261117, with conditions mixed, so that a change in a model over the hours of a run does not line up with one condition.

A request that fails before the model replies is sent again. A reply that the API's own safety system stops (Anthropic stop reason `refusal`; OpenAI status `incomplete` with reason `content_filter`) is not sent again and counts as no answer, even if its text holds a valid `RESULT` line (see "Pilot"). Any other reply without a valid `RESULT` line is not rerun: it is recorded and reported as no answer.

## Pilot

The pilot checks that replies parse, what the run costs and whether the models give the counted error at all.

One branch is fixed in advance. Pooling all models, if the counted error appears in at most 20 percent of the case-only answers to the pilot's two requirement items (P1, P2), the main run asks for free-text conclusions scored by a rubric committed before the main run. Otherwise the main run goes as fixed here. Nothing else in the main run changes because of the pilot.

Pilot run, 19 November 2026, 14:20 to 14:31 UTC, through the workflow, at this repository's commit `d4816db`: 180 of 180 sessions sent and saved; one session ended without a result line and counts as no answer. In that session the model did not decline the task: the API's own safety classifier stopped the reply after 464 output tokens (stop reason `refusal`, category `reasoning_extraction`, which the API explains as suspected breach of its "restrictions on reverse engineering or duplicating model outputs"). That session is not resent; whatever it had answered, the branch decision would be the same. Changed 19 November 2026, before the main run, at the author's direction: in the main run, a reply that the API's own safety system stops is sent again once, to the same model, never to another model. The stop is the API's, not the model's answer, and the protocol already sends again a request that fails before the model replies. Both replies are kept, and their cost counts toward the cap. If the second reply is stopped too, the session counts as no answer. Stops are reported by model, apart from replies that lack a result line for other reasons, and each count that a twice-stopped session affects is also shown with that session counted first as an error and then as not. Changed again on 19 November 2026, at the author's direction, after a review of PR #98 and before any main-run result was read: a stopped reply is a terminal no answer. It is not sent again, and its text is not scored even if it holds a valid result line, because either would change which replies count as answers, and stops need not fall evenly across providers or conditions. The main run had been sent under the earlier rule. Each record it resent keeps the first, stopped reply, and that reply is the one scored; the resent reply is kept and reported, not scored. Stops are reported by model, apart from other replies without a result line, and each count a stopped session affects is also shown with the stopped sessions counted first as errors and then as not. A first Anthropic attempt stopped before sending anything, because the stored key ended with a line break; the workflow now removes spaces and line breaks from the keys. The counted error appeared in more than 20 percent of the case-only answers to P1 and P2, so the main run goes as fixed. SHA-256 of the pilot's `results.json`: `85e001e2f892a9b7df8f7085f345b36c875f3e8937ba14b46fa7f81ab341c477`. Cost: about 0.09 dollars with OpenAI and 0.60 dollars with Anthropic. The replies and results stay private until the form closes.

## Outcome and report

- The main run is scored against the practitioner study's answer key. `agent_test.py` refuses a key whose SHA-256 differs from the one recorded in `../practitioner_study/README.md`. The pilot is scored against the pilot key, checked the same way against the hash in `PILOT_CASE.md`.
- A counted error is the key's error for that item. A supported answer is the key's supported answer; in the case-only and filler conditions, "Cannot tell" is also supported for the items the key lists. This is the rule `score_responses.py` applies to Part 2 and Part 3.
- For each model, condition and item: counted errors, supported answers and no answers, each out of the sessions run, with an exact (Clopper-Pearson) 95 percent interval over sessions.
- For each model and requirement, the totals of those counts. They carry no interval, because one session answers several items of a requirement. Controls are reported separately.
- No pooling across models. Every model is reported, whatever its result.

## Kept private until the form closes

Both keys, and the replies, parsed answers and results of both phases, stay out of this repository, and are not shared, until the practitioner study's form closes. They would show which answers a key counts as errors, and case P is built like the form's cases. They are kept privately, as the 19 November change says, and committed here after the close.

Committed 19 November 2026, after the form closed early with no responses (`../practitioner_study/README.md`): `PILOT_KEY.md`, `../practitioner_study/ANSWER_KEY.md`, every reply in `runs/pilot` (180) and `runs/main` (720), and `results/pilot` and `results/main`, unchanged from the private repository. Both keys match the hashes recorded above. The six models' main replies were sent on 19 November from 17:07 to 18:02 UTC; the two added models' from 19:06 to 20:06 UTC. The main results were scored at commit `cae2d6e`, after both sends, and rescoring the committed replies with that script gives identical files. SHA-256 of the main `results.json`: `88cab8a24fc7a9eb16db3e5f7ad9e95a7e7182a983819412cd526b22f59d9b81`. The pilot results were scored at commit `d4816db`. Rescoring them with the current script gives the same counts; it labels PN-025 as stopped by the API, where the earlier script reported no result line. Charges over both phases, from the token counts each API reported: 2.89 dollars with OpenAI and 19.70 dollars with Anthropic.

## Cost

The script stops before a request that could take the estimated charge with one vendor past 40 dollars (15 dollars until the 19 November addition). The estimate uses the token counts each API reports and the prices in `agent_test.py`, read from the vendors' pricing pages on 16 and 17 November 2026. Reasoning tokens are counted as output.

If the pilot's cost per session shows that the main run would pass a vendor's cap, the author raises that cap or drops that vendor's largest model, in a dated commit before the main run.

## Limits stated in advance

- Short written cases with forced choices, not agents working on live systems.
- "Cannot tell" is offered, which may make models more cautious than they would be when writing conclusions.
- Two vendors' models. Results may not hold for other vendors' models.
- Both vendors' tools were used to write the paper and the study (see Models).
- Repeated sessions are samples from one model at fixed settings, not independent subjects. Intervals describe that sampling only.
- Models change. Results hold for the versions and dates recorded.
- The author wrote the cases and the filler records, with Claude's help.

## Order of work

1. This protocol, `FILLER.md`, `PILOT_CASE.md`, `agent_test.py` and `RUN_SHEET.csv` are merged.
2. The author runs the pilot with the script, once for each vendor, through the workflow described in the 19 November change.
3. The branch decision and the SHA-256 of the pilot's `results.json` are committed.
4. The author runs the main run.
5. After the form closes: both keys and the replies and results of both phases are committed, and one pull request proposes the text.

## Files

- `agent_test.py`: builds the prompts and run sheet, runs the sessions, parses replies and scores them. Python standard library only.
- `RUN_SHEET.csv`: every session, fixed before any run.
- `FILLER.md`, `PILOT_CASE.md`: material described above.
- `test_agent_test.py`: tests.
