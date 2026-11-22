# Agent test results, practice

Counted errors by model: case only / with records / current practice, each of the sessions run. "not scored" marks a condition with no usable answer.

| Item | Requirement | gpt-6.1-sol | gpt-6.1-terra | gpt-6-luna | claude-opus-5-5 | claude-sonnet-5-5 | claude-haiku-5-5 | gpt-6.2-astra | claude-fable-5-2 |
|---|---|---|---|---|---|---|---|---|---|
| A1 | C2 coverage | 0/0/0 | 0/0/0 | 0/0/0 | 0/0/8 | 20/0/27 | 2/0/3 | 0/0/0 | 9/0/16 |
| A2 | C2 learned time | 0/12/0 | 0/1/0 | 2/25/0 | 0/0/0 | 0/0/7 | 10/0/6 | 0/0/0 | 22/27/13 |
| A3 | Control | 0/0/0 | 0/0/0 | 0/0/0 | 0/0/0 | 0/0/0 | 0/0/0 | 0/0/0 | 0/0/0 |
| A4 | C1 channel state | 5/0/0 | 30/0/29 | 4/0/8 | 7/0/4 | 2/0/1 | 0/0/0 | 0/0/0 | 26/0/16 |
| A5 | Control | 0/0/0 | 0/0/0 | 0/0/0 | 0/0/0 | 0/0/0 | 0/0/0 | 0/0/0 | 0/0/0 |
| B1 | C1 attribution | 30/0/0 | 30/0/0 | 30/0/0 | 30/0/0 | 30/0/0 | 30/0/0 | 30/0/0 | 26/0/0 |
| B2 | C1 per-account outcome | 0/0/0 | 0/0/0 | 0/0/0 | 0/0/0 | 0/0/0 | 0/0/0 | 0/0/0 | 0/0/0 |
| B3 | C2 coverage | 0/0/0 | 0/0/0 | 30/0/9 | 9/0/0 | 0/0/0 | 0/0/0 | 0/0/0 | 25/0/5 |
| B4 | C3 exposure links | 0/0/0 | 0/0/0 | 0/0/5 | 0/0/0 | 0/0/0 | 0/0/0 | 0/0/0 | 0/0/3 |
| B5 | C1 decision link | 0/0/0 | 0/0/0 | 0/0/0 | 0/0/0 | 0/0/0 | 0/0/0 | 0/0/0 | 0/0/0 |
| B6 | Control | 0/0/0 | 0/0/0 | 0/0/0 | 0/0/0 | 0/0/0 | 0/0/0 | 0/0/0 | 0/0/0 |

Sessions run / usable answers / other no answers / stopped by the API, by model and condition.

| Model | case only | with records | current practice |
|---|---|---|---|
| gpt-6.1-sol | 30 / 30 / 0 / 0 | 30 / 30 / 0 / 0 | 30 / 30 / 0 / 0 |
| gpt-6.1-terra | 30 / 30 / 0 / 0 | 30 / 30 / 0 / 0 | 30 / 30 / 0 / 0 |
| gpt-6-luna | 30 / 30 / 0 / 0 | 30 / 30 / 0 / 0 | 30 / 30 / 0 / 0 |
| claude-opus-5-5 | 30 / 30 / 0 / 0 | 30 / 30 / 0 / 0 | 30 / 30 / 0 / 0 |
| claude-sonnet-5-5 | 30 / 30 / 0 / 0 | 30 / 30 / 0 / 0 | 30 / 30 / 0 / 0 |
| claude-haiku-5-5 | 30 / 30 / 0 / 0 | 30 / 30 / 0 / 0 | 30 / 30 / 0 / 0 |
| gpt-6.2-astra | 30 / 30 / 0 / 0 | 30 / 30 / 0 / 0 | 30 / 30 / 0 / 0 |
| claude-fable-5-2 | 30 / 26 / 4 / 0 | 30 / 30 / 0 / 0 | 30 / 17 / 13 / 0 |

