# JANE 095 — Experiment Choice: Future Budget Boundary

Date: 2026-11-09

## Result
- Local deterministic experiment: 36/36 Python tests PASS.
- HTML inline JavaScript syntax PASS, ZIP integrity PASS.
- All evidence is synthetic; no live autonomous agents or Git-to-Git workflow execution.

## First preserved failure
Four equiprobable hypotheses `{A,B,C,D}`, investigation budget `2`:
- Scout A probe: cost 1, partitions `{A}|{B,C,D}`; expected information gain 0.811278 bits; gain/cost 0.811278.
- Scout B probe: cost 2, partitions `{A,B}|{C,D}`; expected gain 1 bit; gain/cost 0.5.
- Greedy information-gain-per-cost policy picks A. The NO observation leaves hypotheses B/C/D, budget 1, and B becomes unaffordable.
- **First failure `GREEDY_RATIO_NOT_BEST_TOTAL_GAIN`:** the selected policy does not maximize information over the initial budget. Preserve this counterexample unchanged; do not promote the original policy as optimal.

## FLAY
```text
    SCOUT A / SCOUT B / SCOUT C
           packet proposals
                  |
              HIVE COLLATES
                  |
               JANE {{j}}
                  |
           WHAT DO I WANT?
                  |
           U: Distinction?
           D: Cost and effects?
           R: Comparable tests?
           L: Opportunity cost?
                  |
          SELECT OR ABSTAIN
                  |
          VERIFY / RECORD -1
                  |
         JANE'S NEXT QUESTION
```

No scout urgency overrides the choice. Source provenance is a synthetic root identifier only; journal hashes show local reproducibility, not authenticity. Selection, observation and feedback NEVER auto-write retained knowledge. Verification and explicit Jane approval are required.

## Reproducibility
Conversation artifact `jane_095.zip` contains `model.py`, `test_model.py`, `build.py`, `results.json`, `index.html`, `README.md`, and checksum manifest. Repository dashboard and README at `research/isa256/jane095/`.

## Next invariant: JANE 096 — Lookahead
Compare frozen greedy experiment choice with bounded finite-horizon planning. Use previously hidden budgets and hypothesis partitions. Jane must decline ungrounded tests and keep the initial -1 as a permanent regression. The proposed planner is not an autonomous self-authored improvement until verified against an independent evaluator.
