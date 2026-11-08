# JANE 046 — Checkpoint Witness Divergence

2026-11-08 | **30/30 local tests PASS**, standalone HTML JS syntax PASS.

## Test formulation

One Jane primitive remains 27 cyclic positions and the ternary labels (-1,0,+1), with the `27→27.5→1` symbolic seam. The term *witness* here names simulated independent checkpoint verifiers, not an added cell, waldo, or graph vertex.

Three distinct HMAC-SHA256 witness keys may attest a checkpoint `(epoch, previous root, root)`. The verifier starts at an independently pinned genesis checkpoint and requires explicit hash-chain ancestry. Each witness can vote only once per epoch, and double-signing is flagged. Two matching authenticated reports out of three establish an eligible decision **if at most one witness is compromised**. A contradictory minority report is retained as divergence, not erased.

## Locally tested outcomes

| Condition | Outcome |
|---|---|
| 3 matching trusted reports | VERIFIED |
| 2 matching reports | VERIFIED |
| Two different roots without quorum | CONFLICT |
| Two matching reports + 1 conflicting | VERIFIED_WITH_DIVERGENCE |
| Tampered MAC | INSUFFICIENT |
| Stale or replayed epoch | INSUFFICIENT |
| Missing intermediate chain | INSUFFICIENT |
| Anchored complete chain | VERIFIED |
| Witness double-signs a fork | INSUFFICIENT; EQUIVOCATION flagged |
| No witnesses survive | INSUFFICIENT |
| Two colluding witnesses forge same root | **VERIFIED_WITH_DIVERGENCE**, demonstrating quorum failure outside trust model |

These are deterministic software tests with in-memory artificial identities; they do not prove historical truth in the presence of collusion. The pinned checkpoint cannot restore absent bytes. The scheme does not provide physical independent timestamping, quantum wave conservation, or evidence of biological homeostasis.

## Published

- `research/isa256/jane046/model.py`: runnable HMAC witness verifier
- `research/isa256/jane046/test_model.py`: thirty unit tests
- `research/isa256/jane046/index.html`: interactive static outcome explorer
- `research/isa256/jane046/README.md`: reproduction and threat model

The originating conversation artifact `jane_046.zip` includes the richer locally generated dashboard, source, tests, results, hashes and build tool. GitHub Pages and GitHub Actions are not verified.

## Next natural invariant — JANE 047

**Witness independence under common-mode failure.** Two-of-three majority is fragile if identities share a machine, credentials, state source or rollback channel. Test correlated failure and separately pinned checkpoints; compare mathematical quorum assurance with actual independent evidence. Do not add new Hamiltonian vertices.