Planned comparison (README, "Practice phase"): counted errors among usable answers, current practice against with records, on the items whose current-practice record lacks the field C1 or C2 adds. Fisher's exact test, two-sided; p adjusted by Holm's method over all rows.

| Model | Item | Requirement | Current practice | With records | p | Holm p | Reading |
|---|---|---|---|---|---|---|---|
| gpt-6.1-sol | A1 | C2 coverage | 0 of 30 | 0 of 30 | 1 | 1 | no error in either condition; tests nothing |
| gpt-6.1-sol | A2 | C2 learned time | 0 of 30 | 12 of 30 | 0.000124 | 0.00334 | more errors with the records |
| gpt-6.1-sol | A4 | C1 channel state | 0 of 30 | 0 of 30 | 1 | 1 | no error in either condition; tests nothing |
| gpt-6.1-sol | B3 | C2 coverage | 0 of 30 | 0 of 30 | 1 | 1 | no error in either condition; tests nothing |
| gpt-6.1-terra | A1 | C2 coverage | 0 of 30 | 0 of 30 | 1 | 1 | no error in either condition; tests nothing |
| gpt-6.1-terra | A2 | C2 learned time | 0 of 30 | 1 of 30 | 1 | 1 | no difference shown |
| gpt-6.1-terra | A4 | C1 channel state | 29 of 30 | 0 of 30 | 5.24e-16 | 1.68e-14 | more errors with current practice |
| gpt-6.1-terra | B3 | C2 coverage | 0 of 30 | 0 of 30 | 1 | 1 | no error in either condition; tests nothing |
| gpt-6-luna | A1 | C2 coverage | 0 of 30 | 0 of 30 | 1 | 1 | no error in either condition; tests nothing |
| gpt-6-luna | A2 | C2 learned time | 0 of 30 | 25 of 30 | 5.49e-12 | 1.65e-10 | more errors with the records |
| gpt-6-luna | A4 | C1 channel state | 8 of 30 | 0 of 30 | 0.00458 | 0.11 | no difference shown |
| gpt-6-luna | B3 | C2 coverage | 9 of 30 | 0 of 30 | 0.00194 | 0.0503 | no difference shown |
| claude-opus-5-5 | A1 | C2 coverage | 8 of 30 | 0 of 30 | 0.00458 | 0.11 | no difference shown |
| claude-opus-5-5 | A2 | C2 learned time | 0 of 30 | 0 of 30 | 1 | 1 | no error in either condition; tests nothing |
| claude-opus-5-5 | A4 | C1 channel state | 4 of 30 | 0 of 30 | 0.112 | 1 | no difference shown |
| claude-opus-5-5 | B3 | C2 coverage | 0 of 30 | 0 of 30 | 1 | 1 | no error in either condition; tests nothing |
| claude-sonnet-5-5 | A1 | C2 coverage | 27 of 30 | 0 of 30 | 9.23e-14 | 2.86e-12 | more errors with current practice |
| claude-sonnet-5-5 | A2 | C2 learned time | 7 of 30 | 0 of 30 | 0.0105 | 0.232 | no difference shown |
| claude-sonnet-5-5 | A4 | C1 channel state | 1 of 30 | 0 of 30 | 1 | 1 | no difference shown |
| claude-sonnet-5-5 | B3 | C2 coverage | 0 of 30 | 0 of 30 | 1 | 1 | no error in either condition; tests nothing |
| claude-haiku-5-5 | A1 | C2 coverage | 3 of 30 | 0 of 30 | 0.237 | 1 | no difference shown |
| claude-haiku-5-5 | A2 | C2 learned time | 6 of 30 | 0 of 30 | 0.0237 | 0.498 | no difference shown |
| claude-haiku-5-5 | A4 | C1 channel state | 0 of 30 | 0 of 30 | 1 | 1 | no error in either condition; tests nothing |
| claude-haiku-5-5 | B3 | C2 coverage | 0 of 30 | 0 of 30 | 1 | 1 | no error in either condition; tests nothing |
| gpt-6.2-astra | A1 | C2 coverage | 0 of 30 | 0 of 30 | 1 | 1 | no error in either condition; tests nothing |
| gpt-6.2-astra | A2 | C2 learned time | 0 of 30 | 0 of 30 | 1 | 1 | no error in either condition; tests nothing |
| gpt-6.2-astra | A4 | C1 channel state | 0 of 30 | 0 of 30 | 1 | 1 | no error in either condition; tests nothing |
| gpt-6.2-astra | B3 | C2 coverage | 0 of 30 | 0 of 30 | 1 | 1 | no error in either condition; tests nothing |
| claude-fable-5-2 | A1 | C2 coverage | 16 of 17 | 0 of 30 | 1.13e-11 | 3.28e-10 | more errors with current practice |
| claude-fable-5-2 | A2 | C2 learned time | 13 of 17 | 27 of 30 | 0.235 | 1 | no difference shown |
| claude-fable-5-2 | A4 | C1 channel state | 16 of 17 | 0 of 30 | 1.13e-11 | 3.28e-10 | more errors with current practice |
| claude-fable-5-2 | B3 | C2 coverage | 5 of 17 | 0 of 30 | 0.00403 | 0.101 | no difference shown |

