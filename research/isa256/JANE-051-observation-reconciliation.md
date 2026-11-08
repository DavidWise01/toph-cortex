# JANE 051 — Observation Reconciliation: Repetition Is Not Independence

**2026-11-08.** 40/40 locally executed Python tests passed. JavaScript syntax check passed. Exact Python model, exact 40-test suite, and exact measured `results.json` were committed and verified by Git blob SHA comparison to the local package. HTML and README are also committed, but their GitHub text export differs slightly from the original packaged formatting; exact original HTML is in `jane_051.zip`. GitHub Actions and Pages execution are unverified.

## Canonical primitive unchanged

1 tensor > 1 Jane > 1 brace > 2 waldos `{-()+}` > 1 box > 1 toroid > 27 spatial positions. Three **ternary labels** (-1,0,+1) give 27+3=30 counted components; this is not 30 spatial sites. The return seam remains 27→27.5→1; the 30-sample palindrome is `{([111222333444555555444333222111])}`. No new vertices or actual physical wave equation are claimed.

## Experiment

An authenticated historical claim says the ternary value is **+1**. In the synthetic test, hidden reality is **-1**. The verifier does not read that hidden truth; the scoring harness does.

Compare:
- Naive repeated-vote policy: one vote for the historical claim plus one vote per sensor reading.
- Source-aware policy: group nine repeated readings by their declared origin, assigning at most one unanimous vote per root. A mixed root or conflicting roots produces CONFLICT; fewer than three unanimous roots produces INSUFFICIENT; three matching roots consistent with the historical claim produces CORROBORATED. It does not claim empirical learning of true independence.

### 1,000 seeded trials per condition

| Condition | Readings | Claimed roots | Naive false acceptances | Source-aware false acceptances | Source-aware abstentions/conflicts |
|---|---:|---:|---:|---:|---:|
| Independent source failures (12% error per root) | 27 | 3 | 44 | 2 | 998 |
| Nine clones of a single source (12% error) | 9 | 1 | 108 | 0 | 1000 |
| Three nominal roots with 20% shared upstream failure and 12% individual error | 27 | 3 | 254 | 220 | 780 |

On 1,000 **correct-claim** trials, the group-aware policy corroborated **683** with three independently imperfect roots and **0** with one cloned root. Conservatism improves rejection of copied false evidence, but it sacrifices availability. More importantly, a hidden correlated failure defeats a quorum built only from **declared** source identities.

The simulator initially contained a bug applying shared failure to independent trials; it was corrected before the released results. All 40 tests were rerun after that correction.

## Invariant and limits

**Repeated agreement does not establish independent corroboration.** Grouping known duplicate readings prevents naïve pseudoreplication, but the root names are assumed accurate and their physical independence is not verified. Correlated upstream errors can still make apparently distinct roots agree on the wrong value. This is a controlled classical simulation, not demonstrated autonomous homeostasis, quantum tunneling, biological intelligence or a physical model of sensors.

## Next natural invariant — JANE 052: Learned Source Dependence

Learn candidate shared-failure relationships across diverse observed events without feeding hidden truth into the learner. Compare a static root registry against inferred covariance, track false positives and unidentifiable dependencies, and preserve conflicting evidence without silently declaring a new authority.
