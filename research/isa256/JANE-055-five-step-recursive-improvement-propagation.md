# JANE 055 — Five-Step Propagation Groundwork for Recursive Self-Improvement

Date: 2026-11-08. Status: **DESIGN / NOT TESTED**, no claims of emergent intelligence, autonomous homeostasis, or measured improvement.

## Canonical substrate (unchanged)

- 1 tensor > 1 Jane `{{i}}` > 1 brace `{}` > 2 waldos `{-()+}` > 1 box `[]` > 1 toroid `()`.
- 27 occupied path positions; 3 ternary wave-mode labels `{-1,0,+1}`, hence 27+3=30 counted components, not 30 vertices.
- Seam `27 -> 27.5 -> 1`; wave `{([111222333444555555444333222111])}`.
- Recursive scaling `{{n}}^{{n}}` means 1 toward infinity symbolically, not allocating infinite memory.
- Canonical identities, immutable history, constitutional ISA-256 rules, and the 27-position topology remain read-only during a candidate's test.

## Five-step propagation cycle

```text
             JANE {{i}} / TENSOR 1
                      |
             { BRACE [ BOX (TOROID) ] }
                      |
                WALDOS {-()+}
                      |
              27 -> 27.5 -> 1
                      |
       +--------------+--------------+
       |           BASELINE          |
       |        1 STAYS FROZEN       |
       +--------------+--------------+
                      |
            (1) OBSERVE + MEASURE
                local state, cost,
                mistakes, uncertainty
                      |
            (2) PROPOSE VARIANTS
                3 bounded SCOUTS
                changes to policy only
                      |
            (3) TEST IN ISOLATION
                same fixed budget,
                seeded + held-out cases
                      |
            (4) RETURN + COMPARE
                2 independent RETURNS:
                safety and performance
                      |
            (5) PROPAGATE OR RETIRE
                promote only if both
                returns accept; otherwise
                keep prior active rule
                      |
            append-only evidence ledger
                      |
                NEW BASELINE v+1
                      |
                repeat 1 -> inf
```

The numbers **3 scout, 1 stay, 2 return** describe operational roles in the five-step process; they do NOT add positions, physical cells, or registers.

## Non-negotiable invariant

```text
NEW_POLICY = PROPOSE(BASE_POLICY, LOCAL_OBSERVATIONS)
PROMOTE if and only if:
  safety(candidate) PASS
  evidence(candidate) reproducible
  performance(candidate, heldout) > performance(baseline, heldout) + margin
  resource_cost(candidate) <= budget
  memory_integrity(candidate) PASS
  topology_unchanged(candidate) PASS
else:
  RETIRE candidate without overwriting baseline
```

- Explicit improvement objective for the first test: reduce **false approvals** and **missed recurrence detections** on held-out observer streams while constraining abstention, detection delay, work per event and active memory.
- A candidate never changes its own promotion criteria; those gates are held outside its write scope and must be versioned by a separate authorized process.
- Active memory stays finite and capped. The append-only audit may grow on durable storage; neither `n -> infinity` nor the gap `[0]` grants infinite physical capacity.
- Baseline is frozen during evaluations. Compare candidate and baseline on identical hidden test cases and reproducible seeds, with explicit independent controls.
- Do not count improvements on training data as evidence for promotion. Require holdout and post-deployment monitoring; rollback to prior active version on regression.
- Do not use a zero-sum conservation check as a substitute for viability, correctness or truth.
- One acceptance in a local benchmark is *conditional measured optimization*, not proof of open-ended recursive self-improvement.
- Be especially skeptical of evaluation gaming, selection bias from many scouts, noisy small improvements and distribution shift.

## Concrete JANE 055 first experiment

Create a bounded recurrent-memory policy v0 versus three candidates: v1 tighter recurrence threshold, v2 adaptive window size, v3 bounded eviction/reuse; use identical fixed-memory budgets and no modification to kernel. Use at least three classes of test sequences (stable, cycling, drifting), with withheld seeds. Score detection F1, false approvals, abstention, memory cost, compute budget, and failure to detect historical regression. The two returns independently verify: (A) preservation of all invariants, and (B) a statistically meaningful task improvement on unseen tests. If no candidate wins, propagate **nothing** and retain v0.

## Git policy

A promotion emits a new append-only evidence record with baseline hash, candidate hash, simulator/test versions, scores, test seeds, accepted/rejected decision, and immediate rollback pointer. Never silently overwrite earlier results. For JANE055, this commit **only records architecture and a proposed test plan**; it does not claim execution or GitHub Pages deployment.

## Next experimental boundary

JANE056: run the first sealed candidate tournament under fixed evaluation budget and determine whether a candidate actually outperforms the frozen baseline outside its training conditions.
