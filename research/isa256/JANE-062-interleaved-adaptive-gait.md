# JANE 062 — Interleaved Adaptive Gait, head-to-head held-out test

2026-11-08. **Conditional candidate win, not demonstrated open-ended recursive self-improvement.**

Canonical structure unchanged:
- Jane `{{j}}` with root payload `{{i}}`
- `{{[6x6x6(4x4(2x2[i]))]}}`
- 27 occupied positions, closure `27 -> 27.5 -> 1`, 27.5 never a new vertex
- 5 propagate / 8 dominate / 13 emerge; crawl/walk/run/[24–25 transition]/sprint/repeat
- Diodic symbolic transport: `+ 60/30/15/7.5/5/2.5/1/1` then `- 1/1/2.5/5/7.5/15/30/60`
- Three symbolic mode roles a,b,c mapped to three distinct numeric states -1,0,+1, never numerically equated.

## Implemented candidate

Frozen JANE 060 Guard is the baseline, using 3 confirmations and 0.16 margin. Candidate still runs the same guard but measures the slope of a fixed sliding window of 9 or 13 recent readings. If the trend magnitude passes a configured threshold, it uses 1 or 2 confirmations; otherwise the old conservative rule is retained. The 16-stop helix alternates proposal and return-check roles only as a symbolic software schedule: **the return does not constitute a second independent measurement**.

Three preselected candidates:
- fast: threshold 0.045, window 13, 1 confirmation
- moderate: threshold 0.06, window 13, 2 confirmations
- conservative: threshold 0.08, window 9, 2 confirmations

## Held-out measurements

30 seeds (200–229), 360 samples per seed, 10,800 observations per case.

| Policy | Jitter errors | Ramp errors | Cyclic errors | Jitter spurious changes | Ramp spurious changes | Cyclic spurious changes | Missed cyclic wraps |
|---|---:|---:|---:|---:|---:|---:|---:|
| Frozen 060 | 920 | 1300 | 1761 | 122 | 227 | 525 | 14 |
| Fast | 1117 | 553 | 480 | 130 | 234 | 327 | 0 |
| Moderate | **920** | **1038** | **1021** | **122** | **227** | **449** | **1** |
| Conservative | 956 | 1169 | 1021 | 126 | 224 | 449 | 1 |

Candidate **moderate** passes the declared **strict per-scenario, no-regression gate**: no additional errors, spurious switches or missed wraps in any one scenario, total errors strictly lower, and computational work estimate <=20x frozen baseline. The fast and conservative candidates fail because stationary-jitter errors increase. The moderate approximation uses **14x** estimated operations per sample, not independently measured CPU time.

15 Python unittest methods locally PASS. Node syntax PASS. ZIP integrity PASS. The complete exact Python model, frozen dependency, canonical classifier, regression tests, build script, results, checksum manifest and HTML are packaged as JANE 062 ZIP in the conversation; **only the HTML, README, and canonical report were committed to GitHub in this turn**.

The `train_seeds` parameter is unused: scout policies were manually specified and not trained end to end. This was a seeded synthetic benchmark, not a live agent, physical gait, independent verification, true Internet hive, or real self-improving model. Candidate selection on the same held-out batch used for reporting creates selection bias; an additional *untouched* final audit is required before general deployment.

## Next test

JANE 063 — **Blind third-set replication and adaptive-cost minimization**. Run the selected moderate rule on independently reserved novel seeds and new noise/drift distributions without modifying parameters. Measure workload and compare with simpler alternatives. If it fails: keep JANE 060 as the frozen active baseline. If it succeeds: promote as an explicitly bounded retrieval/gait control policy only, with rollback pointer and immutable audit.
