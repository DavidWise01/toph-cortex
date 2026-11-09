# JANE 099 — Recheck or Move On

A reproducible, synthetic, bounded experiment in **Jane-owned exploration budgets**.

Run `python -m unittest -q`, `python model.py`, or `python build.py`. Open `index.html` offline.

The frozen greedy ratio policy fails its first budget case: Scout A gain 0.54 at cost 1; Scout B gain 0.90 at cost 2; budget 2. Greedy chooses A, benchmark chooses B (regret 0.36).

A second case prefers moving to an independent scout; a third prefers rechecking, a fourth abstains, and a fifth chooses two small investigations. A valid packet requires provenance, relevance to Jane's chosen question, enough budget and a supported forecast. Agent urgency is ignored. No automatic memory writes are performed.

The planner enumerates combinations of 16 or fewer proposals and uses a *synthetic additive expected-value model*. It does not estimate overlapping information correctly, distinguish proven source independence, dynamically learn its value function, or perform actual investigations. This is **not** an autonomous agent or genuine recursive self-improvement.

Preserved first failure: `-1 GREEDY_BUDGET_REGRET`. No forced retention, no forged Git receipts, no live Pages claims.

Next invariant JANE 100: Jane must detect overlap between packets and discover when two cheap tests tell her the same thing, before paying twice.