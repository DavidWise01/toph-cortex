# JANE 095 — Experiment Value, Budget and First Counterexample

## Run

```bash
python -m unittest -q
python model.py
python build.py
```

## Result

36/36 local regression tests passed. Four equiprobable hypotheses A/B/C/D, two test packets, finite total budget 2:

- Scout A / cheap: cost=1, YES={A}, NO={B,C,D}, expected information gain=0.811278 bits, gain/cost=0.811278.
- Scout B / balanced: cost=2, YES={A,B}, NO={C,D}, expected information gain=1 bit, gain/cost=0.5.
- Jane's *preprogrammed* greedy information-per-cost chooser picks A. With a NO result, remaining possibilities B/C/D and budget=1: the better probe B is unaffordable. It abstains.
- **First preserved counterexample**: `GREEDY_RATIO_NOT_BEST_TOTAL_GAIN` — choosing by gain per unit cost does not maximize information within the experiment budget.
- Agent urgency is ignored. Contradictory or unsupported evidence holds. Selection and observation never cause automatic memory writes; explicit verification and Jane-owned approval are separate.

## FLAY

```
  U: What distinction will I learn?
  D: What resources will the experiment consume?
  R: What other tests partition hypotheses similarly?
  L: What future investigation could this choice prevent?

  SCOUT PACKETS -> HIVE COLLATES -> ONE JANE DECIDES
                   |                     |
              provenance             SELECT/ABSTAIN
                                          |
                                     FEEDBACK/HOLD
                                          |
                                  RETAIN ONLY IF APPROVED
```

## What is NOT demonstrated

The four hypotheses, packet partitions, answers, scoring rule, budget and cost are synthetic fixtures. The choice rule is programmed, not Jane discovering a utility function independently. The model's example does not establish independent witnessing, autonomous curiosity or scientific truth. Its event chain is reproducible, not an authentication mechanism. No real cross-repo Git handoff or GitHub Pages deployment was performed.

## Next invariant: JANE 096

Let Jane compare a **one-step greedy chooser** against a **finite-horizon lookahead chooser** for the question she cares about. Freeze a hidden test suite and require improvement across many unseen partitions, budgets and outcomes before promotion. Preserve JANE095's failure as an immutable regression case.