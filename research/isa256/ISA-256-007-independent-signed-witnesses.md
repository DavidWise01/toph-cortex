# STOICHEION ISA-256.007 — Independent Signed Witnesses

**Date:** 2026-11-06. **Status:** Local prototype implemented, **90/90 tests passed** (70 retained + 20 new). Complete implementation, test suite, and manifest are available in the conversation artifact `stoicheion_isa_007.zip`, not yet deployed into this repository.

## Invariant

No witness record is accepted without verified Git source proof, a pinned public-key registry, matching witness identity and registry epoch, and a valid Ed25519 signature over the complete canonical receipt.

`Accept = ValidGitCommitTreePathBlob ∧ TrustedRegistryPin ∧ DistinctWitnessKey ∧ ValidSignature ∧ ExactSourceContext`

Signed receipt fields: event ID, A/B/C witness lane, Ed25519 public-key ID, registry epoch, observer-provided timestamp (timezone required), commit ID, path, blob ID, content SHA-256, rule SHA-256, schema SHA-256, full observation. Canonical JSON bytes are signed and replayed verbatim. Absence or alteration blocks authentication.

## Independent lanes

A, B, C must possess **different keys** and separate key IDs. Contradictory reports may all authenticate as attributable reports. **No quorum; no consensus; no promotion from authentic signature to empirical truth.** Repeated (lane, event_id) is rejected from an in-memory append-only hash-linked journal.

## Pinned registry and rotation

The caller must provide an externally trusted SHA-256 digest of the exact registry JSON. Changing an Ed25519 key or epoch without providing a new trusted registry pin rejects prior signatures. The implementation does not automatically trust new keys or infer key revocation from elapsed time.

## Tests

Synthetic temporary Git repositories and ephemeral Ed25519 signing keys; no private keys in deliverables. 20 added tests: valid source/signature, wrong commit/content, forgery, altered observation, cross-lane substitution, untrusted registry, shared key rejection, duplicate event, witness dissent, journal corruption, change of registry epoch, timestamp format, rule digest binding, provenance misbinding, and absent signer. Total 90/90 passed locally, including 70 tests from ISA003–006.

## Limits

A signed receipt proves possession of a key registered under a separately trusted registry, **not** a person's legal identity, observation truth, source authorship, or externally synchronized event time. The timestamp is only a signed claim. The journal's history should be independently checkpointed to resist whole-ledger replacement. The register still has 49,152 addresses, with only T009/T013/T014 proxies semantically executable.

## Next boundary

ISA-256.008 — externally anchored journal checkpoints, explicit key enrollment/rotation/revocation, and independently authenticated identity binding; reject unknown keys and unanchored history.
