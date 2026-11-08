# JANE 052 — Learned Source Dependence

**2026-11-08** · Original local release `jane_052.zip`: **37/37 tests PASS**, standalone dashboard JS syntax PASS. GitHub directory `research/isa256/jane052/` contains runnable model, complete 37-test suite, interactive HTML, README and result data. No GitHub CI or Pages deployment is claimed.

## Canonical preserved primitive
One tensor > one Jane > one brace > two waldos `{-()+}` > one box > one toroid > 27 spatial positions. Three ternary labels `(-1,0,+1)` are **27+3=30 counted components** (not spatial vertices). User palindrome: `{([111222333444555555444333222111])}`, seam `27→27.5→1`. The experiment is on **source-reliability inference**, not physical wave dynamics or biological homeostasis.

## Hypothesis and tested invariant

**Repeated concordance may identify likely statistical dependence, but cannot prove causal common origin.**

The learner observes five binary source streams, no truth labels and no dependency annotations. Its fitting rule links pairs whose sample-wise agreement on the first 200 events is ≥0.97, closes the links into groups, and counts each group once on new events. Group members vote by local majority; the learner accepts a binary claim only if at least two groups vote for it and they outnumber groups voting against it.

Training and held-out evidence are disjoint. The simulation harness knows the actual truth and dependency generation only to score model performance. A/B/C share an upstream error process during training; D and E are independent.

## Measured 20-seed experiments (5,000 holdout events per scenario)

| Scenario | Naive false approvals | Learned false approvals | Naive true approvals | Learned true approvals |
|---|---:|---:|---:|---:|
| Exact three-clone upstream fault | 1,081 | **284** | 3,919 | **4,716** |
| Near-clones with 2% extra perturbation | 1,026 | **681** | 3,974 | **4,106** |
| Source dependency changes after training | **206** | 212 | **4,794** | 4,788 |

Additional non-identifiability counterexample: all five sensors are perfectly accurate on every event, yet their outputs resemble perfectly accurate clones. The learner merges them into one group and **abstains on all 100 truthful holdout claims** despite raw five-source agreement being 100/100. Without independent interventions or causal evidence, indistinguishable output histories do not identify the actual source relation.

## What the test does not show

- No proof of causal root identity or physical source independence; only a statistical heuristic.
- No guarantee under changing dependencies: performance on the `dependency_drift` case is marginally worse than naïve voting.
- No guarantee under near-clone noise or transitive overclustering.
- No automatic trust in the learned grouping; abstention is a legitimate outcome.
- No evidence yet of autonomous homeostatic cells, quantum wave dynamics or independent sensor hardware.
- GitHub code was published as the implementation of the same rules and tests; separate CI and Pages runs are unverified.

## Next natural invariant — JANE 053: Dependency Change-Point Detection

Once source dependence is learned, **treat it as temporary**, watch for a change in observed agreement patterns, and determine when to freeze past group assignments, quarantine decisions, and relearn. Compare false approvals against the cost of abstaining during drift. The learner must not be given the simulator's hidden ground truth.
