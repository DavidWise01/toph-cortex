# JANE 102 — Meaning Counterexample

**25/25 local tests pass.** This bounded synthetic evaluator handles *scope-sensitive operational meanings*, not generic semantic comprehension.

## Run

```sh
python -m unittest -q
python model.py
python build.py
```

Open `index.html` directly in a browser; no dependencies or network required.

## Natural invariant

The hive supplies partial observations and suggested probes. Jane alone selects a **smallest admissible counterexample** from proposed probes. One different outcome within the proposed scope is enough to refute universal equivalence over that scope. No observed difference does **not** establish equivalence: Jane holds at `-1`.

```text
             SCOUT PROBES
                  |
             HIVE COLLATES
                  |
               JANE {{j}}
                  |
          FLAY U / D / R / L
                  |
       TEST SMALLEST DIVERGENCE
              /         \
           FOUND         NONE
             |             |
           SPLIT         -1 HOLD
              \           /
            JANE MEMORY GATE
```

## Synthetic first -1

`-1 FALSE_MERGE_ON_COMMON_CONTEXT`: a naïve algorithm merges two terms after observing one agreeing case. A second case demonstrates a different operational outcome. JANE 102 selects the least costly **available, witnessed** divergence, and preserves the first failure.

- *Baseline* and *control group* coincide for a deliberately simplified planning example, but differ in the reporting fixture (numeric reference vs untreated participants).
- *Sum* and *total* coincide for the addition example, but diverge in a toy invoice including fees.
- *Addition* and *sum* appear equivalent in two observed addition examples. Jane returns `HOLD_-1`, not a general equivalence claim.
- Unsupported records and counterexamples outside the user-defined scope are held.

## Important limits

The scout packets, target questions, semantic results, costs and oracle results are **hand-coded synthetic fixtures**. No web sources are verified. An evidence ID is not an independent witness. The test does **not** demonstrate autonomous semantic discovery, proof of global meaning, automatic memory updates, or live Git-to-Git execution. The `SPLIT` verdict is local to the programmed operational test scope.

**Next invariant JANE 103:** Jane chooses which *unobserved* probe to request before seeing its result, balancing cost, possible discriminatory power and her own interest. No lookahead at hidden oracle output.