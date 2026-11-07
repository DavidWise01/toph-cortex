# JANE — Focal Remembrance v0.20

Date: 2026-11-07. Continuation of Jane focal-cell prototype.

## Natural invariant

A recurrence should change how Jane's one focal cell responds next time, and learned transitions must remain testable after the present context is erased.

Geometry remains **[(1×9) × 1 × (9×1)]**: exactly 9 input positions, 1 focal position, 9 output positions. No new spatial cells or independent agents. The focal cell stores a bounded associative record (up to 32 distinct 9-bit patterns) that counts observed transitions. The 9-cell output shows the most-supported predicted next input pattern. A history-free focus says UNKNOWN.

## Execution

- Pure JavaScript engine core020.js learns 9-bit pattern transitions A→B→C.
- Training vs frozen test mode; altered world A→B→D; reset present context without clearing learned memory; export/import state.
- Minimalist standalone HTML front end: clickable input cells, 19-node visual lattice, one focal memory and predicted 9-cell output, live trace of match/error/unknown.
- 16 of 16 automated Node tests PASS. Inline JavaScript and module syntax checks PASS.
- Fixed deterministic demonstration: after 36 ABC learning observations, 30 ABC test inputs gave **28 correct / 29 evaluated predictions**; changing to ABD gave **10 correct / 20 evaluated**, with nine unknown opportunities. Counts exclude initial no-history observations.
- Local package with full runnable code/test/README and SHA256 is linked from originating conversation as jane_focal_020.zip; this GitHub entry is a specification and test receipt, NOT a hosted executable.

## Limits

This is an associative next-pattern learner using focal internal state; it does not demonstrate general intelligence. The visual fan-in/fan-out is an abstraction, not strict nearest-neighbor propagation physics. Frozen tests reuse familiar symbols in new presentations and do not establish novel-symbol transfer. A stronger next experiment should require delayed prediction, noisy patterns, distractors and performance against frequency-only and random baselines.

Prior STOICHEION constitutional identities and 49,152-address lattice remain unchanged. No ROM, NES emulator, or new security witness infrastructure is involved.

## Next natural invariant

Focal generalization under noise and time delay, with exact disjoint train/test sequences and an independently computed predictive baseline.