# STOICHEION ISA-256.010 — Remote Anchor Acquisition and Independent Trust Pin

**Date:** 2026-11-06. **Status:** Implemented locally, **154/154 tests PASS** (134 retained ISA003–009, 20 ISA010). The standalone executable package is available in the conversation; this GitHub record does not claim the code or checkpoint has been remotely deployed.

## Invariant

A remote checkpoint must not be admitted unless a separately trusted, full Git commit OID and expected anchor-file SHA-256 are supplied **before** fetching the source. For accepted input, obtain that exact Git commit through Git transport, verify commit→tree→path→blob with ISA006, validate the canonical cross-repository anchor with ISA009, and validate ROOT's signed checkpoint and journal tip with ISA008.

`Accept = IndependentTrustPin ∧ ExactRepositoryURL ∧ FetchedCommitOID=Pin ∧ CommitTreePathBlobProof ∧ FileSHA256Pin ∧ SignedCheckpoint ∧ JournalTipIntegrity`

A valid Git object proves object identity relative to the pin, not who owns a remote or whether the observed claims are true. An independently trusted source must deliver the pins; the fetched record cannot certify itself. HTTPS remotes are restricted to exact `github.com/<owner>/<repo>[.git]` identity. Local `file://` transport exists solely under an explicit synthetic test flag.

## Tests

**154/154 pass** with 20 new tests: successful remote acquisition from a synthetic local Git repository, bad/missing commit pin, bad/missing digest, wrong path/origin, self-repository anchor, changed checkpoint, changed predecessor, dirty worktree, disabled local transport by default, host substitution, URL credentials/query/path trick, invalid timeout, unreachable remote, and corrupted journal.

Earlier 134 tests remain green. No public remote checkpoint was published or independently witnessed by another administrator in this exercise. No claim of independent network time evidence is made.

## Security boundary

- No quorum or forced consensus among A/B/C.
- Prior evidence and checkpoints are append-only.
- Timeouts and exact ref required.
- Git source proof limited by ISA006 file/object bounds, but a production fetch still needs external transfer quotas, egress policy, and independent publisher authentication.
- The 49,152-address lattice is unchanged; only T009, T013, T014 operational semantic proxies execute.

## Delivery

Standalone source and tests are in `stoicheion_isa_010.zip`, with manifest and README. The SHA-256 of local `isa010.py` is `223141d4e41f8038daf0bcee00779385d96a81a2854e4d8b6fcb640f7ec162b8`.

## Next natural bound — ISA-256.011

Independently supplied trust root / signer enrollment and bounded remote publisher verification; publish an actual checkpoint under independently administered control, preserving provenance and separate A/B/C observations.
