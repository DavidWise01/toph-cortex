# JANE 048 — Provenance Closure / Independence of the Registry

Date: 2026-11-08. **37/37 local Python tests PASS**. Local dashboard JavaScript passed a Node syntax check. The conversation ZIP `jane_048.zip` contains model, tests, results, HTML, README and a SHA-256 manifest. Committed GitHub `research/isa256/jane048/` includes the Python model, 37 tests, dashboard, results and README. The GitHub Python module and test files were separately transcribed from the locally tested originals; **GitHub CI execution and exact byte identity have not been independently verified**.

## Geometry unchanged

1 tensor → 1 Jane → 1 brace → 2 waldos `{-()+}` → 1 box → 1 toroid → 27 occupied path positions; ternary `{-1,0,+1}` accounts for 27+3=30 counted components without adding vertices. Closure seam `27→27.5→1`. This experiment concerns external trust metadata, not new cellular parts.

## Invariant

`A correctly signed provenance registry != a fresh registry != an accurate description of dependency independence.`

Three configured anchors use distinct HMAC keys/domains and sign registry sequence plus digest. Require at least two distinct authenticated domains endorsing the same root. A separately held monotonic minimum sequence rejects stale signed registries. An independent observation of the underlying dependency map may contradict a validly signed endorsement.

## Exact tested scenarios

| Scenario | Result |
|---|---|
| Three authentic distinct roots | ANCHORED |
| Two authentic distinct roots | ANCHORED |
| Only one authentic root | INSUFFICIENT |
| Three copies of one authentic root | INSUFFICIENT |
| Signed rollback seq 7 when independently pinned seq 8 | ROLLBACK |
| Same signed rollback without trusted pin | ANCHORED (no freshness guarantee) |
| Registry altered without matching anchors | INSUFFICIENT or TAMPERED |
| Fake anchor signature or wrong configured domain | Rejected |
| Two valid authorized signers endorse **false** independence claims | ANCHORED — explicit false-approval counterexample |
| Independent fact/source observations contradict claims | CONTRADICTED |

Five synthetic deterministic conditions were exercised for 1,000 seeds each: clean 1000 ANCHORED; edited data 1000 TAMPERED; rollback 1000 ROLLBACK; one anchor 1000 INSUFFICIENT; two endorsers of invented dependency graph 1000 ANCHORED. These are scenario fixtures, *not* empirical frequencies of real-world attack success.

## Trust boundary

The HMAC roots are chosen/provisioned by the experimenter. Their *actual* administrative independence is an assumption, not cryptographically provable from separate key bytes or labels. A controlling adversary with two authorized keys can sign bad provenance. A trusted externally pinned minimum sequence must itself survive rollback; otherwise freshness cannot be established. The `known_dependencies` comparator is a simulated trusted observation and is not a discovered ground truth. The result demonstrates fail-closed validation in a stipulated classical model; not physical quantum phenomena, autonomous biological homeostasis or infinite-scale guarantees.

## Next natural invariant JANE 049

**Trust-Root Closure:** trace the recursive question "who authenticates the independent authenticators?" until a clear minimal root-of-trust assumption is stated. Test common-mode compromise of all supposedly separate roots, independent pin loss, and bounded evidence without silently adding more witnesses or vertices.
