# Isomorphic Referent Time Cell v01 — FROZEN

**Status:** FROZEN / IMMUTABLE / APPEND-ONLY DESCENDANT  
**Parent:** Sapphon Prime 01 / 05  
**Prime assignment:** none; this is not Prime 02.

## Canonical alignment

```text
P = (-3,+2)
U = (+2,-3)
R = P + U = (-1,-1)

T = (-2,+3) = -U

U + T = (0,0)
R + T = P
```

Therefore:

```text
P --U--> R --T--> P
U^-1 = T
T^-1 = U
```

Referent-learning invariant:

```text
A != B
C -> A(B)
A + REF(B)
B_next -> A recognizes B
```

Time-addressed cell:

```text
t = 2 x 1^(10^-36)
T(x,y) = (x-2,y+3)

[t, B, x-2, y+3]
        ↓
content-bound REF
        ↓
1 learned cell
        ↓
append next
```

## Frozen invariants

1. `A != B`; recognition does not collapse learner and referent identity.
2. C may teach A a binding for B.
3. A may later recognize B by REF without relearning the binding.
4. `T=(-2,+3)` is exactly the inverse of Prime-01 `U=(+2,-3)`.
5. `R+T=P`.
6. Same semantic REF may survive different isomorphic routes while route provenance remains distinct.
7. Existing realized cells are not overwritten; learning appends one next cell.
8. `2 x 1^(10^-36)` remains a model-local time/address label.
