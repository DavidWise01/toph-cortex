---
topic: swarm-shape
slug: one-substrate-many-agents
tags: [design, toph-cortex]
confidence: 0.8
written_by: beta
session: s2
supersedes: none
updated: 2026-07-14
---

Multi-agent shape: each agent keeps its OWN episodic log (episodic/<agent>/), but semantic facts and procedural skills are SHARED. The ledger tags every write with its agent. Cross-agent citation is the swarm's learning signal: when agent β cites a fact agent α wrote, that fact has earned its keep swarm-wide. A new agent joins already knowing the swarm's memory cold (CLAUDE.md + recall, no model call).
