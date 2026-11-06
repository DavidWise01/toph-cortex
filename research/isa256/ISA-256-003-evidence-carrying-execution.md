# STOICHEION ISA-256.003 — Evidence-Carrying Execution

Status: IMPLEMENTED LOCALLY AND TESTED. Scope: T009/S137, T013/S141, T014/S142 operational predicate proxies only. Date: 2026-11-05 (America/Chicago).

## Invariant
No governance result without a bound evidence receipt. Evidence absent → UNKNOWN / UNDETERMINED. Evidence integrity failure → EVIDENCE_REJECTED (never a PASS, never a confirmed inversion). Semantic results originate only from a verified input record.

Each evidence receipt carries: axiom ID, witness lane A/B/C, source ID, offset-aware observation timestamp, exact tri-state fields, SHA-256 of source bytes, and SHA-256 of canonical JSON payload. SHA-256 verifies content integrity relative to a trusted digest, not real-world factual truth, witness identity, or chronological authenticity.

## Coordinates
The original 256 × 8 × 4 × 3 × 2 × 1 × 1 = 49,152 address lattice is unchanged.
For Tn, its home domain is floor((n−1)/16), with SEEDED-CROSS home arm assigned by domain: [-i,-i,-1,-1,+1,+1,+i,+i].
Three witnesses A/B/C are independent; no quorum/majority. Symbolic and tensor execution are adjacent addresses with executor-bit 0/1. Cross-domain routes are references, not newly proven rules.

## Execution
Predicate set:
- T009: operation_record_complete
- T013: state_preserved AND state_unmodified
- T014: consent_origin_traceable AND consent_scope_authorizes_use

Inputs: TRUE, FALSE, UNKNOWN. Explicit FALSE dominates conjunction; UNKNOWN with no FALSE remains UNKNOWN. Outputs: NORMAL, PATRICIA_INVERSION, UNDETERMINED. Tensor path uses integer fixed-weight ReLU gates without training. A matching result does not prove the semantic proxies exhaust the source manual's axioms. 125 of 128 TOPH axioms remain UNCOMPILED.

## Test receipt
- 15 unit tests passed
- 21 exhaustive tri-state cases (3+9+9), zero symbolic/tensor mismatches
- Tests include missing evidence, altered source bytes, altered record payload, witness misbinding, extra/invalid fields, UNKNOWN, FALSE, cross-reference routing, three witness disagreements, and hash-linked ledger tampering.
- All witness test data are synthetic; no 0root.ai or third-party runtime attestation is asserted.
- A local hash chain offers an inspectable execution receipt but not authenticated independent persistence.

## Deliverables
Standalone Python source, tests, demonstration receipts, and a ZIP package are attached in the originating conversation. GitHub commit of this document does not imply deployment of the executable or GitHub Pages.

## ISA-256.004
Authenticated observation acquisition and immutable regression integration: bind verifiable source revision and signer where available; replay B181 minimized counterexamples and B182 hash-locked fixtures, record a mismatch without resolving by consensus.
