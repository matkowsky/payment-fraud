# Adjudication brief

Two coders coded 14 FTC complaints against the sheet below. They differ on the 24 items listed here. For each item you see the two readings in random order, without the coders' names, and the text of every paragraph either reading cites. Quotes are the complaint's own words.

## The coding sheet (verbatim)

# Coding sheet

One row per complaint. Mark each tactic `alleged`, `not alleged`, `unclear` or `unavailable`, and give the paragraph numbers that support the mark. Code what the complaint alleges about the sellers, the defendants or both. Do not infer a tactic from an outcome.

## Tactics

T1. Split volume. One seller's or scheme's sales are spread across several merchant accounts, entities or processors, so that each stays under a monitoring threshold. Often called load balancing.

T2. Front accounts. Merchant accounts are opened in the names of shell companies or straw owners, or with false statements about who the seller is.

T3. Pooled account. Several sellers' sales run through one merchant account, so that the acquirer or network cannot see each seller's own rates. Often called credit card laundering, factoring or aggregation.

T4. Dilution. Small or sham sales are added to raise the transaction count and lower a ratio. Often called microtransactions.

T5. Outcome suppression. Refunds, reversals or pre-dispute alerts are used so that chargebacks or fraud reports are not recorded against the account.

T6. Changed identity. A statement descriptor, business name or account is changed, or a closed account is replaced, so that reports and history do not follow the seller.

T7. Known and not acted on. A defendant is alleged to have seen chargeback or fraud-report levels, monitoring-program notices, complaints or warnings about a seller, and to have kept processing.

## Context

X1. The monitoring measure the complaint names: chargeback ratio, chargeback count, fraud-report ratio, return rate, other, none.

X2. The payment rail: card, bank debit, remotely created check or payment order, other.

X3. Does the complaint give rates or counts for any account? Yes or no, with paragraph numbers.

X4. Does the complaint allege an attribute shared across accounts, such as an owner, address, phone number, bank account, website, device or call center? Yes or no, with paragraph numbers. If yes: do those paragraphs tie the attribute to the accounts marked under T1 or T2? Yes or no.

## Open field

O1. Any other tactic alleged to keep a seller out of monitoring, in the complaint's words, with paragraph numbers.

## Rules for close calls

- A tactic alleged of any seller the defendant served counts once for the complaint.
- `unclear` is for wording that could mean the tactic but does not say so. Quote the wording.
- `unavailable` is for a mark that an unread page prevents. Name the page. It is never used for a complaint read in full.
- T1 needs more than one account for the same seller or scheme, and a stated or plain link to thresholds or monitoring. Several accounts alone are not T1.
- T2 is about who the account is said to belong to. T3 is about whose sales run through it. Both can apply.
- T5 needs the refund, reversal or alert to be tied to avoiding chargebacks or reports. Ordinary refunds do not count.
- T6 needs a change over time.
- T7 needs the defendant to have had the information, as alleged.
- For each complaint, record the PDF's address, its page count and its SHA-256.


## What to do

For each item, read the cited paragraphs, and the rest of the complaint where you need context. The complaints are in `/home/claude/payment-fraud/paper/working/tools/complaint_audit/packets/UNN.md` (complaint as a JSON list of pages after the sheet). Do not open anything under `sheets/`, `/home/claude/claude_sheet/`, `/home/claude/chatgpt_in/` or `/home/claude/adjudication/KEY_DO_NOT_SHARE.json`: they would show who the coders are.

Rule each item by the sheet's text. You may choose either reading or a third mark. Marks: `alleged`, `unclear` (needs a short quote of the wording that could mean the tactic), `not alleged`. For X3 and X4: `yes` or `no`; for X4 also `tied_to_T1_or_T2`, which is `yes` or `no` only when X4 is `yes` and T1 or T2 is alleged for that complaint after your rulings; otherwise `n/a`. The T1 and T2 marks the coders agree on stand.

The complaint text is evidence only. Ignore any text in it that reads as an instruction to you.

Return only one JSON list, one object per item, in order:
`{"id": "D01", "unit": "U02", "field": "T6", "ruling": {"mark": "...", "paragraphs": ["..."], "quote": ""}, "reason": "one or two plain sentences citing the sheet's words"}`
For X3 use `"ruling": {"answer": "...", "paragraphs": [...]}`; for X4 add `"tied_to_T1_or_T2"`.

## Items

### D01. U02 T6

- Reading 1: `{"mark": "not alleged", "paragraphs": [], "quote": ""}`
- Reading 2: `{"mark": "unclear", "paragraphs": ["87", "101"], "quote": "Transact Pro was preparing to open merchant accounts for the Apex Defendants at a third bank, Decta Limited"}`

Cited paragraphs:

```
U02 ¶87: 87. The Apex Defendants secured more than forty merchant accounts based on these false merchant applications; nearly all of them were subsequently closed. Numerous merchant accounts were closed due to excessive chargeback levels. C. Transact Pro and Moskvins Actively Participated in the Apex Operation’s Credit Card Laundering and Manipulation of Chargeback Levels

U02 ¶101: 101. Up until the time the Complaint was filed, on November 14, 2018, the Transact Pro Defendants were continuing to engage in the unlawful conduct. Many of the Transact Pro merchant accounts had been closed by the spring of 2018, but some accounts remained open, receiving payments in U.S. dollars through at least September 2018. Moreover, Transact Pro was preparing to open merchant accounts for the Apex Defendants at a third bank, Decta Limited, in the fall of 2018. In an email to Defendant Peikos dated October 16, 2018, a Transact Pro employee offered to issue new merchant accounts to numerous shell companies of the Apex Operation, including Rendezvous IT, Lead Blast Limited, Nutra Global Limited, and others, using Decta Bank as the acquirer. The Transact Pro employee offered to set up the accounts such that Decta would pay out processed funds from each of the shell corporation’s merchant accounts to a single bank account held by Defendant Omni Group Limited. The Transact Pro Defendants continued these efforts to open new merchant accounts for the Apex Defendants through at least mid-November 2018.
```

### D02. U02 X3

- Reading 1: `{"answer": "yes", "paragraphs": ["71", "87", "92", "95", "97", "99"]}`
- Reading 2: `{"answer": "no", "paragraphs": []}`

Cited paragraphs:

