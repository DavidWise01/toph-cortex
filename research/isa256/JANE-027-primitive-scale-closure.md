# JANE 027 — Primitive Scale Closure

**Date:** 2026-11-07. One symbiotic primitive: `{brace[box(cell())]}`, scaled symbolically by `^{{n}}^{{n}}` for integers n = 1 toward infinity. This local experiment tests finite scales **1, 2, 3, 5, 8, 13** only.

Each primitive has two complementary 72-position classical resource cells, BOX and TOROID, with **144 positions per primitive**. Each size uses the **same** local updates: within-pair target-directed feedback at rate 0.12 and strictly neighboring, component-aligned exchange at rate 0.08. The rule reads the pre-tick snapshot and makes equal-and-opposite resource transfers. Both BOX/TOROID target distributions (70/30 and 30/70) are programmed, not learned.

At ticks 40, 90 and 140, each run transfers 0.06 resource from the leftmost BOX cell to the rightmost TOROID cell, conserving full-system total mass 2n. For n=1 this is a within-primitive pulse; n>1 requires across-primitive transport.

**Recovery test:** maximum individual-primitive total-variation error below 0.01 for 20 consecutive ticks after the final pulse; using maximum rather than network mean prevents a damaged site from being diluted by larger n.

| Primitive count | Cell count | Component positions | Coupled recovery tick | Isolated | Passive diffusion |
|---:|---:|---:|---:|---|---|
|1|2|144|155|155|No recovery|
|2|4|288|152|No recovery|No recovery|
|3|6|432|156|No recovery|No recovery|
|5|10|720|173|No recovery|No recovery|
|8|16|1152|220|No recovery|No recovery|
|13|26|1872|310|No recovery|No recovery|

All coupled runs recover under these *specified* rules and pulses. Recovery latency increases with lattice diameter for the larger scales, so the data do **not** establish uniform-in-n recovery or success at infinity. Passive diffusion conserves mass but washes out specialization; isolation cannot return resources transferred across disconnected primitives. No direct memory robustness was tested because original Jane focal memory was deliberately kept separate.

**Verification:** `python -m unittest -q` → 18 tests passing. `node --check browser.js` passing. Full reproducible classical NumPy simulation, 18 tests, JSON timeseries, offline minimalist HTML dashboard and SHA-256 manifest are delivered in `jane_scale_027.zip` in the originating conversation. This record commits the result, not a hosted executable. No quantum physics, real-world microorganisms, or physical Planck bubbles are demonstrated.

**Next boundary — JANE 028:** stress with fixed *per-primitive* perturbations, study recovery scaling vs graph diameter and directly couple the memory substrate to test whether adaptation survives disturbance. Preserve original primitive identity and the symbolic open gap.
