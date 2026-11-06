# STOICHEION ISA-256.008 — Externally Pinned Checkpoints and Witness Revocation

**Date:** 2026-11-06. **State:** executable local prototype, **117/117 tests PASS** (90 ISA003–007 retained + 27 ISA008). This GitHub record is a specification and test receipt; Python source and archive are supplied separately in the conversation.

## Natural invariant

`AcceptWitness = VerifiedCommitTreePathBlob ∧ PinnedRegistry ∧ ActiveLaneKey ∧ ValidEd25519Signature ∧ CurrentRegistryEpoch`

`AcceptCheckpoint = IndependentlyTrustedRootPublicKey ∧ ValidRootSignature ∧ IndependentCheckpointSHA256Pin ∧ ExactRegistryTip ∧ ExactJournalTip ∧ ExactJournalLength`

All three witness lanes A/B/C are independent. There is **no quorum**, no automatic reconciliation, and no promotion of signatures into evidence of empirical truth.

## Key lifecycle

- Three distinct A/B/C Ed25519 key identities.
- ROOT-authorized signed `ROTATE` and `REVOKE` lifecycle events, sequential and hash-linked.
- One registry epoch per accepted event; stale epochs fail admission.
- Former key IDs and key material cannot be re-enrolled under another name.
- Revocation blocks future receipt admission; previously recorded receipts remain audit-verifiable against their original epoch snapshots.
- Reject forged ROOT events, reused keys, duplicate revocation, corrupted registry histories, unknown or wrong lanes.
- Sequence determines local effective order; signed timestamps alone are not independent time evidence.

## Journal checkpoint

Root-signed checkpoint binds registry epoch, registry event tip/count, registry digest, ROOT key digest, journal tip/length, and prior checkpoint digest. Verify with a SHA-256 pin **obtained independently of the received record**. A self-computed digest is not an external anchor. Replacing or truncating a journal is detected against a previously trusted checkpoint. A root-signed checkpoint establishes neither legal identity nor the truth of an observation.

## Verified local tests

`python -m unittest discover -p 'test_isa*.py' -q` → **117 tests OK**. New cases cover valid genesis/append checkpoints, missing and wrong external pins, signed witness dissent, altered journal, omitted events, registry rotation/revocation, stale epochs, key reuse, forged ROOT events, signed checkpoint tampering, continuity, and historical replay under old registry snapshots.

**Scope limitation:** Key and source observations are synthetic and locally generated. No external checkpoint publication, third-party timestamping, key owner's real-world identity, or live GitHub witness attestation has been independently performed.

The **256 × 8 × 4 × 3 × 2 × 1 × 1** addressing lattice (49,152 positions) remains invariant. Only T009/S137, T013/S141, and T014/S142 have executable operational semantic proxies. All others remain uncompiled.

## Artifact reproducibility

Complete Python modules ISA003–008, tests, README, test-output.txt, and per-file SHA-256 manifest are in locally produced `stoicheion_isa_008.zip`. The new `isa008.py` SHA-256 is `a3e2e73c62a29db123bc1dba44eebbaf041aff46544a5880af4baf0c63db31c2`. No private test keys shipped.

## Next natural boundary — ISA-256.009

Publish immutable checkpoint digests to a **genuinely independent location** and verify them by source-pinned retrieval, adding identity enrollment and cross-repository provenance without assuming network consensus.
