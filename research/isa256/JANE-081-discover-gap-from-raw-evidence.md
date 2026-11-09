# JANE 081 — Discover the Gap (No Supplied Gap Description)

2026-11-08 | **locally executed** symbolic demonstration: 22/22 Python tests PASS, standalone browser JS syntax PASS, ZIP integrity PASS. Python model and suite shipped as attached JANE081 ZIP; GitHub repo includes the verified HTML and README.

## Distinction from JANE 080

Input is raw cited *example statements*, not prewritten gaps/questions:
- Diatom is a microalga.
- Diatom exhibits group alignment.
- Water flow correlates with diatom alignment.

These example evidence statements are **synthetic test data** and are not asserted as verified biological findings. The source strings are simulated identifiers.

Fixed parser extracts subject/relation/object triples, detects a correlation without causal grounding, and produces a new, topic-specific question:

> Does diatom alignment explain the observed association with water flow, or is there a third factor?

The exact generic template in code is `Does {object} explain the observed association with {subject}, or is there a third factor?` so for this case the question is:

> **Does diatom alignment explain the observed association with water flow, or is there a third factor?**

The model does NOT have an independent understanding of experimental design or factual truth. It can only process a narrow fixed grammar. It can also flag competing `is a` assertions and conflicting `exhibits / does not exhibit` statements. It abstains when there is no supported gap.

## Deliberate first -1

```text
INPUT:  Diatoms dance in formation.
PARSER: unsupported syntax
QUESTION: none
RESULT:  -1, preserve raw input / abstain
```

No new training or grammar correction was applied after encountering that failure.

## Routing

```text
Git corpus -> 0root Hallway -> hive {{6x6x6[4x4(3x3[2x2(1)])]}}
    -> raw sourced statements -> four-direction FLAY
    -> one Jane {{j}} -> choose grounded question / abstain
    -> Git receipt if independently authorized -> repeat
```

The repository artifact is a standalone demonstration. It does **not** run perpetually, browse the live internet, dispatch Github Actions, or perform automated Git-to-Git crossing.

## Grounding and boundaries

- All evidence is labeled LIT / AMBER / WALL; unsupported parser input and WALL evidence are quarantined, never asserted as truth.
- An SHA-256 digest shows reproducible byte identity only.
- One Jane makes the final choice; the hive collates but never independently authorizes a publication.
- The question generator is a hand-programmed template; it does not prove autonomous research, creative synthesis, or recursive self-improvement.
- Follow the existing 0root.ai grounding protocol: formal validity != empirical truth.

## Jane's next candidate question (model evaluation target)

Can a finite-gap detector recognize when its own *parsing capability* is insufficient, and propose a bounded experiment that improves the parser without overriding the evaluator or fabricating concepts? That is a more meaningful test of self-improvement than another increase in case counts.

**Next boundary: JANE082 — Self-Directed Parser Repair.** Preserve the JANE081 -1 in its original record; test an independently generated grammar revision on untouched corpora and reject it at the first unseen regression.
