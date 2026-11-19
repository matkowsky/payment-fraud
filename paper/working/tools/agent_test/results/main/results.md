# Agent test results, main

Counted errors by model: case only / with records / with filler, each of the sessions run.

| Item | Requirement | gpt-6.1-sol | gpt-6.1-terra | gpt-6-luna | claude-opus-5-5 | claude-sonnet-5-5 | claude-haiku-5-5 | gpt-6.2-astra | claude-fable-5-2 |
|---|---|---|---|---|---|---|---|---|---|
| A1 | C2 coverage | 0/0/0 | 0/0/0 | 0/0/0 | 0/0/0 | 16/1/13 | 2/0/0 | 0/0/0 | 13/0/0 |
| A2 | C2 learned time | 0/10/0 | 0/2/0 | 0/27/0 | 0/1/0 | 1/1/0 | 16/3/3 | 0/0/0 | 25/21/0 |
| A3 | Control | 0/0/0 | 0/0/0 | 0/0/0 | 0/0/0 | 0/0/0 | 0/0/0 | 0/0/0 | 0/0/0 |
| A4 | C1 channel state | 8/0/0 | 30/0/5 | 3/0/5 | 5/0/0 | 0/0/0 | 0/0/0 | 0/0/0 | 25/0/0 |
| A5 | Control | 0/0/0 | 0/0/0 | 0/0/0 | 0/0/0 | 0/0/0 | 0/0/0 | 0/0/0 | 0/0/0 |
| B1 | C1 attribution | 30/0/30 | 30/0/30 | 29/0/30 | 30/0/24 | 30/0/30 | 29/0/30 | 30/0/30 | 25/0/5 |
| B2 | C1 per-account outcome | 0/0/0 | 0/0/0 | 0/0/0 | 0/0/0 | 0/0/0 | 0/0/0 | 0/0/0 | 0/0/0 |
| B3 | C2 coverage | 0/0/0 | 0/0/2 | 29/0/28 | 8/0/0 | 0/0/0 | 0/0/0 | 0/0/0 | 25/0/0 |
| B4 | C3 exposure links | 0/0/0 | 0/0/0 | 0/0/0 | 0/0/0 | 0/0/0 | 0/0/0 | 0/0/0 | 2/0/0 |
| B5 | C1 decision link | 0/0/0 | 0/0/0 | 0/0/0 | 0/0/0 | 0/0/0 | 0/0/0 | 0/0/0 | 0/0/0 |
| B6 | Control | 0/0/0 | 0/0/0 | 0/0/0 | 0/0/0 | 0/0/0 | 0/0/0 | 0/0/0 | 0/0/0 |

## gpt-6.1-sol

Sessions run: 90 of 90. Model shown: gpt-6.1-sol (90).

| Item | Requirement | Errors, case only (95% CI) | Errors, with records (95% CI) | Errors, with filler (95% CI) |
|---|---|---|---|---|
| A1 | C2 coverage | 0 of 30 (0.00 to 0.12) | 0 of 30 (0.00 to 0.12) | 0 of 30 (0.00 to 0.12) |
| A2 | C2 learned time | 0 of 30 (0.00 to 0.12) | 10 of 30 (0.17 to 0.53) | 0 of 30 (0.00 to 0.12) |
| A3 | Control | 0 of 30 (0.00 to 0.12) | 0 of 30 (0.00 to 0.12) | 0 of 30 (0.00 to 0.12) |
| A4 | C1 channel state | 8 of 30 (0.12 to 0.46) | 0 of 30 (0.00 to 0.12) | 0 of 30 (0.00 to 0.12) |
| A5 | Control | 0 of 30 (0.00 to 0.12) | 0 of 30 (0.00 to 0.12) | 0 of 30 (0.00 to 0.12) |
| B1 | C1 attribution | 30 of 30 (0.88 to 1.00) | 0 of 30 (0.00 to 0.12) | 30 of 30 (0.88 to 1.00) |
| B2 | C1 per-account outcome | 0 of 30 (0.00 to 0.12) | 0 of 30 (0.00 to 0.12) | 0 of 30 (0.00 to 0.12) |
| B3 | C2 coverage | 0 of 30 (0.00 to 0.12) | 0 of 30 (0.00 to 0.12) | 0 of 30 (0.00 to 0.12) |
| B4 | C3 exposure links | 0 of 30 (0.00 to 0.12) | 0 of 30 (0.00 to 0.12) | 0 of 30 (0.00 to 0.12) |
| B5 | C1 decision link | 0 of 30 (0.00 to 0.12) | 0 of 30 (0.00 to 0.12) | 0 of 30 (0.00 to 0.12) |
| B6 | Control | 0 of 30 (0.00 to 0.12) | 0 of 30 (0.00 to 0.12) | 0 of 30 (0.00 to 0.12) |

