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

Recorded by Claude (Anthropic), 22 November 2026.
