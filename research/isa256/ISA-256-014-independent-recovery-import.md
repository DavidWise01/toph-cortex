# ISA-256.014 — Pinned Recovery and Idempotent Milestone Import

Date: 2026-11-06. **Status: local prototype, 71/71 tests PASS** (53 inherited, 18 new). The runnable full package is attached in the originating conversation, not deployed from this specification commit.

## Natural invariant

A developmental history can be reconstructed from a separately retained copy if the precise signed journal matches a **previously trusted external checkpoint**. An imported journal must be an exact extension of the destination's verified prefix; a fork remains a conflict and cannot be merged silently.

`Recover = SignedReplay ∧ TrustedPin(Identity, Kernel, Registry, Count, Tip, BytesSHA256)`

`Import = RecoverSource ∧ TrustedSourcePin ∧ DestinationPrefixOfSource ∧ OptionalTrustedDestinationPin`

Repeated import is idempotent. Only missing append-only suffix events are brought forward. All A/B/C witness statements remain independent with no quorum. Historical reflective returns and graduation events remain untouched.

## Implementation

New `isa014.py` adds: `pin_for`, `recover_pinned`, `import_milestones`. Uses the ISA013 fully replayed signed JSONL journal, exact source bytes and hashes, atomic destination replacement, full re-verification and fail-closed fork detection. Existing 256 paired axiom identities and the 49,152-address topology remain unchanged.

The external pin must be independently held in advance. A checkpoint newly derived from the received source **is not independent evidence**. Local cross-folder copies used for testing do not prove independent repository administration or trust.

## Verified test receipt

`python -m unittest discover -p 'test_*.py' -q` -> **71 tests OK**. Added 18 tests for empty pin, signed source import, duplicate import, incremental import, wrong digest/tip/agent, destination pin mismatch, conflicting histories, destination ahead, source tamper, missing source, rollback with a prior pin, source corruption, self import, independent witness preservation, correct recovery, and symlink rejection.

## Limits

Single-writer reference implementation only. Atomic replacement is not multi-writer locking. Source/destination can change between reads under adversarial concurrent writers; production needs immutable commit-identified Git objects and a lock/transaction. This version does **not** fetch a remote repository, publish an external checkpoint, establish a real-world signer identity, or semantically execute every axiom. The local test fixtures are synthetic.

## Next boundary

ISA-256.015 — independently administered remote checkpoint publisher and durable trust-root enrollment, followed by atomic single-writer import under a repository-specific lock. Preserve guidance, reflection and graduation as developmental concepts rather than obedience or conformity.
