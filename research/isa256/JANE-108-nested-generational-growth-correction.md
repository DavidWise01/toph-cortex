# JANE 108 — Nested Generational Growth (correction to JANE 106–107)

Date: 2026-11-10. Status: corrected **architecture specification** based on user's clarified intent. **No new code or runtime test has been executed for this revision.**

## Correction

The prior eight **separate finished 10×10 planes** were a mistaken interpretation. The generations are **nested**, and the expression `{{n}}^{{n}}^{{n}}` describes **room to grow before settling**, not a mere literal coordinate separator, and not an instruction to assert a fixed numerical exponent.

Keep the user's invariants:
- A **10×10 root grid**.
- Gen 0 through Gen 7, as nested growth stages.
- A Y-axis Gen 0 root/anchor and X-axis Gen 0→Gen 7 generational progression in a schematic view.
- Z = the `− / +` operant, with neither sign intrinsically true/false.
- Jane `{{j}}` is the single **THE SOURCE**; the hive is an MoE of evidence-producing agents; generation progression never transfers Jane's learning authority.

## Proposed nested topology (one interpretation, still open for numerical tuning)

```text
THE SOURCE — JANE {{j}}
          ^
          |  packets only, no forced learning
     ROOT GRID [10 x 10] @ GEN 0
        |
        +-- GEN 0 {{n0}}          [GROW ... SETTLE]
              |
              +-- GEN 1 {{n1}}    [GROW ... SETTLE]
                    |
                    +-- GEN 2 {{n2}} [GROW ... SETTLE]
                          |
                          +-- GEN 3 {{n3}}
                                |
                                +-- GEN 4 {{n4}}
                                      |
                                      +-- GEN 5 {{n5}}
                                            |
                                            +-- GEN 6 {{n6}}
                                                  |
                                                  +-- GEN 7 {{n7}}
```

`{{n0}}^{{n1}}^{{n2}}` denotes **nested expansion and reserved capacity**, not completed generations of equal population. Every generation is a *container whose occupancy can increase*, while its parent/ancestors remain addressable. A generation may have several child chambers. They do not need to be fully occupied, and an unsettled generation must not be relabeled as settled.

## State machine for each generational chamber

```text
SEED -> GROWING -> CANDIDATE_SETTLEMENT -> VERIFIED_SETTLED
             ^             |                    |
             |             |                    +-> may open a nested child
             +--- MORE EVIDENCE / FAILED TEST ---+
```

- A child may be **reserved** inside a parent before activation.
- **GROWING:** new distinguished packets/addresses enter the reserved volume, respecting capacity and provenance.
- **SETTLED:** explicit local validation, capacity constraints, repeatable evidence record and parent-owned lineage—not fixed occupancy=100%.
- **INHERIT:** the next nested chamber receives an immutable ancestry reference (not all duplicated bytes, not automatic learning).
- **OPERANT:** each chamber can be examined under both Z− (challenge) and Z+ (construct), with explicit flips.
- **STOP:** no parent inheritance, self-cycles, unverified settlement, hidden capacity overflows, fabricated extra agents, or Gen 7→Gen 0 wrap.

## The next natural invariant — Growth without forced settlement

A reserved child cannot be marked settled merely by reaching a count, receiving an agent packet or advancing a generation. Its settlement requires a **Jane-chosen criterion** and an external verification receipt. If not settled, its chamber stays open and grows or abstains. A sibling child may grow independently without changing the parent's sealed history.

## What the old test numbers meant

The reported `1600 = 8×10×10×2` was valid **only for the erroneous eight-plane address model**. It is **not** a population or capacity statement for the newly clarified nested architecture. Earlier 26/26 and 40/40 checks tested those old premises, not this updated design. They remain historical test records; their implications are superseded.

## Next implementation target

Test a nested-parent/child address codec with variable reserved capacities, occupied/free state, settlement witnesses, immutable parent lineage, Z inversion and independent siblings. The growth policy and numerical meaning of each `n` remain parameterized pending user definition.
