# Second-coder check of the mechanism-to-signal links

Purpose: test whether a rater who has not seen the paper's links reaches the same links from a written rule.

What it is not: a human coder, or a check that the sources say what the paper says. The rater sees the recorded scope of each source, not the source.

## Files

- `build_packet.py` builds `PACKET.md` and `KEY.json`. The packet holds the rule, the 68 mechanism-specific signals and a seeded random sample: 20 of the 61 mapped mechanisms and 5 of the 13 judged covered by existing records. It holds none of the paper's links. Mechanism IDs are masked as M01 to M25.
- `score.py ANSWERS.txt [KEY.json]` compares the rater's lines with the paper's links: Cohen's kappa over every mechanism-signal cell, the share of links each side made that the other also made, and every disagreement.
- `dry_run/` holds two dry-run answer files from Claude subagents. They tested the packet. They are not the independent check: Claude proposed the paper's mappings, and both subagents reported that they recognized the project.

## The rule was written after the mappings

The paper did not state a linking rule. Claude wrote the rule in `PACKET.md` on 10 November 2026 for this check. The first dry run (seed 20261110) showed three unclear points: sources from other settings, raw observations versus derived features, and whether control outcomes can be linked. The rule was clarified from the paper's definitions and from counts over all 163 links (for example, 46 of 54 links to a derived feature have one of its inputs linked for the same mechanism). A fresh sample (seed 20261111) was then drawn for the real run; 7 of its 25 mechanisms were also in the dry-run sample.

## Dry-run results (seed 20261110, 20 mapped mechanisms, 1,360 cells)

| Rule version | Kappa | Paper's links the rater made | Rater's links in the paper | "Missing record" answers (of 25) |
|---|---|---|---|---|
| First | 0.60 | 53 of 62 | 53 of 109 | 16 |
| Clarified | 0.62 | 54 of 62 | 54 of 107 | 2 |

## The real run

1. Open a temporary chat with memory off, outside any project, with no connectors or web access.
2. Paste the whole of `PACKET.md`.
3. Save the reply as `ANSWERS.txt`, with the model name and version shown and the date.
4. Run `python3 tools/second_coder/score.py ANSWERS.txt`.
