# JANE 054 — Predictive Drift and Familiar-State Recurrence

Canonical proposed primitive (unchanged): **1 tensor > 1 Jane > 1 brace > 2 waldos `{-()+}` > 1 box > 1 toroid > 27 positions**; three ternary mode labels (-1,0,+1), 27+3=30 counted components, *not* a 30-vertex Hamiltonian graph. Closing seam `27→27.5→1` is unchanged. This study works at the software observation layer rather than claiming real biology or a Planck-scale object.

## Run
`python -m unittest -q` (42 local tests)
`python model.py > results.json`
Open `index.html` in any modern browser (fully offline, no server).

## Experiment
Five observers A–E, two hidden common-failure groups (`ABC` and `ADE`); five synthetic environments: stable, abrupt switch, gradual switching probability, periodic alternation, and transient switch-and-return. Jane is exposed to only raw five-channel readings, **never underlying truth or source labels** in her monitor. After 100 initial training observations, evaluate 500 further observations per seed. 35 seeds per case and method -> 17,500 decisions per bar. Baselines: permanently frozen grouping and a continually recomputed 40-sample rolling grouping. Third model: hash-linked versions and local hysteretic detection, 20-observation uncertainty/probation, and memory lookup for a matching previously encountered pattern. The hash chain is unkeyed and not adversarially authenticated.

## Results
In periodic environment: frozen false approvals **3,252**, rolling **2,636**, versioned **2,275** (17,500 comparisons each). The versioned approach also abstains on **3,770** observations, appends **65** new memory versions and recognizes **98** returns to old versions across 35 seeded experiments. It trades coverage for fewer false approvals; it isn't a pure Pareto improvement and the 65 unnecessary/ambiguous revisions reveal memory growth pressure. In steady state versioned falsely detects changes, appending 15 new versions across 35 trials; not a perfect drift detector. Across gradual drift the versioned approach gives 2,403 false approvals versus rolling 2,448, while abstaining 2,010 times.

## Crucial limitations
`assess()` separately tests potential true and false claims on the same sample; these counts are *not mutually exclusive* because independent group votes may support both under the defined at-least-two-groups rule. They measure each tested proposition's support, not calibrated probabilities. The regime inference is statistical, not true causal discovery; identities are labels in the generator. The model assumes fixed 40-sample windows, five observers and stationary error rates within each regime. No learned bodily self-regulation, quantum tunneling, physical wave exchange, or infinite-scale guarantee.

## Next boundary
**JANE 055 — Bounded Memory and Recurrence Compression:** can Jane recognize repeated regimes without allocating unlimited new versions, while preserving immutable observations and refusing to erase contrary evidence? Compare number of anchors, regret and false approvals under 100+ periodic regime returns.