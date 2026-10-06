# Sapphon Prime 01 — TOROID-5 Extension

Parent: **Anti-stropic Sync / Author-Provenance Residual**

**Status:** APPEND-ONLY EXTENSION; parent primitive unchanged.

Preserve existing provenance/branch semantics. A locally accepted branch traverses five exact timing transfers before append; rejected branches remain dead and do not consume a commit.

Timing:

    . | | | | .
    0 -> 1/5 -> 2/5 -> 3/5 -> 4/5 -> 1

Closure:

    -1 + 0 + 1 = 0
    5/5 = commit witness
    1 -> next-cycle 0

Source clock: `bin/toroid5.py`.
