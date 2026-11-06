# STOICHEION ISA-256.006 — Commit → Tree → Path → Blob Proof

**Date:** 2026-11-05. **Status:** Local executable prototype verified with **70/70 tests** (15 ISA003 + 21 ISA004 + 17 ISA005 + 17 ISA006). The executable and full tests are delivered separately as `stoicheion_isa_006.zip`; this GitHub record does not claim code deployment.

## Invariant

A witness may execute only when an **externally trusted exact Git commit object ID** resolves, through correctly hashed and typed commit/tree objects, to the expected regular-file blob at the exact path, and that blob matches its independent SHA-256 source digest.

```
Trusted Commit OID
  -> Git commit raw object: verify Git object hash and "tree" header
  -> root tree raw object: verify tree hash and entry mode/name
  -> subtrees: verify each exact entry and tree hash
  -> final blob raw object: verify blob hash, mode, size, SHA-256
  -> version-compatible replay of existing ISA005 fixture
  -> separate witness A / B / C receipt, chained append-only
```

Git object hash is computed over `type + " " + length + NUL + raw_content`; SHA-1 or SHA-256 object format follows the repository's configured Git object format.

## Tested negative cases

Wrong commit, missing object, incorrect file digest, wrong blob pin, nonexistent path, traversal path, directory as file, symlink as file, changed rule, wrong anchor context, invalid witness lane, and deliberate changes to prior witness receipts all fail closed. A changed HEAD or dirty worktree does **not** replace bytes from the already pinned commit. No evaluator call is allowed after source proof failure.

**Bounds:** Git object read <=1,048,576 bytes; evidence blob <=16,384 bytes; unchanged ISA004 maximum 12 regression fixtures. No quorum: A, B, C independent; disagreement preserved.

## Source-backed versus unverified

This implementation proves byte/object/path consistency relative to a separately supplied trust anchor and local Git object storage. It does **not** independently verify that a GitHub organization owns the repository, who authored/signed the commit, that an actor is A/B/C, or that the content is scientifically true. There is no network fetch, remote API verification, or live target attestation.

The 49,152-coordinate ISA lattice is unchanged. Only three T/S predicate proxies (T009/S137, T013/S141, T014/S142) are executable; no claim of full 256-axiom semantic verification is made. B181/B182 mechanisms remain a standalone implementation, not an import of their original source files.

## Reproduction

Unzip local `stoicheion_isa_006.zip` and run:

```sh
python -m unittest discover -p 'test_isa*.py' -q
```

Observed: `Ran 70 tests ... OK` in the current local runtime, using synthetic temporary Git repositories.

## Next natural boundary — ISA-256.007

External repository/commit trust verification and independently signed witness attestations. Do not infer identity from a Git object hash or collapse A/B/C into a quorum.
