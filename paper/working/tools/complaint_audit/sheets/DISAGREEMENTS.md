# Disagreements for the author's rulings

Coder 1 is Claude and coder 2 is ChatGPT. Both sheets were fixed before this list was made. Same mark on 78 of 98 tactic cells (pooled kappa 0.60). The full table comes from `python3 compare_sheets.py sheets/CLAUDE_SHEET.json sheets/CHATGPT_SHEET.json`.

There are 24 differences: 20 tactic marks and 4 context answers. Coder 1 wrote this list, so it is a party to every item. Each item gives the sheet's rule and the complaint's own words so the ruling can be checked against the text. Quotes are from the complaints.

Reply with item numbers and a mark, for example "A1-A8 coder 1; B1 alleged; B2 unclear".

## A. The complaint uses the rule's own words (8)

Coder 1 marked these; coder 2 did not.

- **A1. U11 T5.** Rule: a refund counts if it is "tied to avoiding chargebacks". ¶109: the processor told the owners "to immediately issue refunds to consumers who complain so that they would not initiate chargebacks". Coder 1 alleged; coder 2 not alleged.
- **A2. U12 T2.** Rule: accounts "in the names of shell companies or straw owners". ¶106: the two sellers' companies "were registered to straw owners or directors ... and not to the actual owners". Coder 1 alleged; coder 2 not alleged.
- **A3. U12 T6.** Rule: "business name ... is changed", over time. ¶81: PC Vark was "shuffling through different company names ... in a span of weeks". ¶134: Paddle changed its billing descriptors so Visa saw only Paddle. Coder 1 alleged; coder 2 not alleged.
- **A4. U06 T6.** Rule: "a closed account is replaced". ¶61 and ¶91: a new account for Nesch after "a prior account under a different business name that was closed two weeks earlier for excessive chargebacks and refunds". Coder 1 alleged; coder 2 not alleged.
- **A5. U04 T6.** Same rule. ¶71: after closure, the seller was "setting up [merchant accounts] with different signers". ¶76: the processor's agent said to "re-paper it" with the wife signing. ¶78: the account was re-opened. Coder 1 alleged; coder 2 not alleged.
- **A6. U07 T6.** Same rule. ¶140: after closure, "The only possible way to take this somewhere else is to present it as new". ¶143 and ¶144: the processor saw the closed account's kinds of transactions going to the Summit account. Coder 1 alleged; coder 2 not alleged.
- **A7. U14 T6.** Same rule. ¶8: accounts "often were closed within six months", and "the continuous supply of shell accounts ... enabled the online scams ... to avoid detection". ¶103: most closed in under a year. Coder 1 alleged; coder 2 not alleged.
- **A8. U12 X4.** Rule: an attribute shared across accounts. ¶63: nine PC Vark accounts under other names, linked by "the same account representative or account contact information". Coder 1 yes; coder 2 no. Whether it is tied to T1 or T2 follows B5 and A2.

## B. Close calls (16)

- **B1. U06 T1.** ¶49: 40 pairs of identical applications are "a strong indication" of load balancing, which the paragraph defines as spreading sales "to avoid triggering chargeback thresholds". This is stated as an indication, not as fact. Coder 1 unclear; coder 2 alleged.
- **B2. U07 T1.** ¶43: the processor put MOBE on seven accounts under its own policy of one account per product type. ¶32 explains that per-account counting lets ten accounts carry ten times the chargebacks. There is no allegation that MOBE split sales to stay under a threshold. Coder 1 unclear; coder 2 alleged.
- **B3. U05 T1.** ¶38: "if we move everything off PayPal, we'll send the PayPal account into severe chargeback state which will get reported to Visa". So ICE's sales stay split across two processors. Coder 1 unclear; coder 2 not alleged.
- **B4. U11 T1.** ¶110: "a plan to move volume back", so that processing "would not draw additional scrutiny" from Fiserv or the networks. Coder 1 unclear; coder 2 not alleged.
- **B5. U12 T1.** ¶102: Reimage wanted Paddle accounts "to spread Reimage's sales processing volume across more providers", which the paragraph ties to sellers that "anticipate having their accounts terminated". The link is to termination, not a stated threshold. ¶63 gives nine linked accounts but no threshold link. Coder 1 alleged; coder 2 not alleged.
- **B6. U03 T2.** Madera opened bank accounts under its clients' trade names. ¶65: it "falsely represented that Madera does not engage in processing payments for third-parties". Is this a false statement about who the seller is (T2), or about the type of business (O1, where coder 2 put it)? Coder 1 did not code T2 for U05 and U10, where the processor's own account hid what was sold. Coder 1 alleged; coder 2 not alleged.
- **B7. U07 T2.** ¶112: the processor told the bank MOBE "is US owned and located in the US". ¶140: the US signer "holds no actual ownership". Coder 1 alleged; coder 2 not alleged.
- **B8. U09 T2.** ¶40: AFTS "pretended that its 'client' was the processor", knowing the merchant was SLG. Coder 1 also cited ¶89, which is about the type of business; by coder 1's own rule that belongs in O1, so the mark rests on ¶40. Coder 1 alleged; coder 2 not alleged.
- **B9. U03 T3.** Clients' payment orders run through Madera's bank accounts (¶63, ¶69). The rule names a "merchant account" and the "acquirer or network". Does T3 cover bank checking accounts on the check rail? Coder 2 coded a similar structure on cards as T3 (U05). Coder 1 alleged; coder 2 not alleged.
- **B10. U09 T3.** ¶39 to ¶41: SLG's ACH debits ran through a "nested" relationship with another processor, PAN, which passed the funds on to SLG. Coder 1 unclear; coder 2 not alleged.
- **B11. U02 T6.** ¶87: more than 40 accounts, nearly all closed. ¶101: the processor offered "new merchant accounts to numerous shell companies" at a third bank. The complaint does not say the new accounts replaced particular closed ones. Coder 1 unclear; coder 2 not alleged.
- **B12. U10 T6.** ¶76 and ¶77: after Adyen required Nexway to stop sending Tech Live Connect's charges, Nexway sent them through Ingenico. Is moving to another acquirer "a closed account is replaced"? Coder 1 alleged; coder 2 not alleged.
- **B13. U13 T6.** ¶142: after a Mastercard notice, volume moved to other processors. ¶144: Reimage was told to change its descriptor to avoid "suggest[ing] an unregistered [payfac] relationship". That descriptor change hides a relationship, not past reports. Coder 1 alleged; coder 2 not alleged.
- **B14. U02 X3.** The complaint gives no rate or count for any account. Coder 2 cites mentions of "high chargeback rates" (¶92) and ratio management (¶95 to ¶99). Does X3 need a stated number? Coder 1 no; coder 2 yes.
- **B15. U09 X4.** ¶57: two related companies with "nearly identical website services, from adjacent suites". Coder 1 yes (not tied to T1 or T2); coder 2 no.
- **B16. U03 X4.** Both coders say yes. Whether it is tied to T1 or T2 follows B6: if T2 is not alleged, the answer is "n/a".

## After the rulings

The final marks go in `sheets/ADJUDICATED.json`, with each ruling cited by item number. Counts and the Section 8.5 and S10 text are drafted from that file. Agreement before the rulings is reported as above.
