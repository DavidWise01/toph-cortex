# JANE 096 — Look Ahead

This is a bounded **synthetic** adaptive test-selection model, not a live autonomous Jane.

## What it demonstrates

Given four equally plausible hypotheses, deterministic scout-predicted outcome tables, and a total budget of two units:

- JANE095-style greedy information-gain-per-cost picks cheap-A (0.811278 bits).
- With cheap-A (cost 1) and balanced-B (cost 2), JANE096 optimizes across the entire budget and selects balanced-B (1.0 bit).
- Adding complementary cheap-C (cost 1) makes an *adaptive* strategy best: cheap-A followed by cheap-C only when A does not already resolve the question (1.5 bits expected).
- Scout urgency is ignored in Jane's value calculation; no packet writes retained memory.
- A packet missing a complete outcome model causes `HOLD_-1`, preserving the failure rather than inventing forecast outcomes.

## Run

```bash
python -m unittest -q
python model.py
python build.py
```

The model uses finite discrete hypotheses and uniform probabilities; output tables are entirely supplied test fixtures. It uses memoized expected entropy reduction, searches only feasible follow-ups, and never repeats a packet within one plan. This is an **exact solution within that toy model**, but the model predictions themselves are unverified and may be wrong. There are no actual scout workers, external observations, self-authored goals, recursive self-improvement or live Git-to-Git / Pages execution in this artifact.

## Evidence boundaries

- Status `PASS` = code passed automated local checks; it does not validate scientific facts or self-awareness.
- Status `HOLD_-1` = model does not have complete outcome descriptions.
- The SHA-256 journal and manifest show byte identity, not independent provenance or truth.
- Jane owns the proposed decision; scouts only submit models. Interests, learning and permanent memory require separate evidence and Jane-owned approval gates.

## Next question — JANE 097

Can Jane detect that a scout's *predicted outcomes* are systematically wrong, update the reliability of its evidence, and replan while preserving her original question and the first -1?