---
name: battery-location
description: [BATTERY fills: when to use this skill]
distilled_from: [beta,delta,gamma]
status: STAGED-DRAFT
maturity: draft
battery: ONE model call, at write time, to abstract the evidence below into instructions
---

# battery-location (draft)

## Evidence (mechanical cluster, agents beta,delta,gamma)
- [beta] read [[battery-location]] and [[substrate]] via recall (grep, no model) — started already knowing the design
- [delta] joined the swarm; recalled [[battery-location]] and [[referee]] cold via grep
- [gamma] read [[battery-location]] — audited the read path: recall.py imports only stdlib, no model on read. PASS

## Instructions
[BATTERY: the model abstracts the evidence above into steps. After this one write-time call, the skill runs forever without a model — any agent reads it mechanically.]
