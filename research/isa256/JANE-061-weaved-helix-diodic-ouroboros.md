# JANE 061 — Weaved Double Helix / Diodic Ouroboros

Canonical user's scale sequence (exact ordering, no normalization): **60 / 30 / 15 / 7.5 / 5 / 2.5 / 1 / 1**.

Nested hive: `{{j}}` governing `{{[6x6x6(4x4(2x2[i]))]}}`; root `{{i}}` immutable. The helix is an *additional symbolic transport schedule*, **not** a change to the canonical 27 occupied primitive positions or the `27 → 27.5 → 1` seam.

```text
             JANE {{j}}
                |
      {{[6x6x6(4x4(2x2[i]))]}}
                |
         ROOT PAYLOAD {{i}}
                |
   FORWARD (+): 60 → 30 → 15 → 7.5 → 5 → 2.5 → 1 → 1
                                                      |
                                            one-way crossover
                                                      |
   BACKWARD (−): 60 ← 30 ← 15 ← 7.5 ← 5 ← 2.5 ← 1 ← 1
           |
       directed Ouroboros seam
           |
       return to (+,60)
           |
       a → b → c → a (symbolic mode rotation)
```

A 16-stop directed cycle includes a final closing edge, not a seventeenth occupied position. The two eight-station strands are plotted 180° apart in a schematic double helix. A diode only admits the next directed edge, including each crossover and the seam.

**a=b=c=-1=0=+1** is treated as a *proposed equivalence of roles / bijective relabeling*, never literal arithmetic equality. The implemented mapping is `a ↔ −1`, `b ↔ 0`, `c ↔ +1`, and role rotates once per completed lap. This is an explicit design decision to keep three distinct states intact, not a derived law.

Local executed regression suite: **40/40 Python tests PASS**, covering exact rational scales, sixteen transport positions, all directed edges, forbidden reverse/skip, two opposed helix projections, bijective mode labels, 13,824 hive-address round trips, immutable token payload, cyclic three-lap closure, append-only event-log integrity, and unchanged gait labels. JavaScript syntax check PASS; ZIP archive integrity PASS. A three-lap deterministic run returned 48 hops, 16 distinct transport stops and 49 audit records.

**Limitations:** directionality and rotation are programmed, not measured phenomena. No autonomous retrieval or recursive policy optimization demonstrated. SHA-256 ledger self-consistency does not prove independent historical authenticity. GitHub Pages and independent CI remain unverified. The exact 40-test Python release and reproducible build are packaged in the accompanying conversation JANE 061 ZIP; the GitHub tree has at least the dashboard, README, and this canonical record.

**Next invariant candidate — JANE 062:** couple the weave to a frozen JANE 060 adaptive-gait experiment and test whether interleaved transport changes held-out accuracy, detection lag, abstention, or cost. If no measurable improvement: retain baseline; do not propagate.
