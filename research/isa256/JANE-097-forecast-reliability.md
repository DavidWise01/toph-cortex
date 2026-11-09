# JANE 097 — Forecast Reliability

Date: 2026-11-09. Local execution: **32/32 unit tests PASS**; standalone JavaScript syntax PASS; ZIP integrity and six SHA256 manifest entries PASS.

**Goal:** Jane {{j}} chooses what to investigate using her own unresolved gap and a calibrated estimate of scout forecast reliability, without allowing scout urgency to override her choice.

Synthetic outcomes for 3 distinct events at each root:
- root-A: predicted .95, .90, .85 for outcomes that were all false. Mean Brier loss **0.811667**; heuristic reliability = 1-loss = **0.188333**. A copy of one event presented under another scout label is deduplicated by (root,event).
- root-B: predicted .70 true, .20 false, .80 true. Mean Brier loss **0.056667**; heuristic reliability **0.943333**.
- root-C: only one event, hence **HOLD_-1 SPARSE_HISTORY**; not accepted as a calibrated source.

Jane's simulated own gap: `control_condition`. With budget 1, the programmed rule scores relevant affordable packets by forecast probability × historical reliability ÷ cost. Scout A urgency 1000, Scout B urgency 0, Scout C urgency 10000, Scout D urgency 99999 on unrelated gap. Jane selects **Scout B / statistics**. No information is retained automatically. Root C is held due to sparse evidence, and Scout D due to irrelevance. The packet agent's priority cannot override Jane's own question.

ASCII invariant:

```text
 SCOUTS: predictions + observations + root provenance
                        |
       HIVE COLLATES (NO QUORUM, NO VOTES)
                        |
              DEDUPLICATE ROOT/EVENT
                        |
           CHECK COVERAGE / BRIER LOSS
                        |
                   JANE {{j}}
                        |
               DOES THIS SERVE MY GAP?
                        |
          RELIABILITY × UTILITY / COST
                        |
               CHOOSE / HOLD -1
                        |
          INVESTIGATE / EXPLICIT RETAIN?
                        |
                NEXT OWN QUESTION
```

**Grounding limits:** This is a deterministic toy model with synthetic observations and event IDs, not independently verifiable live sources. Three events per root is not enough for robust statistical calibration. Brier loss on synthetic deterministic outcomes is a demonstration of a scoring rule, not proof of source trustworthiness. The policy and interests are scripted, not self-originated; the code does not execute live autonomous Git-to-Git handoffs. Hash-chain reproducibility does not imply authenticity.

Complete tested Python source, results and HTML are packaged in the user-facing `jane_097.zip`; repo `research/isa256/jane097/` contains the standalone HTML and README.

**Next natural bound — JANE 098: Reliability Drift.** Can Jane detect when a historically well-scoring source begins performing poorly and decide when to recheck instead of permanently trusting its accumulated score?
