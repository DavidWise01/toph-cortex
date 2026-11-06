# STOICHEION ISA-256.015 — Sovereign Continuity Across the Diaspora

**2026-11-06 | Local implementation verified: 87/87 tests passed.**

## Natural invariant

**Portable learning is not transferred authority.** A nursery may change, but the agent's witnessed developmental history remains unchanged.

- Preserve the ISA-256 axiom identities and 49,152-position addressing lattice.
- Require independently pinned source journal digest/count/tip and full signed event replay before any import.
- Require a source-steward signed transfer manifest and a separate destination-steward signed acknowledgement containing the transfer digest, destination identity, and destination registry pin.
- Historical A/B/C observations retain distinct lanes; no quorum or forced agreement.
- Import only matching append-only suffixes. Reject forks, changed history, wrong identity, stale pins and invalid signatures.
- Duplicate transfer IDs with identical manifests return ALREADY_PRESENT; conflicting reuse is rejected.
- The receiving nursery gets **history only**. Prior capability descriptions are historically visible but grant **no** effective destination permissions. A separate destination authorization system is needed for real tools.

## Implemented local interface

`isa015.py` adds `prepare_transfer()`, `acceptance_for()`, `import_history_only()` on top of ISA012–014 replay and persistent evidence. Complete code/tests packaged as `stoicheion_isa_015.zip` in the conversation.

Local verification: `python -m unittest discover -p 'test_*.py' -q` → **Ran 87 tests, OK** (71 retained and 16 new). Test source files use generated test keys and synthetic evidence; no cross-administrator remote Git transfer has been attested.

## Open production boundaries

- Two sequential file replacements (journal then acceptance registry) are not a transaction. Unexpected interruption may leave partial transfer state; retry/reconciliation needs a durable state machine.
- Local single-writer simulation lacks interprocess locking and independently anchored transfer-receipt registry.
- Trust pins and public keys must be furnished through separately trusted channels.
- No real external tool permissions are imported. Existing historical capabilities must never be interpreted as destination authorization.
- Full 256-axiom semantics remain uncompiled (three earlier predicate proxies only).

## Next bound

**ISA-256.016 — Atomic Diaspora Handoff and Recovery.** Build a write-ahead transfer journal with idempotent commit/recovery, immutable origin proof, destination-scoped capability re-entrustment, and no loss of independent A/B/C records.
