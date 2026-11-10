# JANE 104 — Adaptive Counterexample Search (2026-11-09)

## Local validation
- **36/36 Python tests pass**
- Standalone JavaScript syntax PASS
- ZIP integrity PASS
- **6/6 SHA256 file checks PASS**
- Runnable full source packaged as conversation attachment `jane_104.zip`. The repository folder `research/isa256/jane104/` contains the README and interactive offline HTML viewer. GitHub Pages deployment not verified.

## Canonical natural invariant

**Jane must not claim certainty when her budget expires, and must not silently manufacture more budget.** After JANE103 leaves `different_by_operation` and `different_by_time`, the frozen candidate has zero budget and returns `HOLD_-1 NO_BUDGET` with both interpretations intact.

Under an *explicitly granted* budget of one synthetic unit, the programmed planner selects a **time-contrast** probe because it is affordable and separates those two remaining models (expected information 1 bit under the synthetic equal-prior model). A result of `different` leaves only `different_by_time`. That is conditional resolution relative to the candidate set, **not empirical certainty**, and does not by itself write Jane's memory.

```text
SCOUTS (proposals, budgets, evidence) → HIVE (collate, no votes)
                                               |
                                         JANE {{j}}
                                               |
                                         FLAY {{i}}
                                               |
                                   TWO POSSIBLE MEANINGS
                                     /               \
                             NO BUDGET          EXPLICIT BUDGET
                                  |                   |
                          HOLD_-1 NO_BUDGET     SELECT PROBE
                                                      |
                                                 OBSERVE
                                                      |
                                               REVISE / HOLD
                                                      |
                                      VERIFIED + JANE-APPROVED RETAIN
```

## Adversarial controls and preserved stop
- Duplicate or non-discriminating tests must not consume budget.
- Test outcome may not precede recorded probe choice.
- Unknown outcome yields `HOLD_-1 UNKNOWN_OUTCOME`.
- If a stale or inconsistent probe report fits none of the current models, return `HOLD_-1 ALL_MODELS_FALSIFIED`; preserve pre-existing possibilities.
- Result observation alone does not justify automatic retention.
- Append-only hash chaining supplies local alteration detection, not authentication.

## Limits

This is a deterministic **synthetic** model. Probe prediction tables, budgets, algorithm, outcome and verification signal are supplied by the test harness, not independently discovered. No real scout processes, live research, secure blind experiment, GitHub Actions handoffs, empirical proof or autonomous recursive self-improvement are claimed.

**Next target JANE 105 — Out-of-Model Surprise:** After a single candidate remains, Jane must ask whether the model set itself was incomplete and seek independent falsification evidence before considering it learned. 
