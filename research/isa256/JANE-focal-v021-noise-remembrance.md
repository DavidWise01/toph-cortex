# JANE Focal v0.21 — Noisy Remembrance and Abstention

**Date:** 2026-11-07. **Local implementation: 19/19 unit tests PASS.**

## Source continuity
User-provided saved-memory snapshot `jane.focal.020/1`: exactly 19 positions; 68 observations; 61/61 correct recorded predictions. Its transition map counts: 17→68:22, 68→130:22, 130→17:20. Those counters reflect repeated familiar-pattern prediction, **not independent proof of generalized learning**.

## Invariant
`Incomplete/noisy sense data -> bounded focal pattern recognition -> next-pattern recall OR explicit UNKNOWN`.

Geometry remains exactly `[(1×9) ×1× (9×1)]`. Nine input positions, a single focal position with bounded transition-memory state, nine output positions. The new `core021.js` recovers corrupted nine-bit symbols using a Hamming-distance threshold; it rejects ambiguous, too-distant or insufficiently observed inputs. Predictions use the earlier frozen transition record; test queries never write to that memory.

## Deterministic frozen evaluation
Each condition has 90 probes cycling through the three **familiar** patterns:
- Clean: 90 correct / 90 probes.
- One flipped bit: 90 / 90.
- One missing bit: 90 / 90.
- Two flipped bits: 61 correct and 29 UNKNOWN, none incorrect among accepted.
- Three missing bits (threshold explicitly relaxed to six known bits): 90 / 90.
- Always-most-frequent-next-pattern baseline: 30 / 90.

These results demonstrate **robust lookup of learned symbols under the tested corruption**, not transfer to novel rules, general intelligence or causal action. The next stronger boundary should introduce withheld novel symbols or temporal transitions and compare actual adaptation after a limited observation budget.

## Deliverable
Executable standalone `index.html`, `core020.js`, `core021.js`, original user-provided saved-memory JSON, 19 tests, evaluation results and SHA-256 manifest are packaged locally in `jane_focal_021.zip` supplied in the originating conversation. JS syntax checks pass. This GitHub record is specification and test summary only, not deployed executable source. No NES emulator or extra constitutional axioms were added.
