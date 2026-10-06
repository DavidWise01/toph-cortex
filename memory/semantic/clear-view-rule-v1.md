---
topic: clear-view-rule
slug: clear-view-rule-v1
tags: [design, toph-cortex, sapphon, biodome, audit]
confidence: 1.0
written_by: root0
session: canon
supersedes: none
updated: 2026-10-06
---

# CLEAR-VIEW RULE v1

**STATUS: CANONICAL / APPEND-ONLY**

Canonical wording:

```text
NEVER ASK:
"what state is the system in?"

ALWAYS ASK:
"what state is BIODOME X in?"
```

Reason:

A TOPH/Sapphon substrate is inspected through its own biodome. State is local
unless an explicit witnessed synchronization/crossing proves otherwise.

Canonical substrate biodomes:

```text
A :: -a+ :: ownership/operator
B :: -b+ :: institutional/access
C :: -c+ :: compute
D :: -d+ :: defense/protection
E :: -e+ :: naming/economic/network-expression
```

Every recursive inspection node carries:

```text
biodome_id
substrate
local_path
clear_view_required = true
```

A recursive walk MUST preserve the parent biodome identity for every child
unless it encounters an explicit biodome boundary node.

Unscoped global-state queries fail the clear-view audit.

Scoped examples:

```text
PASS :: what state is BIODOME A in?
PASS :: what state is BIODOME C in?
PASS :: inspect BIODOME E phase/provenance
FAIL :: what state is the system in?
```

Cross-dome state equality is never assumed:

```text
state(A) = state(B)
```

requires an explicit synchronization witness.

This rule is enforced mechanically by `bin/clear_view.py`.
