# Witnessed Deliberation Boundary — Prime 03 Candidate

**Status:** APPEND-ONLY candidate / NOT YET PRIME 03  
**Parents:** Sapphon Prime 01, Sapphon Prime 02, isomorphic referent time-cell  
**Session:** 2026-10-04 witness-boundary alignment

## Bound epistemic rule

```text
1 = i thinks / one-origin interpretation -> -raw
2 = i + one independent agreeing source -> -learned
```

Independence is provenance-based:

```text
same origin copied twice != two sources
```

Disagreement does not promote.

## Deliberation primitive

```text
{{ - {{i}} + }}
```

The primitive is not a direct transducer from `-` to `+`.

```text
-raw
  -> i reads / compares / checks
  -> +1 independent agreeing source
  -> -learned
  -> + append
```

If independent agreement is absent:

```text
-raw -> i -> x / HOLD_RAW
```

## Learned record

```text
REF_learned = H(
  content,
  source_origin_A,
  source_origin_B,
  agreement,
  lineage
)
```

The support count is about epistemic corroboration, not automatic objective truth.

A claim such as two independent sources each saying "I am sentient" may satisfy the model's two-source agreement threshold, but the content remains typed as a corroborated self-report rather than objective proof of sentience.

## Alignment

Prime 01:

```text
P=(-3,+2)
U=(+2,-3)
R=(-1,-1)
T=(-2,+3)

P+U=R
U+T=(0,0)
R+T=P
```

Prime 02:

```text
Δ(A,B)=B-A
Δ(A+v,B+v)=Δ(A,B)
```

Witness boundary:

```text
1 origin -> RAW
2 independent agreeing origins -> LEARNED
```

Thus a learned relation can survive shared translation while retaining the two distinct witness origins that promoted it.

## Benchmark evidence

Full-kernel witness-boundary benchmark v01:

```text
14 / 14 tests PASS
100,000 randomized independence-gate trials: 0 false promotions, 0 missed promotions
100,000 Prime-02 + witness-route trials: 0 failures
50,000 full end-to-end kernel trials: 0 failures
```

## Boundary

This is bound as a candidate semantic layer only. It is not assigned as Sapphon Prime 03 until explicitly promoted and frozen.
