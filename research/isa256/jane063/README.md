# JANE 063 — Blind Replication

## Freeze

Copied `model.py`, `frozen060.py`, `canonical059.py` byte-for-byte from JANE 062 before replication. Candidate is the unretuned moderate scout (`threshold=.06`, `lookback=13`, `fast_confirmations=2`). No selection or parameter search on the new cases.

## Experiment

Seven new synthetic cases × 30 newly reserved seeded runs (90100–90129) × 720 observations = 151,200 per policy. Heavy-tail jitter introduces 3.5% occasional large excursions; correlated jitter uses AR(1) with coefficient .92; ramps vary speed; cycles are longer and nonuniform. Baseline and candidate see identical inputs.

Run `python -m unittest -q` (16 regression tests) and `python replication.py > results.json`. Then `python build.py` for the dashboard and ZIP manifest.

## Outcome

Although moderate scout lowers aggregate errors 18,459→16,392, heavy-tail jitter errors increase 901→1,057 and correlated jitter errors increase 6,867→6,883. The same cases also regress in spurious transitions. The strict no-regression gate from JANE 062 **fails**; do not promote. Estimated work remains 14× baseline. No post-hoc gate relaxation.

## Limits

These are deterministic, hand-authored synthetic stress distributions, not a genuinely independent third-party study or a sealed external dataset. Benchmarks are not proof of generalization or open-ended recursive self-improvement. The `model.py` file contains the frozen prior tournament and `replication.py` contains the new test. JANE {{j}}, root {{i}}, 27 occupied positions, 27→27.5→1 seam and two 8-scale strands unchanged.