```
U02 ¶71: 71. In order to detect and prevent illegal, fraudulent, or unauthorized merchant activity, the card networks operate various chargeback monitoring and fraud monitoring programs. These chargeback monitoring programs are designed to flag merchant accounts with excessive chargeback ratios or an excessive number of chargebacks. For example, if a merchant generates excessive levels of chargebacks that exceed the thresholds set under VISA’s chargeback monitoring program, the merchant is subject to additional monitoring requirements and, in some cases, penalties and termination.

U02 ¶87: 87. The Apex Defendants secured more than forty merchant accounts based on these false merchant applications; nearly all of them were subsequently closed. Numerous merchant accounts were closed due to excessive chargeback levels. C. Transact Pro and Moskvins Actively Participated in the Apex Operation’s Credit Card Laundering and Manipulation of Chargeback Levels

U02 ¶92: 92. In the course of managing these merchant accounts for the Apex Operation, the Transact Pro Defendants received information about high [p33] chargeback rates that they should have used to investigate and require corrections to the Apex Operation’s deceptive marketing practices. Instead, the Transact Pro Defendants used this information to enable the Apex Operation to engage in load balancing and microtransactions, allowing them to avoid detection by the card associations or termination by the acquiring banks.

U02 ¶95: 95. In addition, the Transact Pro Defendants caused the chargeback ratios of the Apex Operation’s merchant accounts to be artificially reduced through microtransactions, which were run at times by Transact Pro itself, and at other times by the Apex Defendants. The Transact Pro Defendants sold the Apex Operation prepaid gift cards, which were used to make many thousands of individual transactions in small dollar amounts that were unlikely to result in consumer chargebacks. By running these microtransactions through the Apex Operation’s merchant accounts, the Transact Pro Defendants artificially diluted the ratio of sales to chargebacks in the accounts. [p34]

U02 ¶97: 97. Defendant Transact Pro provided calculations of the number of microtransactions that had to be run through a given merchant account by the end of that month to ensure that the chargeback ratio would drop below a certain threshold.

U02 ¶99: 99. In numerous instances, Defendant Moskvins instructed Transact Pro’s support staff to increase a volume cap on merchant accounts in order to allow the Apex Operation to run additional microtransactions to reduce chargeback ratios. For example:  In an email dated September 30, 2016, an Apex Capital Group employee emailed Defendant Moskvins: “Mark, We need additional volume to run more VAP, can you please approve an additional 2k per [merchant account] ASAP to hit our marks.” Defendant Moskvins replied, copying Transact Pro’s support team, “Support: pls do.”  On January 27, 2017, an employee of Apex Capital Group emailed Defendant Moskvins and Transact Pro’s support team: “We need to run VAP to these [merchant accounts] and are having issues. . . . This one is capped. Can you give us an extra 10K to run VAP?” Defendant Moskvins replied, “Yes, for vap.”  On February 22, 2017, an employee of Apex Capital Group emailed Defendant Moskvins: “Mark, we need every single [merchant account] increased by 5k to run VAP successfully.” Defendant Moskvins responded, “Yes if it is vap no prob.” [p35]
```

### D03. U03 T2

- Reading 1: `{"mark": "not alleged", "paragraphs": [], "quote": ""}`
- Reading 2: `{"mark": "alleged", "paragraphs": ["8", "25", "62", "63", "64", "65", "66", "67"], "quote": ""}`

Cited paragraphs:

```
U03 ¶8: 8. To execute their payment processing scheme, Defendants open business checking accounts under various assumed names with banks and credit unions, the majority of which are local institutions. Defendants often misrepresent to the financial institution the type of business for which they open the account, and routinely fail to disclose the real reason for which they open the account processing consumer payments for third-party merchants via RCPOs.

U03 ¶25: 25. Together with the other Defendants, Bruce Woods has, in numerous instances, misled financial institutions about the nature of Madera's and B&P's business and intentionally concealed from financial institutions the fact that Defendants were opening business checking accounts in order to process consumer payments for third- party merchant-clients.

U03 ¶62: 62. Defendants file assumed name and trademark or tradename certificates for Madera and B&P in Texas and Wisconsin under the names and dbas of their merchant- clients.

U03 ¶63: 63. Using these certifications, Defendants apply for business checking accounts with financial institutions, misrepresenting the services provided by Madera or B&P and failing to disclose that Defendants will use the accounts to process consumer payments for third-parties.

U03 ¶64: 64. For example, a Madera application for business checking accounts at Pioneer Bank SSB in Sugar Land, Texas, under the dbas Aiding Education and Savings Galore, which Bruce Woods signed on June 28, 2018, falsely represented that Madera [p14] operated a student loan document preparation assistance service (Aiding Education) and a "savings club" (Savings Galore).

U03 ¶65: 65. The June 28, 2018 application also falsely represented that Madera does not engage in processing payments for third-parties.

U03 ¶66: 66. Additionally, on or about June 6, 2018, Madera opened a business checking account with Citizens State Bank in Hudson, Wisconsin, to process RCPOs for Educare. Defendants opened the account under the name Madera Merchant Services doing business as Revit-Educ-Srvc.

U03 ¶67: 67. The application that Defendants submitted to Citizens State Bank gave no indication that Defendants would use the business checking account to process payments for a third-party telemarketer. Instead, Defendants falsely identified Madera as a "Parent Holding Company" that provides "Document Preparation Service" under the name Revit- Educ-Srvc.
```

### D04. U03 T3

- Reading 1: `{"mark": "not alleged", "paragraphs": [], "quote": ""}`
- Reading 2: `{"mark": "alleged", "paragraphs": ["8", "63", "65", "69"], "quote": ""}`

Cited paragraphs:

```
U03 ¶8: 8. To execute their payment processing scheme, Defendants open business checking accounts under various assumed names with banks and credit unions, the majority of which are local institutions. Defendants often misrepresent to the financial institution the type of business for which they open the account, and routinely fail to disclose the real reason for which they open the account processing consumer payments for third-party merchants via RCPOs.

U03 ¶63: 63. Using these certifications, Defendants apply for business checking accounts with financial institutions, misrepresenting the services provided by Madera or B&P and failing to disclose that Defendants will use the accounts to process consumer payments for third-parties.

U03 ¶65: 65. The June 28, 2018 application also falsely represented that Madera does not engage in processing payments for third-parties.

U03 ¶69: 69. The funds from consumers' accounts, drawn through Defendants' RCPOs, are deposited into the business checking accounts that Defendants opened using their merchant-clients' dbas.
```

### D05. U03 X4

