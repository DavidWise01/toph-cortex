# Sapphon Prime 02 — TOROID-5 Extension

Parent: **Relative Difference / Referent Delta**

**Status:** APPEND-ONLY EXTENSION; parent primitive unchanged.

Preserve Δ(A,B)=B-A and shared-translation invariance. TOROID-5 times the commit of a validated delta reference; it does not alter Δ.

Timing:

    . | | | | .
    0 -> 1/5 -> 2/5 -> 3/5 -> 4/5 -> 1

Closure:

    -1 + 0 + 1 = 0
    5/5 = commit witness
    1 -> next-cycle 0

Source clock: `bin/toroid5.py`.
