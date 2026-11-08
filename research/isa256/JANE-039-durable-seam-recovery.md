# JANE 039 — Durable Seam Recovery

Date: 2026-11-07. Source and reproduction dashboard committed under `research/isa256/jane039/`. **Local original package: 40/40 Python tests PASS, Node syntax check PASS.** Its exact local source and tests and JSON result traces are distributed as the conversation file `jane_039.zip`. The separately authored GitHub model is a compact equivalent; it includes its own 24 regression tests, which have not been run in online CI.

## Canonical geometry
User primitive: 1 tensor > 1 Jane > 1 brace > 2 waldos `{-()+}` > 1 box > 1 toroid > 27 occupied positions. Three ternary mode labels `(-1,0,+1)` yield 27+3=30 *counted components*. Palindromic wave `{([111222333444555555444333222111])}`. Closing seam `27→27.5→1`. No additional spatial vertices.

## Invariant
**Logged decisions survive process restart, but safe retries do not imply immediate atomic global resource conservation during partitions.** Each participant durably appends PREPARED, COMMITTED or ABORTED; coordinator logs an immutable COMMIT or ABORT decision before dissemination. Reconstructing state from journal history makes repeated COMMIT idempotent. Per-node JSONL writes call flush and fsync. The failure model assumes complete writes, stable intact storage and benign nodes; torn writes, media loss and malicious actors are excluded.

## Executed numerical experiment
200 seeded trials per fault condition. Two-party prepare, coordinator decision, left-party commit with right party temporarily disconnected, restart by new Python objects using the *same on-disk journals*, then up to 80 reconnection attempts.

| Independent message loss | CLOSED | ABORTED | IN_DOUBT | Final norm conserved |
|---:|---:|---:|---:|---:|
| 0% | 200 | 0 | 0 | 200/200 |
| 10% | 200 | 0 | 0 | 200/200 |
| 20% | 200 | 0 | 0 | 200/200 |
| 40% | 200 | 0 | 0 | 200/200 |
| 100% | 0 | 0 | 200 | 200/200 |

The full-loss case records ABORT but cannot deliver it; report **IN_DOUBT**, not completed ABORT. With only the left waldo COMMITTED, combined squared amplitude is **802.3125**, compared with **741.3125** before and after full closure. The transient imbalance is real within this *classical amplitude-proxy model*. A permanently unreachable partner can remain blocked forever.

## Limits
The experiment simulates process restarts, not media damage, torn writes, or actual physical wave tunneling. It employs a central coordinator and assumes eventual reconnection for liveness. No general distributed atomicity/consensus theorem, autonomous homeostasis or physical Planck-bubble behavior is demonstrated. The dashboard is a client-side protocol walk-through and precomputed trial table, not a running filesystem-backed simulation.

## Next boundary
**JANE 040 — Peer-led recovery / coordinator crash:** two waldos need to reconcile a known durable decision without depending on one permanently available coordinator; quantify cases that safely remain blocked under a true permanent partition, and the minimum extra durable evidence needed for recovery.
