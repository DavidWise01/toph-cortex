# JANE 052 — Learned Source Dependence

**Experimental result: 37/37 Python tests pass.**

The source-aware learner begins with five binary observation streams but receives neither truth labels nor the source genealogy. On 200 training events, it clusters high-agreement observers and counts each inferred cluster once when testing *new* events. The scoring harness retains hidden truth solely to measure false approvals.

Primitive stays unchanged: 1 tensor / 1 Jane / `{-()+}` waldo pair / 1 box and toroid / 27 positions / ternary labels `(-1,0,+1)` / cycle seam `27 → 27.5 → 1`. This is a synthetic evidence model, not a physical simulation of the primitive's wave motion.

### Run

```sh
python -m unittest -q
python model.py
```

Open `index.html` offline to explore the measured scenarios.

### Measured results (20 independent seeds × 250 holdout events = 5,000 per scenario)

| Scenario | Naïve false acceptances | Learned false acceptances | Naïve true acceptances | Learned true acceptances |
|---|---:|---:|---:|---:|
| Three exact clones + two independent | 1081 | 284 | 3919 | 4716 |
| Near clones, ±2% perturbation | 1026 | 681 | 3974 | 4106 |
| Dependency drift after training | 206 | 212 | 4794 | 4788 |

**Non-identifiability test:** five perfectly accurate independent sources produce the exact same measurements as five perfectly accurate clones. All five are grouped together. Over 100 holdout trials, the learned quorum abstains on all 100 *correct* claims. This is expected conservatism, not evidence that the actual sources shared a root.

### Limitations

- Dependence is *inferred from near-equal output*, not proven causal. Hidden common-source failures can go undetected, and independent accurate sensors can be misgrouped.
- The 0.97 pairwise threshold and group majority rule are chosen by design. A chain of pairwise links can overcluster via transitive closure.
- The event generator uses binary measurements and synthetic error probabilities, not physical sensors.
- Training truth is never exposed to the learner. It **is** known by the testing harness for scoring.
- The current implementation has a central offline learner and no proven independent waldo clocking, durable journal updates, or self-grown homeostatic behavior.
- The dashboard is a precomputed visualization, not a Python simulation running inside the browser.

### Next invariant — JANE 053

**Change-point recognition / dependency drift.** Train on early observations, detect when the correlation structure changes, and quarantine claims during relearning. Compare false approvals and abstention while an adversary makes historically independent sources suddenly share an upstream failure.