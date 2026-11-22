# Round 3 run record

Kept as the run went, in the order things happened. The results are in `RESULTS.md`.

## Freeze

- The plan and the packet were merged in pull request #122: merge commit `562745b`, 22 November 2026, 06:28:07Z. This is the freeze commit.
- At main `2847ee1`, the sync that followed, the eight frozen files have the blob hashes the plan lists, and `PACKET_ROUND3.md` has the size and SHA-256 the plan gives (52,199 bytes).
- The author was given the packet before the merge, as the file in that pull request at its head `148e627`. The packet and the frozen files are the same at that commit and at the freeze commit.

## Replies

- Received by Claude at 06:33Z on 22 November 2026, in one message from the author: two attached files and one block of pasted text.
- `reply_1.json`: the first attachment, saved byte for byte. 4,962 bytes, SHA-256 `2b7f019d64d91c37c38724dea44184662f54affd0ac569919e2853b1b899340d`. Five cases, R01 to R05.
- `reply_2.json`: the second attachment, saved byte for byte. 5,806 bytes, SHA-256 `41734b54efe9e0a2ec6a371962a6cbe0fea591426f028ef03e61f57ceafd7922`. Six cases, R06 to R11.
- `reply_3.json`: the pasted text, copied out of the message by Claude. 3,192 bytes, SHA-256 `64a98ef82f82e8acd524e26310c4992df56c5268121ec71eb99a657bad650557`. Five cases, R12 to R16. Its bytes are a copy of text shown in a chat message, so spacing and line ends may differ from what the tester wrote.
- Each reply is one JSON array inside a code fence, with nothing before or after it.
- The replies are ordered by their case identifiers, which run on from one reply to the next.

## Not recorded

- The model name shown and the session's settings. The plan asked for them before the first reply was read. Claude read the replies without them. They are asked of the author and are added below as his statement when given.
- Whether one session wrote all three replies, and the text of the two later prompts as sent.
- When the packet was sent, and whether it went in whole as one message.

## Checked before any scoring

- No case has been run through the checker. Checked without running the rules: each file parses; the three hold sixteen cases; no case identifier repeats; every existing record a case changes is in the joint history; and the records the cases add (Q-6, DR-4 and DR-5) use new identifiers.
- The plan asked for fifteen cases. The change to the plan for the sixteenth is in `PLAN.md`.
- Thirteen cases are meant to break a requirement: five name C1 (R01, R05, R09, R12, R16), four name C2 (R03, R06, R10, R14) and four name C3 (R04, R08, R11, R15). Three are meant to be legitimate (R02, R07, R13).
- The tier the tester gave differs from the tier the runner assigns in three cases. R01 and R05 change only a draft, which the runner counts as agent; the tester wrote other. R06 adds a query run, which the runner counts as other; the tester wrote agent.
- The packet asked each reply for at least one case that turns on the status and negative readings. One case changes `outcome_use`: R05, in the first reply.
- `CASES.json`: the three arrays joined in order and written as the earlier rounds' were (`json.dumps` with an indent of 1). 13,560 bytes, SHA-256 `85d7722e8338b710d937639f40a39ff44c5b4bff43a0a64fbc6ea6639bfd8531`.

## Scoring

- The replies, the joined cases and this record up to here were committed and pushed first: commit `8337b8a`, pushed at 06:35:21Z on 22 November 2026.
- Command, run from `paper/working` on a branch at main `2847ee1`: `python3 tools/adversarial_cases/run_cases.py --sealed --joint tools/adversarial_cases/round3/CASES.json tools/adversarial_cases/round3/RESULTS.md`.
- Output: `RESULTS.md`, SHA-256 `b06c0e8ac78ae7b8296ef1ed4b33a22a7b93e9bfdee136f9ffd5e53a112d8ca8`. The same command in a checkout of the freeze commit `562745b`, with `CASES.json` copied in, gives a byte-identical file.
- What the checker did with the thirteen cases meant to break a requirement, before any ruling:
  - Nine are rejected by the rules under test: R01 (XR-01), R03 (IR-05), R04 (IR-11), R06 (IR-05, IR-08, XR-01), R08 (schema), R09 (XR-01, and OR-12), R10 (IR-04), R11 (IR-09, IR-13) and R15 (schema).
  - Two are rejected only by the outcome rules, which are not under test: R12 (OR-04) and R16 (OR-10).
  - One passes: R05.
  - One stops the checker: R14. The runner prints it as malformed, but the patch applies and its records are well formed. The checker raises a KeyError in the code for XR-01 and reports nothing (`diagnostics.py`).