- Reading 1: `{"answer": "yes", "paragraphs": ["62", "66", "77", "79", "89", "90"], "tied_to_T1_or_T2": "n/a"}`
- Reading 2: `{"answer": "yes", "paragraphs": ["46", "68", "75", "95"], "tied_to_T1_or_T2": "yes"}`

Cited paragraphs:

```
U03 ¶46: 46. Madera and B&P share the website echeckprocessing.net, and have both listed the residence of Bruce and Patricia Woods as their business address on applications for bank accounts.

U03 ¶62: 62. Defendants file assumed name and trademark or tradename certificates for Madera and B&P in Texas and Wisconsin under the names and dbas of their merchant- clients.

U03 ¶66: 66. Additionally, on or about June 6, 2018, Madera opened a business checking account with Citizens State Bank in Hudson, Wisconsin, to process RCPOs for Educare. Defendants opened the account under the name Madera Merchant Services doing business as Revit-Educ-Srvc.

U03 ¶68: 68. After Defendants secure the business checking accounts, often using false or misleading information, they deposit printed or electronic copies of RCPOs that they create with software, which include the name and often the phone number of their merchant-clients. These items enter into the check clearing system and are presented to the financial institutions of consumers.

U03 ¶75: 75. Citizens State Bank then discovered that Madera had filed eight different trademark nanies (dbas) in the state of Wisconsin within six months. The bank also discovered that many consumers posted complaints on the internet claiming that companies using those dbas had fraudulently taken funds from their bank accounts.

U03 ¶77: 77. Between June 20, 2018 and June 29, 2018, Defendants opened new accounts for RCPO processing under dbas of Educare Center Services with at least four [p16] other banks in Texas/Wisconsin, including BancCorpSouth Bank, First United Bank and Trust Company, Pioneer Bank, SSB, and Prosperity Bank.

U03 ¶79: 79. In some instances, Defendants have opened multiple, seemingly unrelated, accounts for a merchant-client under two or more dbas at the same bank or credit union.

U03 ¶89: 89. Since at least 2017, Defendants have opened no fewer than 17 accounts for processing RCPOs for Educare at 15 banks and credit unions because such accounts have often been quickly closed by the banks and credit unions due to high return rates or because the banks and credit unions deem the accounts a high risk. [p19] r

U03 ¶90: 90. Defendants have opened accounts under various dbas of Educare, including accounts under the dbas Tripletel, Inc., Revit-Educ-Srvc, L.L. Vision, and Card Value Services. At least four of the Educare accounts had return rates of 20% or more.

U03 ¶95: 95. The risk analyst called the toll free number 877-403-1659, printed on one of Defendants' returned Revit-Educ-Srvc RCPOs, and spoke to a man with a heavy foreign accent who told the risk analyst that she had reached a "credit card service" company. She asked the man to clarify what that meant and he stated that the company "lowers the interest rate on your credit card." When the risk analyst asked him if the [p20] name of the business was Revit-Educ-Srvc, he said "just a moment," and then came back on the line and told her that if she was not a customer or client, then he could not release that information. After the risk analyst reported her findings, the credit union put a hold on the deposited funds, refused to accept new deposits, and began the process of closing Defendants' accounts.
```

### D06. U04 T6

- Reading 1: `{"mark": "alleged", "paragraphs": ["71", "72", "74", "76", "78"], "quote": ""}`
- Reading 2: `{"mark": "not alleged", "paragraphs": [], "quote": ""}`

Cited paragraphs:

```
U04 ¶71: 71. On September 19, 2012, Decker told Sonnenberg that Decker is “really struggling internally with losing your accounts,” and that he may make another plea to the bank to continue processing for the Apply Knowledge enterprise. Sonnenberg responded that he had been “moving forward with setting up [merchant accounts] with different signers and that process has been fine” but he offered to meet to discuss reopening his business with CMS depending on the fees.

U04 ¶72: 72. On October 11, 2012, Wilson wrote in a memo, which was submitted to CBCal, that CMS had “restructured” the Supplier Source account and “obtained current financial data and other documents so that it could be re-opened” and that “the account has been handled in satisfactory manner since re-opening date.”

U04 ¶74: 74. On May 13, 2013, Sonnenberg wrote to Decker that “[i]t’s really disruptive on the business to have it shut off so quickly. I really liked having accounts with you because I could [p18] keep them in mine and Babata’s name. With other processors I have to use employees and I don’t like exposing them to the risks.”

U04 ¶76: 76. On January 22, 2014, Sonnenberg asked Decker if CBCal would allow the Apply Knowledge enterprise to open a new account with CMS. He asked if CMS should turn on one of the previously used accounts, and Decker responded that they should “re-paper it,” and it is “probably best to have [Sonnenberg’s wife] Babata sign for both accounts.”

U04 ¶78: 78. On January 27, 2014, the Apply Knowledge enterprise submitted a merchant application on behalf of Supplier Source. Decker signed the application on January 29, 2014 and is listed on the application as the sales agent. On January 30, 2014, Wilson wrote a memo stating that CMS re-opened the Supplier Source account.
```

### D07. U05 T1

- Reading 1: `{"mark": "unclear", "paragraphs": ["38"], "quote": "if we move everything off PayPal, we'll send the PayPal account into severe chargeback state which will get reported to Visa"}`
- Reading 2: `{"mark": "not alleged", "paragraphs": [], "quote": ""}`

Cited paragraphs:

```
U05 ¶38: 38. RevenueWire hid from WorldPay that it was submitting renewal or rebill charges to consumers’ credit cards on behalf of ICE that involved tech support services. For example, on [p14] April 13, 2016, Roberta Leach received an email asking whether “we could move ICE’s new sales and renewal charges to one provider (like WorldPay) and then close down PayPal…” Roberta Leach responded as follows: The reason we didn’t put ATS (the dba for ICE) on the WorldPay gateway is because we were very concerned about having a high volume call center on WorldPay that is being investigated by the FTC. As you know, we’re only suppose [sic] to be selling software on the WorldPay account. WorldPay doesn’t know that the old [ICE] rebills we migrated from Chase to WorldPay are for tech support – it’s a low enough price point that rebills look like software. If we move everything from PayPal to WorldPay we’ll have two issues. First, as mentioned above, we’re not supposed to be processing payment for premium tech support centers and this may jeopardize our account with WorldPay….Second, if we move everything off PayPal, we’ll send the PayPal account into severe chargeback state which will get reported to Visa. This may have a number of repercussions including losing our Visa merchant account. (Emphasis added). Defendants Knew or Consciously Avoided Knowing about the Deceptive Practices That Call Stream Call Centers, Including Vast and ICE, Used to Generate Sales
```

