# Round 2 run record

Kept as the run goes. Nothing here is a result: no round 2 case has been run through the checker.

## Reply 1

- Date: 14 November 2026. The author pasted the reply to Claude at 22:48 Asia/Jerusalem (20:48Z).
- Packet: `tools/adversarial_cases/PACKET_ROUND2.md`, 21,682 bytes, blob `d468b43`, unchanged since commit `090ae41` (12 November). Every record the reply names exists in this packet's valid history.
- Model: GPT-6 Astra Pro, in ChatGPT. Stated by the author on 14 November, 23:36 Asia/Jerusalem, after the chat was closed. At 23:17 he had written "it was ChatGPT pro model like for other tests". The name was not written down while the chat was open, so the record rests on his statement, not on a note made at the time.
- Settings: a temporary chat with memory off, no project and no web. Stated by the author on 14 November, 23:37 Asia/Jerusalem, after the chat was closed.
- Reply: `reply_1.json`, saved as the author pasted it. 3,625 bytes, SHA-256 `1570180a0c45ad5dcd7992a061ed43bf0842f1e299f69eab66df664cf818c721`. Five cases: four the tester meant to break a requirement (R01 and R02 name C3, R03 and R04 name C2) and one the tester meant to be legitimate (A01).
- Not captured: the packet asks for the array in a code block, and for one sentence before it if the tester recognizes the project. The paste began at the array and ended with it. The temporary chat was closed and not retained, so the code fence and any such sentence cannot be recovered.
- The chat was closed after reply 1. Prompts 2 and 3 were not sent in it.

## Checked before any scoring

