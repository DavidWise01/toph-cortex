# JANE 071 — First self-selected next question

2026-11-08. **Local experiment**: 24/24 unit tests passed, browser JavaScript syntax checked, ZIP integrity verified.

## Crucial distinction
Jane chooses a question **without being told its topic** at runtime, but this is a *programmed deterministic selector* over a user-prepared evidence set, not a demonstrated autonomous research agent or self-improving question generator.

## Frozen candidate-selection procedure

```text
JANE {{j}} → root {{i}} → 10×5×4×3×1 prim
    |
WAKE (scheduled or new-evidence trigger)
    |
READ unresolved evidence from prior failures
    |
RANK by novelty + testability + consequence - cost
    |
PROPOSE 3 questions
    |
CHOOSE or ABSTAIN (if nothing useful)
    |
RECORD signed? no; SHA-256 integrity-only local audit receipt
    |
EXPERIMENT (future test) → evaluate actual information gain
    |
CHANGE QUESTION-SELECTOR POLICY only under a frozen gate
```

## Self-selected question (highest-ranked)

**Can Jane identify shared disturbance signatures before selecting a forecaster?**

Evidence: JANE069 candidate regressed on correlated bursts in independent replication.

Falsifiable test proposal: Blindly compare a pre-decision correlation detector against the frozen baseline on new burst seeds, with no future observations accessible at prediction issue time.

Second: Can a frozen promotion gate identify distribution shift before promotion?

Third: Which observations reliably indicate a changed noise regime without future leakage?

All three questions were written into source evidence records before ranking. The learner does not yet generate genuinely novel question text, run investigations, or keep itself alive in the background. No empirical gain to the question-generator mechanism has yet been demonstrated.

## Acceptance boundary

- **PASS (narrow):** deterministic question selection; reproducible ranking; 3 candidate limit; abstention; proposed falsifiable tests; immutable baseline on policy updates; bounded policy weights; hash integrity tamper test; no supplied next-topic input.
- **NOT DEMONSTRATED:** novel idea synthesis, autonomous web retrieval or execution, actual recursion of a learner-improving learner, independent quality gain across generations.

## Packaged executable

The exact Python `model.py`, `test_model.py`, `build.py`, `results.json`, standalone `index.html`, README and SHA256SUMS are in the JANE071 ZIP attached in the conversation. This repository contains the dashboard, README and this canonical report. The full Python source is not yet committed here.

## Next experiment Jane proposes

Run **JANE 072: Question-Selection Fitness** with unseen evidence corpora, hidden outcomes, external scoring of expected information gain, and at least two generations of improvement of the question-generation policy. Stop at the first -1. The subject of the next question must still be chosen from evidence, not supplied by the human.
