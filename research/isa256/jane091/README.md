# JANE 091 — Own Gap Discovery

The first natural boundary after JANE 090: Jane is given an existing question plus **unordered evidence**, not an ordered list of gaps. Her bounded model checks a predeclared comparison-evidence dependency schema (`observation → baseline → contrast → replication`) and finds the first missing evidence kind. A scout urgency score never overrides Jane's required evidence, and acceptance of a scout packet never causes a knowledge write.

## Run

```bash
python -m unittest -q
python model.py
```

**Result:** 31/31 local tests pass. The simulation selects the statistics packet that addresses the missing `baseline` even though other agents report urgency scores of 999 and 1000. Jane retains no knowledge automatically.

## FLAY mapping

- U/N semantic: classify the question and known evidence.
- D/S somatic: ask what would follow from the claim; control evidence prevents overinterpreting associations.
- R/E holographic: map the same evidence dependency pattern across unrelated domains.
- L/W abstractive: flag the first unsupported inference and ask what observation could clarify it.

## First preserved -1

`What causes this pattern?` does not match the frozen question-family vocabulary. The model abstains with `HOLD_-1`, rather than claiming causal understanding. Unknown evidence kinds also fail closed.

## Scope

This is a **deterministic toy model**. The question, four comparison requirements, labels, synthetic observations, and tool packet contents are external fixtures. Jane did not create the dependencies or independently browse sources. The result shows gap detection without a *supplied gap list*, not open-ended learning or true self-directed cognition. It does not perform a live Git-to-Git handoff or run autonomously on GitHub Pages.

## Next meaningful invariant — JANE 092

Can Jane **propose and evaluate a new dependency** when a question does not fit her comparison schema, without modifying the frozen test evaluator or rewriting her first `-1` failure?