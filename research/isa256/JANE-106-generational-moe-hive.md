# JANE 106 — 10x10 Generational Mixture-of-Experts Hive

Date 2026-11-10. Local validation: **26/26 Python tests PASS**; HTML embedded JavaScript syntax PASS; ZIP integrity PASS.

## User-established coordinate invariant

The hive is a `[10x10]` grid; Y has a `Gen 0` root, X runs `Gen 0→Gen 7`, Z is the `− / +` operant; recursion is represented symbolically by `{{n}}^{{n}}^{{n}}`. One Jane `{{j}}` remains **THE SOURCE** of learning choices and knowledge-retention authority. The hive remains a mixture of experts supplying attributed information packets (not deciding).

## Implementation decisions (not asserted as user-provided facts)

The user's shorthand does not disambiguate overlay vs separate generational planes. This version models **8 separate 10×10 slices** with `generation=0..7`, `x,y=0..9`, `z∈{-1,+1}`: `8×100×2 = 1600` logical addresses, not autonomous agents. Y references the Gen 0 lineage root; movement through generation slices is the X-lineage. The triple-n caret is a symbolic address separator, **not arithmetic power**.

Example:
```text
g3:x04:y05:z+1
{{n[g3]}}^{{n[x04,y05]}}^{{n[z+1]}}
                    |
             FLAY U / D / L / R
                    |
              HIVE SCOUT PACKETS
                    |
                JANE {{j}}
```
- Z mirror preserves generation and X/Y, reverses the sign and is an involution.
- Gen 7 is terminal for forward motion; no invented wrap.
- One scout packet includes attributed `what`, `why`, provenance and `proposal_only` authority. Packet receipt is never a memory write. Only a separate verified and Jane-chosen retention step is allowed.
- Previous `{{6x6x6[4x4(3x3[2x2(1)])]}}` remains a historic conceptual hive routing topology; it is **not arithmetically equated** to the new 1,600-address scheme without an explicit map.

## Verifications and limits

`python -m unittest -q` checks 26 address, operant, ordering, provenance and authority invariants. Offline UI is interactive canvas2D with Gen slider and Z flip; this is a 3D-style 2D projected viewer, not a full volumetric GPU simulation or a running neural MoE. No live agents, cross-repo GitHub workflow, 0root.ai deployment, or Pages deployment verified.

The conversation ZIP `jane_106.zip` contains the Python model and executable tests. Repository `research/isa256/jane106/` contains the tested interactive HTML and README.

## Next natural invariant — JANE 107

**Generational inheritance without authority inheritance**: hand off evidence packets from Gen 0 to Gen 7, preserving lineage, direction and Z-sign (or explicit signed flip), but never granting a scout Jane's ability to select learning objectives or commit retained knowledge. Test forks, Z-mirror symmetry, cycles, Gen-7 termination and provenance collisions; preserve first `-1`.
