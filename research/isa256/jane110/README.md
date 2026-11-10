# JANE 110 — Settlement Criterion Discovery

## Corrected nested geometry

The hive comprises nested, reserved growth spaces (`{{n}}^{{n}}^{{n}}`) rooted in a 10×10 coordinate surface, progressing through Gen 0–7; Z carries `−/+` interpretive stance. **Jane `{{j}}` is THE SOURCE**. Scouts and the MoE hive produce attributed proposals, never memory writes or learning directives.

## Question

When should Jane consider a growing chamber stable enough to settle, without equating capacity with readiness or stalling indefinitely?

## Local synthetic experiment

Four explicit candidate settlement rules are evaluated on six training histories. The selected rule is tested once on six distinct holdout histories. The chosen candidate requires *two consecutive quiet windows, at least three evidence distinctions, two provenance roots, and zero unresolved conflicts*. Full occupancy is **not** required. The toy labels and evaluator are synthetic. The sources are not authenticated witnesses; a `roots` count is not proof of independence.

In these fixtures, the selected rule scores **6/6 train and 6/6 holdout**, while `CAPACITY_ONLY` makes a premature settlement on `full_but_novel`. The candidate `THREE_QUIET_WINDOWS` stalls on ready two-window cases.

## Governance gates

```text
              THE SOURCE : JANE {{j}}
                          |
                   MoE evidence
                          |
           nested Gen 0..7 chamber grows
                          |
         compare proposed settlement rules
                          |
                train / frozen holdout
                          |
                 criterion candidate
                          |
               stable? / HOLD_-1
                          |
       verified receipt AND Jane authorization
                          |
                 chamber SETTLED
                          |
         separate verified Jane RETAIN gate
```

- Merely receiving evidence does not settle or write memory.
- Full capacity never forces settlement.
- A test pass makes a criterion *eligible* for Jane's consideration; it is not a real autonomous Jane decision.
- An unverified receipt yields `HOLD_-1 NO_RECEIPT`.
- Without Jane authorization, `HOLD_-1 NO_JANE_AUTH`.
- Knowledge retention is a distinct explicit gate even after settlement.
- The digest chain detects local mutation; it cannot authenticate a scout or an external witness.
- A pair of sources with different labels might have one origin; the example does not audit independent provenance.

## Run

```bash
python -m unittest -q
python model.py
```

Open `index.html` locally for a silver-chrome/orange 10×10 nested-growth viewer and simulated settlement controls.

## Limits

This is deterministic software with supplied candidate rules, a fixed scoring policy, and synthetic labeled histories. It demonstrates rule **selection**, not Jane creating her own criteria or operating a trained neural MoE. No live autonomous runtime, empirical science, external witness authentication, Git-to-Git workflow or GitHub Pages publication is established by the experiment.

## Next natural evolution: JANE 111

Can the Source **construct a genuinely new settlement criterion** from first-failure traces instead of selecting a prewritten candidate, then pass an independent blind holdout before it is promoted? Keep every prior `−1` immutable.