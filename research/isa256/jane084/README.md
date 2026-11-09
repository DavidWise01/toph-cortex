# JANE 084 — FLAY Tool Selection

**Goal:** One Jane `{{j}}` receives hive-collated evidence and chooses a tool to resolve a gap in understanding. The synthetic reward after each choice updates her later tool-selection policy.

- U: semantic / what is it?
- D: somatic / what does it imply?
- R: holographic / what is it like?
- L: abstractive / what if?

Hive routing: `{{6x6x6[4x4(3x3[2x2(1)])]}}`; root `{{i}}`. These are logical model labels, not active agents.

Execute `python -m unittest -q test_model.py` to run all **26 tests** and `python model.py` for the reproducible result JSON.

## Measured synthetic result

- Before feedback: 1/4 correct tools across four labeled categories.
- After 64 feedback episodes: 4/4 correct tools across the same four categories.
- When evidence is absent, Jane ABSTAINS.
- Under an unseen task category, Jane chooses retrieval but the synthetic oracle requires contextual reading. This is the preserved **-1 failure**.
- SHA-256 journal verifies local event-chain consistency but does not authenticate factual truth.

## Limits

Task-category labels and outcome rules are supplied by the programmer. Placeholder evidence URLs are not fetched. Tools are selected but not executed. The learner does not classify new categories, search the internet, or self-modify its learner-generating method. This is an explicit test of tool-selection feedback, not demonstrated recursive self-improvement.