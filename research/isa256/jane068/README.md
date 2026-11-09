# JANE 068 — Branch Fitness / 600-address Prim

The JANE 067 baseline was frozen. JANE 068 reserves 15 unused addresses each for three distinct fixed prediction strategies, maintaining the 600-address primitive and 2,000 ms look-ahead. The winning candidate is a shrinkage forecast, not a learned autonomous algorithm.

Run: `python -m unittest -q`; `python experiment.py > results.json`; `python build.py`.

Results: `scout_0` passes all six prespecified held-out no-regression checks. Each of 6 scenarios uses 30 new seeds and 180 observations per seed. Baseline costs 45 abstract work units per issue versus 60 for each scout (+33.3%). Work units are a crude computational proxy, not measured execution latency. The no-regression gate is synthetic and does not guarantee out-of-sample generalization.

No network access, hard real-time guarantee, physical tachyon, 600 agents, independently sourced hive or autonomous recursive improvement are claimed. A 2,000 ms forecast is a delayed-evaluation simulation.

The 45 unused-address reservations are routing metadata. Actual candidate models use one additional algorithm each; reserved address count does NOT imply 15 independent forecasters per scout. The full model and original frozen predictor are included.

Canonical substrate preserved: `{{j}}`, payload `{{i}}`, logical prim `10×5×4×3×1`, 27-position root path `27→27.5→1` and ternary carrier `{{-+-+-+}}`.