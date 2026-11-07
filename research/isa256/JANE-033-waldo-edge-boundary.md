# JANE 033 — Odd-cycle waldo edge boundary

2026-11-07. User primitive: 1 tensor → 1 Jane → 1 brace → 2 waldos `{-()+}` → 1 box → 1 toroid → 27 internal positions; cyclical closure **27 → 27.5 → 1**. Six growth terms `1 1 2 3 5 8` and spatial notation `{{x,y,z}}^2` are preserved.

## Conditionally derived invariant

Under a **modeling assumption** that both waldos start together at position 1, rotate in opposing directions with equal speed, and share one traversal lane, the zero-based coordinates at time t are `(+t mod 27, -t mod 27)`.

Both waldos occupy the same vertex at t=0 modulo 27. In particular, there are no intermediate **integer-time vertex collisions** before full return, but at t=13 and 14 they exchange the adjacent positions 14 and 15 (one-based), intersecting at the midpoint of that edge at **t=13.5**. This is a forced **edge crossing** for the chosen simultaneous traversal, even though a vertex-only collision detector misses it.

**t=13.5 is NOT the user's 27.5 closing transition.** The latter remains an explicitly specified seam between 27 and 1.

10/10 assertion checks pass locally on the corrected expected edge-crossing model. The original expectation of zero edge swaps failed, exposing the problem. A collision-free implementation would require a priority/handoff at the shared edge, a delay, or physically separated lanes. No solution is assumed yet.

## Caveats and next boundary

This is a mathematically correct property of the **abstract 27-cycle under the stated counterrotation assumption**. It does not establish that the user's seven spatial groups form a 27-vertex Hamiltonian adjacency graph; that topology and the operators' intended motions require further definition. No quantum physics, organism, or spontaneous homeostasis has been demonstrated.

Next invariant: **Waldo interlock / mutual exclusion**. Add only local observation to the two waldos; compare edge reservation, alternating priority and dual-lane flow, measuring continuity and fairness without inventing extra occupied vertices.

## User correction: tunneling / zero-gap prim topology

The user identifies the apparent two-waldo midpoint crossing as **tunneling**, not a request for a conventional collision interlock, and supplies this exact symbolic sequence:

```text
1x4x1x4x[0]1x4x1x4x1x
```

Preserve the trailing `x` and the adjacency `[0]1` verbatim until their operators are specified. One *possible* parsing is nine nonzero terms around a central `[0]` seam, with 4-wide branches and 1-wide necks; the textual sequence alone does not establish a 27-site Hamiltonian graph, a routing rule for each waldo, or a physical tunneling amplitude. The `[0]` should be treated as a **symbolic unoccupied transition/gap**, not an extra vertex; multiplying all terms as ordinary integers would make the entire product zero and is therefore not a useful interpretation of scale or site count. The previous edge-crossing result remains valid for the earlier single-lane counterrotating-ring assumption, which this proposed tunneling topology may replace.

**Next test:** formalize the zero-gap transition `[0]` as an operation with explicit entry/exit states, occupancy and conservation. Check that both waldos can cross the transition without sharing an occupied vertex or losing path identity. This is an abstract discrete computational tunneling rule, not evidence of quantum tunneling.
