# JANE 050 — Independent Observation

Canonical geometry unchanged: 1 tensor, 1 Jane, 1 brace, 2 waldos `{-()+}`, 1 box, 1 toroid, 27 path positions and ternary `-1,0,+1` labels. Symbolic seam: `27 → 27.5 → 1`. The 30-character wave palindrome is unchanged.

## Reproduce

```bash
python -m unittest -q test_model.py
python model.py > results.json
```

No dependencies besides the Python standard library. Open `index.html` directly in a browser. It replays numerical results; it does not execute the Python simulation or connect to a real sensor.

## Invariant

A signed historical claim and a local observation may agree because both are correct, or because both are wrong. A disagreement is detectable but cannot alone identify which input failed. Even with a valid signature, an authenticated claim can be incorrect. A pinned epoch detects old signed claims, only if the epoch pin is trustworthy.

### 1,000 independent trials per setting

Synthetic 8% independent historical claim errors and 8% independent sensor errors; add 0%, 5%, or 20% correlated shared errors. All signed claims are validly authenticated in the trial batch, so the model tests correctness versus authenticity separately.

| Shared fault probability | False corroborations | Conflicts | Correct corroborations |
|---:|---:|---:|---:|
| 0% | 9 | 141 | 850 |
| 5% | 54 | 136 | 810 |
| 20% | 205 | 111 | 684 |

The classifier has no access to the evaluator's hidden truth. It returns CORROBORATED, CONFLICT, INVALID_SIGNATURE, ROLLBACK, INVALID_SENSOR, or INSUFFICIENT. A false corroboration is a wrong claim and a matching wrong sensor observation. The deterministic trial generator assumes ternary truth is one of ±1 for ease of explicit sign flips; a neutral 0 is supported by the classifier but not in the numerical batch.

The exact test suite passes **40/40** locally. Model limitations: toy HMAC key, simulated oracle used only to evaluate, no actual quantum tunneling, no independently discovered homeostasis, no verified 27-vertex spatial embedding, no production authentication and no access to a real observation device.

## Next bound JANE 051 — Observation Reconciliation

Instead of choosing a winner from one conflict, preserve both reports, sample local observations over time, estimate correlated failure from measurement history, and abstain or revise with a transparent log. Validate whether independent repeated observations improve calibration without falsely presuming independence.