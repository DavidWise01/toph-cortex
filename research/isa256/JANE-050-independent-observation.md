# JANE 050 — Independent Observation versus Signed History

2026-11-08. **40/40 local Python tests PASS**; offline HTML browser JavaScript syntax PASS. The complete reproducible experiment (local exact Python model, test suite, result JSON, HTML, README, SHA256 manifest) is in conversation artifact `jane_050.zip`. The GitHub directory `research/isa256/jane050/` contains a separately transcribed equivalent Python model and 40 named regression tests; no independent GitHub CI execution is claimed.

## Canonical substrate

1 tensor > 1 Jane > 1 brace > 2 waldos `{-()+}` > 1 box > 1 toroid > 27 Hamiltonian path positions (abstract ring assumed). Three ternary labels `(-1,0,+1)` add to a **count of 30 components** without adding spatial vertices. Seam `27→27.5→1`. Envelope `{([111222333444555555444333222111])}` remains unchanged.

## Invariant

An authenticated historical claim is not the same as a local sensor observation. If a signed claim matches the sensor, the correct classification is **CORROBORATED**, not VERIFIED_TRUE. If the claim and sensor differ, the model reports CONFLICT, not a determination of which was wrong. Invalid HMAC or stale signed epoch is separately flagged. If the sensor is absent, the comparison returns INSUFFICIENT. HMAC uses a toy shared key here, so it must not be interpreted as production identity proof.

The evaluator knows hidden synthetic truth, but the primitive's `classify` method never accesses it.

## Executed 1000-trial comparisons

Each source has an independently induced 8% sign-flip error rate, with additional shared common-cause error rate. Signed claims in these batches are authenticated, even when semantically wrong.

| Shared fault rate | False corroboration | Sensor–claim conflicts | Correct corroboration |
|---:|---:|---:|---:|
| 0% | 9 | 141 | 850 |
| 5% | 54 | 136 | 810 |
| 20% | 205 | 111 | 684 |

With common cause, a wrong claim and wrong sensor frequently **agree**, thereby increasing apparent corroboration while destroying reliability. In the deliberately forced both-wrong scenario, the signature and reading match and the classifier outputs CORROBORATED even though both are false.

## Limitations

This is a controlled classical evidence experiment with simulated binary ±1 truth (neutral 0 still recognized by classifier), no real external sensors, no physical quantum tunneling, no scientifically verified homeostatic cells, and no demonstrated emergent intelligence. The 27-site geometry and ternary exchange remain formal project structures. The HTML is precomputed/replay visualization rather than live hardware sensor.

## Next boundary JANE051

**Observation Reconciliation / Calibration without false confidence.** Record repeated direct observations; measure noise and common-cause correlation before trusting multi-sample corroboration. Preserve contradicting claims in an append-only history, distinguish persistent shared bias from independent random measurement error, and abstain when both channels agree but independence is unestablished.
