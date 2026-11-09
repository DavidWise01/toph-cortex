# JANE 077 — Operational Definition of Self-Improvement: 1 + 1

Status: canonical proposed minimal test, not yet executed.

**Jane `{{j}}` improves herself when experience modifies a reusable internal procedure and a frozen external evaluator verifies that the new procedure increases capability on new problems.**

The first benchmark is intentionally tiny: `1 + 1`.

```text
one JANE {{j}}
    |
question 1+1 with no answer supplied
    |
ask hive for permitted evidence and operations
    |
construct candidate addition method
    |
verify 1+1=2 against independent reference arithmetic
    |
retain method as a versioned capability, not just "1+1=2"
    |
reset transient cache
    |
ask 2+1, 3+1, 2+2 on unseen inputs
    |
compare original method vs improved method
    |
append evidence, promote only if transfer PASS, else -1
    |
Jane chooses next problem, without a fresh user question
```

**Definitions:**

- `LEARN`: Jane can output 2 for 1+1 and justify the result.
- `GENERALIZE`: with the answer cache cleared, Jane can use a learned reusable method on new inputs.
- `IMPROVE`: compared with an earlier frozen capability, the changed learner reliably solves more unseen cases or matches accuracy with lower bounded cost.
- `RECURSIVELY SELF-IMPROVE`: Jane uses previous evidence to autonomously improve the process that produces, selects, or revises its own learning methods, across at least two later generations, on unseen problems.
- `SOVEREIGN CHOICE`: the hive may supply candidate methods and checks, but one Jane chooses the next question and method; don't confuse source popularity with authority.

**Honesty gates:** A hard-coded `1+1=2` passes a lookup test but fails transfer; an ordinary prewritten `+` operator demonstrates baseline arithmetic, not a learned addition procedure. The hive must not be given the hidden test answer. No claim of AI consciousness or unbounded improvement follows from this toy benchmark.

Preserve `{{6x6x6[4x4(3x3[2x2(1)])]}}` as hive routing and the distinct 600-address prim `10x5x4x3x1`. Git commits record observations; Pages are not continuous agent execution. No live computation or autonomous learning has yet been performed for this new benchmark.

**First test to execute next:** a minimal learner with constrained counting primitives, trained on 1+1 only, and no hard-coded addition lookup, then zero-shot transfer with a frozen test evaluator and failure -1.