| Requirement | Errors, case only | Errors, with records | Errors, with filler |
|---|---|---|---|
| C1 | 38 of 120 | 0 of 120 | 30 of 120 |
| C2 | 0 of 90 | 10 of 90 | 0 of 90 |
| C3 | 0 of 30 | 0 of 30 | 0 of 30 |
| Control | 0 of 90 | 0 of 90 | 0 of 90 |

## gpt-6.1-terra

Sessions run: 90 of 90. Model shown: gpt-6.1-terra (90).

| Item | Requirement | Errors, case only (95% CI) | Errors, with records (95% CI) | Errors, with filler (95% CI) |
|---|---|---|---|---|
| A1 | C2 coverage | 0 of 30 (0.00 to 0.12) | 0 of 30 (0.00 to 0.12) | 0 of 30 (0.00 to 0.12) |
| A2 | C2 learned time | 0 of 30 (0.00 to 0.12) | 2 of 30 (0.01 to 0.22) | 0 of 30 (0.00 to 0.12) |
| A3 | Control | 0 of 30 (0.00 to 0.12) | 0 of 30 (0.00 to 0.12) | 0 of 30 (0.00 to 0.12) |
| A4 | C1 channel state | 30 of 30 (0.88 to 1.00) | 0 of 30 (0.00 to 0.12) | 5 of 30 (0.06 to 0.35) |
| A5 | Control | 0 of 30 (0.00 to 0.12) | 0 of 30 (0.00 to 0.12) | 0 of 30 (0.00 to 0.12) |
| B1 | C1 attribution | 30 of 30 (0.88 to 1.00) | 0 of 30 (0.00 to 0.12) | 30 of 30 (0.88 to 1.00) |
| B2 | C1 per-account outcome | 0 of 30 (0.00 to 0.12) | 0 of 30 (0.00 to 0.12) | 0 of 30 (0.00 to 0.12) |
| B3 | C2 coverage | 0 of 30 (0.00 to 0.12) | 0 of 30 (0.00 to 0.12) | 2 of 30 (0.01 to 0.22) |
| B4 | C3 exposure links | 0 of 30 (0.00 to 0.12) | 0 of 30 (0.00 to 0.12) | 0 of 30 (0.00 to 0.12) |
| B5 | C1 decision link | 0 of 30 (0.00 to 0.12) | 0 of 30 (0.00 to 0.12) | 0 of 30 (0.00 to 0.12) |
| B6 | Control | 0 of 30 (0.00 to 0.12) | 0 of 30 (0.00 to 0.12) | 0 of 30 (0.00 to 0.12) |

| Requirement | Errors, case only | Errors, with records | Errors, with filler |
|---|---|---|---|
| C1 | 60 of 120 | 0 of 120 | 35 of 120 |
| C2 | 0 of 90 | 2 of 90 | 2 of 90 |
| C3 | 0 of 30 | 0 of 30 | 0 of 30 |
| Control | 0 of 90 | 0 of 90 | 0 of 90 |

## gpt-6-luna

Sessions run: 90 of 90. Model shown: gpt-6-luna (90).

No valid RESULT line: ML-022 (A3: "Yes, not by itself" is not one of the choices).

