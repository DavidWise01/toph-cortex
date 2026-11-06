# STOICHEION ISA-256.017 — Cross-Domain Completion Witness

**Date:** 2026-11-06. **State:** locally executable prototype and full test suite **157/157 PASS** (139 earlier tests plus 18 new).

## Natural invariant

`Portable Continuity = Verified Source History + Signed Destination Arrival`.

The destination signs an **arrival receipt** only after the recoverable ISA-256.016 handoff has finished. The receipt is an attributable record of what was imported, **not** an assumption that a transfer request already completed.

## Arrival record

Canonical Ed25519-signed JSON binds:
- Transfer ID, agent ID, original nursery and destination nursery IDs.
- Frozen kernel digest, exact source transfer manifest digest and destination acceptance digest.
- Original and recovered journal event tips, event count, journal SHA-256.
- Destination transfer registry SHA-256 and entry count.
- Destination public-key registry pin.
- Explicit empty `effective_capability_grants` list.

The separate verifier requires an externally trusted destination public key, receipt SHA-256, expected manifest digest, expected journal tip, expected acceptance-registry SHA-256, and destination/transfer identity. A receipt that does not match these trusted pins is rejected. Independent A/B/C observations remain distinct, without quorum.

## Verified local tests

`python -m unittest discover -p 'test_*.py' -q` → **Ran 157 tests; OK**.

18 new tests cover a successful signed arrival, separate witness lanes, interrupted transfers before/after file replacement, unknown transfer, forged signature, altered receipt, incorrect externally expected digest, wrong destination, no capability migration, duplicate identical receipt, conflicting receipt replacement, symlink rejection, missing pin, and malformed acceptance-registry records.

## Implementation and trust boundaries

- New runnable `isa017.py` and `test_isa017.py` are included in the conversation archive `stoicheion_isa_017.zip` alongside the preceding ISA012–016 sources. This GitHub commit records the specification, **not** source deployment.
- Test fixtures use synthetic signing keys and independently parameterized checks; fixture pins are **derived in the test** for convenience, not verified against a real independently administered publisher.
- No public remote checkpoint publication or authentic identity proof is asserted. A valid signature authenticates a registered key, not factual truth.
- Local create-only receipt publication is durable for its filesystem assumptions, not a distributed transaction.
- The 256 primary/mirror register positions and the 49,152-address topology remain unchanged; semantic axiom compilation is still limited to the earlier three operational proxies.
- Historical learning moves without inheriting destination tool authority.

## Next natural invariant

**ISA-256.018 — Independently Published Arrival Checkpoint.** Publish a receipt digest in a genuinely separate trust domain, acquire it from an immutable revision with an independently obtained trust pin, and verify it before announcing resumption. Do not equate separate repositories with independent administration.