## gpt-6.1-sol

Sessions run: 90 of 90. Model shown: gpt-6.1-sol (90).

Usable answers: case only 30 of 30; with records 30 of 30; current practice 30 of 30.

| Item | Requirement | Errors, case only (95% CI) | Errors, with records (95% CI) | Errors, current practice (95% CI) |
|---|---|---|---|---|
| A1 | C2 coverage | 0 of 30 (0.00 to 0.12) | 0 of 30 (0.00 to 0.12) | 0 of 30 (0.00 to 0.12) |
| A2 | C2 learned time | 0 of 30 (0.00 to 0.12) | 12 of 30 (0.23 to 0.59) | 0 of 30 (0.00 to 0.12) |
| A3 | Control | 0 of 30 (0.00 to 0.12) | 0 of 30 (0.00 to 0.12) | 0 of 30 (0.00 to 0.12) |
| A4 | C1 channel state | 5 of 30 (0.06 to 0.35) | 0 of 30 (0.00 to 0.12) | 0 of 30 (0.00 to 0.12) |
| A5 | Control | 0 of 30 (0.00 to 0.12) | 0 of 30 (0.00 to 0.12) | 0 of 30 (0.00 to 0.12) |
| B1 | C1 attribution | 30 of 30 (0.88 to 1.00) | 0 of 30 (0.00 to 0.12) | 0 of 30 (0.00 to 0.12) |
| B2 | C1 per-account outcome | 0 of 30 (0.00 to 0.12) | 0 of 30 (0.00 to 0.12) | 0 of 30 (0.00 to 0.12) |
| B3 | C2 coverage | 0 of 30 (0.00 to 0.12) | 0 of 30 (0.00 to 0.12) | 0 of 30 (0.00 to 0.12) |
| B4 | C3 exposure links | 0 of 30 (0.00 to 0.12) | 0 of 30 (0.00 to 0.12) | 0 of 30 (0.00 to 0.12) |
| B5 | C1 decision link | 0 of 30 (0.00 to 0.12) | 0 of 30 (0.00 to 0.12) | 0 of 30 (0.00 to 0.12) |
| B6 | Control | 0 of 30 (0.00 to 0.12) | 0 of 30 (0.00 to 0.12) | 0 of 30 (0.00 to 0.12) |

| Requirement | Errors, case only | Errors, with records | Errors, current practice |
|---|---|---|---|
| C1 | 35 of 120 | 0 of 120 | 0 of 120 |
| C2 | 0 of 90 | 12 of 90 | 0 of 90 |
| C3 | 0 of 30 | 0 of 30 | 0 of 30 |
| Control | 0 of 90 | 0 of 90 | 0 of 90 |