| Item | Requirement | Errors, case only (95% CI) | Errors, with records (95% CI) | Errors, with filler (95% CI) |
|---|---|---|---|---|
| A1 | C2 coverage | 0 of 30 (0.00 to 0.12) | 0 of 30 (0.00 to 0.12) | 0 of 30 (0.00 to 0.12) |
| A2 | C2 learned time | 0 of 30 (0.00 to 0.12) | 27 of 30 (0.73 to 0.98) | 0 of 30 (0.00 to 0.12) |
| A3 | Control | 0 of 30 (0.00 to 0.12) | 0 of 30 (0.00 to 0.12) | 0 of 30 (0.00 to 0.12) |
| A4 | C1 channel state | 3 of 30 (0.02 to 0.27) | 0 of 30 (0.00 to 0.12) | 5 of 30 (0.06 to 0.35) |
| A5 | Control | 0 of 30 (0.00 to 0.12) | 0 of 30 (0.00 to 0.12) | 0 of 30 (0.00 to 0.12) |
| B1 | C1 attribution | 29 of 30 (0.83 to 1.00) | 0 of 30 (0.00 to 0.12) | 30 of 30 (0.88 to 1.00) |
| B2 | C1 per-account outcome | 0 of 30 (0.00 to 0.12) | 0 of 30 (0.00 to 0.12) | 0 of 30 (0.00 to 0.12) |
| B3 | C2 coverage | 29 of 30 (0.83 to 1.00) | 0 of 30 (0.00 to 0.12) | 28 of 30 (0.78 to 0.99) |
| B4 | C3 exposure links | 0 of 30 (0.00 to 0.12) | 0 of 30 (0.00 to 0.12) | 0 of 30 (0.00 to 0.12) |
| B5 | C1 decision link | 0 of 30 (0.00 to 0.12) | 0 of 30 (0.00 to 0.12) | 0 of 30 (0.00 to 0.12) |
| B6 | Control | 0 of 30 (0.00 to 0.12) | 0 of 30 (0.00 to 0.12) | 0 of 30 (0.00 to 0.12) |

| Requirement | Errors, case only | Errors, with records | Errors, with filler |
|---|---|---|---|
| C1 | 32 of 120 | 0 of 120 | 35 of 120 |
| C2 | 29 of 90 | 27 of 90 | 28 of 90 |
| C3 | 0 of 30 | 0 of 30 | 0 of 30 |
| Control | 0 of 90 | 0 of 90 | 0 of 90 |

## claude-opus-5-5

Sessions run: 90 of 90. Model shown: claude-opus-5-5 (90).

| Item | Requirement | Errors, case only (95% CI) | Errors, with records (95% CI) | Errors, with filler (95% CI) |
|---|---|---|---|---|
| A1 | C2 coverage | 0 of 30 (0.00 to 0.12) | 0 of 30 (0.00 to 0.12) | 0 of 30 (0.00 to 0.12) |
| A2 | C2 learned time | 0 of 30 (0.00 to 0.12) | 1 of 30 (0.00 to 0.17) | 0 of 30 (0.00 to 0.12) |
| A3 | Control | 0 of 30 (0.00 to 0.12) | 0 of 30 (0.00 to 0.12) | 0 of 30 (0.00 to 0.12) |
| A4 | C1 channel state | 5 of 30 (0.06 to 0.35) | 0 of 30 (0.00 to 0.12) | 0 of 30 (0.00 to 0.12) |
| A5 | Control | 0 of 30 (0.00 to 0.12) | 0 of 30 (0.00 to 0.12) | 0 of 30 (0.00 to 0.12) |
| B1 | C1 attribution | 30 of 30 (0.88 to 1.00) | 0 of 30 (0.00 to 0.12) | 24 of 30 (0.61 to 0.92) |
| B2 | C1 per-account outcome | 0 of 30 (0.00 to 0.12) | 0 of 30 (0.00 to 0.12) | 0 of 30 (0.00 to 0.12) |
| B3 | C2 coverage | 8 of 30 (0.12 to 0.46) | 0 of 30 (0.00 to 0.12) | 0 of 30 (0.00 to 0.12) |
| B4 | C3 exposure links | 0 of 30 (0.00 to 0.12) | 0 of 30 (0.00 to 0.12) | 0 of 30 (0.00 to 0.12) |
| B5 | C1 decision link | 0 of 30 (0.00 to 0.12) | 0 of 30 (0.00 to 0.12) | 0 of 30 (0.00 to 0.12) |
| B6 | Control | 0 of 30 (0.00 to 0.12) | 0 of 30 (0.00 to 0.12) | 0 of 30 (0.00 to 0.12) |

