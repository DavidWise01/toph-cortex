# STOICHEION ISA-256.018 — Independently Pinned Arrival Checkpoint

**2026-11-06. Local implementation: 176/176 tests PASS (157 previous, 19 new).**

## Natural invariant

**Verified arrival precedes developmental resumption.** A handoff receipt and a second publisher's checkpoint must agree on exact source identity, transfer ID, destination, journal tip, transfer registry digest and evidence history. A signed assertion cannot bootstrap its own trust.

`AcceptArrival = VerifiedSignedArrival ∧ PinnedPublisherKey ∧ ExactPinnedGitCommit ∧ ExactPathBlob ∧ PinnedAnchorFileSHA256 ∧ ValidPublisherSignature ∧ MatchedProvenance ∧ NoImplicitCapabilityGrant`

## Executed verification

- Verify the Ed25519-signed destination arrival receipt from ISA-256.017 using independently provided receipt and journal pins.
- Verify a separately enrolled publisher public key via a trusted SHA-256 fingerprint.
- Navigate exact *local* Git commit/tree/path/blob objects from a supplied immutable commit OID; reject symlinks and invalid paths.
- Enforce canonical JSON encoding and fixed anchor-file size.
- Check publisher-signed checkpoint fields: origin repository name, publisher repository name, source receipt digest, transfer, agent, destination, journal tip, registry digest and previous anchor SHA-256.
- Require empty effective capability grants. Preserve original A/B/C independent observations; no quorum, no historical rewrite.

## Reproduction

Python `python -m unittest discover -p 'test_*.py' -q` → **176 tests OK**, including 19 new ISA-256.018 tests. Synthetic fixtures include a new local Git repository and ephemeral Ed25519 signer. New tests cover wrong commit, file hash, signer/key pin, origin, publisher, journal, transfer, registry, predecessor, changed HEAD, symlink path, traversal, non-matching anchor and repeat verification.

Local executable `isa018.py` SHA-256:
`93de85b060c086ad358a74a2c28ff3dfccf5e409669660451bce9b91cc8de449`

Complete code/tests/README/manifest supplied as `stoicheion_isa_018.zip` in the conversation. This GitHub commit is a specification and test receipt, not executable code deployment.

## Boundary

**Independent administration has NOT been demonstrated.** A separate locally created Git repository is not independent real-world publisher infrastructure. No authenticated live remote retrieval, independent publisher identity enrollment, external timestamp, or cross-administrator checkpoint has been established. Signature verifies possession of the pinned key, not factual truth. Existing ISA-256 identities and 49,152 lattice addresses remain unchanged; full axiomatic semantic compilation remains pending.

## Next

**ISA-256.019: Independent Publisher Enrollment and Durable Resumption Witness** — verify a checkpoint from a separately administered public source through externally obtained pins, then append an independently signed resumption event without inheriting tool permissions.
