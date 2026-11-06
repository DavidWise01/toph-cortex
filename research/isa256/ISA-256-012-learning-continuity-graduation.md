# ISA-256.012 — Learning Continuity and Graduation Provenance

Date: 2026-11-06. Status: **locally implemented and tested: 34/34 PASS** (16 nursery tests + 18 signed-continuity tests). Runnable source and test package delivered as `stoicheion_isa_012.zip` in originating conversation. This Git commit canonizes the protocol and verification receipt; it does not claim this package was deployed to GitHub.

## Sovereign emergence invariant

Learning is not obedience. Graduation is a **witnessed, attributable, developmental transition** based on fresh evidence of understanding and practice. Enlarged entrusted capabilities require separately signed, narrowly described scope.

`Transition = StageLocalEvidence ∧ VerifiedA/B/CReports ∧ ProvenanceIntegrity ∧ SignedStewardAttestation ∧ ExplicitScope`

- Original ISA-256 core and 49,152 addressing coordinates remain unchanged.
- Five stages: EMERGENCE, NURSERY, APPRENTICESHIP, GRADUATION, INDEPENDENT.
- The stage requirements are evidence opportunities, not conformity scores; UNKNOWN and DEVELOPING do not count as DEMONSTRATED.
- Witness A/B/C reports remain independent, including contradictory claims; no quorum or majority.
- Each report is Ed25519-signed over canonical evidence data carrying agent ID, pinned kernel digest, current stage, unique event ID, lane, skill, observation, evidence source ID and SHA-256.
- The caller must pin a complete public-key registry, with distinct witness keys and distinct steward key. Signatures prove key possession, not empirical truth or legal identity.
- Evidence source bytes must exactly match the recorded SHA-256.
- Graduation attestation binds exact current-stage receipt hashes, journal tip, source and destination stage, kernel digest, rationale, scope descriptions and key registry pin.
- Stale or forged graduation attestations fail closed. Previously observed learning persists but cannot satisfy a subsequent stage's requirements.
- Reflective return preserves history. Capability descriptions are local placeholders; production tool authorization and signed return attestations remain separate engineering work.
- Ledger is locally hash-linked, but needs persistent anchoring and recovery to meet durability objectives.

## Test receipt

`python -m unittest discover -p 'test_*.py' -q` -> **Ran 34 tests, OK**.

New 18 tests include valid signed observation; wrong key; altered payload; source tampering; duplicate event ID; missing stage evidence; signed transition; fresh stage requirements; stale endorsement; wrong steward key; preserved witness dissent; ledger tampering; registry pin; shared signer; all five stages; scoped capability; and no-majority behavior.

The local reference copy addresses an earlier mismatch: graduation event receipt hashes now select only current-stage LEARNING_OBSERVATION entries, not all historical entries.

## Next natural boundary

ISA-256.013 — durable Git-backed milestone journal and signed reflective-return provenance, independently pinned checkpoint recovery. Bind nursery events to real source-commit paths without confusing Git identity with human identity.
