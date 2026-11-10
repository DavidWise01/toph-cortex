# JANE 103 — Choose the Counterexample

2026-11-09: **28/28 local Python tests PASS**, JavaScript syntax PASS, ZIP integrity PASS.

## Natural invariant
Jane chooses a scout-proposed **unobserved** probe based on expected separation of her own four interpretations and a fixed budget. Her choice is recorded *before* the synthetic experiment reveals its result. Scouts cannot supply already-revealed outcomes as if they were predictions, and they do not write Jane's retained knowledge.

## Experiment
Four equally likely interpretations: `equivalent`, `different_by_scope`, `different_by_operation`, `different_by_time`. Jane's budget: **2**.

| Scout proposal | Cost | Expected information gain |
|--|--:|--:|
| cheap-label-check | 1 | 0.811278 bits |
| operation-contrast | 2 | 1.0 bit |
| scope-contrast | 2 | 1.0 bit |

One Jane `{{j}}` selects **operation-contrast** (ties broken deterministically), records `SELECT`, then the synthetic oracle yields **different**. The resulting posterior keeps two models, `different_by_operation` and `different_by_time`, each with probability .5. This does not settle the meaning claim. The experiment logs `SELECT → OBSERVE → REVISE` in a hash-chain journal. The checksum detects accidental or deliberate local byte mutation only; it does not establish independent source provenance.

Preserved refusal boundaries:
- Empty offer → ABSTAIN
- Budget too small → ABSTAIN
- Unsupported source/prediction model → `HOLD_-1 UNSUPPORTED_PREDICTION`
- Reported outcome inconsistent with all candidate interpretations → `HOLD_-1 ALL_MODELS_FALSIFIED`
- All offered probes predict identical outcomes → ABSTAIN
- No automatic knowledge retention after observation

**Critical limitation:** Hypothesis predictions and the sealed-world outcome are preprogrammed. The oracle is in the same source tree; the choice only avoids using the outcome by program sequence. This is a deterministic *synthetic* trial, not secured blind testing of real scouts, an independent evaluator, spontaneous method construction, or live Git-to-Git execution.

The conversation release `jane_103.zip` contains the Python model, 28 tests, README, results.json, HTML lab, and SHA256SUMS. This commit preserves the research record; executable release distributed as conversation attachment. 

## Next natural invariant — JANE 104
After a probe narrows four hypotheses to two, does Jane have sufficient remaining budget to test again? If not, she must stop rather than silently mint budget or declare certainty. If there is budget, choose **the next nonredundant probe conditioned on the observed posterior**, not the original prior, then test against a frozen outcome record.