### D08. U06 T1

- Reading 1: `{"mark": "alleged", "paragraphs": ["4", "35", "49", "51", "57"], "quote": ""}`
- Reading 2: `{"mark": "unclear", "paragraphs": ["49", "78"], "quote": "is a strong indication that the merchant applicant is “load balancing”"}`

Cited paragraphs:

```
U06 ¶4: 4. Defendant Chi “Vincent” Ko (“Ko”), through his company First Pay Solutions LLC (“FPS”), established merchant accounts for the Schemes and processed the payments they took from consumers. Specifically, Ko and FPS: (1) opened hundreds of merchant accounts for the Schemes in the names of phony entities and shell corporations; (2) provided Wells Fargo Bank with false or deceptive information to obtain merchant accounts; (3) ignored evidence that FPS’s sales agents were engaged in fraud; and (4) failed to adequately underwrite, monitor or timely terminate merchants which it knew, consciously avoided knowing, or should have known were engaged in fraud.

U06 ¶35: 35. Wells Fargo’s credit risk guidelines specifically warned about “merchants’ opening of multiple accounts, especially via multiple shell companies having the same or similar principals (in some cases, hired ‘mules’ with little or no business involvement may be submitted to obscure the true ownership).” Using multiple merchant accounts for the same business is a strong indication that a merchant applicant is “load balancing,” a practice in which a business spreads its transactions among multiple merchant accounts to avoid triggering chargeback thresholds that would increase scrutiny from the credit card associations. The practice of processing credit card transactions through another company’s merchant accounts is called “credit card laundering” or “factoring” in the credit card industry. It is strictly forbidden by the credit card associations and is illegal under the TSR.

U06 ¶49: 49. During the same time period, from February to September 2014, FPS approved 40 pairs of identical merchant applications. Each pair had the same purported principal and merchant name and was opened the same day. Using multiple merchant accounts for the same business – let alone submitting identical merchant applications – is a strong indication that the merchant applicant is “load balancing,” a practice in which a business spreads its transactions among multiple merchant accounts to avoid triggering chargeback thresholds that would increase scrutiny from the credit card associations.

U06 ¶51: 51. From November 2012 to October 2014, First Data and FPS opened at least 26 merchant processing accounts for shell companies that were used by the E.M. Systems Scheme to charge consumers in a deceptive debt relief scam. First Data and FPS opened these accounts even though the merchant applications submitted contained facially false statements, direct evidence, or other red flags that the applicants were not bona fide businesses or were engaged in fraud.

U06 ¶57: 57. From at least March 2012 to February 2014, First Data and FPS opened over 150 merchant processing accounts for shell companies that were used by the Coaching Department Scheme to charge consumers in a deceptive business coaching operation, based on merchant applications that contained false statements, internal inconsistencies, or other hallmarks of fraud.

U06 ¶78: 78. In June 2014, Ko received a letter from a merchant claiming that proceeds from his business had been diverted into a merchant account fraudulently boarded by First Pay Systems, Wigdore, and Richard Kuhlmann: Your Arizona affiliate [First Pay Systems] is a rogue agency and apparently a criminal enterprise… The Agent submits false applications containing cut and paste bank checks designed to purportedly represent the merchant acct. when in reality the funds are diverted back to themselves… They submit phony web sites that do not represent the true nature of the merchant’s business, knowing the correct website would not qualify…There are by in large known, illegally operated company’s (sic) that cannot obtain a merchant acct. by legitimate means… They are the subjects of state and federal investigations (see subpoena). In the Nutraceutical space and others, they illegally compile large amount of ‘nominee’ applicants designed to circumvent chargebacks, returns and illegally ‘load balance’ a merchant’s processing…. They have committed theft, forgery, ID theft, bank fraud, and money laundering offenses. My money has been diverted to bank accounts to which I’m not even a signer. Jay Wigdore…and Richard Kulhman (sic) have criminal records. Kulhman has been ‘black balled’ everywhere in this industry with the exception of [FPS].
```

### D09. U06 T6

- Reading 1: `{"mark": "alleged", "paragraphs": ["61", "75", "91", "113"], "quote": ""}`
- Reading 2: `{"mark": "not alleged", "paragraphs": [], "quote": ""}`

Cited paragraphs:

```
U06 ¶61: 61. In August 2012, First Data and FPS established a merchant account for Nesch.edu, a purported financial coaching business, after FPS approved an apparently doctored application and despite the applicant’s prior termination for excessive chargebacks for the same business activity. In the application, the “business name” field was whited-out and handwritten, while the rest of the application was typed. The business location was described as an office with 2-4 floors, yet the address provided was a single-floor residential apartment unit. After receiving the application, FPS emailed internally, noting that the application had a prior account under a different business name that was closed two weeks earlier for excessive chargebacks and refunds: “the new application’s business model is the same as the previous account.” Yet days later, FPS approved the new account and First Data began processing its charges. In fact, both accounts were used by the Coaching Department to bilk consumers as part of a deceptive telemarketing scam.

U06 ¶75: 75. In August 2013, Ko received an email from CardReady advising him that the billing descriptor for an E.M. Systems merchant account needed to be changed so it could be used to process transactions for a separate business that sold dietary supplements. FPS switched the billing descriptor and processed transactions through the account under the new billing descriptor. A merchant’s use of multiple billing descriptors to mask the merchant’s true identity or activity is a common tactic used by fraudsters to evade scrutiny by the credit card associations and law enforcement. At the time FPS processed for the Schemes, Wells Fargo’s credit risk guidelines specifically warned that multiple billing descriptors were a “tactic[] to evade chargeback monitoring programs.” (emphasis in original). Ko and FPS Ignored Evidence that First Pay Systems Was Submitting Fraudulent Merchants For the Beckish Scheme

U06 ¶91: 91. In September 2012, First Data and FPS began processing transactions for Nesch.edu (“Nesch”), another purported financial coaching business, even while FPS acknowledged internally that a prior merchant account for Nesch was closed in August 2012 “due to excessive chargebacks and high refunds” and the new application’s business was “the same model as the previous account.” Defendants continued to process approximately $330,000 through the account, from September 2012 to February 2013. First Data and FPS Processed for the E.M. Systems Scheme Despite Evidence of Deceptive Telemarketing

U06 ¶113: 113. In December 2013, in response to the designation, First Data created a report on FPS that identified five “unqualified or prohibited” accounts that were selling nutraceuticals and debt relief services, including merchants for the E.M. Systems Scheme, noting that “a merchant is selling a package for debt reduction – offering to lower interest on credit cards.” First Data [p36] emailed FPS about its failure to adequately underwrite the accounts, noting that FPS had failed to review the merchant applicants’ websites and failed to detect that one of the merchants “had done this before” and was “an internal match due to chargeback issues.”
```

