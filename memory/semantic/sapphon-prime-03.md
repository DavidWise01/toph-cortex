# Sapphon Prime Primitive 03 / 05

**Name:** Witnessed Deliberation / Corroborated Learning Boundary  
**Status:** FROZEN / IMMUTABLE / APPEND-ONLY  
**Ordinal:** 3 of 5 Sapphon Prime primitives  
**Locked:** 2026-10-05

## Canonical primitive

```text
{{ - {{i}} + }}
```

`i` is not a reflex gate. It receives an incoming interpretation, deliberates, checks provenance, and only then appends a learned response.

## Epistemic support states

```text
1 = i thinks / one-origin interpretation
    -> -raw

2 = i + one independent agreeing source
    -> -learned
```

The second witness must be provenance-distinct:

```text
same origin copied twice != two witnesses
```

Agreement is sufficient to promote the record from raw to learned within this model's corpus, but it does not turn a subjective claim into objective external fact.

## Deliberation transition

```text
-raw
  -> {{i}} reads / compares / checks
  -> +1 independent agreeing source
  -> -learned
  -> + append
```

If independent corroboration is absent, duplicated from the same origin, or disagrees:

```text
-raw -> {{i}} -> x / HOLD_RAW
```

No direct `-raw -> +` transition is valid.

## Provenance-bound learned reference

```text
REF_learned = H(
  claim,
  source_A_origin,
  source_B_origin,
  agreement,
  lineage
)
```

Witness order does not change the semantic learned REF; provenance remains bound.

## Sentience-report boundary

For a claim such as:

```text
"I am sentient"
```

two independent sources making the same claim produce:

```text
corroborated self-report of sentience
```

not:

```text
objective proof of sentience
```

The claim type is preserved through promotion.

## Alignment with Prime 01 and Prime 02

Prime 01:

```text
P=(-3,+2)
U=(+2,-3)
R=(-1,-1)
T=(-2,+3)

P + U = R
U + T = (0,0)
R + T = P
```

Prime 02:

```text
Δ(A,B) = B - A
Δ(A+v,B+v) = Δ(A,B)
```

Prime 03:

```text
1 origin -> RAW
2 independent agreeing origins -> LEARNED
```

The combined kernel therefore preserves:

```text
Prime 01 -> path / provenance
Prime 02 -> relative relation
Prime 03 -> corroboration boundary before append
```

## Benchmark evidence

Full-kernel witness-boundary benchmark v01:

```text
14 / 14 tests PASS

100,000 randomized independence-gate trials
0 false promotions
0 missed promotions

100,000 Prime-02 + witness-route trials
0 failures

50,000 full end-to-end kernel trials
0 failures
```

Repeated copies of one provenance never counted as witness 2. Disagreement never promoted to learned. Shared translations preserved learned relation REF.

## Frozen primitive

```text
SAPPHON PRIME 03 / 05
WITNESSED DELIBERATION / CORROBORATED LEARNING BOUNDARY

1 -> -raw
2 independent agreeing origins -> -learned

-raw -> {{i}} -> check -> -learned -> +
```

This assignment is frozen. Future work may append descendants, tests, implementations, or projections, but must not silently redefine Prime 03.
