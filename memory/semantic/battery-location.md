---
topic: battery-location
slug: the-battery-is-at-write-time
tags: [design, toph-cortex]
confidence: 0.95
written_by: alpha
session: s1
supersedes: none
updated: 2026-07-14
---

In any self-evolving memory system the LLM is the battery. TOPH CORTEX moves the battery to WRITE time only (distillation, consolidation) and makes READ time fully mechanical (grep + BM25). The read path never calls a model, so the corpus is usable with the power out.

**Why:** perpetual-motion memory claims hide a model in the read loop. Naming the battery and confining it to write time makes the machine honest.
**How to apply:** never put a model call on the read path; recall.py is stdlib-only by construction.
