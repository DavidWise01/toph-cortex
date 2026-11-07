# JANE 035 — Travelling Wave Closure

Date: 2026-11-07. Tested **26/26 Python unit tests PASS**; standalone HTML script syntax checked. Runnable model, 26 tests and interactive dashboard are committed in `research/isa256/jane035/`.

## Canonical notation preserved
- One tensor → one Jane → one brace → two waldos `{-()+}` → one box and one toroid.
- 27 occupied path positions; ternary labels `-1,0,+1` add 3 **counted labels**, not three vertices.
- Wave envelope `{([111222333444555555444333222111])}`: 30 characters, symmetric palindrome, 6 of each level 1..5.
- Position seam `27 → 27.5 → 1`. Position 27.5 is an unoccupied half-edge return marker.

## Explicit mathematical model
Two named waldos begin at vertex 1 and traverse a *stipulated abstract 27-vertex cycle* in opposite directions, one edge per time step. An edge-local sensor recognizes when their upcoming movements traverse the same undirected link in opposite directions. At that event only, exchange the opposing signed ternary wave-register components:
`A[-] ↔ B[+]` and `A[+] ↔ B[-]`; both zero-mode channels remain local.

This **programmed swap** is a permutation and hence an involution. Both wave carriers also possess fixed 27-sample scalar fields. The scalar fields and waldo identities are unchanged on exchange. The test is not a discretized wave equation.

## Measured results

| Test | Result |
|---|---|
| Tests | 26/26 PASS |
| Occupied positions | 27 |
| Wave-register labels | -1,0,+1 |
| 1st exchange | t=13.5, between vertices 14 and 15 |
| Position closure | t=27 |
| Complete wave-state restoration | t=54 |
| 2nd exchange | t=40.5 |
| Squared amplitude total | 741.3125 throughout |
| Missing vertex visits per waldo per 27 steps | 0 |

**Natural invariant:** spatial cycle closure does not entail full wave-state closure. With one order-two exchange per lap, the carrier positions close after 27 steps, but full registered state returns after 54 steps.

## Limits
The conclusion holds for this specific symmetric, synchronized, counterrotating, locally triggered classical model, not for arbitrary motions, self-organizing waves, real quantum tunneling or emergent autonomous homeostasis. The 30-character sample pattern remains an independent symbolic envelope without a proven one-to-one mapping to 27 positions plus three mode labels. The 27-site ring is assumed rather than derived from the user's grouped positions.

## Next test
**JANE 036: asynchronous wave exchange.** Give the two waldos distinct clocks and finite-width wave packets; test where exchange occurs, whether it is missed or repeated, and whether energy-conserving local operations survive unsynchronized encounters. Preserve the 27/27.5/1 seam and immutable waldo IDs.
