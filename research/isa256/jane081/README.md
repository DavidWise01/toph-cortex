# JANE 081 — Discover the Gap

**Executed classical symbolic demonstration:** 22 Python unit tests passed. The raw evidence sentences carry source labels but are **synthetic examples**, not factual verification of diatom behavior or other biology.

- Input: raw cited statements with LIT/AMBER/WALL grade; no prewritten gaps or research questions.
- Extractor: a **fixed narrow grammar** (is a, has, exhibits, does not exhibit, correlates with, observed near).
- Detect: conflicting classifications, contradictory observations and correlations lacking a causal explanation.
- Jane: picks a grounded gap or abstains; questions are constructed by programmed patterns. The generated question is a *proposal*, never asserted biological truth.
- Fail closed: unsupported grammar, WALL-only evidence, missing source. The first explicit -1 is **unknown_language**: "Diatoms dance in formation" cannot be interpreted reliably.
- This is not unsupervised natural-language understanding, autonomous research or recursively self-improving question selection.
- No continuous Git/Hallway automation or external internet fetches occur inside this package.

Run `python -m unittest -q test_model.py` then `python build.py`. Open `index.html` locally.

Git evidence → 0root Hallway → hive `{{6x6x6[4x4(3x3[2x2(1)])]}}` → one Jane `{{j}}` → new question → Git receipt, if independently authorized.