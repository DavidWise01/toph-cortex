# JANE v0.23 — Mirrored Tesseract Contextual Memory

2026-11-07. **One Jane / nineteen body positions.**

## Invariant

Jane's established body stays `[(1x9)x1x(9x1)]`. Focal `{{i}}` consults sparse memory addressed by `(1x3x6x[9x11x11x9]x6x3x1)`: exactly **3,175,524 possible mixed-radix addresses**. The ten mirrored factors describe a logical memory address space, not ten new agents or a mathematical 4-D hypercube. Occupied addresses alone are allocated.

`(previous-2, previous-1) -> predicted current` is a learned contextual relation, with first-order recall preserved as fallback.

## Actual results

The user's seed snapshot `jane.focal.020/1` retains the original cycle `17→68→130`. New contextual stream repeats `[1,7,3,2,7,4]`; same last symbol 7 has different successors depending on prior context:

- Before training: 0 correct, 0 wrong, 72 UNKNOWN (72 observations)
- Training across 12 repeats: 65 correct, 1 wrong, 6 UNKNOWN
- Frozen replay: **71 correct, 0 wrong, 1 UNKNOWN**
- Old-cycle frozen replay: **35 correct, 0 wrong, 1 UNKNOWN**
- Sparse context records occupied: **6 / 3,175,524**
- `node test023.cjs`: **18/18 tests PASS**
- Embedded JavaScript Node syntax checks PASS

## Implemented artifact

A standalone offline HTML dashboard, `core023.js`, `test023.cjs`, source seed, README and SHA-256 manifest delivered in conversation archive `jane_tesseract_023.zip`. The GitHub record is a specification, not executable source deployment. Browser end-to-end couldn't run due local navigation policy; tests execute the core under Node.

## Limits / next natural boundary

This is a **symbolic associative second-order learner**, not a strictly local cellular automaton or a physical hypercube. Frozen testing repeats the trained contextual stream, so it demonstrates remembrance, not transfer to unfamiliar grammar. Next: sparse-lattice local propagation and variable-delay context generalization under truly disjoint testing.

The existing 256-axiom constitutional identities and 49,152-address ISA perimeter remain unchanged.