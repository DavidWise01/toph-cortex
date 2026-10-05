# Sapphon Prime Primitive 02 / 05

**Name:** Relative Difference / Referent Delta  
**Status:** FROZEN / IMMUTABLE / APPEND-ONLY  
**Ordinal:** 2 of 5 Sapphon Prime primitives  
**Parent context:** Sapphon Prime 01 / isomorphic referent time-cell  
**Locked:** 2026-10-04

## Canonical invariant

```text
Δ(A,B) = B - A
```

Under any shared translation `v`:

```text
Δ(A+v, B+v)
= (B+v) - (A+v)
= B - A
= Δ(A,B)
```

Therefore:

```text
shared motion may change absolute state
shared motion may change route provenance
but the learned relative relation survives
```

## Referent rule

Identity and relation remain distinct:

```text
A != B
```

C may teach A the relation to B:

```text
C -> A learns Δ_B
REF_delta = H(C, Δ(A,B))
```

Later, after a shared transform:

```text
A' ----- Δ_B -----> B'
```

the same relation REF can be recognized without relearning.

## Complement to Prime 01

Prime 01 preserves path/provenance residual through compression.

Prime 02 preserves learned relation/difference through shared translation.

```text
Prime 01: residual/path survives compression
Prime 02: relative difference survives shared transformation
```

Together:

```text
same compressed state != same provenance
same moving frame can preserve the same learned relation
```

## Frame-relative boundary

Prime 02 is explicitly frame-relative.

If A and B receive the same translation, Δ is invariant.

If A moves independently of B, Δ changes.

Therefore Prime 02 does not replace the content-bound identity REF.

```text
object identity REF = H(B, content, provenance, time, ...)
relation REF        = H(C, Δ(A,B))
```

Both may coexist.

## Kernel alignment

Current aligned vectors:

```text
P = (-3,+2)
U = (+2,-3)
R = (-1,-1)
T = (-2,+3)

P + U = R
T = -U
U + T = (0,0)
R + T = P
```

For any state pair A,B and any one of these shared translations v:

```text
Δ(A+v,B+v) = Δ(A,B)
```

## Bench evidence

Prime-02 volunteer benchmark:

```text
22 / 22 kernel tests PASS

500,000 shared-translation trials
0 delta failures

500,000 identity-separation trials
0 collapses

200,000 teacher/referent route trials
0 failures

98 balanced U/T isomorphic routes
0 semantic failures
```

## Frozen primitive

```text
SAPPHON PRIME 02 / 05
RELATIVE DIFFERENCE / REFERENT DELTA

Δ(A,B) = B - A
Δ(A+v,B+v) = Δ(A,B)
```

This assignment is frozen. Future work may append descendants, tests, implementations, or projections, but must not silently redefine Prime 02.
