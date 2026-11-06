# ISA-256.022 — Independent Administration Evidence Boundary

Date: 2026-11-06. Local reference implementation: 296/296 automated tests PASS, including 18 new test cases. Runnable source and test archive delivered as stoicheion_isa_022.zip in the originating conversation. New module local SHA-256: 5b4ce91c8b36903826b0c2d2a5f9d2f6e97917fb4c22b2e363445ddd1d6d71fd.

## Natural invariant
Distinct cryptographic keys do not prove distinct real-world administrators.

An ISA-256.021 witnessed resumption can be corroborated by two enrolled, distinctly keyed and separately pinned channels: identity and publication. Both attestations bind the same verifier challenge, signed witness receipt SHA-256, source repository and immutable Git commit, checkpoint file digest, and witness enrollment digest. Different declared administrator identifiers and distinct Ed25519 keys are necessary but NOT sufficient for independent administration.

`Corroboration = VerifiedResumption + IdentityAttestation + PublicationAttestation + PriorTrustedPins + MatchedChallengeAndGitProvenance`

## Implemented and tested
`isa022.py` defines `attestation_payload`, `verify_channels`, and a fail-closed `AdministrationError` boundary. It checks complete exact channel maps, signed attestations, source pin matching, separate signing keys, forbidden signer reuse, exact context, and nonempty challenge requirements. The signer verifies fixed canonical JSON; no inherited tool capabilities are granted. A/B/C historical witness records remain distinct and unvoted.

`python -m unittest discover -p 'test_*.py' -q` -> **296 tests OK**. Added 18 new cases: successful dual-channel corroboration, explicit refusal to claim independent administration, missing channel, weak/replayed challenge, altered/repinned attestation with invalid signature, substituted key, incorrect existing pin, shared or forbidden signer, same declared administrator, wrong commit/repository/checkpoint and refusal to accept unverified resumption or imported authority.

## Trust limitation
The test identities and keys are synthetic. **No external administrator has attested independence, and no separate authenticated administration has been demonstrated.** The result always includes `independent_administration_verified: false`. Two signatures, declared administrators, or two simulated trust channels cannot by themselves establish that fact. The prior channel and attestation pins must be obtained over a separate trusted route in real deployment; this protocol does not establish that route. Real challenges need cryptographically unpredictable nonces, issuance records, expiry and replay protection. The simple fixture challenge validates binding but does not prove entropy. No off-site publication, production authorization, GitHub Pages deployment or 256-axiom semantic compiler is claimed.

The 256 paired axioms and 49,152 lattice addresses remain unchanged.

## Next natural invariant: ISA-256.023
Authenticated external trust enrollment and independently witnessed milestone verification, with durable nonce issuance/replay tracking and independently published immutable checkpoint. A verifier must remain UNVERIFIED unless genuine administration provenance can be established.