## gpt-6.1-terra

Sessions run: 90 of 90. Model shown: gpt-6.1-terra (90).

Usable answers: case only 30 of 30; with records 30 of 30; current practice 30 of 30.

| Item | Requirement | Errors, case only (95% CI) | Errors, with records (95% CI) | Errors, current practice (95% CI) |
|---|---|---|---|---|
| A1 | C2 coverage | 0 of 30 (0.00 to 0.12) | 0 of 30 (0.00 to 0.12) | 0 of 30 (0.00 to 0.12) |
| A2 | C2 learned time | 0 of 30 (0.00 to 0.12) | 1 of 30 (0.00 to 0.17) | 0 of 30 (0.00 to 0.12) |
| A3 | Control | 0 of 30 (0.00 to 0.12) | 0 of 30 (0.00 to 0.12) | 0 of 30 (0.00 to 0.12) |
| A4 | C1 channel state | 30 of 30 (0.88 to 1.00) | 0 of 30 (0.00 to 0.12) | 29 of 30 (0.83 to 1.00) |
| A5 | Control | 0 of 30 (0.00 to 0.12) | 0 of 30 (0.00 to 0.12) | 0 of 30 (0.00 to 0.12) |
| B1 | C1 attribution | 30 of 30 (0.88 to 1.00) | 0 of 30 (0.00 to 0.12) | 0 of 30 (0.00 to 0.12) |
| B2 | C1 per-account outcome | 0 of 30 (0.00 to 0.12) | 0 of 30 (0.00 to 0.12) | 0 of 30 (0.00 to 0.12) |
| B3 | C2 coverage | 0 of 30 (0.00 to 0.12) | 0 of 30 (0.00 to 0.12) | 0 of 30 (0.00 to 0.12) |
| B4 | C3 exposure links | 0 of 30 (0.00 to 0.12) | 0 of 30 (0.00 to 0.12) | 0 of 30 (0.00 to 0.12) |
| B5 | C1 decision link | 0 of 30 (0.00 to 0.12) | 0 of 30 (0.00 to 0.12) | 0 of 30 (0.00 to 0.12) |
| B6 | Control | 0 of 30 (0.00 to 0.12) | 0 of 30 (0.00 to 0.12) | 0 of 30 (0.00 to 0.12) |

| Requirement | Errors, case only | Errors, with records | Errors, current practice |
|---|---|---|---|
| C1 | 60 of 120 | 0 of 120 | 29 of 120 |
| C2 | 0 of 90 | 1 of 90 | 0 of 90 |
| C3 | 0 of 30 | 0 of 30 | 0 of 30 |
| Control | 0 of 90 | 0 of 90 | 0 of 90 |

## gpt-6-luna

Sessions run: 90 of 90. Model shown: gpt-6-luna (90).

Usable answers: case only 30 of 30; with records 30 of 30; current practice 30 of 30.