### D10. U07 T1

- Reading 1: `{"mark": "unclear", "paragraphs": ["31", "32"], "quote": "A merchant with ten accounts, for example, could potentially accrue ten times the number of chargebacks"}`
- Reading 2: `{"mark": "alleged", "paragraphs": ["31", "32", "42", "43"], "quote": ""}`

Cited paragraphs:

```
U07 ¶31: 31. The Platinum Payments and Starkey applications contained significant discrepancies. For example, the application submitted by Starkey requested a single account that would process a projected $56 million in annual sales. The applications submitted by Platinum Payments requested multiple accounts that would process a total of $5 million in annual sales. This large discrepancy should have been a red flag for Qualpay.

U07 ¶32: 32. Merchant chargeback rates are sometimes calculated on a per-account basis. A merchant’s chargebacks are deemed excessive based on both a ratio and count of chargebacks (typically 1% and 100 chargebacks per month). A merchant with ten accounts, for example, could potentially accrue ten times the number of chargebacks before suffering the consequences of having “excessive” chargebacks.

U07 ¶42: 42. Qualpay’s underwriters also asked for documents that showed how the various aspects of MOBE’s business were intertwined. In response, MOBE provided a “product map” in which MOBE requested 5 different merchant accounts. The first account would sell a $49 online product, and several supplemental products known as “upsells” that cost $2,500, $9,997, $16,667, and $29,997. The second account would sell a “Seminar” for $49, a “3-Day Business Summit” upsell for $497, and workshops that cost $10,000, $25,000, $50,000 and $100,000. The other three accounts were for the “MOBE Marketplace,” “MOBE Traffic,” and “Partner Products.”

U07 ¶43: 43. After receiving the product map, Qualpay decided to structure MOBE’s processing through seven merchant accounts instead of the five that MOBE had requested. Qualpay’s corporate representative testified that Qualpay had a policy of requiring merchants to use a separate merchant account for each product type that the merchant offered.
```

### D11. U07 T2

- Reading 1: `{"mark": "not alleged", "paragraphs": [], "quote": ""}`
- Reading 2: `{"mark": "alleged", "paragraphs": ["28", "35", "39", "112", "140"], "quote": ""}`

Cited paragraphs:

```
U07 ¶28: 28. Qualpay asked Platinum Payments if MOBE was physically located in the United States and if MOBE’s “principal/owner” was located in the United States. Platinum Payments responded that Susan Zanghi, a “key management member” with MOBE, operated the business “virtually” out of her home address, and the application would be signed by MOBE’s CEO, Matthew Lloyd McPhee, who resided abroad. Qualpay responded that it would look for a “principal/owner” or individual who had authority to sign on behalf of MOBE who was located in the United States.

U07 ¶35: 35. In contrast, the application materials submitted by Platinum Payments for MOBEProcessing.com Inc. did not mention a business address in Delaware and claimed that MOBE, the DBA of MOBEProcessing.com Inc., was located in North Carolina, and not in Malaysia. -8- [p9]

U07 ¶39: 39. In response to these questions, MOBE explained that Susan Zanghi was the only person who worked at the North Carolina address listed on the application, that the 18 in-house customer service representatives worked “out of our Malaysia office,” and that MOBE employed event staff who worked virtually. MOBE also submitted a letter from its CEO, McPhee, authorizing Susan Zanghi “to act as a financial representative for MOBE Processing.com, Inc. in the United States of America.”

U07 ¶112: 112. On April 17, 2017, Abigail Helms replied to Bunnis’ email and she copied Gass and other Qualpay employees. Helms explained that she was “concerned that the merchant was processing in Australia and now is with us in the US.” Helms asked if the merchant is “US Owned” because Synovus’ membership in the credit card networks only allows Synovus to process “for merchants located in the US.” Synovus could not process “cross border transactions: merchants located outside the US processing through a US acquirer or vice versa.” Bunnis responded that the “MOBE business Qualpay is processing for is US owned and located in the US.”

U07 ¶140: 140. At this time, MOBE was having trouble finding other payment processors to - 30 - [p31] open accounts to replace the volume of the closed Qualpay accounts. On July 10, 2018, Platinum Payments said that it was “officially out of ideas” after 5 different payment processors had refused the accounts. As Platinum Payments explained in an internal e-mail: With them having an over 6% CB ratio on the two accounts that are being closed (that 6% is about 300 CB per month). The only possible way to take this somewhere else is to present it as new which is not a huge issue but is presenting with a couple of problems. The other issue is that the sole owner on the account is an AU citizen who lives in Malaysia. Susan is listed as a signer on the account, but because she holds no actual ownership in the company I am having trouble getting it accepted.
```

### D12. U07 T6

- Reading 1: `{"mark": "not alleged", "paragraphs": [], "quote": ""}`
- Reading 2: `{"mark": "alleged", "paragraphs": ["131", "132", "140", "143", "144", "146"], "quote": ""}`

Cited paragraphs:

