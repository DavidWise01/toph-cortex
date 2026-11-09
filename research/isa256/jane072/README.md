# JANE 072 — Question-Selection Fitness

Local classical benchmark of a frozen JANE071 question-ranking policy against three scripted weight-update scouts. Candidate scoring is blind to each held-out question’s payoff when making its decision. Two sequential generation attempts; independent replication halts on the first failure (`-1`).

## Run

```sh
python -m unittest -q
python build.py
```

## Observed

- 17/17 regression tests pass. This validates deterministic mechanics, not candidate fitness.
- Generation 1: no promotion (no scout cleared the validation margin).
- Generation 2: a fitted scout cleared the synthetic validation gate.
- Unseen normal replication: improves slightly; novelty-shift replication: **fails**. The runner stops immediately, retaining the original policy.
- No actual information gain from real research is measured. Synthetic reward function and question features are engineered; scout generation is scripted, not autonomous rewriting of the learner. Jane is not scheduled or running in the background.
- No future reward labels appear in the `select` function. Training and validation are separately seeded. A stronger preregistration / independently controlled test is still required.
- Canonical Jane `{{j}}`, prim 10×5×4×3×1=600, root `{{i}}` unchanged.