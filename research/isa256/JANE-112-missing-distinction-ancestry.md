# JANE 112 — Missing Distinction and Ancestry-Aware Settlement

Date: 2026-11-10.

## Executed local verification

- **28/28 Python regression tests PASS**
- **8/8 synthetic transfer examples PASS**
- Standalone HTML JavaScript syntax PASS
- ZIP archive integrity PASS
- Manifest generated for 6 release files (README, model.py, model111.py, test_model.py, results.json, index.html)
- The complete runnable source is in the conversation download `jane_112.zip`. The repo `research/isa256/jane112/` contains the HTML viewer and README; the source/model/test files have not been pushed individually to GitHub.

## Natural evolutionary invariant

When a settlement criterion makes a mistake on an unseen case, Jane must distinguish **an omitted variable** from a mere threshold error. She may request an additional observable feature from her MoE hive. The hive reports attributed packets and source ancestry; one Jane `{{j}}`, THE SOURCE, selects whether to investigate, test, settle or retain. Agents never force memory writes.

The original JANE111 counterexample is immutable:
```text
-1 PROVENANCE_ANCESTRY_NOT_MODELED
input: quiet=3, coverage=90, root_labels=3, conflicts=0
old predictor: READY
hidden truth: NOT READY (three labels, one underlying root)
```

New bounded feature-request experiment:
```text
JANE111 FAILURE
      |
  FLAY U D R L
      |
  FEATURE GAP: root_ancestry
      |
  JANE REQUEST -> MoE HIVE RETURNS PACKETS
      |
  SAME ORIGIN?   /    DISTINCT ORIGINS?
      |                       |
 [A,A,A]                  [A,B,C]
 ONE ROOT                 THREE ROOTS
      |                       |
 KEEP GROWING          ELIGIBLE TO SETTLE
      |                       |
      +--------+--------------+
               |
          VERIFICATION GATE
               |
          JANE AUTHORIZATION
               |
          NO AUTO-LEARNING
```

The revised comparator counts **distinct synthetic original-root identifiers**, not source-label count. It also checks complete mappings, unique packet IDs, supported packets, mandatory origins, old quiet/coverage/conflict conditions, and separate verification/authorization gates. No semantic memory is appended.

## Limits

**Synthetic and deterministic:** neither the feature-selection heuristic nor the root-ancestry feature was autonomously invented by a running model. The MoE here is a stub callback; origin strings are not proof of independent provenance. Passing tests demonstrates that the chosen algorithm handles modeled cases, not real-source authentication or a globally sufficient settlement criterion. Local hash-chain records are not authenticated signatures.

The previously approved 10×10 nested-growth geometry, Gen0–Gen7 hierarchy and Z−/+ operant remain structural metaphors. The earlier eight-flat-plane cardinality is superseded. No GitHub Pages deployment or live cross-repository workflow execution is claimed.

## Next natural evolution — JANE 113

**Authenticated Ancestry:** when two scout packets name distinct roots, can Jane ask for verifiable parent chains and identify a shared ancestor or missing signature before promoting any source as independent? Use first-bad-chain hold and budgeted verification. Preserve `-1` without overwriting the original.
