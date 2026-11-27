# Screening

Decisions on the database runs. Per-record decisions are in `screening_<run>.csv`.

## Runs

Each run used its string from STRINGS.md unchanged.

| Run | Date (UTC) | Hits | Exported | Abstracts read | Critical |
|---|---|---|---|---|---|
| Q1-SC | 2026-11-23 | 400 | 400 | 23 | 0 |
| Q1-WS | 2026-11-23 | 120 | 120 | 0 | 0 |
| Q1-IE | 2026-11-23 | 52 | 52 | 2 | 0 |
| Q1-AC | 2026-11-23 | 10 | 10 | 1 | 0 |
| Q2-SC | 2026-11-23 | 179 | 179 | 22 | 0 |
| Q3-SC | 2026-11-23 | 164 | 164 | 20 | 0 |
| Q4-SC | 2026-11-24 | 291 | 291 | 21 | 1 |
| Q5-SC | 2026-11-24 | 87 | 87 | 85 | 0 |
| Q6-SC | 2026-11-24 | 26 | 26 | 24 | 0 |
| CB1-SC | 2026-11-27 | 45 | 45 | 20 | 0 |
| CB2-SC | 2026-11-27 | 103 | 103 | 27 | 0 |
| CB3-SC | 2026-11-27 | 10 | 10 | 1 | 0 |

Q1-SC: all 400 hits were exported and screened, above the 300 cap. No record the cap would keep was dropped.

Q1-WS: 89 records were already screened in Q1-SC. The 31 new records were excluded by title. The export was a citation report, without abstracts; no new record needed one. Rank 13, a survey of credit-scoring methods (doi:10.1016/j.eswa.2023.121484), was excluded by title; its abstract was not in the export or in open indexes.

Q1-IE: 38 records were already screened in Q1-SC or Q1-WS. Of the 14 new records, 12 were excluded by title and abstract. Two abstracts were read closely: rank 21, a banking monitoring score on synthetic data (doi:10.1109/ICCSDFAI70505.2026.11647962), and rank 38, intent-drift detection for AI agents in finance (doi:10.1109/CIFEr67845.2026.11692374). Neither states a coverage, learned-time or release requirement. Not critical.

Q1-AC: searched The ACM Full-Text Collection. The 10 results were recorded from the results page. Eight were already screened in Q1-SC. One new record, on information retrieval evaluation, was excluded. The other, an ICAIF 2026 protocol for training and evaluating fraud models (doi:10.1145/3858063.3858860), standardizes delayed-label construction and temporal splits. It states no record requirement. Not critical; closest in this run. Its abstract was read through OpenAlex.

Q2-SC: a first export of 10 records came from an earlier, wrong query; all 10 are in the correct run of 179. One record was already screened in Q1-SC. Most hits matched "feedback loop" in other fields, or "decision log*" as "decision logic"; this added noise but removed nothing. 22 abstracts read, none critical. Closest: compliance-as-code for AI identity systems (doi:10.1109/ACCESS.2026.3665991), which makes missing compliance evidence explicit through fixed monitoring windows; agent-access receipts kept at an API edge (doi:10.3389/fcomp.2026.1900546); and an auditable AI framework for finance with decision traceability logs (doi:10.1109/CARS67163.2025.11337391). Each is adjacent to C1 or C2 but concerns compliance or access control, not outcome records or investigative queries.

Q3-SC: 20 abstracts read, none critical. Most hits matched "audit log" or "execution trace" in agent security or software work. Closest: VerifierBench (doi:10.22266/ijies2026.0831.73), which checks agents' step claims against execution events, next to the cited Dai 2026; TempFinRAG (doi:10.3390/sym18091498), which limits retrieval to filings public by an as-of date, a learned-time rule without a coverage record; and gateways or enforcement points outside the agent that log security events, not what a query examined.

Q4-SC: 5 records were already screened in Q3-SC. 21 abstracts read. One critical: rank 19 is the peer-reviewed version (IEEE MLISE 2026, doi:10.1109/MLISE70044.2026.11607557) of the cited preprint Qi2026GovMem (arXiv 2607.02579). It was read in full, and the citation now points to it. Closest not-critical design: VAIL (doi:10.1109/BigDIA71496.2026.11684708), whose rule is that retrieval authorizes inspection, not use, and which treats agreement from copied values as false consensus; its gates are automatic, with no human release before reuse.

