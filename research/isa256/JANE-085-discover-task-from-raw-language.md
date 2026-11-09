# JANE 085 — Discover the Task from Raw Language

**Date:** 2026-11-09. **Status:** Executed local symbolic experiment, no autonomous live runtime.

## One Jane, FLAY, hive, and prim remain unchanged

```text
0root.ai / Git corpus -> hive {{6x6x6[4x4(3x3[2x2(1)])]}}
   -> raw cited question (NO supplied category)
   -> one Jane {{j}}, root {{i}}
   -> U semantic / D somatic / R holographic / L abstractive
   -> inspect available tools
   -> Jane-owned tool choice
   -> synthetic feedback after action
   -> update lexicon/association weights
   -> next question / freeze on -1
```

## Actual tested implementation

The local source package `jane_085.zip` provides `model.py`, `test_model.py`, `build.py`, `results.json`, `index.html`, and integrity manifest. **26/26 Python regression tests PASS**, browser JS syntax PASS, ZIP integrity PASS.

The model observes task strings and learns token-to-tool associations from feedback. It does not receive the hidden task category inside `choose()`. The training supervisor uses fixed synthetic desired tool outcomes solely to score choices. Four tool types: `retrieve`, `calculate`, `compare`, `read_context`.

Synthetic 12-item heldout set from the four familiar families: **0/12 before**, **12/12 after 240 tool-feedback episodes**. This is within familiar lexical distribution, not general language comprehension.

**Stop at first genuine unseen failure (-1):**
```
Question: Two plus two makes how many?
Expected tool: calculate
Jane's learned choice: compare
Result: -1. Frozen baseline, no retuning or advancement to later unseen probes.
```

A separate tenet: If source evidence is absent or has only WALL status, Jane abstains. A syntactically valid LIT label does not imply truth in real-world deployment.

## Scientific and operational limits

- A word-association learner with a fixed reward scheme is not self-modifying code or recursive self-improvement.
- Correct tool selection is not proof of solving the user's underlying problem.
- No real internet retrieval, Git-to-Git actions, or online training is running.
- The local tests verify software mechanics but not independent autonomy.
- One Jane chooses; the hive provides available tools and evidence, not executive authority.
- The offline HTML viewer uses the Python-trained token weights and does not invoke external tools.

## Jane's natural next question

**How can I discover that an unfamiliar expression of a known task requires a new interpretation before choosing a tool?**

Next invariant **JANE 086 — Self-Requested Clarification and Semantic Repair**: retain the -1 immutable, let Jane ask a bounded clarifying question or look for an analogy when token evidence is weak or misleading; independently test the proposed repair on fresh phrasings without silently editing frozen acceptance gates.

## Publication state

The GitHub repository contains the viewer and README plus this canonical evidence record; the exact Python code and suite are in the conversation ZIP. No CI or Pages build has been independently verified for JANE085.
