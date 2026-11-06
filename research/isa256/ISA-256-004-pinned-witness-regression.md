# STOICHEION ISA-256.004 — Pinned Evidence and Regression Replay

Status: **locally implemented; 36/36 tests passed** (21 ISA-004 plus 15 ISA-003). Snapshot date: 2026-11-05.

## Next invariant

A decision must be bound to the exact source bytes of a named revision. A replay must create a *new* event, never edit the original witness.

`source_sha256 = SHA256(exact_source_bytes)`

A source mismatch returns `EVIDENCE_REJECTED`, not `NORMAL`. Unavailable evidence remains `UNDETERMINED`.

## Implemented contract

- Source identity = source identifier + revision label + expected SHA-256. Revision labels are not independently authenticated.
- Retain existing ISA003 field-level record digest and T009/T013/T014 tri-state symbolic/tensor execution.
- Never execute a received observation if current source bytes fail their trusted pinned digest.
- Store original and minimized reproducer bytes separately, with individual SHA-256 digests, same exact mismatch signature.
- Replay statuses: `REPRODUCED`, `CHANGED_MISMATCH`, `NO_LONGER_REPRODUCES`, `EVALUATION_ERROR`, `CORRUPT`.
- Hash-linked journal adds `FIXTURE_FROZEN`, `REPLAY`, and `RESOLUTION_DECLARED` events. Resolution requires a recorded cleared replay, explicit actor, reason, and offset-aware timestamp. Historical events are unchanged.
- Bounds: 16,384 maximum source bytes; 12 maximum fixtures per journal.

## Observed local tests

**36/36 pass:** 21 ISA-004 tests for source pinning, tamper handling, missing evidence, unknown state, fixture digest/original preservation, exact signature replay, changed mismatch, cleared mismatch, exception, append-only events, duplicate ID rejection, prohibited premature resolution, explicit resolution, ledger tampering and export; 15 existing ISA003 tests. All fixtures and witness observations are synthetic; no live network source authenticated.

## Limitations

Hashes verify byte equality to an independently trusted digest; they do **not** authenticate authorship, timestamp, Git identity, or scientific truth. An in-process hash chain requires a separately anchored tip to resist whole-history substitution. These tests do not compile all 256 semantic axioms; T009/T013/T014 remain the only executable proxies. B181/B182 *concepts* are implemented in a stand-alone fixture contract, but the earlier B181/B182 files were not imported. GitHub specification commit does not imply deployment of Python source or GitHub Pages.

Local executables and test output delivered in `stoicheion_isa_004.zip` alongside this record in the conversation.

## Next boundary — ISA-256.005

Authenticated witnesses with a real trusted public Git blob/commit anchor and executable replay-compatibility controls; reject unverified signatures and provenance version drift.
