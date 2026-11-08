# JANE 054 — Predictive Drift, Recurrence and Versioned Observation

**2026-11-08.** Local `python -m unittest -q` completed **42/42 PASS**. Offline HTML script syntax verified with Node.js. Full reproducible experiment and rebuilt dashboard are provided as `jane_054.zip` in the originating conversation. The committed GitHub directory `research/isa256/jane054` includes Python source, tests, HTML, README, and measured results; online CI and GitHub Pages are **not** claimed to have run.

## Geometry left unchanged

One tensor > one Jane > one brace > two waldos `{-()+}` > one box > one toroid > **27 occupied positions**. The ternary modes `-1, 0, +1` mean **27+3=30 counted components**, not a 30-position spatial ring. Closure seam **27→27.5→1**. This is an observer learning simulation and does not assert new cell geometry or physics.

## Natural invariant

**A return to a previously observed relationship is not necessarily a new relationship.**

Jane uses five observed channels, builds source-dependency groupings without knowing the synthetic truth labels, records hash-linked versions of each new dependency model, and can reactivate an earlier version if current readings resemble that version. It enters UNCERTAIN when evidence departs from the active regime, then either retains the old regime, revisits a previously known regime, or appends a new version after a fixed probation period.

This is a *conditional property of the specified detector*; the detector also creates spurious versions in unchanged environments and can misclassify correlated error as a stable source relationship.

## Experimental design

Five sources A–E, with two potential shared-error triplets ABC and ADE. Five synthetic regimes: steady, abrupt switch, gradual probabilistic change, periodic alternation, transient switch and return. Each method receives 100 initialization events followed by 500 scoring events, for **35 seeded runs × 500 = 17,500 decisions per scenario/method**. Truth labels are used only in the generator and evaluator, not in the learning algorithm.

Controls: frozen old grouping; rolling 40-sample grouping; versioned drift-aware grouping. Metrics distinguish false-claim support, true-claim support, explicit uncertainty/abstention, number of appended versions, and recognitions of earlier versions.

### Selected results

| Environment | Frozen false approvals | Rolling false approvals | Versioned false approvals | Versioned abstentions | New versions | Revisits |
|--|--:|--:|--:|--:|--:|--:|
| Steady | 1,571 | 1,459 | 1,426 | 1,060 | 15 | 14 |
| Abrupt | 3,733 | 1,729 | 1,634 | 1,750 | 59 | 8 |
| Gradual | 3,381 | 2,448 | 2,403 | 2,010 | 69 | 5 |
| Periodic | 3,252 | 2,636 | 2,275 | 3,770 | 65 | 98 |
| Transient | 1,973 | 1,947 | 1,787 | 2,280 | 47 | 47 |

**The principal observation:** in the cyclic test, explicit regime recognition produces **98 visits to previously learned states** and fewer false approvals than a frozen grouping. But the abstention cost (**3,770/17,500**) and additional versions (**65 across 35 runs**) prevent any claim that recurrent patterns are perfectly recognized or that memory is efficiently bounded. The steady scenario makes the false-alarm limitation explicit: 15 new versions and 1,060 uncertain decisions without any underlying change.

## Measurement cautions

- The model's `supports()` function separately assesses support for the *true* and *false* claim; these are not mutually exclusive tallies in cases where clusters support both propositions. Treat them as proposition-support counts, not a calibrated classification accuracy, posterior or probability of truth.
- The simulated hidden dependency is a synthetic shared binary error, not a causal discovery model for real sensors. A correlation fingerprint alone cannot prove shared cause.
- Snapshots use unkeyed SHA-256 to make ordinary local changes detectable, not to authenticate external authors or withstand rewriting by someone able to regenerate the entire chain.
- Regime labels and the oracle truth never enter `Monitor.step`. The detector's thresholds, window length and probation are explicitly engineered.
- No autonomously homeostatic physical cell, quantum tunneling, or infinite scaling has been demonstrated.

## Next natural boundary — JANE 055: Bounded Recurrent Memory

Stress 100+ cycles and require a fixed budget on *active prototypes*, while preserving append-only historical evidence. Check whether merging near-duplicate state descriptions can bound memory without incorrectly joining distinct regimes. Report the tradeoff between storage, false approvals, abstention, and ability to recover an old regime after a long absence.
