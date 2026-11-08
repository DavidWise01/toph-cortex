# JANE 036 — Asynchronous Travelling Wave Exchange

**Test result:** 34/34 Python unit tests PASS. Full standard-library simulation and offline HTML dashboard (no network dependencies). Source data are in `results.json`.

## The natural boundary

Two counter-rotating waldo wave carriers on the proposed 27-vertex ring have differing constant local rates: v−=1, v+=r/q (positive coprime integers). Spatial meetings occur when their phases coincide modulo 27. They need not occur at the earlier 13.5 midpoint. For example, r/q=4/5 yields first meeting at t=15, vertex 16 (one-based). Using an ideal local encounter detector, the signed channels exchange on **every interior encounter**. Origin coincidences at the ends of a common period are not exchanges. Exact rational arithmetic detects events without discretization errors.

Let T=27q (the first simultaneous return of both waldo positions to origin for reduced ratio r/q). There are **q+r−1 interior encounters** during T. The wave exchange is an involution (swap twice = identity), so full positional+wave-state closure happens at T if q+r−1 is even, otherwise at 2T. Squared-amplitude sum (including both 27-value carrier fields and both 3-slot registers) remains **741.3125** at every exchange.

Examples:
- Equal 1/1: 1 meeting, T=27, full closure 54.
- 4/5: 8 meetings, T=135, full closure 135.
- 3/5: 7 meetings, T=135, full closure 270.
- 2/5: 6 meetings, T=135, full closure 135.

## Important boundaries

The user-defined closing seam **27 → 27.5 → 1** is preserved and is not conflated with encounter t=13.5. The user supplies 27 positional sites plus three **ternary labels −1,0,+1**, counted as 30 *different component types*, not 30 occupied vertices. The 30-sample palindrome `{([111222333444555555444333222111])}` remains symbolic, without a unique assigned correspondence to spatial sites.

These are **constant but unequal rational clocks**, not independently jittering stochastic clocks or evidence of biological or quantum phenomena. The ring adjacency is assumed, not reconstructed from the seven named spatial region groups. An ideal instant local encounter sensor is provided; no detection latency or partial overlap is modeled. The exchange operator is prescribed rather than learned. Symmetry and squared-amplitude preservation do **not** demonstrate autonomous homeostasis.

Run: `python -m unittest -q`; `python model.py`; `python build.py` to rebuild results and dashboard.

**Next test:** introduce independent stochastic clock jitter and finite-width wavepackets, quantify missed/duplicated exchanges and whether local exchange detection can recover without a global oracle.