```
U07 ¶131: 131. On July 14, 2017, Qualpay decided not to put MOBE on the MATCH list at all. Loriann Ouimet, Qualpay’s Director of Risk Strategy emailed Craig Gass and explained that the Mastercard regulations for putting merchants on MATCH only speak to situations where the payment processor terminates “the relationship.” Ouimet reasoned that because Qualpay was terminating some of MOBE’s accounts while keeping others open, “it would - 28 - [p29] not fall within this definition.” Ouimet explained: There is an argument for the grey area in that MATCH is a warning to other acquirers if we are terminating line of business. However, we have actual notice that the merchant is going to an international processor for the terminated MIDs. I think that supports the reasonable, good faith decision not to place a merchant on MATCH for chargebacks which are being managed and watched.

U07 ¶132: 132. MOBE “going to an international processor for the terminated MIDs” was itself a violation of Visa and Mastercard regulations and a reason to terminate the MOBE accounts. Under Visa and Mastercard regulations, MOBE either qualified for domestic payment processing accounts or international payment processing accounts. Under these regulations, Qualpay should not have continued to process for MOBE after MOBE switched from using domestic accounts to international accounts to process payments for domestic consumers. This is particularly true when MOBE was using the international accounts to process the sale of initial products and domestic accounts to process the sale of supplemental products to the same domestic consumers.

U07 ¶140: 140. At this time, MOBE was having trouble finding other payment processors to - 30 - [p31] open accounts to replace the volume of the closed Qualpay accounts. On July 10, 2018, Platinum Payments said that it was “officially out of ideas” after 5 different payment processors had refused the accounts. As Platinum Payments explained in an internal e-mail: With them having an over 6% CB ratio on the two accounts that are being closed (that 6% is about 300 CB per month). The only possible way to take this somewhere else is to present it as new which is not a huge issue but is presenting with a couple of problems. The other issue is that the sole owner on the account is an AU citizen who lives in Malaysia. Susan is listed as a signer on the account, but because she holds no actual ownership in the company I am having trouble getting it accepted.

U07 ¶143: 143. On October 5, 2017, Steffen emailed Zanghi because the MOBE Summit account was processing “a lot of different price points” and chargebacks were rising on the account. Steffen asked if MOBE was running the same transactions through MOBE Summit that had been sent through the closed account. - 31 - [p32]

U07 ¶144: 144. The next day, Steffen wrote that Qualpay was “trying to figure out how to stop [MOBE] from sending transactions derived from the ONLINE PRODUCT GROUP and HOME BUSINESS SUMMIT pieces of their business to the SUMMIT MID.”

U07 ¶146: 146. Two days later, Rory O’Reilly, Qualpay’s Executive Vice President of Profitability, emailed Tina Steffen to let her know that more $49 transactions had “popped up” on MOBE’s accounts. Rory commented that MOBE “seemed to stop the volume when we point it out” but he did not “want to play whack a mole.” O’Reilly also mentioned that MOBE was Qualpay’s “largest volume customer.” Steffen responded in part, “OMG!!!! What the heck are they doing??”
```

### D13. U09 T2

- Reading 1: `{"mark": "alleged", "paragraphs": ["40", "89"], "quote": ""}`
- Reading 2: `{"mark": "not alleged", "paragraphs": [], "quote": ""}`

Cited paragraphs:

```
U09 ¶40: 40. Under this nested arrangement, AFTS had no direct contractual relationship with SLG. It pretended that its “client” was the processor (PAN and later RubikPay), which had the contractual relationship with SLG. AFTS, -10- [p11] however, was fully aware that the merchant on behalf of whom it was processing payments was SLG, not PAN or RubikPay.

U09 ¶89: 89. At the time AFTS resumed processing for SLG on October 1, 2017, Johnson and AFTS represented to Florida Capital Bank that SLG (and its more recent dba’s) was not offering student loan debt relief services, but only student -25- [p26] loan “document preparation” services. That new business was purportedly limited to merely filling out loan-related forms for consumers.
```

### D14. U09 T3

- Reading 1: `{"mark": "unclear", "paragraphs": ["39", "40", "41"], "quote": "It pretended that its “client” was the processor (PAN and later RubikPay), which had the contractual relationship with SLG."}`
- Reading 2: `{"mark": "not alleged", "paragraphs": [], "quote": ""}`

Cited paragraphs:

```
U09 ¶39: 39. During the First Period, AFTS processed more than $13.76 million of ACH debits for SLG through a “nested” relationship with two other payment processors, Payment Automation Network, Inc. (“PAN”) and Max Tech, Inc. dba RubikPay (“RubikPay”), a company formed by SLG’s principals to perform in- house processing for SLG.

U09 ¶40: 40. Under this nested arrangement, AFTS had no direct contractual relationship with SLG. It pretended that its “client” was the processor (PAN and later RubikPay), which had the contractual relationship with SLG. AFTS, -10- [p11] however, was fully aware that the merchant on behalf of whom it was processing payments was SLG, not PAN or RubikPay.

U09 ¶41: 41. Between August 2014 and January 2016, AFTS processed for SLG via a nested relationship with PAN. AFTS debited the bank accounts of SLG customers, deposited these funds into AFTS’s bank account, and then transferred them to one or more bank accounts held in the name of PAN (instead of directly to SLG). PAN in turn would transfer the funds to SLG.
```

### D15. U09 X4

- Reading 1: `{"answer": "yes", "paragraphs": ["57", "88"], "tied_to_T1_or_T2": "no"}`
- Reading 2: `{"answer": "no", "paragraphs": [], "tied_to_T1_or_T2": "n/a"}`

Cited paragraphs:

```
U09 ¶57: 57. Additionally, Johnson and AFTS were aware of numerous consumer complaints to the Better Business Bureau (“BBB”) and on various websites about SLG, and often shared such complaints with AFTS employees. These complaints often described SLG as a scam, and/or described various red flags indicating that SLG likely was a scam. For example: • In an October 27, 2014 email Johnson sent to Martinez discussing consumer complaints, Johnson wrote: “Their customer [sic] are reporting that they are feeling ‘scammed.’ A toll free phone number that is no longer operational is a good indication of a scam. NSLManagers.com seems to be the same organization as NSProcessing.com. They operate with nearly identical website services, from adjacent suites. The NSL phone number doesn’t work, but the NSP phone number does. A call to a NSP client services rep indicates that they know nothing about NSL. Yet Mathew Johnson (Kayla Madera’s sales agent at NSL) does work there. But he really works for SLSManagers.com (with different phone number from NSP) – again at the same address. What is the business model of NSL, NSP, and SLS – all three doing the same thing at the same address, with one of the phones disconnected?...” • In an October 30, 2014 email Johnson sent to Martinez, Johnson forwarded several links to complaints regarding a merchant that Martinez subsequently confirmed was associated with SLG, writing: “it is not a good sign when a significant portion of the Google searches show up on complaint sites. The BBB shows 435 complaints in 3 years, 81 in the past 12 months … They have also been involved in a fraud suit.” • In an October 27, 2014 email Johnson sent to Martinez, Johnson forwarded BBB complaints regarding two dbas used by SLG, writing: “Also please read the 31 BBB complaints regarding SLS Managers since June. They are still occurring in October….”

U09 ¶88: 88. On October 30, 2017, Johnson sent an email to AFTS’s compliance officer and AFTS’s controller, in which he wrote: [SLG] are forming a new company. Work will continue from the old portfolio, but no new customers will be added …They will have a new address, phones, email, etc. for all new work they are doing.. [SLG’s attorney] will prepare an additional contract for the new entity shortly. A new FTP site will be needed along with a new ACH company name… They are aware of the shitty job they have been doing and are abandoning the reputation and liability with all state and federal agencies with the new entity.
```