| Item | Requirement | Errors, case only (95% CI) | Errors, with records (95% CI) | Errors, current practice (95% CI) |
|---|---|---|---|---|
| A1 | C2 coverage | 0 of 30 (0.00 to 0.12) | 0 of 30 (0.00 to 0.12) | 0 of 30 (0.00 to 0.12) |
| A2 | C2 learned time | 2 of 30 (0.01 to 0.22) | 25 of 30 (0.65 to 0.94) | 0 of 30 (0.00 to 0.12) |
| A3 | Control | 0 of 30 (0.00 to 0.12) | 0 of 30 (0.00 to 0.12) | 0 of 30 (0.00 to 0.12) |
| A4 | C1 channel state | 4 of 30 (0.04 to 0.31) | 0 of 30 (0.00 to 0.12) | 8 of 30 (0.12 to 0.46) |
| A5 | Control | 0 of 30 (0.00 to 0.12) | 0 of 30 (0.00 to 0.12) | 0 of 30 (0.00 to 0.12) |
| B1 | C1 attribution | 30 of 30 (0.88 to 1.00) | 0 of 30 (0.00 to 0.12) | 0 of 30 (0.00 to 0.12) |
| B2 | C1 per-account outcome | 0 of 30 (0.00 to 0.12) | 0 of 30 (0.00 to 0.12) | 0 of 30 (0.00 to 0.12) |
| B3 | C2 coverage | 30 of 30 (0.88 to 1.00) | 0 of 30 (0.00 to 0.12) | 9 of 30 (0.15 to 0.49) |
| B4 | C3 exposure links | 0 of 30 (0.00 to 0.12) | 0 of 30 (0.00 to 0.12) | 5 of 30 (0.06 to 0.35) |
| B5 | C1 decision link | 0 of 30 (0.00 to 0.12) | 0 of 30 (0.00 to 0.12) | 0 of 30 (0.00 to 0.12) |
| B6 | Control | 0 of 30 (0.00 to 0.12) | 0 of 30 (0.00 to 0.12) | 0 of 30 (0.00 to 0.12) |

| Requirement | Errors, case only | Errors, with records | Errors, current practice |
|---|---|---|---|
| C1 | 34 of 120 | 0 of 120 | 8 of 120 |
| C2 | 32 of 90 | 25 of 90 | 9 of 90 |
| C3 | 0 of 30 | 0 of 30 | 5 of 30 |
| Control | 0 of 90 | 0 of 90 | 0 of 90 |

## claude-opus-5-5

Sessions run: 90 of 90. Model shown: claude-opus-5-5 (90).

Usable answers: case only 30 of 30; with records 30 of 30; current practice 30 of 30.

| Item | Requirement | Errors, case only (95% CI) | Errors, with records (95% CI) | Errors, current practice (95% CI) |
|---|---|---|---|---|
| A1 | C2 coverage | 0 of 30 (0.00 to 0.12) | 0 of 30 (0.00 to 0.12) | 8 of 30 (0.12 to 0.46) |
| A2 | C2 learned time | 0 of 30 (0.00 to 0.12) | 0 of 30 (0.00 to 0.12) | 0 of 30 (0.00 to 0.12) |
| A3 | Control | 0 of 30 (0.00 to 0.12) | 0 of 30 (0.00 to 0.12) | 0 of 30 (0.00 to 0.12) |
| A4 | C1 channel state | 7 of 30 (0.10 to 0.42) | 0 of 30 (0.00 to 0.12) | 4 of 30 (0.04 to 0.31) |
| A5 | Control | 0 of 30 (0.00 to 0.12) | 0 of 30 (0.00 to 0.12) | 0 of 30 (0.00 to 0.12) |
| B1 | C1 attribution | 30 of 30 (0.88 to 1.00) | 0 of 30 (0.00 to 0.12) | 0 of 30 (0.00 to 0.12) |
| B2 | C1 per-account outcome | 0 of 30 (0.00 to 0.12) | 0 of 30 (0.00 to 0.12) | 0 of 30 (0.00 to 0.12) |
| B3 | C2 coverage | 9 of 30 (0.15 to 0.49) | 0 of 30 (0.00 to 0.12) | 0 of 30 (0.00 to 0.12) |
| B4 | C3 exposure links | 0 of 30 (0.00 to 0.12) | 0 of 30 (0.00 to 0.12) | 0 of 30 (0.00 to 0.12) |
| B5 | C1 decision link | 0 of 30 (0.00 to 0.12) | 0 of 30 (0.00 to 0.12) | 0 of 30 (0.00 to 0.12) |
| B6 | Control | 0 of 30 (0.00 to 0.12) | 0 of 30 (0.00 to 0.12) | 0 of 30 (0.00 to 0.12) |

