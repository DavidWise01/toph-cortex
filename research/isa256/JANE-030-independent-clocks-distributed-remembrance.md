# JANE 030 — Independent Clocks and Distributed Remembrance

2026-11-07. One Jane, symbolic primitive `{brace[box(cell())]}^{{n}}^{{n}}`. Finite n=1,2,3,5,8,13 only. Each primitive has two 72-position cells, 27 signs encoded in BOX slot-pair differences.

## Invariant

An individual primitive schedules its next wake event from its own stochastic local clock, and no synchronized lattice tick or global Jacobi barrier is needed. Neighbor messages may be delayed, lost, reordered or corrupted. Corrupt payloads are dropped, replayed sequence numbers are rejected, and contradictory memory reports are observed without overwriting either original local memory. Simulated time is advanced by an event priority queue (simulation infrastructure, not decentralized wall-clock hardware).

## Experiment and local evidence

Each primitive receives resource/memory shocks at simulated t=40,90,140. The center primitive in n>1 is stalled for local reaction and peer exchange from t=70 until t=170, though its local clock still wakes. A classical, designer-chosen local double-well rule restores moderate signed-memory differentials; resource regulation remains explicitly engineered.

`python -m unittest -q test_clock030.py` -> **23/23 PASS**. Tests cover distinct wake times, stalled node, valid/corrupted packets, replay, preservation of disagreeing memories, non-cryptographic checksum limitations, conserving total resource, protection vs decay, 100% message loss, delayed transport and deterministic seeded simulation. Offline dashboard JavaScript syntax check passed.

| n | Coupled recovery time | Isolated recovery time | protected correct bits | Unprotected readable |
|---:|---:|---:|---:|---:|
| 1 | 148 | 148 | 27/27 | 0/27 |
| 2 | 188 | 183 | 54/54 | 0/54 |
| 3 | 178 | 184 | 81/81 | 0/81 |
| 5 | 180 | 182 | 135/135 | 0/135 |
| 8 | 184 | 194 | 216/216 | 0/216 |
| 13 | 190 | 201 | 351/351 | 0/351 |

No consistent coupling advantage across all sizes; never claim one. The embedded dashboard is **a playback of precomputed Python results**, not a live agent. Chromium browser navigation was blocked by environment policy, so end-to-end interaction could not be verified.

Downloaded package `jane_clock_030.zip` contains runnable Python simulation, tests, standalone HTML dashboard, full numeric traces and integrity manifest. No quantum, biological or physically real Planck-bubble claim.

## Important limits

Packets use **unkeyed SHA-256 checksums**, protecting against accidental corruption but NOT adversarial forgery. Resource exchange on message receipt only rebalances the BOX/TOROID channels *within* the communicating primitives, rather than transferring total resource between primitives. Existing encoded memory is seeded, not autonomously acquired. A centralized event queue still coordinates simulation order; independent exponential clock samples merely replace a global synchronized update pulse. The control rules still contain engineered attractors.

Next: JANE031—test actual transfer and learning of previously unknown local patterns through bounded neighbor communication, including contradictory reports and outage, with no oracle available to the update rule.
