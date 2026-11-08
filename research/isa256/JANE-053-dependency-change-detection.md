# JANE 053 — Dependency Change Detection

Date: 2026-11-08. **42/42 tests PASS locally** for the reproducible offline package `jane_053.zip`. Node JavaScript syntax check PASS. Repository includes runnable `model.py`, 42 regression checks `test_model.py`, an offline HTML dashboard, README and measured results summary. The GitHub model and tests are **independently transcribed equivalents**; a GitHub CI run has not been verified. The ZIP is the exact local build.

## Geometry

Preserve user primitive unchanged: 1 tensor > 1 Jane > 1 brace > 2 waldos `{-()+}` > 1 box > 1 toroid > **27 positions**, plus ternary `(-1,0,+1)` wave-register labels (27+3=30 counted components, not 30 vertices). Closing seam `27→27.5→1`. The five observer streams in this experiment are **input channels**, not extra cells.

## Natural invariant

**Learned source dependence has a time boundary.**

A source dependency learned in one epoch should not silently overwrite itself when observations deviate. Freeze approvals on detected drift; append an explicitly versioned group after independent fresh readings; retain the earlier group and its version hash. No hidden truth or source-root identities are available to the learner. Append-only hashes are unkeyed and are not authentication.

## Simulation

Each of 100 independent seeds generates 630 events with five binary observer streams. Before t=280, A/B/C share one repeatable error; after t=280, A/D/E share it and B/C become independent. The detector learns on 180 events, uses a rolling 64-event pairwise disagreement window, flags a previously clustered pair if mismatch >=17% for 12 consecutive events, then gathers 48 new events before appending a new grouping. Source clustering uses 9% maximal pairwise mismatch (complete linkage). During re-learning, the guarded detector abstains. A latent truth label exists only in the test generator/scorer.

**Post-stabilization evaluation: 260 false and 260 true claims per seed, t=370..629.**

| Scenario | Rule | False approvals / 26,000 | True approvals / 26,000 |
|---|---|---:|---:|
| Changed dependencies | Frozen old group | 7,298 | 18,638 |
| Changed dependencies | Guarded relearning | 2,253 | 23,749 |
| Changed dependencies | Rolling/no guard | 2,277 | 23,879 |
| No actual change | Frozen old group | 2,303 | 23,739 |
| No actual change | Guarded relearning | 2,327 | 23,836 |
| No actual change | Rolling/no guard | 2,299 | 23,803 |

Under changed dependencies, flag + revision occurred for 100/100 seeds; mean first flag t=315.64, approximately 35.64 observed steps after t=280. Under no change, **1/100 spurious flag/revision** occurred. Grouping can be wrong for truthful or dependent observers, and an adversary can forge or replay an unkeyed version chain unless an external trust anchor remains.

## Limitations

No general change-point detection guarantee. The method sees only source agreement patterns; it cannot establish causal relationships, truth, true independence, or change type. Tuning thresholds after seeing the simulated generator limits external applicability. The evaluation is classical synthetic data, not a physical wave/cell experiment or autonomous homeostasis. The browser replays measured data, not a live Python process.

## Next natural invariant — JANE054

**Predictive Drift and Confidence Calibration.** Evaluate gradual drift, seasonal oscillations and abrupt changes separately. Calibrate the cost of abstention against falsely approving claims. Test whether a detector can avoid treating normal cyclical behavior as a permanent new dependency.
