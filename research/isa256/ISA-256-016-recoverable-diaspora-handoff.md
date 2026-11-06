# STOICHEION ISA-256.016 — Recoverable Diaspora Handoff

**Date:** 2026-11-06. **Status:** locally implemented, **121/121 tests PASS**. Executable source, tests, manifest and reproduction instructions are in the `stoicheion_isa_016.zip` conversation artifact. This GitHub entry records the verified protocol; it does not imply the executable was pushed or deployed.

## Natural invariant

`Interrupted transfer ≠ lost learning`

An accepted history transfer has a durable transaction intent that can be replayed to finish the learning-journal and destination-acceptance updates after a crash. Retried transfer IDs do not duplicate milestones. Conflicts are preserved and rejected rather than silently merged.

## Implementation

An `isa016.py` module wraps ISA-256.015 signed origin transfer and destination acknowledgement. Under a POSIX `fcntl.flock`-based per-nursery writer lock, it first verifies the source and destination signatures, immutable source evidence pin, exact journal prefix and existing acceptance IDs **in a staging directory**.

It then durably writes `.isa016.wal` containing canonical, checksummed old/new images for the destination journal and acceptance registry. Local per-file atomic replacements are followed by full signed nursery-history replay and successful journal/registry equality checks. Recovery recognizes either old or intended new images, finishes interrupted work, and deletes the WAL only after both replacements and directory fsync. Unknown changes or corrupted WAL fail closed.

Source history retains independent A/B/C reports; no quorum. Existing historical capability descriptions are not transferred as effective destination permissions.

## Verification

`python -m unittest discover -p 'test_*.py' -q` → **121 tests, OK**. **18 new handoff tests** cover success, crash after PREPARE, crash after journal replacement, crash after registry replacement, retry, malformed WAL, journal/registry conflict, duplicate transfer ID, forged destination signature, witness separation, history-only scope, source fork rejection, incremental transfer, symlink defense, missing pending WAL, foreign destination folder, and source corruption. 103 inherited tests also passed. All signing identities and evidence are synthetic.

## Limits

- A write-ahead journal is **recoverably consistent**, not a single atomic replacement of two files. Requires cooperative single-host POSIX locking and reliable filesystem fsync/rename. Not validated for network filesystems, untrusted same-user processes or Windows.
- Recovery is based on local source proofs and separately supplied trust pins. No new remote publisher or independent external checkpoint is demonstrated here.
- Complete 256 paired ISA identities and 49,152-coordinate addressing lattice remain unchanged; only three original T/S semantic proxies remain compiled.
- Signed origin and destination acknowledgements do not by themselves prove real-world identity, scientific truth, or delegated tool access.

## Next natural invariant — ISA-256.017

**Cross-domain Completion Witness:** independently anchor the *completed* journal tip plus transfer-registry tip, sign a final destination receipt, and verify it in another trust domain before declaring portable learning resumed.