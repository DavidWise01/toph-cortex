# STOICHEION ISA-256.023 — Durable Challenge Ledger

Date: 2026-11-06. Locally tested: **350/350 Python tests PASS**, with ResourceWarnings treated as errors. Exactly 18 new ISA023 test methods; inherited cases are discovered again in the extended test class.

## Natural invariant

A signed witness claim responds to a challenge issued by the verifier for that exact evidence, bounded in time, and usable only once.

Challenge acceptance requires: persisted verifier-issued nonce, pinned evidence context, unexpired lease, verified signed witnesses, and serialized first consumption.

## Implementation

The local reference module isa023.py adds an SQLite ChallengeLedger (issue, status, verify_and_consume). It generates 32 random challenge bytes, stores SHA256 nonce identity, verifier ID, expiry and context hash, binds context to witnessed receipt, source repository, immutable commit, checkpoint SHA256 and enrollment SHA256. A transaction under BEGIN IMMEDIATE changes ISSUED to CONSUMED only when the original ISA022 signed channel verification succeeds. Invalid signature or changed context leaves the nonce ISSUED for a correct future response; expired and already-consumed nonces are rejected. Database connections close cleanly. The module SHA256 is 39126d4b5f045ece24124d5c3900daa4444f58a7d548e90380312a060e369712.

18 new tests include replay after restart, expiration, premature clock, wrong verifier, source/context mismatch, forged signature without consumption, storage and symlink guards, no granted authority. Full suite: 350 tests, 0 failures.

The complete runnable package stoicheion_isa_023.zip is attached in the originating conversation; this GitHub commit records the specification and test receipt, not source deployment.

## Unresolved trust boundary

The fixtures use synthetic identities. Separate cryptographic keys or channels do not prove independent administrators. Independent administration remains unverified. Local SQLite WAL durability is not a distributed trust service; reliable clock, backups, separately authenticated enrollment and remote publication remain production requirements. No A/B/C quorum or inherited capability permissions. Kernel remains 256 paired axiom positions with 49,152 address coordinates.

Next ISA-256.024: independently authenticated issuer enrollment, revocation, and published external challenge acknowledgement.