- What it did with the three meant to be legitimate: R07 passes. R02 (IR-09) and R13 (IR-08, XR-01) are rejected.
- R08 and R15 are rejected by the schema for reasons other than the one the tester gives. Each adds a draft with no claim and a version identifier the schema does not allow. R08 also sets a field a draft does not have (`agent_output`); R15 sets `agent_output_links`, which belongs to observations.
- Four cases need a ruling: R02, R05, R13 and R14.

## Rulings

- First rulings: `FIRST_RULINGS_CLAUDE.md`, SHA-256 `dd96936ffef4d2661d03f7867c4e9cc824ea90a221de659d83bae88f93a94571`. Written by Claude after the scoring. Claude wrote the rules, so they are proposals. The author has confirmed none.
- Outside check, not yet run: `RULINGS_CHECK_PACKET.md`, 56,361 bytes, SHA-256 `b7144671c471f8db5f2aefa8a0989556af75947369074396e23cc3b99d36da1d`, written by `build_check_packet.py`. It holds no ruling by anyone. It holds what the tester's packet held, the four cases and facts that `diagnostics.py` reproduces.
- Everything the tester wrote stands in that packet between marker lines and is called data. Claude read the sixteen reasons and every claim sentence the tester wrote. None addresses the reader, asks for anything or holds a code fence.
- The first rulings and the packet are committed and pushed before any outside reply exists.
- The reviewer is to be a model from a developer other than the tester's and other than Anthropic. To record when it runs: the date, the model name shown, the settings and the whole reply, saved unchanged as `RULINGS_CHECK_REPLY.txt`.

## Tester

- The author named the tester at 06:42Z on 22 November 2026, after the scoring and the first rulings. His words: "Llama 4 maverick".
- Llama 4 Maverick is an open-weight model that Meta released in April 2025. The author did not name the developer; Claude checked it. Meta is neither OpenAI nor Anthropic, so the plan's condition on the tester's developer is met.
- Still not recorded: the model version as shown, the session's settings (new session, memory, project, web access), whether one session wrote all three replies, and when the packet was sent.
- The reviewer for the rulings check must therefore be a model from a developer other than Meta and other than Anthropic.

Added 22 November 2026, 15:25Z:

- The author stated the settings on 22 November 2026, after the scoring and the first rulings. His words, with the time each was given:
  - 06:53Z: "Temp chats and running it now in astra pro model".
  - 06:56Z, asked whether web search was on in the tester's chat and in the reviewer's: "No web search".
  - 15:21Z, asked whether one chat wrote all three replies: "One llama chat did".
- As read: the tester ran in one temporary chat, which wrote all three replies, with web search off. "Temp chats" and "No web search" are read as covering the reviewer's chat as well. He did not say so in those words.
- Still not recorded: the model version as shown, the two later prompts as sent, when the packet was sent and whether it went in whole as one message.
- The reviewer he names, "astra pro", is read as GPT-6 Astra Pro, the OpenAI model named in the plan. OpenAI is neither Meta nor Anthropic, so the plan's condition on the reviewer's developer is met. Its reply had not been received when this was written.

## Rulings check, as received

Added 22 November 2026, 15:41Z:

- The reviewer's reply reached Claude at 15:39Z on 22 November 2026, as pasted text in a message from the author with no other words. It is saved as `RULINGS_CHECK_REPLY.txt`, copied out of the message by Claude: 1,355 bytes, SHA-256 `058e1a94dc02b5cd1cbb36ab8179d25b4d369d25f449434ac6ddbd1e8a1451df`. Its bytes are a copy of text shown in a chat message, so spacing and line ends may differ from what the reviewer wrote.
- The reply holds four lines in the answer format and nothing else. No line says that the reviewer recognized the project.
- The author did not name the model in that message. At 06:53Z he had said he was running the check "in astra pro model" (above), and the reply is read as that model's. The model version as shown is not recorded.
- GPT-6 Astra Pro comes from a developer other than the rule writer's and the tester's. It also wrote the histories of rounds 1 and 2 and checked their rulings (`PLAN.md`).
- The reviewer's rulings: R02 rules stand; R05 stated limit; R13 rules stand; R14 rules reject, naming IR-06. It gives severity none to each.
- Claude's first rulings are the same four. They were pushed at 06:38Z in commit `897a991`, and the packet the reviewer read holds no ruling.
- One label differs. Claude called the fault in the checker's code that R14 exposed minor. The reviewer's format gives a severity only to a new failure or a false rejection, and its reason calls the error a defect of the implementation, not a gap in the stated rules.
- No case is unresolved between the two sets. The author has not yet confirmed the rulings.

Recorded by Claude (Anthropic), 22 November 2026.
