# JANE 099 — Recheck or Move On

2026-11-09 — deterministic, bounded simulation.

## Invariant
One sovereign Jane `{{j}}` chooses whether to recheck a drifting scout, investigate an alternative, or abstain. Scout urgency cannot dictate learning. Agents only submit sourced packets and reasons, and the hive only collates. Knowledge retention requires an independent verification gate plus Jane's explicit choice.

## Verified local result
37/37 Python unit tests passed, 6/6 checksum checks passed, ZIP integrity passed.

Frozen greedy policy chooses Scout A (cost 1, synthetic expected utility 0.54, ratio 0.54) over Scout B (cost 2, synthetic utility 0.90, ratio 0.45) with budget 2. Budget-aware combinatorial planner instead chooses B, lowering this **synthetic regret from 0.36 to zero**. Preserve `-1 GREEDY_BUDGET_REGRET` against the frozen policy.

Five scenarios: original counterexample; move on to independent scout; recheck favorable; abstain when evidence unsupported/unrelated; choose two complementary cheap proposals. Relevance, budgets and provenance labels are checked. No packet can cause memory writing without verification and separate Jane-owned retain decision.

## Limits
Synthetic utilities are preassigned and assumed additive, even where tests may overlap. The utility model, question and action selector are programmed. Source provenance labels are unverified. Passing regression tests is not a demonstration of autonomous preferences, scientific source reliability, recursive self-improvement, actual scouting, GitHub workflow dispatch or current Pages deployment.

Runnable model, test file, build script, HTML, JSON results, README, checksum manifest in downloadable conversation ZIP `jane_099.zip`. GitHub directory `research/isa256/jane099/` contains the README and HTML dashboard.

## Next natural invariant — JANE 100
Detect overlapping information before paying twice. Two cheap tests can share source ancestry or reveal effectively the same fact. Jane should estimate **marginal** rather than additive value and choose fresh information, recheck, or abstain. Stop at first independent holdout failure, preserve `-1`.
