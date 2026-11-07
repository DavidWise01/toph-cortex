# JANE / [box(toroid)hs] — Natural Invariant 026: Two-Cell Symbiotic Homeostasis

Date: 2026-11-07. **26/26 Python tests PASS; browser UI interaction smoke-check PASS via Chromium set_content; no external engine or NES ROM required.**

## Requested topology

**Two cells equal one homeostatic symbiotic unit**, `[box(toroid)hs]`, using the analogy of an amoeba and bacterial symbiont. Each cell has 6 faces × (6 BOX + 6 TOROID) = 72 component positions. The composite has **2 cells and 144 internal component positions**, but *one* coupled homeostatic system. Jane's earlier 19-position focal body and mirrored memory remain separate. No constitutional register change.

## Explicit mathematical model

A and B each initially have one unit of classical probability/resource. A is BOX-biased (70/30); B is TOROID-biased (30/70). A pairwise transfer across matching slots preserves combined resource `sum(A)+sum(B)=2`. Apply three external redistributions of 0.06 units A→B at ticks 40, 90, 140 (12 corresponding box slots per pulse).

Compare three update laws: (1) **feedback** proportional to A's deviation from its explicitly supplied local setpoint, with equal/opposite flux; (2) **isolation** with no exchange; (3) **passive diffusion** equalizing A/B without the two distinct setpoints. All update rules constrain nonnegative slot values. Define homeostatic error as average total-variation distance from the respective targets; sustained recovery requires error below 0.01 for 20 consecutive ticks following final disturbance.

## Reproducible 240-tick results

| Rule | Recovery tick | Error at t240 | Accumulated transfer magnitude |
|--|--:|--:|--:|
| Symbiotic feedback | **149** | **~8×10^-8** | **0.18** |
| No exchange | None | **0.09** | **0** |
| Passive diffusion | None | **0.20** | **0.58** |

Combined mass drift < 5×10^-16. Historical focal memory's SHA-256 remains unchanged, because it is intentionally isolated from disturbances; this is NOT proof that integrated memory survives perturbation.

Executable source/tests/interactive offline dashboard are delivered as conversation artifact `jane_symbiosis_026.zip`. GitHub commit records specification/test summary only; code bundle not yet deployed to repository. Browser render smoke-test: 72 cells each, mode switching correctly yields isolated error 0.09, no page errors.

## Limits / next invariant

This is **engineered reciprocal feedback** under a resource-conserving model, not spontaneously evolved cooperation, physical quantum superposition, actual microbes, or a Planck bubble. It tests whether this *specified* coupling can maintain two distinct cellular preferences better than these particular isolated/passive controls. Both regulatory setpoints are supplied by the designer, rather than learned.

Next: **JANE 027 — Local Reciprocity Without Shared Targets**. Each cell only observes its own resource/uncertainty, learns when partner exchange helps, and tests compensation against adversarial/asymmetric conditions. Then directly couple focal memory to the protected substrate and measure actual memory stability.