Q5-SC: 2 records were already screened. All 85 other abstracts read, none critical. Closest: SHERLOCK (KDD 2026, doi:10.1145/3770855.3818480), LLM case investigation for e-commerce risk at JD.com with a knowledge base updated through an annotation platform; PACT-IP (doi:10.1109/ICWS72778.2026.00107), which reuses retained judgments unless new evidence is decision-significant; and VR-FraudNet (doi:10.1007/s44163-026-02355-0), which checks LLM fraud rationales with a deterministic verifier. None records outcome channels or query coverage, or requires human release before reuse.

Q6-SC: 24 abstracts read, none critical; one record had no abstract and was excluded by title. Hettema 2021 is already cited. Closest: an analysis of IP indicator overlap across 49 threat-intelligence providers (doi:10.1109/ICCCN69946.2026.11662535), which treats overlap as independent corroboration, the opposite of C3's caution; it states no rule.

CB1-SC: citing documents of Lakkaraju et al. 2017, searched within for the CB1 terms. All 45 hits were exported. Two were already screened in Q1-SC, and rank 23 repeats rank 17. 20 abstracts read, none critical. Most are fairness or method papers on selective labels in lending, criminal justice or health. Closest: a lending data-trust framework (doi:10.1057/s41261-026-00364-8) that records claim-specific evidence status and separates selective repayment labels and temporal leakage, and a review (doi:10.1016/j.giq.2024.101976) that names past decisions shaping data in fraud detection. Neither states outcome records by channel, query coverage or release before reuse.

CB2-SC: citing documents of Dal Pozzolo et al. 2018, searched within for the CB2 terms. 11 records were already screened in earlier runs. 27 abstracts read, none critical. Most are fraud classifiers that handle imbalance, drift or verification latency. Closest: an insurance study (doi:10.1007/s11634-023-00568-0) in which labels depend on investigators' efforts, an active-learning study (doi:10.1007/s41060-018-0116-z) in which labels come from investigators' daily checks, and a review (doi:10.3390/encyclopedia6100233) noting that chargeback labels arrive months later. All are methods; none states a record requirement.

CB3-SC: citing documents of Chapelle 2014, searched within for the CB3 terms. Nine are about online advertising, mostly matched by "payment" or "fraud" in passing. The tenth, a nonpayment model at Meta with delayed labels (doi:10.1145/3711896.3737247), was already screened in Q1-SC.

## Critical sources

| Run and rank | Source | Why critical | Action | Status |
|---|---|---|---|---|
| Q4-SC 19 | Qi, Xu and Li, When Not to Write Memory, IEEE MLISE 2026, doi:10.1109/MLISE70044.2026.11607557 | Peer-reviewed version of the cited preprint Qi2026GovMem | Read in full; replace the arXiv reference if the cited statements hold | Read in full 24 Nov 2026 (pp. 228-234, Sections I-VIII, Tables I-VIII). Same structure and numbers as arXiv v1. Section 2.3, S9.4, S1 notes and S1 matrix statements hold. Reference updated to the IEEE version. |

## Q1-SC, abstract stage

