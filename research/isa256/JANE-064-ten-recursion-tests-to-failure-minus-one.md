# JANE 064 — Ten Tests of Policy Recursion to First Failure (−1)

**Executed** 2026-11-08. Stop boundary: **test 10**.

## Canonical unchanged geometry

`{{j}}` supervises `{{[6x6x6(4x4(2x2[i]))]}}`; `{{i}}` remains a root payload. The fixed 27 occupied primitive positions and seam `27 -> 27.5 -> 1` do not change. This experiment tests a separate, synthetic parameter-optimization loop; its threshold is not a spatial coordinate.

## Ten increasing test obligations

```
 1 Closure                           PASS
 2 Isolation                         PASS
 3 Deterministic replay              PASS
 4 Three-scout limit and audit       PASS
 5 First policy generation           PASS  threshold 80 -> 70
 6 Rejected no-op preserves baseline PASS
 7 Second policy generation          PASS  threshold 70 -> 60
 8 New input-order test              PASS  (same distribution)
 9 Work cap and ledger integrity     PASS  800 / 2000 units
10 Unknown distribution shift        -1 FAIL / STOP
```

Synthetic task: classify `x >= true_boundary`, with exactly 100 input values `x=0..99` and fixed candidate thresholds `t-10,t-20,t-30`. Original train/holdout truth boundary 50; initial policy 80 scores 70%, policy 70 scores 80%, policy 60 scores 90% on that distribution. At the previously withheld boundary 90, original policy 80 scores 90%, newer policy 60 scores 70%: **−20 percentage point regression**. The non-regression condition fails. Preserve input `boundary=90, offset=51`, old threshold=80, new threshold=60; stop progression and record `-1`.

All **10 independent unit regression methods PASS** in the exact downloadable Python release; these include checking that ladder test 10 is an expected FAIL. Do not confuse the test-suite PASS with the ten-stage ladder result of nine PASS and one FAIL. The test runner, detailed JSON (with 3 hash-chain audit entries), self-contained HTML, checksum manifest, and exact Python source are included in the JANE064 conversation ZIP.

**Important limits:** the three scout variants, evaluation metric and task labels are authored by the experiment. This is not an autonomous algorithm learning to generate better algorithms; no verified open-internet memory, physical emergence, quantum property or end-to-end homeostasis. The SHA256 ledger is self-consistent, not externally immutable.

## Natural next bound

JANE065: detect unseen domain shift before promoting or deploying policies, avoid evaluation leakage, measure false alarms, rollback, abstention, and cost; preserve this exact JANE064 failure as the fixed counterexample. No silent revision to the 064 decision.
