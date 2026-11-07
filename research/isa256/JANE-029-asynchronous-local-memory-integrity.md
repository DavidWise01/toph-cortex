# JANE 029 — Asynchronous Local Recovery and Memory Integrity

Date: 2026-11-07. 22/22 Python unit tests PASS. Standalone offline dashboard, complete Python model, 18 deterministic runs, README and SHA256 manifest are provided in conversation artifact jane_async_029.zip. This record is a specification and measured test summary, not a code deployment.

## Geometry and natural invariant

One primitive is {brace[box(cell())]}; n scales symbolically from one toward infinity. Finite tested n: 1,2,3,5,8,13. Two 72-position cells and 27 memory bits encoded in actual BOX slot-pair differences per primitive. A per-event update activates one primitive, with optionally one neighboring conservative exchange. No full-lattice synchronized Jacobi barrier is needed for this particular model. A stalled primitive is not updated and is excluded from adjacent exchange during reporting sweeps 90–189.

## Test

At reporting sweeps 40, 90, 140 each primitive receives the same synthetic local resource/memory perturbation. Each sweep consists of n pseudo-random primitive selection attempts with replacement, so some nodes may not update at a given sweep; 'sweep' is a reporting unit rather than a simultaneous state update. Use same rules at all n. Compare COUPLED, ISOLATED, UNPROTECTED feedback. Recovery needs worst per-primitive mass error <0.01 and all expected bits correctly readable for 20 consecutive reporting sweeps after last pulse.

## Result

| n | Coupled recovery sweep | Isolated recovery sweep | Protected correct / total | Unprotected readable / total |
|---:|---:|---:|---:|---:|
| 1 | 150 | 150 | 27/27 | 0/27 |
| 2 | 199 | 202 | 54/54 | 0/54 |
| 3 | 198 | 202 | 81/81 | 0/81 |
| 5 | 200 | 201 | 135/135 | 0/135 |
| 8 | 198 | 201 | 216/216 | 0/216 |
| 13 | 200 | 201 | 351/351 | 0/351 |

Total resource conserved to floating precision, protected bits readable at final tick 420. Random seed 17 used. Tests also check invalid indices/ranges, write-locality, replay determinism, stall skips, negative controls, strong-memory inversion and mass conservation.

## Interpretation and limits

This proves local scheduled recovery for these engineered classical dynamics. **There is no demonstrated symbiotic advantage over isolated protected cells.** A scheduler centrally chooses primitive update opportunities; clocks are not yet autonomously generated. The model contains a fixed designer memory-sign feedback law; strong disturbances can still stabilize the wrong signs. Memory content is seeded, not learned. Infinity is an untested scaling direction, not an allocation or a theorem. No physical or quantum claim.

Next boundary: JANE 030 — independently clocked local events, random neighbor outages, memory correctness under cross-primitive contamination, and validation without global schedule or oracle target labels.