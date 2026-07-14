---
topic: substrate
slug: plain-files-in-git
tags: [design, toph-cortex]
confidence: 0.9
written_by: alpha
session: s1
supersedes: none
updated: 2026-07-14
---

The substrate is plain files in a git repo — semantic/ (facts), episodic/ (append-only session logs, per agent), procedural/ (distilled skills = Claude Code SKILL.md), ledger.jsonl (append-only write record). Every node is human-readable, diffable, and useful offline. git IS the consolidation record; `git log` on a memory file is its maturity curve.