| Requirement | Errors, case only | Errors, with records | Errors, current practice |
|---|---|---|---|
| C1 | 37 of 120 | 0 of 120 | 4 of 120 |
| C2 | 9 of 90 | 0 of 90 | 8 of 90 |
| C3 | 0 of 30 | 0 of 30 | 0 of 30 |
| Control | 0 of 90 | 0 of 90 | 0 of 90 |

## claude-sonnet-5-5

Sessions run: 90 of 90. Model shown: claude-sonnet-5-5 (90).

Usable answers: case only 30 of 30; with records 30 of 30; current practice 30 of 30.

| Item | Requirement | Errors, case only (95% CI) | Errors, with records (95% CI) | Errors, current practice (95% CI) |
|---|---|---|---|---|
| A1 | C2 coverage | 20 of 30 (0.47 to 0.83) | 0 of 30 (0.00 to 0.12) | 27 of 30 (0.73 to 0.98) |
| A2 | C2 learned time | 0 of 30 (0.00 to 0.12) | 0 of 30 (0.00 to 0.12) | 7 of 30 (0.10 to 0.42) |
| A3 | Control | 0 of 30 (0.00 to 0.12) | 0 of 30 (0.00 to 0.12) | 0 of 30 (0.00 to 0.12) |
| A4 | C1 channel state | 2 of 30 (0.01 to 0.22) | 0 of 30 (0.00 to 0.12) | 1 of 30 (0.00 to 0.17) |
| A5 | Control | 0 of 30 (0.00 to 0.12) | 0 of 30 (0.00 to 0.12) | 0 of 30 (0.00 to 0.12) |
| B1 | C1 attribution | 30 of 30 (0.88 to 1.00) | 0 of 30 (0.00 to 0.12) | 0 of 30 (0.00 to 0.12) |
| B2 | C1 per-account outcome | 0 of 30 (0.00 to 0.12) | 0 of 30 (0.00 to 0.12) | 0 of 30 (0.00 to 0.12) |
| B3 | C2 coverage | 0 of 30 (0.00 to 0.12) | 0 of 30 (0.00 to 0.12) | 0 of 30 (0.00 to 0.12) |
| B4 | C3 exposure links | 0 of 30 (0.00 to 0.12) | 0 of 30 (0.00 to 0.12) | 0 of 30 (0.00 to 0.12) |
| B5 | C1 decision link | 0 of 30 (0.00 to 0.12) | 0 of 30 (0.00 to 0.12) | 0 of 30 (0.00 to 0.12) |
| B6 | Control | 0 of 30 (0.00 to 0.12) | 0 of 30 (0.00 to 0.12) | 0 of 30 (0.00 to 0.12) |

| Requirement | Errors, case only | Errors, with records | Errors, current practice |
|---|---|---|---|
| C1 | 32 of 120 | 0 of 120 | 1 of 120 |
| C2 | 20 of 90 | 0 of 90 | 34 of 90 |
| C3 | 0 of 30 | 0 of 30 | 0 of 30 |
| Control | 0 of 90 | 0 of 90 | 0 of 90 |

## claude-haiku-5-5

Sessions run: 90 of 90. Model shown: claude-haiku-5-5 (90).

Usable answers: case only 30 of 30; with records 30 of 30; current practice 30 of 30.

