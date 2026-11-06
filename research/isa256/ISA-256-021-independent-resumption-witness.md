# STOICHEION ISA-256.021 — Signed Resumption Witness

Date: 2026-11-06. Local executable test suite: **278/278 passed**, of which 18 are new ISA-256.021 cases. Deliverable: conversation artifact `stoicheion_isa_021.zip`, with Python `isa021.py` SHA-256 `e39310d037290c132583ac287719bb2f78bbea677fcaf965b26c1ffa12fd4af0`.

## Natural invariant

An agent's destination-signed resumption may be *attested* by a separately enrolled witness without conflating the witness signature, the prior source, and actual operational capability. The resumption must have passed the earlier ISA-256.020 proof before attestation is created.

`WitnessAccepted = PreverifiedResumption ∧ PriorRootPin ∧ SignedWitnessEnrollment ∧ DistinctWitnessKey ∧ ExactProvenance ∧ PinnedWitnessReceipt ∧ ValidWitnessSignature`

New envelope `stoicheion.isa256.independent-resumption-witness/1` binds witness ID, named administrator, registry epoch and enrollment digest to resumption digest, arrival file digest, agent ID, developmental stage, journal tip, origin/publisher repository IDs and immutable commit object ID. The envelope explicitly carries an empty effective capability grant list.

## Protocol

1. Verify the ISA-256.020 remote evidence, enrolled publisher and destination-signed resumption using previously trusted pins.
2. Enroll a witness Ed25519 key under a separately trusted ROOT key and signed enrollment certificate. The enrolled key must be different from the destination/publisher keys.
3. Sign the complete canonical witness payload. Verify enrollment digest, signer key identity, exact receipt digest, stage, agent, source repository and commit context.
4. Publish the witness receipt using durable create-only publication: byte-identical retry is idempotent; conflicting replacement is rejected.
5. Retain A/B/C observations independently; no quorum. Do not grant destination tool capabilities by historical inheritance.

## Tests

`python -m unittest discover -p 'test_*.py' -q` → **278 tests, OK**, including 18 new checks covering valid witness attestation, omitted root pin, wrong root/enrollment key, signer substitution, forbidden shared signer, forged or altered receipt, wrong resumption digest, wrong repository/commit, incorrect epoch, unsigned enrollment revision, create-only idempotency/conflict and symlink rejection.

## Crucial limitation

All identities and Git repositories used by the suite are synthetic. A distinct key or a self-asserted administrator name is **not evidence of independent administration**. Therefore the verifier returns `independent_administration_verified: false`, even when the signature is cryptographically valid. No actual cross-administrator attestation, live independently published checkpoint, or externally trusted temporal record was demonstrated. This boundary is an honest software proof-of-mechanism, not field verification. Existing ISA-256 semantics and 49,152 address lattice unchanged; 256 axiom semantic compilation remains incomplete.

## Next natural invariant: ISA-256.022 — Independent Administration Proof

Enroll and verify a real second administrator via a separately authenticated trust channel, publish the signed completion witness at an immutable Git revision controlled by that party, and verify it from an independently retained trust pin. Preserve the original signed record.
