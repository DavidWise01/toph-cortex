# FLAY Mandel–Juliet Toroid v1

Status: append-only semantic extension.

## Primitive

One question is one complete excursion:

```
MANDEL ? -> JULIET -> ANSWER -> MANDEL'
```

The excursion is exactly:

```
OPEN -> ANSWER -> CLOSE
```

Mandel is the bound corpus/current state. Juliet is a temporary tangent workspace. Juliet may walk backward with WHY, compare evidence, answer the question, retain only important supported facts, then close back into Mandel.

## Ternary state

```
-1 = QUESTION / unresolved opening
 0 = ROOT / referent reached for the local excursion
+1 = CLOSED / supported answer bound back into Mandel
```

`+1` means closure for the current walk, not absolute truth. New evidence opens a new excursion; prior closed records are not overwritten.

## Provenance walk

Backward root search:

```
WHY -> WHO -> WHY -> WHO -> ... -> 0
```

Forward factual walk:

```
0
-> WHAT HAPPENED?
-> WHAT :: WHO :: WHEN :: WHERE :: EVIDENCE
-> WHAT HAPPENED NEXT?
-> ...
-> +1
```

The backward WHY walk is allowed to search for the root. The retained ledger is factual. Do not retain conjectural WHY as fact.

## Anomaly / counterfactual rule

When WHAT HAPPENED does not fit the supported chain:

```
anomaly
-> . WHY?
-> walk backward until the divergence is supported
-> record WHAT HAPPENED
-> derive WHAT SHOULD HAVE HAPPENED under the selected rule
-> simulate WHAT WOULD HAVE HAPPENED if that branch occurred
```

Keep the three products distinct:

- ACTUAL = evidence-backed history/state.
- EXPECTED = rule-relative expectation.
- COUNTERFACTUAL = simulated branch.

A counterfactual never rewrites the actual ledger.

## Close invariant

A Juliet excursion may close only when it has a resolved answer. Closing:

1. binds the answer to Mandel,
2. appends supported facts,
3. increments the Mandel revision,
4. moves the excursion to +1,
5. prevents that excursion from reopening or writing again.

Compact form:

```
M ? -> J(-1) -> OPEN(0) -> ANSWER -> CLOSE(+1) -> M'
```

One question. One open. One answer. One close.
