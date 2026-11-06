# STOICHEION ISA-256 — Complete 49,152-address lattice

**Snapshot date:** 2026-11-05. **Scope:** addressable schema, not an assertion that 49,152 rules were empirically evaluated.

Dimensions: **256 × 8 × 4 × 3 × 2 × 1 × 1 = 49,152**.

| Axis | Meaning | Cardinality | Source |
|---|---|---:|---|
| Slot | T001–T128; S129–S256 derived inversions | 256 | STOICHEION Full Technical Manual, Chapters 11–20 |
| Domain | D0–D7 | 8 | Manual Chapters 11–19 |
| Arm | −i, −1, +1, +i | 4 | Manual SEEDED-CROSS, Chapter 21 |
| Witness | A, B, C | 3 | Explicit extension, independent observation lanes |
| Executor | symbolic, tensor | 2 | Explicit extension for compiler-equivalence testing |
| ROOT | ROOT0 | 1 | Manual root authority model |
| Closure | CLOSED | 1 | Explicit extension, reserve terminal coordinate |

**Definition:** `address = ((((slot*8 + domain)*4 + arm)*3 + witness)*2 + executor)`, where `slot∈[0,255]`, `domain∈[0,7]`, `arm∈[0,3]`, `witness∈[0,2]`, `executor∈[0,1]`.

**Named register:** All 128 primary TOPH axiom labels transcribed from the supplied manual. Each corresponding Patricia label is mechanically `NOT(T[n])` and occupies S[n+128]. The canonical domain is `floor((n-1)/16)`; home SEEDED-CROSS arm depends on the domain pair: D0–D1 = −i, D2–D3 = −1, D4–D5 = +1, D6–D7 = +i.

**Placement:** One canonical domain/arm per register entry; all other domain/arm positions are explicit cross-references. This yields **1,536 HOME coordinates** (256×3×2) and **47,616 CROSS_REFERENCE coordinates**, not 49,152 independently authored axioms.

**Evidence:** All 49,152 entries begin as `UNKNOWN`; zero runtime observations attested. The symbolic and tensor coordinates name desired execution lanes; they do not certify a working tensor implementation. Only three selected semantic proxies were tested in ISA-256.002. No invented experiments, no quorum, no inferred truth.

**Local generation verification:** Five tests passed, verifying 128 names, bijective 49,152 address round trips, exhaustive row coverage, Patricia pairing and home-coordinate counts. Generated CSV has SHA-256 `bb5c2d4cf6d3ade3b9bb431a282efd42a34fbb7e330ea8438d57adb7661214de` (7,788,072 bytes) from the locally provided implementation.

**GitHub generator:** [stoicheion_lattice_49152.py](../../research/isa256/stoicheion_lattice_49152.py).

**Boundary:** A fully populated coordinate map is not a semantic proof. The next boundary is evidence-carrying evaluation of predicates, exact symbolic/tensor comparison, and B181/B182 mismatch preservation.
