# JANE 069 — Independent Replication: −1 (retain baseline)

**Status: measured local simulation, 2026-11-08.** JANE 068 scout_0 is frozen (`0.35 * legacy_forecast + 0.65 * latest_observation`). Compare against frozen JANE 065 45-leaf median predictor.

- 600-address prim `10×5×4×3×1` unchanged. Original forecast uses 45 routes and reserved scout uses 15 addresses; this is logical routing, not new physical cells.
- 2,000-ms forecast horizon (eight × 250-ms ticks); only observations available when issued can influence a forecast.
- 8 fresh scenarios × 12 unseen seeds (19001–19012) × 320 observations = **30,720 observations per policy**; **29,952 matured forecast comparisons** per policy.
- Freeze gate: no MAE regression **in any scenario**, no increase in errors over 0.75, scout within 60 units and meaningful gain > 0.01.
- 17/17 Python regression tests passed locally; offline dashboard JavaScript syntax valid; archive integrity valid.

| Scenario | Frozen baseline MAE | Scout 0 MAE | MAE decision |
|---|---:|---:|---|
| heavy_tail | 0.281047 | 0.257933 | improve |
| **correlated_bursts** | **0.361601** | **0.381732** | **−1 first fail** |
| frequency_change | 0.844011 | 0.653083 | improve |
| reversal | 0.135507 | 0.163796 | regression |
| accelerating | 0.190342 | 0.191559 | regression |
| random_walk | 0.214358 | 0.201983 | improve |
| quasiperiodic | 0.805089 | 0.645108 | improve |
| prior_stationary | 0.083684 | 0.065859 | improve |

**Decision: REJECT scout_0 / RETAIN baseline.** First failure by specified case ordering is the correlated burst. All additional failures remain in evidence. A better overall average cannot override the frozen per-condition gate.

Measured compute nanoseconds use `time.perf_counter_ns` and are hardware/load-dependent. The Python simulation advances simulated timestamps; it is not a guaranteed hard-real-time deployment. JANE 069 does not demonstrate actual internet hive learning or recursive self-improvement.

**Reproducible executable package:** The complete `jane_069.zip` (Python source, 17 tests, offline interactive HTML, results.json, SHA256SUMS) is attached to the JANE 069 conversation. This Markdown commit records the result; remote CI and GitHub Pages execution are **not verified**.

**Next boundary — JANE 070:** sealed train/validate/test for a bounded context-sensitive router that selects baseline or scout before observation maturity, preserves the first failure, and is permitted promotion only after untouched-distribution verification.