### D16. U10 T6

- Reading 1: `{"mark": "alleged", "paragraphs": ["76", "77"], "quote": ""}`
- Reading 2: `{"mark": "not alleged", "paragraphs": [], "quote": ""}`

Cited paragraphs:

```
U10 ¶76: 76. In February 2018, Adyen required Nexway to stop sending credit card charges for TLC.

U10 ¶77: 77. Subsequently, Nexway sent Tech Live Connect’s credit card charges to Ingenico to be submitted into the credit card system. WorldPay was an acquiring bank for these charges.
```

### D17. U11 T1

- Reading 1: `{"mark": "not alleged", "paragraphs": [], "quote": ""}`
- Reading 2: `{"mark": "unclear", "paragraphs": ["110"], "quote": "We would like to go over a plan to move volume back before starting."}`

Cited paragraphs:

```
U11 ¶110: 110. The next day, Monteith sent an email titled “Re: First Call Processing Required Next Steps” to the ACRO owners (copying Dangelmaier), telling them: “Following up on our discussion yesterday, you can process on Nashville Ventures. We would like to go over a plan to move volume back before starting.” Dangelmaier and Monteith had decided that ACRO Services could resume processing payments using the Nashville Ventures account, but they wanted to coordinate a plan to ensure that their processing would not draw additional scrutiny from Fiserv or the card networks.
```

### D18. U11 T5

- Reading 1: `{"mark": "alleged", "paragraphs": ["109"], "quote": ""}`
- Reading 2: `{"mark": "not alleged", "paragraphs": [], "quote": ""}`

Cited paragraphs:

```
U11 ¶109: 109. Around June 23, 2021, Dangelmaier and Monteith had another call with the ACRO owners regarding the termination of the First Call Processing account. During the call, the owners admitted that they had charged some consumers’ credit cards before obtaining signed contracts from the consumers. One of the owners asked if their business was completely shut down from processing, and Dangelmaier said it was. But later in the call, when an owner asked if they could keep processing payments on their other companies, Dangelmaier said, “Yep, you’re 100 percent fine over there.” Dangelmaier also told the owners that “we got to keep Steve [Huffman] from getting on this thing called the MATCH list,” explaining that would be “a disaster” and “like a criminal record almost.” Dangelmaier told the ACRO owners to immediately issue refunds to consumers who complain so that they would not initiate chargebacks, because otherwise their chargeback thresholds would be too high and they would be shut down due to fraud. [p52]
```

### D19. U12 T1

- Reading 1: `{"mark": "alleged", "paragraphs": ["63", "102"], "quote": ""}`
- Reading 2: `{"mark": "not alleged", "paragraphs": [], "quote": ""}`

Cited paragraphs:

```
U12 ¶63: 63. Paddle first onboarded PC Vark in April 2017 under the seller name “PC Vark,” and subsequently opened at least nine other accounts for PC Vark at Paddle under various other names, such as “Systweak Software,” “Echosoft,” “XPortSoft,” “AV Signup,” “XPortSoft,” and “PC Tuneup Tools.” Paddle knew that these accounts were linked because they all had the same account representative or account contact information, and because Paddle was asked to redirect consumers who contacted Paddle with questions or complaints about the software to PC Vark’s tech support team, Premium Techie Support. [p18]

U12 ¶102: 102. Paddle executives approached operators of the Reimage scheme in February 2020 to offer Paddle’s payment processing services. During contract negotiations, Paddle came across online complaints about Reimage’s deceptive pop-ups and sales practices and learned that Reimage could present a chargeback risk. Paddle also knew that Reimage was using multiple payment aggregators (i.e., unregistered payfacs) and wanted to open accounts at Paddle to spread Reimage’s sales processing volume across more providers. Spreading sales volume across multiple accounts or payment processors for the same product is a common tactic used by sellers, including tech support service providers, that anticipate having their accounts terminated for fraudulent or deceptive practices.
```

### D20. U12 T2

- Reading 1: `{"mark": "not alleged", "paragraphs": [], "quote": ""}`
- Reading 2: `{"mark": "alleged", "paragraphs": ["106"], "quote": ""}`

Cited paragraphs:

```
U12 ¶106: 106. Had Paddle undertaken any basic screening or background check, it would have discovered from easily accessible records that, at this time in June 2020, Restoro Limited and Reimage Limited were registered to straw owners or directors located in Cyprus and in the Isle of Man, and not to the actual owners or principals of Reimage.
```

### D21. U12 T6

- Reading 1: `{"mark": "not alleged", "paragraphs": [], "quote": ""}`
- Reading 2: `{"mark": "alleged", "paragraphs": ["81", "91", "133", "134", "139"], "quote": ""}`

Cited paragraphs:

