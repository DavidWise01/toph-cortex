# JANE 072 — Question-Selection Fitness / First −1

Date: 2026-11-08. Status: **LOCAL EXPERIMENT; CANDIDATE REJECTED.**

## Target

Under the user-provided challenge, `{{j}}` should autonomously identify the next valuable research question without a new topical prompt, then recursively improve the **question-selection policy**, not just the answers. This JANE072 implementation tests a narrow surrogate of that goal; it is NOT a claim that Jane is autonomously running on the internet.

## Frozen architecture

```text
JANE {{j}}
 | PRIM 10 × 5 × 4 × 3 × 1 = 600 logical addresses
 | root payload {{i}}
 | OBSERVE five synthetic unresolved questions with numeric feature ratings
 | PROPOSE three policy-weight scouts (.35/.70/1.00 blend)
 | TEST against distinct validation examples (80 episodes)
 | RETURN fitness / regret and immutable baseline checks
 | PROPAGATE only if reward improves >= 0.001 and regret drops > 0.001
 | STOP on first unseen replication failure = -1
```

No holdout reward is visible to a question selector at decision time. The scripted scout generator is *not* itself autonomously self-modified.

## Actual local results

- Python `unittest`: **17 tests pass** (including detection and preservation of −1).
- Generation 1 on 120 training / 80 validation synthetic episodes: **NO promotion**.
- Generation 2 on disjoint train/validation: **one scout accepted for the synthetic task**.
- Unseen normal regime (150 episodes, seed 9001): frozen baseline mean reward **0.605063**, candidate **0.606689**, PASS.
- Unseen novelty-dominant regime (150 episodes, seed 9002): baseline **0.511155**, candidate **0.478214**, **FAIL −1**.
- Hard stop at that failure; do not continue to cost-shift or retune to obtain a pass. Globally retain frozen baseline.
- Node dashboard JS syntax and ZIP integrity both PASS locally.

## Interpretation

Reweighting question features can outperform the original weight vector on a familiar objective, while failing when a new topic population makes novelty more valuable. This is an engineered classical statistical policy-fitting experiment, using synthetic payoff labels, **not** measured real-world information gain. No independent question generation or two successful generations of recursive improvement has been established.

## Artifacts

The exact locally executed `model.py`, `test_model.py`, `build.py`, `results.json`, `README.md`, `index.html` and `SHA256SUMS.txt` are in the conversation ZIP `jane_072.zip`. The GitHub folder contains a copy of the dashboard and README plus this canonical specification; do not claim that the Python files were uploaded if they were not.

## Next question selected from failure

**Can Jane evaluate question importance under shifting research goals, without merely overfitting yesterday's information-gain signals?**

Proposed next test: introduce a transparent abstention / change-point gate for question priority, and assess on hidden new task families under a pre-registered protocol. Keep the JANE072 −1 unmodified and include a no-prompt question proposal as the first artifact.
