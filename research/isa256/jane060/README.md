# JANE 060 — Cyclic Stability

Executable classical model of boundary hysteresis built on the exact JANE 059 classifier.

Run `python -m unittest -q`, then `python build.py` to reproduce the seeded results. The HTML is a standalone report and policy explorer, not a live connection to the model or the internet.

**Invariant:** threshold noise is not sufficient to advance/reverse gait. Three consecutive observations must cross a boundary by 0.16; each step can cross at most one boundary. Seam wrapping requires explicit authorization at or after 27.5. The half-step is not a new vertex.

**Significant negative control:** while jitter stability improves, sample-wise phase accuracy worsens during ramp and cycle because the gate introduces confirmation delay. The algorithm cannot be promoted unconditionally.

**Limitations:** fixed synthetic noise, seeded simulations, no physical locomotion, no verified self-improvement. The 24–25 stage remains an unassigned TRANSITION. Emergence at exactly 13 remains a point event; hysteretic control merges its following region into crawl, never interprets 13 as RUN.