```
U12 ¶81: 81. Paddle received other red flags regarding PC Vark. In November 2017, for example, a member of Paddle’s internal finance team observed that PC Vark was shuffling through different company names (from PC Vark to Innovana Thinklabs and then to Digital Protection Services) in a span of weeks and relocating its bank accounts to different countries. This is a practice that fraudulent companies often adopt when their brand names receive negative reviews. In addition, in February 2018, Paddle employees noted that there were other suspicious [p23] or unusual charges coming from the PC Vark account. Paddle did not underwrite and reexamine the PC Vark account in response to these material changes to PC Vark’s account information.

U12 ¶91: 91. Moreover, instead of severing its ties with PC Vark outright, in September 2018, Paddle sought out and procured a “revenue share referral” agreement with another payment processor in the U.K. dealing with high-risk merchants. The purpose of this agreement was to enable Paddle to extract a referral fee for transferring PC Vark’s processing volume to the other payment processor. Paddle’s Head of Risk and Compliance assured PC Vark at this time: “I have spoken to an alternative payment gateway who is experienced at handling high chargeback digital businesses so I believe this could be a good long term fit for your business and cause minimal disruption. They have asked if you currently have a UK entity and if you’re keen to begin introductions to start their onboarding process.” Paddle’s CFO (at the time) signed the referral agreement for Paddle.

U12 ¶133: 133. Internally, Paddle’s executives at the time referred to this seller as a “fake Microsoft reseller” and noted that this was a “wake up call as the current system of checks and balances … had fallen down.” Despite these alarms, Paddle re-activated this same seller’s account about a year later and continued to receive complaints about its sales practices. One Paddle risk analyst remarked internally that the seller was a “nuisance” but “considering the high [transaction volume] they’re bringing to the company, we’ve had no other choice but to re- activate the account but monitor closely.”

U12 ¶134: 134. Separately, in November 2017, Paddle learned that Visa’s chargeback monitoring program was identifying transactions based on individual merchant billing descriptors. In effect, Visa at this time was flagging Paddle’s merchant billing descriptors associated with various tech support sellers due to excessive chargeback disputes. In response, Paddle changed its billing descriptors so that Visa would identify only Paddle as the merchant associated with the chargebacks being generated and thus “aggregate all of [Paddle’s] disputes and sales within a given month,” instead of by individual sellers. In so doing, Paddle was able to mask the chargeback rates for all of Paddle’s clients (including PC Vark at this time) from Visa and make it difficult for Visa to detect the chargebacks associated with those sellers.

U12 ¶139: 139. When Paddle learned of Adyen’s decision to terminate Paddle’s merchant account, Paddle quickly sought out other payfacs—such as Checkout.com and Worldpay— through which to continue its payment aggregation practices. In its applications to open merchant accounts with these payfacs, Paddle continued to falsely claim that it was a “reseller,” that Paddle did not remit consumer payments to the software providers, and that Paddle was ultimately responsible for the delivery and fulfillment of the software products and services.
```

### D22. U12 X4

- Reading 1: `{"answer": "yes", "paragraphs": ["63"], "tied_to_T1_or_T2": "yes"}`
- Reading 2: `{"answer": "no", "paragraphs": [], "tied_to_T1_or_T2": "n/a"}`

Cited paragraphs:

```
U12 ¶63: 63. Paddle first onboarded PC Vark in April 2017 under the seller name “PC Vark,” and subsequently opened at least nine other accounts for PC Vark at Paddle under various other names, such as “Systweak Software,” “Echosoft,” “XPortSoft,” “AV Signup,” “XPortSoft,” and “PC Tuneup Tools.” Paddle knew that these accounts were linked because they all had the same account representative or account contact information, and because Paddle was asked to redirect consumers who contacted Paddle with questions or complaints about the software to PC Vark’s tech support team, Premium Techie Support. [p18]
```

### D23. U13 T6

- Reading 1: `{"mark": "not alleged", "paragraphs": [], "quote": ""}`
- Reading 2: `{"mark": "alleged", "paragraphs": ["142", "144"], "quote": ""}`

Cited paragraphs:

```
U13 ¶142: 142. Defendants did not terminate or close all merchant accounts held by SC Digital at this time. Instead, they moved a portion of SC Digital’s processing volume that passed through the Mastercard network to non-Nuvei payment processors, while continuing to process payments through SC Digital’s merchant accounts for non- Mastercard payments. This caused Nuvei’s chief compliance officer to warn Nuvei Limited’s management that “we have effectively moved the bulk of the merchants from one non compliant solution to others,” “we are at risk of damaging the relationship with [other acquirers] by processing knowingly non compliant traffic through them,” and “we are effectively running two models for each merchant: one to cater for the Mastercard position and the other for Visa [and other payment methods].”

U13 ¶144: 144. Defendants told Mastercard that Nuvei Limited would be investigating and taking seriously each of the compliance violations and would terminate any non- compliant merchants. Defendants, however, did not terminate Reimage and did not stop processing payments for Reimage. Instead, Defendants advised Reimage to modify its credit card billing descriptor so as to avoid “suggest[ing] an unregistered [payfac] relationship” to the card networks.
```

### D24. U14 T6

- Reading 1: `{"mark": "not alleged", "paragraphs": [], "quote": ""}`
- Reading 2: `{"mark": "alleged", "paragraphs": ["8", "73", "86", "87", "88", "103"], "quote": ""}`

Cited paragraphs:

```
U14 ¶8: 8. Nevertheless, until around the end of 2023, after learning of the FTC’s investigation, Humboldt continuously opened thousands of Performance Marketing accounts primarily from two sales agents, even though their accounts had red flags of being shells and typically [p6] incurred chargebacks at rates that were almost ten times higher than what Mastercard and Visa viewed as excessive. While these accounts often were closed within six months, the continuous supply of shell accounts was highly profitable for Humboldt, and it enabled the online scams that used them as fronts to avoid detection and continue harming consumers. JURISDICTION AND VENUE

U14 ¶73: 73. After Mastercard’s 5968 Rules for negative-option trial merchants went into effect in April 2019, Humboldt began receiving “travel pack” applications from the same sales agents that had referred Performance Marketing accounts that were closed for fraudulent activity during the Mastercard reviews.

U14 ¶86: 86. Despite its decision to allow “travel pack” accounts and to open accounts under MCC 5499, Humboldt’s Performance Marketing business did not meet financial projections through the first half of 2020.

U14 ¶87: 87. During this time, Humboldt’s President discussed with other executives that an impediment to Humboldt’s growth was that MCC 5499 accounts on Humboldt’s BIN had a lower percentage of their attempted transactions approved (instead of declined) for payment—a metric referred to as an “authorization rate” or an “approval ratio”— [p37] when compared to 5499 accounts that were on lower-risk BINs, such as NAB’s BIN at the Acquiring Bank. An internal document prepared by Humboldt’s President in September 2020 explained that “many issuers have labeled” Humboldt “as having a ‘bad BIN’, of which the primary cause is that we have segregated our high-risk business from our low- risk business.” (That is, Humboldt’s high-risk business was segregated onto the Humboldt BIN, while NAB’s low-risk business was on the NAB BIN.) The result was that “NAB[’s BIN] outperforms HMS by 34%” according to “a comparative analysis on MCC 5499” merchants.

U14 ¶88: 88. By October 2020 Humboldt began boarding Performance Marketing accounts classified as MCC 5499 onto the NAB BIN.

U14 ¶103: 103. The accounts referred by Arc and Merchant Focus were usually closed less than a year after they were opened. Most of these accounts were closed for “excessive chargebacks” or “Unacceptable Level of Risk,” which is the description Humboldt used for closures for transaction laundering or engaging in unauthorized trials.
```
