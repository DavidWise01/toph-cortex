# Sapphon TOROID-5 Commit-Clock Extension

**Status:** APPEND-ONLY SHARED EXTENSION

Canonical timing cell:

    {{ . | | | | . }}

Exact phases:

    0 -> 1/5 -> 2/5 -> 3/5 -> 4/5 -> 1
    1 = closure witness = next-cycle 0

Mother-Nature gate:

    -1 + 0 + 1 = 0

TOROID-5 controls WHEN a candidate may commit. It does not replace the existing Sapphon semantic/provenance rules that decide WHETHER a candidate is valid.

Applied to all currently assigned Sapphon Primes:

- Prime 01: path/provenance branch may commit only after five timing transfers and balanced closure.
- Prime 02: relative-delta candidate may commit only after five timing transfers; the delta invariant itself is unchanged.
- Prime 03: corroborated-learning candidate must first satisfy its independent-witness rule, then traverse TOROID-5 before append.

Exact-rational benchmark: 10,000 cycles / 50,000 transfers / 10,000 commits / zero phase error.
