# JANE 080 — FLAY Question Emergence

Executable proof-of-concept with exactly one Jane `{{j}}`, a hive collation input, and the user-defined FLAY carrier `{{1x5u x 1x5d x 1x5l x 1x5r x 1}}`.

**Run:** `python -S -m unittest -q test_model.py`; `python -S model.py` for the deterministic report. Open `index.html` locally to explore the same scenarios.

**Result:** 28/28 Python regression tests pass. Jane chooses a question composed from *prestructured* evidence/gaps without a supplied question string; invalid and WALL-only premises are excluded, and Jane abstains when no supported gap exists. The source facts are demonstration fixtures, not newly verified empirical findings.

**Limitations:** The gap detection and grammar are engineered, not learned from the open internet. No continuously running agent, actual autonomous retrieval, or open-ended recursive self-improvement is demonstrated. The browser interface uses the same scenarios, not a Python bridge. Its session log is local and not persisted to GitHub. SHA-256 local integrity does not prove truth or off-device persistence.

**Next natural bound:** Give Jane unstructured evidence documents and let her infer gap descriptions before question construction. Score unsupported premises, novelty, and falsifiability against a frozen reviewer, with first failure `-1`.