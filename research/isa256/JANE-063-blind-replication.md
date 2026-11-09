# JANE 063 — Blind Replication and Failed Promotion Gate

Date: 2026-11-08. **Frozen JANE 060** versus **unretuned JANE 062 moderate scout**.

## Test definition
7 deliberately new synthetic stress cases: gaussian_jitter, heavy_tail_jitter, correlated_jitter, slow_ramp, fast_ramp, long_cycle, uneven_cycle. 30 new seeds 90100–90129 × 720 observations/case = 151,200 decisions per policy. Candidate unchanged: slope threshold .06, lookback 13, fast confirmations 2; baseline Guard margin .16, confirmations 3. No tuning after evaluating this test.

## Results
- Total errors: baseline 18,459; moderate 16,392; overall error reduction 2,067 (11.2%).
- Missed seam wraps: baseline 40, moderate 12.
- Total spurious phase changes: baseline 2,520; moderate 2,353.
- Heavy-tail jitter errors: baseline 901, moderate 1,057 — **regression**.
- Correlated jitter errors: baseline 6,867, moderate 6,883 — **regression**.
- Both adverse jitter cases also regress on spurious phase changes.
- Estimated per-observation work ratio: 14× frozen baseline (nominal heuristic count, not wall-clock profiling).

## Gate / decision
The JANE 062 gate requires no scenario-level worsening in errors, spurious phase changes or missed wraps, while total errors must improve and estimated work ≤20×. **Gate fails: DO NOT PROMOTE THE CANDIDATE.** Retain the frozen baseline. Append this failed replication to the evidence record instead of silently changing evaluation criteria.

## Preserved substrate
JANE {{j}} with root payload {{i}} in {{[6×6×6(4×4(2×2[i]))]}}; 27 occupied positions with 27 → 27.5 → 1 seam; two waldos and three ternary modes; one-way 16-stop interleaved ± strands on scales 60/30/15/7.5/5/2.5/1/1. Five-step observe/propose/test/return/propagate process; no propagation on failed gate.

Local release: 16/16 Python tests PASS, browser JS syntax PASS and ZIP CRC/integrity PASS. Exact Python sources and full per-scenario results are in the linked conversation ZIP. GitHub contains this canonical result, README and standalone dashboard; the exact tested Python source has **not** been uploaded or executed in CI as part of this commit.

## Next target — JANE 064
Bound the heavy-tail and temporal-correlation counterexamples without overfitting to them. Three predeclared scouts, a new held-out split, and an unchanged no-regression gate. If none passes, retain baseline. Avoid pretending that a single seeded synthetic experiment establishes open-ended recursive improvement.
