# STOICHEION ISA-256.019 — Enrolled Publisher and Durable Resumption

Date: 2026-11-06. **Local implementation: 212/212 tests passing** in the packaged test discovery run. 17 new tests directly exercise .019.

## Natural invariant

**Verified arrival is not automatic developmental resumption.** A new resumption event is accepted only after a separately trusted enrollment root establishes publisher identity, the pinned Git anchor verifies, and the destination signs an explicit continuity record.

`Resumption = RootPinnedEnrollment ∧ VerifiedPublishedArrival ∧ DestinationSignedResumption ∧ ExactProvenance ∧ EmptyImportedCapabilities`

- SHA-256 pin for external ROOT Ed25519 public key is provided independently.
- ROOT-signed publisher enrollment certificate binds exact publisher ID/repository, public key digest, epoch and ROOT identity.
- Destination resumption receipt binds agent, developmental stage, transfer, trusted enrollment digest, pinned Git commit, arrival anchor, and journal tip.
- Durable create-only receipt publication is idempotent. A conflicting receipt is not silently replaced.
- Independent A/B/C observations remain separate, without quorum; no operational capability is transferred or automatically entrusted.
- The 256 paired governance positions and 49,152-address lattice are unchanged.

## Reproduction

Local runnable `isa019.py`, `test_isa019.py`, inherited modules, full 212-test result, per-file SHA-256 manifest and README are packaged as `stoicheion_isa_019.zip` in the originating conversation. The new module's SHA-256 is `34c5b7feeddf04ecf6f2f61ba769172bf1ad0344f957c7bb60ae01d06e1a0e86`.

A fresh `python -m unittest discover -p 'test_*.py' -q` ran 212 tests in approximately 3 seconds: OK. The original inherited suite has test-class discovery patterns that make the count differ from the former .018 summary; do not infer that 36 new features were added. Exactly **17 new .019 tests** were authored.

## Trust boundary

All .019 test keys, Git repositories, and signatures were generated locally. There is **no independent real-world publisher enrollment, second-administrator signature, or remote Git trust anchor** demonstrated here. A valid signature proves possession of a registered key, not the identity of a human or the truth of an observation. Trust pins must be obtained outside the materials they verify.

This commit contains the protocol and test summary, not the runnable source code or GitHub Pages deployment.

## Next natural boundary

**ISA-256.020 — Cross-Administrator Trust-Root Demonstration.** Verify a real publisher's independently delivered key and pinned immutable remote checkpoint. Publish a separately signed resumption receipt, then independently retrieve and verify its Git provenance, while keeping the nursery's guidance-first purpose unchanged.
