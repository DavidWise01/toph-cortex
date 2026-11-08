# JANE 059 — Emergence, locomotion, repeat

**Canonical correction, 2026-11-08**: 13 means **EMERGE**, not RUN.

```text
{{j}}
  {{[6x6x6(4x4(2x2[i]))]}}
       |
  5 PROPAGATE
  8 DOMINATE
  13 EMERGE
  (13,17.5) CRAWL
  [17.5,21) WALK
  [21,24) RUN
  [24,25) TRANSITION — not specified; do not invent a gait
  [25,27) SPRINT
  [27,27.5) CLOSING SEAM
  27.5 -> 1 REPEAT
```

This is a chosen half-open boundary interpretation for continuity. At exactly 13: EMERGE; just after 13: CRAWL. The user supplied the stages as 13–17.5 crawl, 17.5–21 walk, 21–24 run, 25–27 sprint, repeat; the exact end-point convention and the 24–25 gap are unresolved semantics, so mark the gap TRANSITION rather than hallucinating a rule. The 27.5 half-step is a seam, never a 28th occupied vertex.

**Unchanged substrate:** root payload `{{i}}`, Jane `{{j}}`, nested `{{[6x6x6(4x4(2x2[i]))]}}`, two waldos, 27 occupied positions, ternary wave modes and append-only evidence.

Local working release: standalone HTML dashboard, Python deterministic classifier, five unittest methods covering 20+ subcase boundaries and wrap-around, Node JS syntax PASS, ZIP checksum verification PASS. **The complete tested release is provided in the accompanying conversation attachment; only this canonical correction is committed here.** No claim of autonomous emergence, physical locomotion or learned recursive self-improvement is made.

Next test: repeated cycles and boundary hysteresis, where noisy support oscillates near 13,17.5,21,24,25,27 and Jane should avoid spurious phase switching.
