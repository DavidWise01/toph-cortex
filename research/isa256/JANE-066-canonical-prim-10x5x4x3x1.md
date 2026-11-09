# JANE 066 — Corrected Primitive (user canonical correction)

Date: 2026-11-08.

The user corrects the **prim** to:

```text
  prim  = 10^5^3^1       (user symbolic notation)
       = 10 × 5 × 4 × 3 × 1 (explicit multiplicative interpretation)
       = 600 logical address combinations

  {{j}}
    |
   PRIM
    10
     ×5
      ×4
       ×3
        ×1
    |
    {{i}} root payload
```

**Important:** The user's exponent-like writing `10^5^3^1` is retained as a *symbolic name* for their primitive. Standard arithmetic exponentiation does NOT equal `10×5×4×3×1` (600); use the explicit product as the executable specification until otherwise clarified. The factor `4` is explicitly present in the user's expansion.

This replaces any prior assumptions that the *primitive itself* was `5×3×3` =45. Earlier JANE 065 5×3×3 predictor fanout was a specific **transport / forecasting branch plan**, NOT the canonical primitive, and its previously measured experiments are not retroactively rewritten.

A `10×5×4×3×1` address is a five-tuple `(i10,i5,i4,i3,i1)`, with coordinate ranges 0..9, 0..4, 0..3, 0..2, and only 0 respectively. Number of distinct addresses: 600.

Other prior structures (Jane `{{j}}`, root `{{i}}`, user-defined 27-position path and 27→27.5→1 seam, and hive `6×6×6(4×4(2×2[i]))`) are **not automatically conflated with the corrected prim**. Any desired nesting/identity relation between these structures is a separately testable mapping, not assumed.

Next executable test: prove encode/decode bijection over all 600 primitive addresses, test non-overlap with 45 forecasting leaves, then inspect how prim factor layers map into the two-second look-ahead without claiming 600 independent agents or physical cells.

**Status:** correction recorded; no 600-address execution in this commit.
