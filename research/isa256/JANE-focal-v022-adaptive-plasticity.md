# JANE Focal v0.22 — Adaptive Focal Plasticity

Date: 2026-11-07. One cellular Jane; exactly [(1x9) x1x (9x1)] = 19 positions. Preserve original focal memory snapshot unchanged.

## Invariant
Previously learned pattern transitions should survive a bounded episode of new learning. Measure performance on new symbols against a fresh same-architecture learner exposed to the same training budget.

## Executed results
User-supplied snapshot jane.focal.020/1 has 68 observations, original links 17→68 (22), 68→130 (22), 130→17 (20), and 61/61 historical recorded hits.

Novel cyclic symbol sequence 7→259→448:
- Before training: warmed Jane 0 predictions / 36 probes; all 36 UNKNOWN. Fresh baseline: identical.
- Train both with 12 cycles (36 observations), no external action/authority or extra cells.
- Frozen replay afterward: warmed Jane 35/35 evaluated correct, one initial UNKNOWN; fresh learner 35/35 with one initial UNKNOWN.
- Frozen old-cycle replay after training: 35/35 evaluated correct, one initial UNKNOWN. Old transitions retained.

18/18 new Node logic tests PASS. JavaScript syntax checks PASS. The standalone offline HTML dashboard uses the exact user memory as a fallback and allows retraining, frozen retest and exporting the adapted memory. Executable bundle is the conversation artifact jane_focal_022.zip.

## Limitations
Novel *symbols* are not novel transition *structure*. This is deterministic association memorization. There is **NO measured improvement in learning speed compared with a fresh cell**, and no reason to infer general intelligence or genuine nearest-neighbor cellular automata from a bounded transition table visualized as 19 positions. The app uses JavaScript memory inside its focal state rather than additional spatial cells.

Next boundary: delayed and context-dependent transitions, held-out grammatical structure, calibrated prediction error, and a genuine learning-speed comparison.

No change to historical STOICHEION ISA-256 register or addressing lattice.
