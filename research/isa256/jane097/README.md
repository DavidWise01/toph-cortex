# JANE 097 — Forecast Reliability

One Jane `{{j}}` retains control of learning and investigation choices. Scout packets present forecast probabilities, observations, provenance roots, and costs. Jane's bounded tool-selection rule discounts historically inaccurate forecast sources and refuses to score sparse histories. No agent urgency can override her stated gap.

## Run

```bash
python -m unittest -q
python build.py
```

## Local test

32/32 tests PASS. Two synthetic source roots have three distinct forecast events each, plus a duplicated report from the same root. The duplicate is counted once. Root A repeatedly forecasts high probabilities for outcomes that do not occur; Root B is closer to observed outcomes. Root C has only one event and remains `HOLD_-1: SPARSE_HISTORY`. A high-urgency packet from Root A loses to the lower-urgency Root B packet for Jane's chosen `control_condition` gap. No memory is written.

### First negative control

`root-C: one observation` does not establish forecast reliability. Its packet is held, even though it predicts a relevant outcome with high confidence. Tampering with a recorded event breaks the local hash-chain verification.

## Important limitations

This is a **deterministic synthetic demonstration**, not deployed autonomous Jane, live scouts, independent witness verification or self-generated interest. Distinct event IDs under a root model separate reports; they are not cryptographic proof of independent reality. Brier scores on three events are noisy and should not be interpreted as calibrated probabilities in operational settings. The scoring rule and choice policy are prewritten. The local SHA-256 journal checks byte integrity only, not external source authenticity.

## Next natural boundary — JANE 098

Can Jane **detect when a seemingly calibrated scout's reliability drifts over time** and choose when to recheck a source instead of treating historical fit as permanent truth?