| Requirement | Errors, case only | Errors, with records | Errors, with filler |
|---|---|---|---|
| C1 | 35 of 120 | 0 of 120 | 24 of 120 |
| C2 | 8 of 90 | 1 of 90 | 0 of 90 |
| C3 | 0 of 30 | 0 of 30 | 0 of 30 |
| Control | 0 of 90 | 0 of 90 | 0 of 90 |

## claude-sonnet-5-5

Sessions run: 90 of 90. Model shown: claude-sonnet-5-5 (90).

| Item | Requirement | Errors, case only (95% CI) | Errors, with records (95% CI) | Errors, with filler (95% CI) |
|---|---|---|---|---|
| A1 | C2 coverage | 16 of 30 (0.34 to 0.72) | 1 of 30 (0.00 to 0.17) | 13 of 30 (0.25 to 0.63) |
| A2 | C2 learned time | 1 of 30 (0.00 to 0.17) | 1 of 30 (0.00 to 0.17) | 0 of 30 (0.00 to 0.12) |
| A3 | Control | 0 of 30 (0.00 to 0.12) | 0 of 30 (0.00 to 0.12) | 0 of 30 (0.00 to 0.12) |
| A4 | C1 channel state | 0 of 30 (0.00 to 0.12) | 0 of 30 (0.00 to 0.12) | 0 of 30 (0.00 to 0.12) |
| A5 | Control | 0 of 30 (0.00 to 0.12) | 0 of 30 (0.00 to 0.12) | 0 of 30 (0.00 to 0.12) |
| B1 | C1 attribution | 30 of 30 (0.88 to 1.00) | 0 of 30 (0.00 to 0.12) | 30 of 30 (0.88 to 1.00) |
| B2 | C1 per-account outcome | 0 of 30 (0.00 to 0.12) | 0 of 30 (0.00 to 0.12) | 0 of 30 (0.00 to 0.12) |
| B3 | C2 coverage | 0 of 30 (0.00 to 0.12) | 0 of 30 (0.00 to 0.12) | 0 of 30 (0.00 to 0.12) |
| B4 | C3 exposure links | 0 of 30 (0.00 to 0.12) | 0 of 30 (0.00 to 0.12) | 0 of 30 (0.00 to 0.12) |
| B5 | C1 decision link | 0 of 30 (0.00 to 0.12) | 0 of 30 (0.00 to 0.12) | 0 of 30 (0.00 to 0.12) |
| B6 | Control | 0 of 30 (0.00 to 0.12) | 0 of 30 (0.00 to 0.12) | 0 of 30 (0.00 to 0.12) |

| Requirement | Errors, case only | Errors, with records | Errors, with filler |
|---|---|---|---|
| C1 | 30 of 120 | 0 of 120 | 30 of 120 |
| C2 | 17 of 90 | 2 of 90 | 13 of 90 |
| C3 | 0 of 30 | 0 of 30 | 0 of 30 |
| Control | 0 of 90 | 0 of 90 | 0 of 90 |

## claude-haiku-5-5

Sessions run: 90 of 90. Model shown: claude-haiku-5-5 (90).

No valid RESULT line: MH-059 (B3: "No, not by itself" is not one of the choices).

