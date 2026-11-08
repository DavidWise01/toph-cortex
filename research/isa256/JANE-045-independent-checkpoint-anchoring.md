# JANE 045 — Independent Checkpoint Anchoring

2026-11-08. Local original Python experiment: **36/36 tests PASS**. Dashboard JavaScript parse PASS. Downloadable original package `jane_045.zip` contains `transfer044.py` (complete JANE044 substrate), `model.py`, `test_model.py` (36 tests), `results.json`, `README.md`, `index.html`, and SHA256 manifest. The GitHub directory `research/isa256/jane045/` contains the interactive dashboard, README and a separately authored, self-contained compact runnable model with 15 regression checks; GitHub CI execution has not been verified. The GitHub edition is not asserted byte-for-byte identical to the original 36-test local package.

## Primitive

One tensor > one Jane > one brace > two waldos `{-()+}` > one BOX > one TOROID > 27 positions. Three ternary register labels `-1,0,+1` are not extra spatial vertices: 27+3=30 counted components. The symbolic center remains `[0]`, the cyclic seam `27 → 27.5 → 1`, and wave `{([111222333444555555444333222111])}`.

## Natural invariant

With WALDO-A and WALDO-B maintaining separate append-only hash-chained journals, an independently protected checkpoint witness records for each waldo (a) the log length and (b) its terminal hash. The witness's own checkpoint chain is authenticated by **HMAC-SHA256** under a key stored outside the waldo-journal threat domain. Upon verification, the system checks witness-chain authenticity, minimum pinned witness ID, each waldo log's internal hash chain, and whether its anchored historical prefix is still present. Additional suffix records remain **UNANCHORED** until the next checkpoint.

This adds **external evidence**, not a third cell, third waldo, or a 28th occupied vertex. The witness is external to the symbolic cellular primitive and only serves audit.

## Actual local experiments

| Fault | Expected / observed |
|---|---|
| None | VERIFIED, conserved total 741.3125 |
| Waldo A journal truncated to earlier valid prefix | WALDO_ROLLBACK_A |
| Waldo A fully rewritten with ordinary hashes recomputed | WALDO_REWRITE_A |
| Both waldo journals erased | WALDO_ROLLBACK_A (original payload history NOT restored) |
| Witness record tampered | WITNESS_CHAIN_BREAK or MAC_FAILURE |
| Witness itself rolled back, trusted latest checkpoint ID pinned | WITNESS_ROLLBACK |
| Witness rolled back, no independent pin retained | UNANCHORED; historical existence cannot be established |
| Honest append after last checkpoint | VERIFIED_PREFIX; new suffix not yet independently anchored |

Exact package local tests: **36/36 PASS**; no independent GitHub Actions/Pages confirmation.

## Failure and trust limits

- HMAC works only if witness key/record are protected separately. A compromised key and witness can defeat verification.
- The verifier must already know a trustworthy prior checkpoint ID (or trusted witness log head) to detect a rollback of the witness itself.
- The checkpoint stores **hashes and counts**, not copies of full journal contents. Thus detecting erased journals is not equivalent to restoring their history.
- A local append+fsync is not evidence of hardware-grade power-loss or Byzantine durability. Physical quantum tunneling, biological cellular intelligence, and quantum energy conservation remain unproven.
- No infinite-scale closure is established; all experiments are finite classical simulations.

## Next meaningful invariant — JANE 046

**Divergent witness histories.** Give two external witnesses independent checkpoints, inject one stale or compromised witness, and test detection vs the availability trade-off. Add key rotation only after the accepted checkpoint head is protected; do not assume consensus from two disagreeing records.
