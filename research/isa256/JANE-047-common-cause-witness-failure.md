# JANE 047 — Common-Cause Witness Failure

Date: 2026-11-08. **Original local package: 36/36 Python regression tests PASS.** Browser JavaScript syntax check PASS. Numerical data: 1000 fixed-seed trials per condition.

## Unchanged primitive
1 tensor → 1 Jane → 1 brace → 2 waldos `{-()+}` → 1 box → 1 toroid → 27 spatial positions; ternary `(-1,0,+1)` labels count as three additional symbolic states, not vertices. Closure `27 → 27.5 → 1`. Palindromic envelope `{([111222333444555555444333222111])}`. Witness A/B/C are audit roles, not new cells.

## Natural invariant
**Count independent failure domains, not the number of matching witness names.**

A verified HMAC signature establishes integrity and identity only under trusted keys; it does not prove the historical content true. A source-aware two-of-three rule accepts matching attestations only where at least one pair has disjoint registered dependencies and distinct signing roots. The registry of dependencies is an **assumed trusted external input**; the experiment does not prove that the metadata is honest.

Five layouts tested: three independent witnesses, two sharing an upstream source, all three copying one source, all three sharing the same signing root, and overlapping upstream dependencies. Simulated per-domain common failure probability = 8%; per-witness independent failure probability = 8%. A failed common source generates a common forged history.

| Topology | Naive false accepts /1000 | Source-aware false accepts /1000 | Source-aware abstentions /1000 |
|---|---:|---:|---:|
| Independent | 56 | 56 | 0 |
| Paired source | 109 | 27 | 209 |
| Three clones | 86 | 0 | 1000 |
| Shared signing key | 86 | 0 | 1000 |
| Overlapping dependency | 165 | 19 | 257 |

**Abstention is not correct verification.** For three cloned reports the source-aware approach refuses all 1000 trials, including those where the report is true. Two genuinely independent corrupted sources can still cause false acceptance. The test also rejects signature tampering, duplicate amplification, conflicting statements from one signer, epoch rollback against a known minimum, and forged digests conflicting with a previously pinned digest.

## Downloadable and GitHub artifacts
- The complete, exactly locally tested Python model + **36-test** suite, rebuild script, numeric results, source manifest and interactive dashboard are downloadable as `jane_047.zip` in the originating conversation.
- `research/isa256/jane047/` contains a separately transcribed compact Python model + its own regression tests, measured results JSON and interactive HTML dashboard. The original ZIP is authoritative for the local 36-test result; **the GitHub copy has not been independently tested in CI**.
- The browser dashboard replays fixed outcomes, not continuously running external witnesses.

No physical quantum tunneling, biological homeostasis, Planck physics or learned general intelligence is claimed.

## Next natural invariant — JANE 048: Provenance Closure
Test how an independently authenticated dependency registry can be pinned and audited when source claims change, a root key is compromised, or the trusted registry itself is rolled back. The threshold should remain `INSUFFICIENT` when independence cannot be demonstrated; it must not silently become truth.
