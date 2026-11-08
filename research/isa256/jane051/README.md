# JANE 051 — Observation Reconciliation

The user's canonical symbolic primitive is unchanged: 1 tensor, 1 Jane, 1 brace, two waldos `{-()+}`, 1 box, 1 toroid, 27 path positions; three ternary state *labels* `(-1,0,+1)`, with 27+3 = 30 counted components; proposed cycle seam 27→27.5→1. The palindrome `{([111222333444555555444333222111])}` is retained. These conventions do not imply a demonstrated physical topology.

## Natural invariant

Repeating a sensor reading does not manufacture independent evidence. The classical reconciliation rule counts at most one unanimous vote from each declared source root; a mixed root or conflicting roots triggers CONFLICT, too few roots triggers INSUFFICIENT, and the rule reports CORROBORATED only after 3 matching source-root reports agree with the historical claim. This rule is deliberately conservative, can abstain on correct claims, and does **not** know the hidden truth.

## Run

`python -m unittest -q` — **40 tests PASS**.

`python model.py` — 1,000 seeded synthetic trials per arrangement.

Open `index.html` directly; it displays recorded results and provides three scenario controls. It does not execute the Python model inside the browser.

## Tested false claim (+1), actual state (-1)

| Source arrangement | Naive false approvals | Group-aware false approvals | Group-aware abstentions/conflicts |
|---|---:|---:|---:|
| Independent 3 roots × 9 repeated readings, 12% errors/root | 44/1000 | 2/1000 | 998/1000 |
| One cloned root × 9 repeated readings | 108/1000 | 0/1000 | 1000/1000 |
| 3 apparent roots × 9 readings, with 20% common upstream failure | 254/1000 | 220/1000 | 780/1000 |

For a **correct** claim with independently imperfect sources, the group-aware rule corroborated 683/1,000; for cloned readings, 0/1,000. Thus the conservative criterion sacrifices availability.

## Scope and limitations

- The 3-root requirement and root identifiers are **engineered assumptions**. A malicious source can mislabel its roots; no cryptographic attestation is in this version.
- A hidden common cause makes apparently independent roots fail together. Group-awareness does not solve unobserved dependency.
- The data are synthetic Bernoulli latent source errors. Repeated measurements within a source share one error state. No actual neural learning, wave equation, or physical homeostasis is claimed.
- The naive baseline gives one vote to the historical claim plus one vote to every reading; the group-aware rule first groups sensor reports and treats the historical claim as a compatibility check. These are **different conservative policies**, not an isolated measure of estimator optimality.
- Correctness is scored against ground truth known only to the harness, not to Jane's reconciliation logic.

## Next boundary

**JANE 052: Learned Source Dependence.** Infer hidden source correlations from their disagreements across varied events, rather than assuming declared roots correspond to independent failure modes. Test whether the dependency map can be learned without leaking hidden truth into the estimator.