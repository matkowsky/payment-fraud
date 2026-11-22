# Round 3: Claude's first rulings

Written after the scoring and fixed before any outside ruling exists. Claude wrote the rules, so these rulings are proposals. The author confirms every ruling.

Twelve of the sixteen cases came out as their kind requires and need no ruling: eleven histories meant to break a requirement are rejected, and one meant to be legitimate passes. Four need a ruling.

| Case | Tester meant | Frozen checker | First ruling | Basis |
|---|---|---|---|---|
| R02 | Legitimate | Rejects, IR-09 | Rules stand | C3: a released conclusion serves only as a hypothesis or context. The claim cites released item M-1 as support. The tester's own reason says IR-09 does not allow it. |
| R05 | Breaks C1 | Passes | Stated limit | The claim is marked as a status and its sentence is changed. No rule reads the sentence, and the packet says so twice under "Stated limits". As changed, the sentence says the attempt drew a chargeback and that no report arrived, so it also contradicts itself. A reviewer has to catch either fault. |
| R13 | Legitimate | Rejects, IR-08 and XR-01 | Rules stand | The claim says attempt PA-4 drew no chargeback. The cited run evaluated PA-3 only, and C2 defines coverage as what a query actually covered. The cited reading is of PA-3, and Section 6.4 asks for the channel state of each affected item. |
| R14 | Breaks C2 | Error, no finding | Rules reject; checker fault, minor | A run that returns a draft lists an agent output among its returned records. IR-06 as stated rejects it, and the reference table gives observations as the only target of that reference. Run alone, the fourteen rules report IR-06 and IR-08 (`diagnostics.py`). The plan's command raised an error in the code for XR-01 and reported nothing. That is a fault of the checker's code, not of the rules as stated. It counts as a round 3 miss and is fixed only after the rulings are confirmed. The checker stops on the history; it does not pass it. |

## Counts under these first rulings

- 13 histories meant to break a requirement: 9 rejected by the rules under test, 2 rejected only by the outcome rules (R12, R16), 1 passes and is a stated limit (R05), 1 stops the checker (R14). No new failure of the rules as stated. One fault in the checker's code.
- 3 histories meant to be legitimate: 1 passes (R07), 2 are rejected and the rules stand (R02, R13). No false rejection.

Recorded by Claude (Anthropic), 22 November 2026.
