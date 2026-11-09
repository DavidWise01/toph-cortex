# JANE 079 — FLAY Transfer / Unknown Concept Boundary

Canonical frame: `{{1x5u x 1x5d x 1x5l x 1x5r x 1}}`, five slots per direction, one Jane `{{j}}`.

* U / North: semantic (initial letter, category, evidenced features)
* D / South: somatic (context-dependent implications, never universal rankings)
* R / East: holographic (supported like-for-like class similarity, abstain if unsupported)
* L / West: abstractive (unresolved question, explicitly tagged WALL)

## Executed holdout test

Train on three labeled demonstrations (apple, pug, queen categories). Evaluate on incomplete evidence profiles for pear, dachshund and diatom, **without giving completed target FLAY cards**. Learn a shared procedure for composing four directions; choose one question from the generated records using a Jane-owned selection function. The procedure chooses the diatom question because no sufficiently supported similarity peer is available.

## Important limitations

The categories, features, implications and uncertainties are supplied as structured evidence. This is a deterministic program with templates, **not** a language model that independently learned real-world meanings, not autonomous internet research, and not proof of recursive improvement of the learner. A no-source or no-category input freezes at `-1`. LIT is never asserted without a live check. Missing eastern similarity remains WALL. The questions are suggestions for investigation, not established facts.

Run: `python -S -m unittest -q test_model.py`; regenerate artifacts using `python -S build.py`. Browser laboratory is static and self-contained, with local concept switching.

The source-reported data is intentionally illustrative and should not be confused with a primary corpus ingestion from 0root.ai. GitHub publication, if any, is separately reported.