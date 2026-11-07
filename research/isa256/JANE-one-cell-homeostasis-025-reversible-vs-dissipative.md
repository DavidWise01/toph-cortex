# JANE / [()] — Invariant 025: Reversible vs Dissipative Homeostasis

2026-11-07. One homeostatic cell: six faces × (six BOX + six TOROID slots) = 72 amplitude/probability positions. Focal remembrance remains separate and unchanged. The gap remains symbolic.

## Tested invariant

**Conservation of total amplitude norm does not, by itself, imply return to homeostatic balance.**

Compare two local 72-slot update models on a graph of 180 undirected links:
1. Classical dissipative symmetric averaging, which conserves total probability by construction and mixes toward uniform distribution.
2. Reversible amplitude evolution, composed of five layers of two-state real orthogonal rotations with angle 0.23 radians. Each layer preserves squared norm, and each step is explicitly invertible.

Both begin with the same probability distribution: uniform except a 0.12 injected displacement. Apply identical externally forced 0.12 probability redistributions at ticks 96, 192 and 256; the external forcing is nonunitary even for the otherwise reversible arm, and is NOT intrinsic quantum dynamics.

Criterion: after the final disturbance, total variation distance from uniform < 0.01 for at least 20 consecutive ticks.

## Executed 320-tick results
- Dissipative: first sustained threshold recovery at **tick 288**; TV at tick 320 approximately **0.000569**.
- Reversible: **no sustained recovery** by tick 320; TV at tick 320 approximately **0.601579**.
- Total probability drift: 0 within floating precision; squared norm drift < 2e-13.
- Original focal remembrance hash-equivalent throughout by isolation.
- Python unit tests: **19/19 PASS**.
- Browser JavaScript syntax check: PASS.
- Interactive offline HTML, Python model, tests, complete numeric series, README and SHA-256 manifest are packaged as conversation file `jane_homeostasis_025.zip`. This commit records the test, not executable deployment.

## Interpretation and limitation
The tests validate these particular mathematical rules, not a physical Planck bubble, actual quantum state, emergent intelligence or self-regulating adaptation. Averaging is explicitly dissipative. Unitary-like evolution conserves norm but does not generally mix to equilibrium. Memory persistence is guaranteed by isolating memory from perturbations; this does not test resilience of coupled memory.

## Next invariant
**JANE / [()] 026 — Local Homeostatic Feedback without Memory Erasure.** Couple the 72-slot probability field to a bounded, local error-sensing feedback channel; test response to external perturbations against fixed averaging and unregulated coherent controls, measuring recovery cost, conserved quantity, and interference with learned focal memory. No new cells or witnesses.
