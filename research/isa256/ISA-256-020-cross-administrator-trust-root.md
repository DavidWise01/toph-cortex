# STOICHEION ISA-256.020 — Cross-Administrator Trust-Root Verification

Date: 2026-11-06. Status: locally implemented; **243/243 automated tests PASS**, including **14 directly authored ISA020 test methods**. Complete runnable package: `stoicheion_isa_020.zip` delivered in originating conversation. This GitHub record is protocol/specification plus test summary, not executable code deployment.

## Natural invariant
No independent-source attestation may be accepted on the basis of source bytes or a key derived only from the source being verified.

`ValidResumption = PriorTrustedRootPin ∧ SignedPublisherEnrollment ∧ EnrolledRepositoryIdentity ∧ ImmutableRemoteCommitOID ∧ ExactPathBlobSHA256 ∧ SignedArrival ∧ SignedResumption ∧ NoInheritedPermissions`

The caller must obtain ROOT public key fingerprint, enrollment digest, commit OID and anchor-file SHA-256 from a trustworthy separate channel **before** acquisition. Missing or altered pins fail closed.

## Local executable implementation
`isa020.py` provides `normalize_remote`, `fetch_pinned` and `verify_remote_enrolled_resumption`.
- Restricts production remote format to exact HTTPS GitHub owner/repository locations; no query/fragment/credentials, suspicious paths, or host lookalikes.
- Enforces the fetched GitHub owner/repository identity matches the publisher repository in the signed enrollment.
- Fetches a specific immutable Git commit into a temporary object store with Git object integrity checking; never falls back to HEAD.
- Verifies commit/tree/path/blob and pinned SHA-256, then delegates signed source and resumption checks to ISA018/019.
- Allows local `file://` remotes only with explicit synthetic-test mode; does not equate this with a real independent publisher.
- Preserves separate A/B/C reports, stage-specific learning, and **zero imported effective capability grants**.
- All incoming observations remain source claims even after valid signatures; signed provenance does not establish factual truth or legal identity.

## Tests and limitations
`python -m unittest discover -p 'test_*.py' -q` => **Ran 243 tests: OK**.

New cases cover pinned local Git transport, absent/wrong commits and file digests, tampered enrollment/root, altered resumption, publisher identity mismatch, HTTPS repository identity binding, fake-host URL rejection, explicit opt-in local transport, missing OID and bounded timeout. All identities and remotes in these tests are synthetic; **no actual independent second administrator has enrolled or published a verified checkpoint**.

Production requires independent authentication of publisher administration, resource/egress constraints during Git fetch, verified transport/pinning policy and durable independently signed resumption publication. A git file hash proves byte matching relative to a prior pin, not source truth or independence.

Existing 256 TOPH/Patricia identities and 49,152 lattice addresses unchanged; full 256-axiom semantic compilation remains pending.

Executable `isa020.py` local SHA-256:
`6f58ccc09f5bc84eb65349124a3e3c498cadeb3707c845e66c8af9c367169190`.

## Next boundary — ISA-256.021
A real independently administered publisher supplies a verifiable public-key fingerprint and immutable remote checkpoint via separately authenticated channels, followed by a new signed arrival/resumption event externally anchored in a second administration domain. No quorum, no silent rewriting, no inherited operational authority.
