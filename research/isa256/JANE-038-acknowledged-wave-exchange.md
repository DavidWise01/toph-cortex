# JANE 038 — Acknowledged Wave Exchange / Idempotent Gap Closure

Date: 2026-11-07. **32/32 local Python unit tests PASS.** A standalone HTML dashboard JavaScript syntax check passed. The actual runnable simulation and test source, dashboard and README are committed under `research/isa256/jane038/`. The conversation ZIP `jane_038.zip` contains the local Python model, tests, dashboard, result data and manifest. GitHub Actions and Pages were not separately verified.

## Geometry and conditional modeling

One tensor > one Jane > one brace > two waldos `{-()+}` > one box > one toroid > 27 positions. The three ternary labels `-1,0,+1` give **27+3=30 counted components**, not three added occupied vertices. The 27→27.5→1 closing seam and exact palindromic wave `{([111222333444555555444333222111])}` are preserved.

This run models a **single presumed wave encounter** as a discrete two-party transaction. It does not independently simulate the motion around the cycle.

## Invariant and test

Local waldos carry a unique transaction ID, in-process prepared/applied/aborted ledgers, and a three-value wave register. A coordinator gets both READY responses, logs COMMIT in memory, sends COMMIT with bounded retries, and receives ACK. Each waldo applies its signed-channel permutation once and ignores duplicate COMMIT for the same ID. Opposing signed channels exchange while neutral channels stay local.

### 200 seeded trials per fault setting

| Packet loss | Duplicate probability | Corruption probability | Naive one-swap correct | Acknowledged CLOSED | ABORTED | IN_DOUBT |
|---:|---:|---:|---:|---:|---:|---:|
| 0% | 0% | 0% | 200 | 200 | 0 | 0 |
| 10% | 10% | 0% | 163 | 200 | 0 | 0 |
| 20% | 25% | 1% | 125 | 200 | 0 | 0 |
| 40% | 25% | 3% | 125 | 194 | 6 | 0 |

The six aborted trials in the last case did not apply the wave exchange. At successful closure, original total squared-amplitude proxy **741.3125** is restored by permutation. There were zero unresolved outcomes in the listed bounded random trials, but this is not a universal guarantee.

### Explicit counterexample — permanent partition after COMMIT

With one waldo unreachable after the coordinator records COMMIT, the other can apply its half while its partner remains uncommitted. The transaction becomes **IN_DOUBT**, and the intermediate global squared-amplitude proxy is not conserved. This proves the present model does **not** provide crash-safe atomic exchange. If acknowledgments are lost, idempotent repeated delivery still prevents a double swap on the same reachable participant.

## Limits

- The ledger is only persistent within the running simulation process; not durable across power loss or process crash.
- The in-memory coordinator can directly abort prepared parties when it has not committed; it does not prove safe abort under partition.
- Message corruption is a simulated detectable bit flip; there is no cryptographic sender authentication.
- The physical 27-region Hamiltonian embedding and mapping of 30 waveform characters are not established.
- No proof of autonomous homeostasis, emergent biological symbiosis, actual quantum tunneling or wave-equation propagation.
- GitHub source is a separately transcribed equivalent of the locally tested code; CI on the GitHub copy remains unverified.

## Next natural invariant JANE 039 — Durable Seam Recovery

Append-only transaction journal, crash/restart simulation on both waldos and the coordinator, and bounded reconciliation after link restoration. Test safety (no conflicting commit/abort, no repeated signed swap), conditional liveness under eventual reconnection, and explicitly track global conservation during half-completed transactions. Avoid claiming atomicity without validating the recovery assumptions.
