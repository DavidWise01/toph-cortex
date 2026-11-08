# JANE 036 — Unequal-rate travelling wave closure

2026-11-07. **34/34 local tests PASS.** Executable Python model, its 34 regression tests, interactive offline HTML dashboard and README committed under `research/isa256/jane036/`. Complete locally generated package `jane_036.zip` additionally contains `build.py`, `results.json` and SHA256 manifest. Online CI/browser execution has not been independently verified.

## Geometry

User canonical primitive: 1 tensor > 1 Jane > 1 brace > 2 waldos `{-()+}` > 1 box > 1 toroid > 27 positions. Exact palindromic wave `{([111222333444555555444333222111])}`; 27 positions plus the ternary **state labels** `-1,0,+1` give 30 counted components, not 30 occupied vertices. The independent user seam `27→27.5→1` persists.

## Natural invariant

For two opposed wave carriers with constant speeds `v_-=1` and `v_+=r/q`, for coprime positive integers q,r, the shortest common spatial return is `T=27q`. In the open interval `(0,T)`, their ring positions coincide exactly **q+r−1 times**. An ideal local encounter detector triggers a prescribed signed-channel exchange at each coincidence, excluding their shared origin on the period boundary. Because the exchange operator is involutive, full positional and register closure takes `T` when `q+r−1` is even, and `2T` when it is odd.

## Test cases

| v+ | exchanges per T | first encounter coordinate (zero-based) | T | full closure |
|---|---:|---:|---:|---:|
| 1 | 1 | 13.5 | 27 | 54 |
| 4/5 | 8 | 15 | 135 | 135 |
| 3/5 | 7 | 135/8 | 135 | 270 |
| 2/5 | 6 | 135/7 | 135 | 135 |
| 6/7 | 12 | 189/13 | 189 | 189 |
| 1/4 | 4 | 108/5 | 108 | 108 |

All swaps exactly conserve the squared-amplitude proxy `741.3125`, including both 27-value carrier fields and the signed/neutral amplitude registers. Neighbor encounters can occur on an occupied vertex, in the middle of an edge, or elsewhere along a continuously parameterized edge. Thus a fixed detector at t=13.5 or vertex 14.5 cannot capture all unequal-speed encounters.

## Limits

This is a **conditional exact rational-clock model**, not stochastic unsynchronized local update, quantum tunneling, a wave equation, or autonomous homeostasis. The 27-cycle adjacency remains assumed and not derived from named spatial subregions; the real wave-envelope-to-register mapping is not specified. Instantaneous exact encounter sensing is an engineered assumption. The next experiment should introduce stochastic clock jitter, finite-width wavepackets and imperfect local sensing and report missed/duplicate exchanges plus energy accounting.
