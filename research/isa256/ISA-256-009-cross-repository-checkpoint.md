# STOICHEION ISA-256.009 — Cross-Repository Checkpoint Attestation

**Date:** 2026-11-06. **Status:** Implemented locally; **134/134 tests PASS** (117 retained, 17 new).

## Natural invariant

A root-signed ISA-256.008 checkpoint is accepted only when its SHA-256 agrees with an exact canonical anchor document retrieved from a second Git repository, under a previously trusted commit OID and pinned document SHA-256.

`Accept = CommitTreePathBlobProof ∧ TrustedExternalCommit ∧ TrustedFileDigest ∧ CanonicalAnchor ∧ ExpectedOrigin ∧ ValidRootSignedCheckpoint ∧ CorrectJournalTip`

The external anchor document is a canonical sorted-key UTF-8 JSON object:

```json
{
  "schema": "stoicheion.isa256.cross-repo-checkpoint/1",
  "origin_repo": "DavidWise01/toph-cortex",
  "origin_commit": "<40 or 64 character original-commit OID>",
  "checkpoint_sha256": "<64 character checkpoint digest>",
  "previous_anchor_sha256": null
}
```

The `origin_commit` is an identity field and needs an independently verified binding to the original checkpoint to achieve full provenance. The source path is checked with local Git object integrity, not an authenticated network fetch. The verifier checks anchor continuity against the caller's separately trusted predecessor pin.

## Boundaries

- Anchor file maximum **4,096 bytes**; underlying source pin verification follows ISA006 limits.
- No self-derived trust pins. No automatically accepted new upstream revisions.
- Changed local worktree does not mutate the pinned historical commit.
- Previous A/B/C witness records remain independent and unchanged; no quorum or consensus.
- An invalid journal or changed signed checkpoint fails closed.
- **Local synthetic tests only.** No second remote repository has yet received an authenticated live checkpoint and no independent operator has supplied the source trust pin.
- A separate Git repository is not inherently independently controlled or externally timestamped.
- Full 49,152-address lattice remains unchanged; only T009, T013 and T014 operational proxies execute.

## Test receipt

`python -m unittest discover -p 'test_isa*.py' -q`: **134 tests OK** in the local runtime, including 17 new tests for wrong external commit, source digest, origin, checkpoint tamper, journal alteration, missing pins, path substitution, dirty worktree, noncanonical anchor document, 4KB size bound, and chained anchor continuity.

The runnable files and SHA-256 manifest are delivered in the conversation's `stoicheion_isa_009.zip`. This GitHub commit records the specification and summary, **not** a remote checkpoint publication or source deployment.

## Next bound

**ISA-256.010 — Remote Anchor Acquisition and Independent Trust Pin.** Fetch a commit-identified remote anchor through an authenticated transport or verified repository mirror, require a separately furnished trust root, and fail closed on untrusted publisher, ref drift, or unavailable source.