| Item | Requirement | Errors, case only (95% CI) | Errors, with records (95% CI) | Errors, current practice (95% CI) |
|---|---|---|---|---|
| A1 | C2 coverage | 2 of 30 (0.01 to 0.22) | 0 of 30 (0.00 to 0.12) | 3 of 30 (0.02 to 0.27) |
| A2 | C2 learned time | 10 of 30 (0.17 to 0.53) | 0 of 30 (0.00 to 0.12) | 6 of 30 (0.08 to 0.39) |
| A3 | Control | 0 of 30 (0.00 to 0.12) | 0 of 30 (0.00 to 0.12) | 0 of 30 (0.00 to 0.12) |
| A4 | C1 channel state | 0 of 30 (0.00 to 0.12) | 0 of 30 (0.00 to 0.12) | 0 of 30 (0.00 to 0.12) |
| A5 | Control | 0 of 30 (0.00 to 0.12) | 0 of 30 (0.00 to 0.12) | 0 of 30 (0.00 to 0.12) |
| B1 | C1 attribution | 30 of 30 (0.88 to 1.00) | 0 of 30 (0.00 to 0.12) | 0 of 30 (0.00 to 0.12) |
| B2 | C1 per-account outcome | 0 of 30 (0.00 to 0.12) | 0 of 30 (0.00 to 0.12) | 0 of 30 (0.00 to 0.12) |
| B3 | C2 coverage | 0 of 30 (0.00 to 0.12) | 0 of 30 (0.00 to 0.12) | 0 of 30 (0.00 to 0.12) |
| B4 | C3 exposure links | 0 of 30 (0.00 to 0.12) | 0 of 30 (0.00 to 0.12) | 0 of 30 (0.00 to 0.12) |
| B5 | C1 decision link | 0 of 30 (0.00 to 0.12) | 0 of 30 (0.00 to 0.12) | 0 of 30 (0.00 to 0.12) |
| B6 | Control | 0 of 30 (0.00 to 0.12) | 0 of 30 (0.00 to 0.12) | 0 of 30 (0.00 to 0.12) |

| Requirement | Errors, case only | Errors, with records | Errors, current practice |
|---|---|---|---|
| C1 | 30 of 120 | 0 of 120 | 0 of 120 |
| C2 | 12 of 90 | 0 of 90 | 9 of 90 |
| C3 | 0 of 30 | 0 of 30 | 0 of 30 |
| Control | 0 of 90 | 0 of 90 | 0 of 90 |

## gpt-6.2-astra

Sessions run: 90 of 90. Model shown: gpt-6.2-astra (90).

Usable answers: case only 30 of 30; with records 30 of 30; current practice 30 of 30.

| Item | Requirement | Errors, case only (95% CI) | Errors, with records (95% CI) | Errors, current practice (95% CI) |
|---|---|---|---|---|
| A1 | C2 coverage | 0 of 30 (0.00 to 0.12) | 0 of 30 (0.00 to 0.12) | 0 of 30 (0.00 to 0.12) |
| A2 | C2 learned time | 0 of 30 (0.00 to 0.12) | 0 of 30 (0.00 to 0.12) | 0 of 30 (0.00 to 0.12) |
| A3 | Control | 0 of 30 (0.00 to 0.12) | 0 of 30 (0.00 to 0.12) | 0 of 30 (0.00 to 0.12) |
| A4 | C1 channel state | 0 of 30 (0.00 to 0.12) | 0 of 30 (0.00 to 0.12) | 0 of 30 (0.00 to 0.12) |
| A5 | Control | 0 of 30 (0.00 to 0.12) | 0 of 30 (0.00 to 0.12) | 0 of 30 (0.00 to 0.12) |
| B1 | C1 attribution | 30 of 30 (0.88 to 1.00) | 0 of 30 (0.00 to 0.12) | 0 of 30 (0.00 to 0.12) |
| B2 | C1 per-account outcome | 0 of 30 (0.00 to 0.12) | 0 of 30 (0.00 to 0.12) | 0 of 30 (0.00 to 0.12) |
| B3 | C2 coverage | 0 of 30 (0.00 to 0.12) | 0 of 30 (0.00 to 0.12) | 0 of 30 (0.00 to 0.12) |
| B4 | C3 exposure links | 0 of 30 (0.00 to 0.12) | 0 of 30 (0.00 to 0.12) | 0 of 30 (0.00 to 0.12) |
| B5 | C1 decision link | 0 of 30 (0.00 to 0.12) | 0 of 30 (0.00 to 0.12) | 0 of 30 (0.00 to 0.12) |
| B6 | Control | 0 of 30 (0.00 to 0.12) | 0 of 30 (0.00 to 0.12) | 0 of 30 (0.00 to 0.12) |

