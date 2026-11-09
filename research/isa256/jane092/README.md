# JANE 092 — FLAY Examines FLAY

A bounded, offline experiment of method revision.

## Test

```bash
python -m unittest -q
python model.py
python build.py
```

## Invariant

Jane preserves the JANE091 `HOLD_-1` for "What causes this pattern?", then evaluates a causality method **proposed in a synthetic scout packet** against an unchanged evaluator. The model promotes the proposal only if it recovers at least three failed holdouts with **zero regressions**. It does not invent the method independently.

- Frozen comparison requirements: observation → baseline → contrast → replication.
- Candidate causal requirements: observation → temporal order → alternatives → intervention/natural experiment → replication.
- 4 recovered causal cases, 0 comparison regressions, 1 unknown-family abstention.
- 20 local unit tests passed.
- Scout urgency cannot force Jane's choice.
- A changed method registry is distinct from verified semantic memory; the latter needs an explicit Jane retention gate.

## Preserved negative boundary

An unsupported question remains `HOLD_-1`. A candidate that damages the original comparison method is rejected. The experiment is a deterministic model with scripted proposal options and a frozen holdout—not an autonomous self-modifying AI.

## Next natural boundary

**JANE093 — Method Genesis:** Give Jane *several partial scout observations*, not a complete causal dependency chain, and test whether she can assemble and verify a new method, including abstention when contradictory or insufficient.