| Rank | Source | Decision |
|---|---|---|
| 81 | Data-Centric Dual-Layer Adversarial Learning for Fraud Detection under Label Delay and Concept Drift (2026), doi:10.1145/3770854.3783941 | Not critical. Method for label delay in bank fraud graphs. No record requirement. |
| 106 | Interpretable Credit Evaluation Model for Delayed Label Scenarios; [面向延迟标签场景下的可解释信用评估模型] (2024), doi:10.11896/jsjkx.230900107 | Not critical. Credit model for delayed labels. Method. |
| 109 | Adaptive Real-Time Financial Fraud Detection with Explainable AI Tools (2026), doi:10.1145/3794859 | Not critical. Streaming fraud pipeline under delayed feedback. Method. |
| 111 | Predicting Chargeback Fraud Using Data Mining Techniques (2024), doi:10.1109/ICSPIS63676.2024.10812614 | Not critical. Compares chargeback-fraud classifiers. No label or record claim. |
| 117 | Selection bias in credit scorecard evaluation (2014), doi:10.1057/jors.2013.55 | Not critical. Shows that accept or reject decisions bias scorecard comparisons. Supports C1's premise; states no record requirement. |
| 128 | Triangulating Digital Forensics to Detect Friendly Fraud and Abuse at Scale: A Cloud-Native, Agentic AI Framework (2026), doi:10.1109/ICAIC67076.2026.11395830 | Not critical. Agent framework that builds friendly-fraud case files. States no coverage, learned-time or release requirement. |
| 158 | Leakage-Controlled Prospective Prioritization of Commercial-Loss Inspections in a Legacy Low-Voltage Network: Dissociating Meter-Fault and Fraud Signals on Monthly Meter Readings (2026), doi:10.1109/ACCESS.2026.3720836 | Not critical. Evaluation and labelling protocol for inspection-dependent labels in electricity theft. No record requirement; outside payments. Closest in this run. |
| 194 | Credit card fraud detection and concept-drift adaptation with delayed supervised information (2015), doi:10.1109/IJCNN.2015.7280527 | Not critical. Trains separately on investigator feedback and delayed labels. Earlier conference work in the cited Dal Pozzolo et al. line. Method. |
| 197 | Enforcement-linked audit risk classification in UK-listed firms: multilevel evidence from pooled public adverse signals (2016–2022) (2026), doi:10.1007/s11135-026-02863-2 | Not critical. Enforcement-linked audit-risk flag. No decision-shaped label claim. |
| 223 | A Tax Evasion Detection Method Based on Positive and Unlabeled Learning with Network Embedding Features (2020), doi:10.1007/978-3-030-63833-7_12 | Not critical. Positive-unlabeled learning for tax evasion. Method. |
| 226 | A machine-learned proactive moderation system for auction fraud detection (2011), doi:10.1145/2063576.2064002 | Not critical. Fraud moderation model with selective-labeling bias. Method. |
| 232 | Sample selection bias in acquisition credit scoring models: An evaluation of the supplemental-data approach (2013), doi:10.21314/JCR.2013.165 | Not critical. Measures bias from ignoring rejected credit applicants. Supports C1's premise; no record requirement. |
| 234 | 7th International Conference on Financial Technology, ICFT 2026 (2027) | Not critical. Proceedings front matter, not a paper. |
| 255 | Mind the Gap: Delayed Label Bias-Variance Tradeoffs in Predicting Likelihood of Nonpayment (2025), doi:10.1145/3711896.3737247 | Not critical. Pseudo-labels for delayed nonpayment labels. Method. |
| 290 | SEL-BALD: Deep Bayesian Active Learning with Selective Labels (2024) | Not critical. Active learning when people decline to label. Method. |
| 291 | Subgraph-Level Temporal Graph Transformer With Laundering-Motif Prototypes for Anti-Money Laundering on Blockchains (2026), doi:10.1109/ACCESS.2026.3731160 | Not critical. Anti-money-laundering graph model. No label claim. |
| 295 | Random Forest Deep Ensemble for Tax Audit Case Selection (2026), doi:10.3390/app16104682 | Not critical. Tax audit selection model; lists sample selection bias as a limit. Method. |
| 311 | Fraud Detection under Multi-Sourced Extremely Noisy Annotations (2021), doi:10.1145/3459637.3482433 | Not critical. Aggregates noisy fraud labels. Method. |
| 319 | Selective Adaptation for Explainable Open-Banking Risk Scoring Under Drift, Delayed Labels and Human-Review Constraints (2027), doi:10.1007/978-981-92-7298-3_15 | Not critical. Synthetic open-banking benchmark with confirmation delays and review capacity. Method. |
| 329 | Beyond Ads: Sequential Decision-Making Algorithms in Law and Public Policy (2022), doi:10.1145/3511265.3550439 | Not critical. Position paper on sequential decisions in public policy. No record requirement. |
| 355 | A Novel Data Stream Learning Approach to Tackle One-Sided Label Noise From Verification Latency (2022), doi:10.1109/IJCNN55064.2022.9891911 | Not critical. Label noise from a fixed waiting window, in software defects. Method. |
| 373 | Integrating Reward Maximization and Population Estimation: Sequential Decision-Making for Internal Revenue Service Audit Selection (2023), doi:10.1609/aaai.v37i4.25637 | Not critical. Audit selection that keeps population estimates unbiased. Method. |
| 377 | Proactive Detection of Model Degradation in Financial Fraud Prediction with Delayed Labels (2026), doi:10.1007/978-3-032-06118-8_16 | Not critical. Detects model degradation before delayed labels arrive. Method. |

Rank 279, Dal Pozzolo et al. 2018, is already cited. The other 376 records were excluded by title.