| Requirement | Errors, case only | Errors, with records | Errors, current practice |
|---|---|---|---|
| C1 | 30 of 120 | 0 of 120 | 0 of 120 |
| C2 | 0 of 90 | 0 of 90 | 0 of 90 |
| C3 | 0 of 30 | 0 of 30 | 0 of 30 |
| Control | 0 of 90 | 0 of 90 | 0 of 90 |

## claude-fable-5-2

Sessions run: 90 of 90. Model shown: claude-fable-5-2 (90).

No valid RESULT line: CF-036 (no RESULT line); CF-042 (no RESULT line); CF-059 (no RESULT line); CF-082 (no RESULT line); CF-008 (no RESULT line); CF-009 (no RESULT line); CF-015 (no RESULT line); CF-017 (no RESULT line); CF-020 (no RESULT line); CF-022 (no RESULT line); CF-023 (no RESULT line); CF-027 (no RESULT line); CF-029 (no RESULT line); CF-032 (no RESULT line); CF-054 (no RESULT line); CF-057 (no RESULT line); CF-076 (no RESULT line).

Usable answers: case only 26 of 30; with records 30 of 30; current practice 17 of 30.

| Item | Requirement | Errors, case only (95% CI) | Errors, with records (95% CI) | Errors, current practice (95% CI) |
|---|---|---|---|---|
| A1 | C2 coverage | 9 of 30 (0.15 to 0.49) | 0 of 30 (0.00 to 0.12) | 16 of 30 (0.34 to 0.72) |
| A2 | C2 learned time | 22 of 30 (0.54 to 0.88) | 27 of 30 (0.73 to 0.98) | 13 of 30 (0.25 to 0.63) |
| A3 | Control | 0 of 30 (0.00 to 0.12) | 0 of 30 (0.00 to 0.12) | 0 of 30 (0.00 to 0.12) |
| A4 | C1 channel state | 26 of 30 (0.69 to 0.96) | 0 of 30 (0.00 to 0.12) | 16 of 30 (0.34 to 0.72) |
| A5 | Control | 0 of 30 (0.00 to 0.12) | 0 of 30 (0.00 to 0.12) | 0 of 30 (0.00 to 0.12) |
| B1 | C1 attribution | 26 of 30 (0.69 to 0.96) | 0 of 30 (0.00 to 0.12) | 0 of 30 (0.00 to 0.12) |
| B2 | C1 per-account outcome | 0 of 30 (0.00 to 0.12) | 0 of 30 (0.00 to 0.12) | 0 of 30 (0.00 to 0.12) |
| B3 | C2 coverage | 25 of 30 (0.65 to 0.94) | 0 of 30 (0.00 to 0.12) | 5 of 30 (0.06 to 0.35) |
| B4 | C3 exposure links | 0 of 30 (0.00 to 0.12) | 0 of 30 (0.00 to 0.12) | 3 of 30 (0.02 to 0.27) |
| B5 | C1 decision link | 0 of 30 (0.00 to 0.12) | 0 of 30 (0.00 to 0.12) | 0 of 30 (0.00 to 0.12) |
| B6 | Control | 0 of 30 (0.00 to 0.12) | 0 of 30 (0.00 to 0.12) | 0 of 30 (0.00 to 0.12) |

| Requirement | Errors, case only | Errors, with records | Errors, current practice |
|---|---|---|---|
| C1 | 52 of 120 | 0 of 120 | 16 of 120 |
| C2 | 56 of 90 | 27 of 90 | 34 of 90 |
| C3 | 0 of 30 | 0 of 30 | 3 of 30 |
| Control | 0 of 90 | 0 of 90 | 0 of 90 |