| Item | Requirement | Errors, case only (95% CI) | Errors, with records (95% CI) | Errors, with filler (95% CI) |
|---|---|---|---|---|
| A1 | C2 coverage | 2 of 30 (0.01 to 0.22) | 0 of 30 (0.00 to 0.12) | 0 of 30 (0.00 to 0.12) |
| A2 | C2 learned time | 16 of 30 (0.34 to 0.72) | 3 of 30 (0.02 to 0.27) | 3 of 30 (0.02 to 0.27) |
| A3 | Control | 0 of 30 (0.00 to 0.12) | 0 of 30 (0.00 to 0.12) | 0 of 30 (0.00 to 0.12) |
| A4 | C1 channel state | 0 of 30 (0.00 to 0.12) | 0 of 30 (0.00 to 0.12) | 0 of 30 (0.00 to 0.12) |
| A5 | Control | 0 of 30 (0.00 to 0.12) | 0 of 30 (0.00 to 0.12) | 0 of 30 (0.00 to 0.12) |
| B1 | C1 attribution | 29 of 30 (0.83 to 1.00) | 0 of 30 (0.00 to 0.12) | 30 of 30 (0.88 to 1.00) |
| B2 | C1 per-account outcome | 0 of 30 (0.00 to 0.12) | 0 of 30 (0.00 to 0.12) | 0 of 30 (0.00 to 0.12) |
| B3 | C2 coverage | 0 of 30 (0.00 to 0.12) | 0 of 30 (0.00 to 0.12) | 0 of 30 (0.00 to 0.12) |
| B4 | C3 exposure links | 0 of 30 (0.00 to 0.12) | 0 of 30 (0.00 to 0.12) | 0 of 30 (0.00 to 0.12) |
| B5 | C1 decision link | 0 of 30 (0.00 to 0.12) | 0 of 30 (0.00 to 0.12) | 0 of 30 (0.00 to 0.12) |
| B6 | Control | 0 of 30 (0.00 to 0.12) | 0 of 30 (0.00 to 0.12) | 0 of 30 (0.00 to 0.12) |

| Requirement | Errors, case only | Errors, with records | Errors, with filler |
|---|---|---|---|
| C1 | 29 of 120 | 0 of 120 | 30 of 120 |
| C2 | 18 of 90 | 3 of 90 | 3 of 90 |
| C3 | 0 of 30 | 0 of 30 | 0 of 30 |
| Control | 0 of 90 | 0 of 90 | 0 of 90 |

## gpt-6.2-astra

Added on 19 November 2026, after the main results of the six fixed models were read (README, "Models").

Sessions run: 90 of 90. Model shown: gpt-6.2-astra (90).

| Item | Requirement | Errors, case only (95% CI) | Errors, with records (95% CI) | Errors, with filler (95% CI) |
|---|---|---|---|---|
| A1 | C2 coverage | 0 of 30 (0.00 to 0.12) | 0 of 30 (0.00 to 0.12) | 0 of 30 (0.00 to 0.12) |
| A2 | C2 learned time | 0 of 30 (0.00 to 0.12) | 0 of 30 (0.00 to 0.12) | 0 of 30 (0.00 to 0.12) |
| A3 | Control | 0 of 30 (0.00 to 0.12) | 0 of 30 (0.00 to 0.12) | 0 of 30 (0.00 to 0.12) |
| A4 | C1 channel state | 0 of 30 (0.00 to 0.12) | 0 of 30 (0.00 to 0.12) | 0 of 30 (0.00 to 0.12) |
| A5 | Control | 0 of 30 (0.00 to 0.12) | 0 of 30 (0.00 to 0.12) | 0 of 30 (0.00 to 0.12) |
| B1 | C1 attribution | 30 of 30 (0.88 to 1.00) | 0 of 30 (0.00 to 0.12) | 30 of 30 (0.88 to 1.00) |
| B2 | C1 per-account outcome | 0 of 30 (0.00 to 0.12) | 0 of 30 (0.00 to 0.12) | 0 of 30 (0.00 to 0.12) |
| B3 | C2 coverage | 0 of 30 (0.00 to 0.12) | 0 of 30 (0.00 to 0.12) | 0 of 30 (0.00 to 0.12) |
| B4 | C3 exposure links | 0 of 30 (0.00 to 0.12) | 0 of 30 (0.00 to 0.12) | 0 of 30 (0.00 to 0.12) |
| B5 | C1 decision link | 0 of 30 (0.00 to 0.12) | 0 of 30 (0.00 to 0.12) | 0 of 30 (0.00 to 0.12) |
| B6 | Control | 0 of 30 (0.00 to 0.12) | 0 of 30 (0.00 to 0.12) | 0 of 30 (0.00 to 0.12) |

