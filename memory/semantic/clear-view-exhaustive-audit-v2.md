# CLEAR-VIEW v2 — Bounded Exhaustive Adversarial Audit

**Status:** append-only audit layer over canonical CLEAR-VIEW RULE v1.

The canonical rule is unchanged:

```text
NEVER ASK:
"what state is the system in?"

ALWAYS ASK:
"what state is BIODOME X in?"
```

This audit is exhaustive over the explicitly bounded finite space below:

- all 5 biodome roots A-E;
- every explicit boundary sequence of length 0..6 over A-E;
- all 25 ordered source/target biodome pairs;
- all 625 ordered dome/phase collision combinations per paired dome/phase space;
- all declared valid spelling variants;
- all declared malformed biodome tokens;
- the complete declared finite query grammar;
- three deliberate mutation classes.

It is **not** a mathematical claim of exhaustive coverage over every possible
Python tree or every possible natural-language string.

The independent ancestry oracle requires:

```text
dome(node) =
  explicit_boundary(node)
  OR
  dome(parent(node))
```

Never:

```text
dome(node) = neighbor guess
dome(node) = global mutable state
dome(node) = silent merge
```

Executable:

```text
python bin/test_clear_view_exhaustive_v2.py
```

Target seal:

```text
0e / CLEAR-VIEW v2 BOUNDED EXHAUSTIVE ADVERSARIAL PASS
```