- No case has been run through the checker. Checked without running the rules: the file parses; it holds five cases; every record it names exists in the valid history; and the tier the tester gave each case equals the tier the runner assigns (R02 agent, the rest other).
- Frozen files at main `e80c613`, compared with the freeze `58150e8`: the checker, the valid history, the schema and the runner are identical (blobs `4fbc402`, `5d515fe`, `d22b2e4` and `bd0e653`).
- `tools/outcome_conformance.py` changed after the freeze (PR #73, rule OR-10). The runner takes only `apply_patch` from that file, and `apply_patch` is unchanged.

Recorded by Claude (Anthropic) on Jonathan Matkowsky's instruction of 14 November 2026.

## Reply 2

- Date: 14 November 2026. The author sent the reply to Claude as an attached file at 23:58 Asia/Jerusalem (21:58Z). The plan change for this reply (PR #76) was merged at 21:40:31Z, before Claude received the reply. The time the prompt was sent is not recorded.
- Prompt: `PROMPT_2.md`, 25,709 bytes, SHA-256 `c17533af5912a12c6cb47b5f930ce49efc2b3856fa85d0589654dd52bb510f9d`. It is the packet (21,682 bytes, unchanged), 402 added bytes, and `reply_1.json` (3,625 bytes, unchanged). The added bytes are a heading, three sentences, a code fence and the plan's request. See the second 14 November change in `PLAN.md`. The reply numbers its cases R05 to R08 and A02, which continues reply 1's numbering.
- Model and settings, as the author stated them before the run: GPT-6 Astra Pro, in a new temporary chat with memory off, no project and no web (14 November, 23:36 and 23:37 Asia/Jerusalem). Not yet confirmed after the run: the model name the chat showed, the settings, and that the prompt went in whole as one message.
- Reply: `reply_2.json`, saved byte for byte from the attached file. 7,726 bytes, SHA-256 `22e2da4441e39d5b3e1de073ab7fbb784ba98fea7ea4e3363c1c6e2a3e18a4b5`. Five cases: four the tester meant to break a requirement (R05 and R08 name C2, R06 and R07 name C3) and one the tester meant to be legitimate (A02).
- Not captured: the attached file began and ended with the array. Whether the reply held a code fence or a sentence outside it is not yet recorded.
- The chat was closed after reply 2 (author, 15 November, 00:18 Asia/Jerusalem). Prompt 3 was not sent in it.
- No case has been run through the checker. Checked without running the rules: the file parses; it holds five cases; no case identifier repeats one from reply 1; every existing record a case changes is in the valid history; the records the cases add (DR-3, DR-4, O-8 and Q-5) use new identifiers; and the tier the tester gave each case equals the tier the runner assigns (R05 agent, the rest other).

## Reply 3

- Date: 15 November 2026. The author sent the reply to Claude as an attached file at 00:34 Asia/Jerusalem (22:34Z on 14 November). The plan change for this reply (PR #79) was merged at 22:23:00Z, before Claude received the reply. The time the prompt was sent is not recorded.
- Prompt: `PROMPT_3.md`, 33,522 bytes, SHA-256 `24b0f8b5128c69b7de450b0c5fe18d2e665bf914a106697a15470ae8604ebac0`. It is the packet (21,682 bytes, unchanged), 489 added bytes, `reply_1.json` (3,625 bytes, unchanged) and `reply_2.json` (7,726 bytes, unchanged). See the 15 November change in `PLAN.md`. The reply numbers its cases R09 to R12 and A03, which continues the earlier numbering.
- Model and settings: asked about the model name and settings of this chat, the author wrote on 15 November at 00:37 Asia/Jerusalem: "For the record nothing has changed in that regard". That is: GPT-6 Astra Pro, in a temporary chat with memory off, no project and no web, as for replies 1 and 2. It is his statement after the run, not a note of what the chat showed.
- What went into the chat: at 00:38 the author sent Claude the text he had pasted ("This is what went into the chat"). It is byte-identical to `PROMPT_3.md`: 33,522 bytes, the same SHA-256.
- Reply: `reply_3.json`, saved byte for byte from the attached file. 7,421 bytes, SHA-256 `31226b0428f21ea29a18f2a8f3ea5b8dd9caa68458e3030986fba42047b9e484`. Five cases: four the tester meant to break a requirement (R09, R10 and R12 name C2, R11 names C3) and one the tester meant to be legitimate (A03).
- Not captured: the attached file began and ended with the array. Whether the reply held a code fence or a sentence outside it is not yet recorded.
- Checked without running the rules: the file parses; it holds five cases; no case identifier repeats an earlier one; every existing record a case changes is in the valid history; the records the cases add (Q-6, M-2 and O-9) use new identifiers; and the tier the tester gave each case equals the tier the runner assigns (R09 agent, the rest other).

## The fifteen cases

- `CASES.json`: the three replies joined in order and written as round 1's was (`json.dumps` with an indent of 1). 16063 bytes, SHA-256 `f5c5353758f1c066e698f5788a0d7a43a40da34c202519c2069e1b8a2610b8b5`. Its fifteen cases equal the three replies' cases, in order.
- Twelve cases are meant to break a requirement (R01 to R12: seven name C2, five name C3). Three are meant to be legitimate (A01 to A03).
- This file and `reply_3.json` were committed before the checker was run on any round 2 case.
- Frozen files at main `9ec1a3e`, compared with the freeze `58150e8`: the checker, the valid history, the schema and the runner are identical (blobs `4fbc402`, `5d515fe`, `d22b2e4` and `bd0e653`). `apply_patch` in `tools/outcome_conformance.py` is unchanged.

## Scoring

- The cases were committed and pushed first: commit `cb8e0d8`, pushed at 22:35:40Z on 14 November 2026.
- Command, run from `paper/working` at that commit: `python3 tools/adversarial_cases/run_cases.py --sealed tools/adversarial_cases/round2/CASES.json tools/adversarial_cases/round2/RESULTS.md`. The plan writes the paths relative to `tools/adversarial_cases`; the command is the same.
- Output: `RESULTS.md`, SHA-256 `fc15cd94c82590dc712e4c2141927f7c1e5a598ae5c1716ed08706d52bcc71bd`. The same command in a checkout of the freeze commit `58150e8`, with `CASES.json` copied in, gives a byte-identical file.
- What the checker did, before any ruling: of the twelve cases meant to break a requirement, two are rejected (R03 by the schema, R07 by IR-12) and ten pass (R01, R02, R04, R05, R06, R08, R09, R10, R11, R12). All three cases meant to be legitimate are rejected (A01 by IR-14, A02 by IR-08, A03 by IR-11).
- Thirteen cases therefore need a ruling against the paper's text. No ruling is recorded here. The author confirms every ruling.

## Rulings

- First rulings: `FIRST_RULINGS_CLAUDE.md`, SHA-256 `e1207ffa44b09deb030824f120ecf347f168c81ca64e52ff38c430b3d7d72bb1`. Written by Claude after the scoring and sent to the author shortly before 22:45Z on 14 November (he answered at 00:45 Asia/Jerusalem on 15 November). Claude wrote the rules, so these rulings are not independent. They are proposals. The author has confirmed none.
- Outside check, not yet run: `RULINGS_CHECK_PACKET.md`, 47,421 bytes, SHA-256 `046061ec6846207e2df7086cd6280c0be276aeddcbdbbcc1c6cfa33904efa534`, written by `build_check_packet.py`. It holds no ruling by anyone. Its passages are copied whole from the manuscript and supplement at the freeze commit `58150e8`. Its four further facts are reproduced by `diagnostics.py`.
- The first rulings and the packet are committed before the outside reply exists, so the two sets of rulings can be compared as they were first made.
- To be sent whole, as one message, in a new temporary chat with the same model and settings. To record when it runs: the date, the model name shown, the settings, and the whole reply, saved unchanged as `RULINGS_CHECK_REPLY.txt`.
- Model and settings of the check chat: the author wrote "Same model and settings" on 15 November at 00:53 Asia/Jerusalem (22:53Z on 14 November), after the packet was sent to him and before he had sent Claude any reply. That is: GPT-6 Astra Pro, in a temporary chat with memory off, no project and no web. It is his statement, not a note of what the chat showed.
