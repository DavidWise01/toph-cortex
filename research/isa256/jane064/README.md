# JANE 064 — Ten Recursive Improvement Tests to First Failure (−1)

This is a **frozen deterministic threshold-optimization toy**. It does not demonstrate autonomous recursive self-improvement or a live network-connected Jane. It tests the policy transition logic used to plan later JANE experiments.

Run:

```bash
python model.py > results.json
python -m unittest -q
```

## Ten tests

1. Closed state and three candidate scouts.
2. Proposals cannot mutate the frozen initial policy.
3. Deterministic replay.
4. Exactly three bounded candidate scouts and valid empty audit.
5. First promotion `threshold=80 -> 70` (accuracy 70% -> 80%).
6. Rejected no-op leaves the active baseline untouched.
7. Second promotion `70 -> 60` (accuracy 80% -> 90%).
8. Generalization under unseen input ordering, but unchanged data distribution.
9. Append-only hash chain, version count and bounded evaluation work.
10. **−1 FAIL** Unseen distribution shift (label boundary 50 -> 90): original threshold 80 scores 90%, new threshold 60 scores 70%. The strict no-regression gate fails by 20 percentage points.

`results.json` includes the full audit ledger and hash chain. The runner reports all ten tests and identifies the first failing step; no remediation after failure. A simulated `v2` was already promoted by its own training/holdout gate before the unseen deployment-style check. It is not rolled back automatically in this release; the test outcome requires freezing that simulated version and retaining v0 as the known comparison policy.

The 10 unittest methods in `test_model.py` validate the 10-step experiment, but they pass when the *expected counterexample* is correctly detected. The ladder outcome is **9 PASS, 1 FAIL**; unit-tests outcome is **10/10 PASS**. These are different counts.

Do not confuse self-consistent SHA256-linked records with independent authentication. The synthetic evaluator has ground-truth labels supplied by the harness. The fixed candidate-generation mechanism does not self-improve.

Next boundary: a **pre-deployment distribution-shift sentinel and rollback** tested with unseen shifts, without giving scouts access to future labels.