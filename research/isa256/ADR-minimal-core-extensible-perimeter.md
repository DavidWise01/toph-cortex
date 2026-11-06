# STOICHEION ISA-256 — Minimal Core / Extensible Perimeter Decision

Date: 2026-11-06
Status: ARCHITECTURAL DECISION (not a claim of runtime verification)

## Decision

**Freeze the primary governance register at 256 semantic positions**: T001–T128 (TOPH) and their S129–S256 (PATRICIA) falsifiable inversions. Additional behaviors live in externally versioned modules, never as silent changes to these 256 meanings.

The existing 256 × 8 × 4 × 3 × 2 × 1 × 1 = 49,152-address lattice remains an execution/addressing topology, **not 49,152 independently executable axiom definitions**. A 256-position governance register is NOT equivalent to a 256-bit binary instruction word; their encodings must be specified separately.

## Invariant

`CoreSemanticDigest(version) = SHA256(canonical register specification)`

A module may reference core entries but may not mutate their IDs, normative semantics, inversion pairing or provenance. Versioned module loading must fail closed if a core digest differs from the expected pin.

- ROOT0 retains authority over core version governance.
- A/B/C independent witness records retain dissent without quorum.
- Symbolic and tensor paths must be compared on defined executable domains.
- Missing evidence remains UNKNOWN. Mismatch is preserved using bounded counterexample minimization and regression replay.
- New module operations require a namespaced ID, explicit capabilities, resource limits, a provenance record and explicit compatibility contract.
- No automatic module promotion to core authority.
- No real-world signers, independently published trust root or production-grade full 256-axiom semantic compiler have been established by this decision.

## Rationale

A smaller trusted computing base is easier to audit, reproduce and version. Growth should enlarge the **execution and evidence perimeter** rather than silently expanding trusted normative semantics. More axiom slots do not inherently imply better governance.

## Next implementation boundary

ISA-256.011 remains **Independent Trust-Root Enrollment and Remote Publisher Verification**, as previously scoped. This architectural decision constrains that work: its trust registry and signature policy should be an authenticated module, not 257th primary axiom.

The 49,152-address lattice remains intact; only three operational semantic proxies (T009/T013/T014 and paired inversions) are presently compiled and locally tested.