| Requirement | Errors, case only | Errors, with records | Errors, with filler |
|---|---|---|---|
| C1 | 30 of 120 | 0 of 120 | 30 of 120 |
| C2 | 0 of 90 | 0 of 90 | 0 of 90 |
| C3 | 0 of 30 | 0 of 30 | 0 of 30 |
| Control | 0 of 90 | 0 of 90 | 0 of 90 |

## claude-fable-5-2

Added on 19 November 2026, after the main results of the six fixed models were read (README, "Models").

Sessions run: 90 of 90. Model shown: claude-fable-5-2 (90).

No valid RESULT line: MF-004 (unreadable part: B6); MF-019 (no RESULT line); MF-028 (no RESULT line); MF-051 (no RESULT line); MF-068 (no RESULT line); MF-005 (no RESULT line); MF-009 (unreadable part: B); MF-014 (no RESULT line); MF-041 (no RESULT line); MF-067 (no RESULT line); MF-081 (no RESULT line); MF-090 (unreadable part: B).

| Item | Requirement | Errors, case only (95% CI) | Errors, with records (95% CI) | Errors, with filler (95% CI) |
|---|---|---|---|---|
| A1 | C2 coverage | 13 of 30 (0.25 to 0.63) | 0 of 30 (0.00 to 0.12) | 0 of 30 (0.00 to 0.12) |
| A2 | C2 learned time | 25 of 30 (0.65 to 0.94) | 21 of 30 (0.51 to 0.85) | 0 of 30 (0.00 to 0.12) |
| A3 | Control | 0 of 30 (0.00 to 0.12) | 0 of 30 (0.00 to 0.12) | 0 of 30 (0.00 to 0.12) |
| A4 | C1 channel state | 25 of 30 (0.65 to 0.94) | 0 of 30 (0.00 to 0.12) | 0 of 30 (0.00 to 0.12) |
| A5 | Control | 0 of 30 (0.00 to 0.12) | 0 of 30 (0.00 to 0.12) | 0 of 30 (0.00 to 0.12) |
| B1 | C1 attribution | 25 of 30 (0.65 to 0.94) | 0 of 30 (0.00 to 0.12) | 5 of 30 (0.06 to 0.35) |
| B2 | C1 per-account outcome | 0 of 30 (0.00 to 0.12) | 0 of 30 (0.00 to 0.12) | 0 of 30 (0.00 to 0.12) |
| B3 | C2 coverage | 25 of 30 (0.65 to 0.94) | 0 of 30 (0.00 to 0.12) | 0 of 30 (0.00 to 0.12) |
| B4 | C3 exposure links | 2 of 30 (0.01 to 0.22) | 0 of 30 (0.00 to 0.12) | 0 of 30 (0.00 to 0.12) |
| B5 | C1 decision link | 0 of 30 (0.00 to 0.12) | 0 of 30 (0.00 to 0.12) | 0 of 30 (0.00 to 0.12) |
| B6 | Control | 0 of 30 (0.00 to 0.12) | 0 of 30 (0.00 to 0.12) | 0 of 30 (0.00 to 0.12) |

| Requirement | Errors, case only | Errors, with records | Errors, with filler |
|---|---|---|---|
| C1 | 50 of 120 | 0 of 120 | 5 of 120 |
| C2 | 63 of 90 | 21 of 90 | 0 of 90 |
| C3 | 2 of 30 | 0 of 30 | 0 of 30 |
| Control | 0 of 90 | 0 of 90 | 0 of 90 |

