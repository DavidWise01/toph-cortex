---
topic: referee
slug: deterministic-referee
tags: [design, toph-cortex]
confidence: 0.85
written_by: gamma
session: s2
supersedes: none
updated: 2026-07-14
---

The referee is DETERMINISTIC, not a nested agent. It measures what a script can measure: retrieval hit-rate (did a later session cite this memory), skill-invocation count, and staleness (a fact contradicted by a newer entry → flag, never silently rewrite). The convergence signal is 'diffs got small' — which git shows for free. No embedding-drift mysticism.

**Why:** FluxMem's PEMS never solved the referee because it nested agents. Deterministic metrics can be trusted cold.
**How to apply:** referee.py reads the ledger + citations; it flags, it does not rewrite.
