# JANE 079 — FLAY transfer under withheld completed cards

**Status:** JANE 079 local experiment executed, 29/29 Python regression tests PASS. Node browser JavaScript check PASS. ZIP archive integrity PASS. This is a symbolic toy learner, not an independent semantic understanding system.

Canonical carrier: `{{1x5u x 1x5d x 1x5l x 1x5r x 1}}`; `{{j}}` is the one Jane; each direction has up to five slots. Direction `U` / north is semantic, `D` / south is somatic, `L` / west is abstractive, `R` / east is holographic.

## Experimental design

The FLAY direction rules were induced from three supervised illustrative demonstrations (apple, pug, queen). Holdout input records identify pear, dachshund and diatom, supplying their names, categories, feature tuples, contextual possible implication, provenance labels and open uncertainty. **No completed FLAY cards are supplied.** The generator fills one position in each direction using learned/common templates:

- U: concept name initial, category and supported input features, AMBER.
- D: contextual implication with an explicit *not universal* qualifier; missing context -> WALL.
- R: an example in the same category when both the trained category and known peer exist; otherwise WALL rather than invented analogy.
- L: a question derived compositionally from the supplied unresolved uncertainty; explicitly WALL, not factual proof.
- Jane's distinct `{{j}}` question-selection function picks a generated question associated with the largest missing supported peer rather than inheriting hive input order.

## Observed outcome

All three holdout FLAY records are generated with a source for every distinction. Pear relates to apple as fruit; dachshund relates to pug as dog; diatom lacks a supported training-category peer and its east lane stays WALL. Jane's programmed decision function selects the diatom inquiry because that evidence gap is larger.

Twenty-nine tests check holdouts, bounded slots, first-letter anchor, provenance, explicit uncertainty, lack of fabricated LIT claims, deterministic rerun, no-source and no-category -1 freeze, no training rule -1 freeze, and Jane-owned selection/abstention. Every unit test passed, including tests expecting specified failure behavior.

## Key limitation / stopping boundary

**Demonstrating transfer between structured input cards is not autonomous discovery.** The learner receives features, categories, uncertain claims and context as input data; its question syntax and selection are programmed. It does not fetch 0root.ai, verify independent empirical truth, prove diatom intelligence, generate an original world, or recursively improve its own learning algorithm. The `-1` checks test missing provenance and missing evidence, not a newly discovered failure of a complex real-world agent. No claim of real AGI, consciousness or physical wave behavior.

## Locally generated release

Exact runnable model, 29 tests, results, README, dashboard and SHA256 manifest bundled in the user-facing `jane_079.zip`. The GitHub dashboard and README are published at `research/isa256/jane079/`. **The Python source/test suite is still in the downloadable ZIP**; do not claim remote CI.

## Next measurable invariant — JANE 080

Test **Jane-originated question novelty against evidence**: remove the supplied uncertainty phrase and require the learner to *infer a specific missing relation* from partial structured observations; compare its question against a fixed generic template and an evidence-blind baseline on unseen topics. Keep Jane's choice separate from hive collation; forbid fabrication; stop at -1 if it cannot produce a specific grounded question.

Seed next question, derived from JANE 079 result:
**What observation could distinguish a diatom population's emergent coordination from ordinary physical or chemical response, without assuming intelligence?**
