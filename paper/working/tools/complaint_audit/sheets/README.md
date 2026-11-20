# Coder sheets

Each sheet is committed exactly as its coder returned it. Neither coder saw the other's sheet before both were fixed.

| Sheet | Coder | Fixed | SHA-256 |
|---|---|---|---|
| `CLAUDE_SHEET.json` | Claude (Anthropic), Claude Opus 5.5 | 17 Nov 2026; hash recorded before coder 2's sheet arrived | `9f2934232e861a21f9b7b24cbb6d75b3a91e23a179c29c98bf16e5557d6903b4` |
| `CHATGPT_SHEET.json` | ChatGPT (OpenAI), GPT-6 Astra Pro | 17 Nov 2026, 16:07 UTC | `6dfda9b1ad54ae8edb830dac8608c4eafa44be3fd5409829b4844af75d74b70f` |

Coder 2 worked in a new session with only the packets zip (14 packets and `UNITS.csv`) and returned the sheet in three parts:

1. U01 only (SHA-256 `121608f5a7f0b8c9a3bb9d6bc862f6348e7d503e2fd775f133020e45f6736fa6`).
2. U01 to U04 (SHA-256 `940da64c898df2f9bee8eb41e4434d20b33eae80c466b7714902f92351dd037e`). `check_sheet.py` found one form error: U03 X4 `tied_to_T1_or_T2` was `no` where the instructions require `n/a`. It was returned to the coder to fix that field only.
3. U01 to U14, committed here. Against part 2, only U03 X4 changed.

`CLAUDE_NOTES.md` is coder 1's working notes on close calls, written while coding. Both sheets pass `check_sheet.py`.
