# JANE 060 — Cyclic Stability: Natural Invariant

Date: 2026-11-08. Canonical primitive preserved: `{{j}}` with root payload `{{i}}`; `{{[6x6x6(4x4(2x2[i]))]}}`. The 27 occupied path positions and `27 -> 27.5 -> 1` seam remain unchanged. The 27.5 half-step is **not** vertex 28.

The user-defined stages remain 5 PROPAGATE, 8 DOMINATE, exactly 13 EMERGE, 13–17.5 CRAWL, 17.5–21 WALK, 21–24 RUN, 24–25 TRANSITION (unassigned gap), 25–27 SPRINT, 27–27.5 SEAM, then REPEAT.

## Tested policy

Compare the direct mapping to a guarded control rule requiring three consecutive observations exceeding each stage boundary by a +/- 0.16 hysteresis margin; permit only one stage advance/retreat per confirmation; require explicit wrap authorization to cross the 27.5 seam. The exact-13 EMERGE event stays distinct from a stable gait.

## Numerical findings

All results below are **100 seeded synthetic trials of 360 samples** (36,000 comparisons per scenario). Python unittest: **16 of 16 passed**. Browser JavaScript passed node --check and ZIP integrity passed.

| Scenario | Direct phase flips | Guarded phase flips | Direct sample errors | Guarded sample errors |
|---|---:|---:|---:|---:|
| Stable, jitter near 17.5 | 16,846 | 402 | 13,680 | 3,795 |
| Advancing ramp | 2,313 | 742 | 1,580 | 4,231 |
| Two cycles | 2,385 | 1,848 | 1,344 | 5,722 |

**Negative invariant:** hysteresis reduces false transitions and noise but introduces lag. A lower phase-flip count is not equivalent to better task performance. Under the 5-step recursive improvement protocol, this candidate is **not automatically promoted**: the ramp/cycle errors worsened. A future adaptive policy should adjust hysteresis to observed change rates while keeping held-out gate tests fixed.

## Reproducibility

The full Python model, exact original JANE059 classifier, tests, seeded results, offline HTML, build script, and checksums are included in the `jane_060.zip` release attached to the conversation. GitHub's `research/isa256/jane060/index.html` and `README.md` were published; this canonical note is a summary, not an assertion that all ZIP sources are on GitHub. No actual emergence, physical gait, or autonomous self-improvement is demonstrated.
