# JANE 053 — Dependency Change Detection

**42/42 locally executed Python tests pass.** No external dependencies.

## Canonical primitive

`1 tensor > 1 Jane > 1 brace > 2 waldos {-()+} > 1 box > 1 toroid > 27 positions`. Additional `(-1,0,+1)` ternary register labels are not vertices; 27 + 3 = 30 counted components. The symbolic closing seam remains `27 → 27.5 → 1`.

This experiment studies observation provenance, not physical wave propagation or cell homeostasis. Five simulated observer channels are external data streams, not new spatial cells.

## Rule / invariant

**An inferred source dependency is only valid for the time interval in which its evidence remains consistent.** Jane infers source groups from pairwise disagreement in a sliding 64-event window without access to truth. If a previously grouped pair disagrees by at least 17% for 12 consecutive steps, it freezes automatic approval, appends a `FLAG`, gathers 48 fresh observations, and appends a new hash-linked grouping rather than overwriting the old one. A cluster requires at most 9% pairwise disagreement using complete linkage. The rule can mis-detect and group distinct-but-accurate sources.

## Reproduce

```bash
cd jane_053
python -m unittest -q test_model.py
python model.py
python build.py
```

Open `index.html` without a server. It displays measured/precomputed trial results, **not a live Python learner**.

## Test setup

100 seeds; 630 binary events per seed; 180 baseline-training events; source change at t=280; post-stabilization evaluation from t=370 through 629 = 260 cases per seed. Baseline sources A/B/C share a hidden error; after change A/D/E share it while B/C become independent. Corrupted claims are scored as the opposite of the latent truth. Truth is used only by the generator/evaluation; the dependency learner never receives it.

### Across 26,000 post-change false-claim evaluations

- Frozen grouping: **7,298** false approvals; true-claim approvals **18,638**.
- Guarded change detection: **2,253** false approvals; true approvals **23,749**.
- Rolling ungated grouping: **2,277** false approvals; true approvals **23,879**.
- Mean first change flag **t=315.64**, or ~36 observations after change.
- Change flagged and new version appended in **100/100 changed trials**.

### No actual source change

- Guarded detector: **1 spurious flag/revision in 100 trials**.
- False approvals among 26,000 evaluations: frozen 2,303; guarded 2,327; rolling 2,299.

The version chain is hash-linked to detect accidental editing but **not authenticated**: someone with write access can recompute the entire unkeyed chain. The new grouping need not identify true causes or independent authorities, and no external trust root is modeled. Always distinguish changed-dependency detection from truth discovery. Results are seeded synthetic trials and not field data.

## Next boundary

**JANE 054 — Predictive Drift and Confidence Calibration.** Distinguish abrupt changes from gradual drift and seasonal variation; calibrate abstention cost vs false approval, rather than treating any deviation as evidence of a new causal relationship.