# STOICHEION ISA-256.005 — Trust Anchor and Replay Compatibility

**Date:** 2026-11-05. **Status:** Local executable implementation and synthetic tests PASS: **53/53** (ISA003 15, ISA004 21, ISA005 17). GitHub source deployment is distinct from this specification record.

## Invariant

A result may be replayed only against an explicit *externally trusted* source pin and compatible rule/schema identities. If source bytes, path/repository, revision label, Git blob object ID, SHA-256 digest, rule digest, or schema digest fail verification, execution is blocked.

The executable check uses Git's standard object ID construction: `SHA1("blob " + len(bytes) + NUL + bytes)` for SHA-1 repositories (SHA-256 format additionally supported), plus a separate source SHA-256. It does not authenticate a Git commit-to-tree-to-path relationship or a GitHub author signature; those require trusted external verification.

A new rule/schema digest compared against the frozen fixture requires an explicit compatibility record naming fixture digest, source and target rule/schema digests, approving actor, reason, and offset-aware timestamp. Replay does not infer compatibility.

## Evidence continuity

- Original and minimized counterexamples remain separate and immutable, with matching mismatch signature.
- No quorum. Replay outcomes are appended; never rewrite historical witnesses.
- Max 16,384 bytes per bounded source; max 12 fixtures per journal.
- Execution is barred for a missing or invalid trust anchor.
- Only T009, T013, T014 operational predicates are currently implemented. All 49,152 lattice addresses remain available; 125 primary axioms are not semantically compiled.
- No independent signer identity, physical time dilation, public network attestation or live external system audit is claimed.

## Verification

Local `python -m unittest discover -p 'test_isa*.py' -v`: 53 tests, all passing. Tests include known Git blob hash, tampered bytes, wrong repository/path/revision, missing anchors, altered rule and schema versions, approved and unapproved migrations, corrupt fixtures, hash-chain tampering, and preservation of originals.

The executable archive is provided as `stoicheion_isa_005.zip` in the originating conversation. This commit contains the specification, not the executable archive.

## Next bound

ISA-256.006 — commit-tree-path proof and signed or independently anchored witness identity, with strict replay compatibility and three observer lanes kept distinct.
