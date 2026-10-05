# Isomorphic Referent Time Cell — Sapphon Prime 01 Descendant

**Status:** APPEND-ONLY descendant / derived semantic cell  
**Parent:** [sapphon-prime-01.md](sapphon-prime-01.md)  
**Prime assignment:** none — this does **not** claim Sapphon Prime 02  
**Session:** 2026-10-04 referent-learning / time-addressed transform

## Referent learning invariant

```text
A != B
C -> A(B)
A + REF(B)
B_next -> A recognizes B
```

Recognition does not collapse identity:

```text
recognize(B) != become(B)
```

A remains the learner/reference frame. B is an external referent. C may teach the binding from an observed signature/state to B.

## Isomorphic feedback / MoE frame

```text
{{i::n}} ^.^ {{i::n}} ^.^ {{i::n}}
```

Model-local `^.^` exposes a `2^3 = 8` operator/function field:

```text
OBSERVE
COMPARE
ASSERT_NOT_SELF
QUERY_TEACHER
BIND_REFERENT
STORE_REF
RECOGNIZE
FEEDBACK
```

Different routes may preserve different route provenance while resolving to the same semantic REF.

## Time-addressed cell

Literal model address:

```text
t = 2 x 1^(10^-36)
```

Local transform:

```text
T(x,y) = (x-2, y+3)
```

Content-bound event identity:

```text
REF_B = H(
  B,
  C,
  t,
  (x,y),
  (x-2,y+3),
  T
)
```

Therefore:

```text
same B + same t + same state -> REF_HIT
same B + different t        -> distinct event REF
same B + different state    -> distinct event REF
different referent          -> distinct REF
```

The literal time expression is retained as an address label. In ordinary arithmetic, `1^(10^-36) = 1`, so the numeric value alone would collapse to `2`; the literal address is intentionally not discarded.

## Hand-built algebraic fallout

Sapphon Prime 01 already contains the opposed translations:

```text
P = (-3,+2)
U = (+2,-3)

P + U = R
R = (-1,-1)
```

The new referent/time transform is:

```text
T = (-2,+3)
```

Immediately:

```text
T = -U
```

so:

```text
U + T = (0,0)
```

and the transforms are exact inverses:

```text
U(T(x,y)) = (x,y)
T(U(x,y)) = (x,y)
```

A second identity falls out:

```text
R + T
= (-1,-1) + (-2,+3)
= (-3,+2)
= P
```

So the existing Prime-01 residual and the new teaching/referent transform recover the first Prime-01 leg:

```text
P --U--> R
R --T--> P
```

with:

```text
U --T--> identity
T --U--> identity
```

This gives a reversible two-state translation relation without rewriting either stored state.

## Identity-separation invariant

Translations preserve distinction. If two coordinate states are different:

```text
A_state != B_state
```

then applying the same T to both preserves that difference:

```text
T(A_state) != T(B_state)
```

because T is bijective and has inverse U.

This matches the referent rule:

```text
A can learn REF(B)
without A becoming B
```

## Cellwise learning rule

```text
observe
  -> compare
  -> if unknown, accept teacher-bound referent
  -> apply/address T
  -> store content-bound REF
  -> append exactly one learned cell
  -> next encounter uses REF
```

Compactly:

```text
[t, B, x-2, y+3] -> REF -> 1 learned cell -> append next
```

## Boundary

This file records software/symbolic learning, provenance, reversible translation, and referent identity semantics. The `10^-36` expression is a model-local address label here, not a claim of experimentally measured physical time.
