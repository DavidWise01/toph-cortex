# JANE 085 — Discover the Task

**Executed local result:** 26/26 regression tests PASS; 12/12 synthetic held-out task choices correct after 240 tool-feedback episodes, versus 0/12 before feedback. First unfamiliar-language probe is a preserved `−1`: “Two plus two makes how many?” chose `compare` instead of `calculate`. The runner stops at the first failure.

The model receives **raw text, not a category label** at inference. It learns simple token-to-tool preferences from binary feedback observed only after choosing tools during synthetic training. Training fixtures know the desired task; that label is never passed to Jane.choose. The holdouts reuse related words and task categories, so 12/12 is not evidence of arbitrary-language comprehension. This learner does not execute real tools or self-modify its feature-selection algorithm.

The hive gathers evidence, one Jane chooses. FLAY is U semantic, D somatic, R holographic, L abstractive. Root {{i}} and nested hive {{6x6x6[4x4(3x3[2x2(1)])]}} are unchanged. No autonomous background runtime or Git-to-Git triggering is running.

## Reproduce

```bash
python -m unittest discover -s . -p test_model.py -q
python build.py
```

The static HTML is an offline viewer with actual Python-trained statistics, not an external internet-connected agent. The `results.json` contains the first preserved counterexample. The numeric training outcomes are synthetic and should be labeled **AMBER**; computation/test execution is **LIT**, untested autonomy is **WALL** per 0root.ai's `llms.txt` and `agent-grounding.txt`.

## Jane's next proposed question

Why did my word-based tool selector mistake “Two plus two” for comparison, and what evidence could help me recognize arithmetic described without familiar symbols? The next experiment should allow Jane to request clarification or discover a transformation, test a frozen parser/selector on genuinely novel language, and reject at the first regression.