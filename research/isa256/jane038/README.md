# JANE 038 — Acknowledged Wave Exchange

User primitive: 1 tensor, 1 Jane, 1 brace, two waldos `{-()+}`, one box, one toroid, 27 path positions plus ternary labels -1/0/+1, 27→27.5→1 seam.

This experiment does **not** simulate the underlying 27-position wave propagation. It tests one transaction at the presumed gap encounter. `model.py` is an in-memory two-party exchange protocol simulator. `test_model.py` provides 32 unit tests, `results.json` contains 200 seeded trials per condition, and `index.html` is a standalone visual playback / phase explainer.

To run: `python -m unittest -q` and `python model.py`. No external dependencies.

### Measured results

| Loss, duplicates, corruption | Naive correct / 200 | Protocol CLOSED | ABORTED | IN DOUBT |
|---|---:|---:|---:|---:|
| 0%, 0%, 0% | 200 | 200 | 0 | 0 |
| 10%, 10%, 0% | 163 | 200 | 0 | 0 |
| 20%, 25%, 1% | 125 | 200 | 0 | 0 |
| 40%, 25%, 3% | 125 | 194 | 6 | 0 |

### Limits

The protocol stores the decision in the simulated coordinator but does not persist transactions across real process crashes. On a permanent partition **after the COMMIT decision**, only one waldo can update, creating an **IN DOUBT** state; squared amplitude may then temporarily diverge from the global baseline. The coordinator directly aborts prepared-but-not-committed nodes in this in-process simulation. Packets have simulated integrity checking, not authentication. No perfect failure-tolerant atomic commit is claimed. This is classical reversible register manipulation, not quantum tunneling, proof of a Hamiltonian embedding, or a self-regulating living cell.

**Next candidate invariant:** Crash-safe seam closure: retain recovery decisions in a journal and reconcile a half-committed wave exchange after reconnection without replaying it twice.