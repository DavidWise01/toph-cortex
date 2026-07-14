---
name: recall-first
description: Before acting on a task the swarm may have seen, mechanically recall shared memory (grep/BM25) FIRST — start already knowing, spend no model call to remember.
distilled_from: [alpha/s1, beta/s2, beta/s3]
maturity: seed
battery: one model call, at write time (this file); free forever after
---

# recall-first

When a swarm agent picks up a task:

1. Run `python bin/recall.py "<task keywords>"` — deterministic, offline, no model.
2. Read the top facts + any procedural skill it surfaces. You now start already knowing what the swarm learned.
3. Only AFTER recall, act. At session end, write an episodic entry citing `[[topic]]` for anything you used, and stage any new fact as a diff.

**Honest limit:** deciding *what* is worth writing, and abstracting a cluster into a skill like this one, needs the model (the battery) — once, at write time. This file then works forever without it: any future agent reads it mechanically.
