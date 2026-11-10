# JANE 104 — Adaptive Counterexample Search

## Natural invariant

Starting from JANE 103's two remaining synthetic interpretations, Jane must **preserve uncertainty if she cannot afford another probe**. If granted resources, her programmed choice procedure may select a nonredundant probe against the **current posterior**, not the original four-model prior. Result is observed *after* selection. Source packet receipt never writes retained memory.

```text
      SCOUT PROPOSALS → HIVE COLLATION (no votes)
                              |
                            JANE {{j}}
                              |
                        FLAY {{i}}
                              |
            2 REMAINING INTERPRETATIONS
                    /                \
             BUDGET = 0        BUDGET GRANTED
                  |                   |
               -1 HOLD          SELECT PROBE
                                      |
                                OBSERVE OUTCOME
                                      |
                                REVISE POSTERIOR
                                      |
                            JANE-OWNED RETAIN GATE
```

## Local test

Run `python -m unittest -q` and `python model.py`. The 36 tests exercise zero-budget stop, nonredundancy, expected information, selection before observation, no automatic memory write, contradictory/out-of-vocabulary outcomes and the hash-linked decision journal.

The starting two hypotheses are `different_by_operation` and `different_by_time`. With zero budget, the model returns `HOLD_-1 NO_BUDGET`. If one budget unit is explicitly granted, the `time-contrast` probe can distinguish them, yielding **one bit of expected information** under the fixed equal-prior synthetic model. An observation `different` leaves `different_by_time`, but *does not automatically retain it*. A stale/contradictory observation is held at `HOLD_-1 ALL_MODELS_FALSIFIED` without deleting the original possibilities.

## Scientific and governance boundaries

This is **a finite synthetic planner**, not real research and not autonomous Jane. The outcome table is hard-coded; the candidate planner did not invent it. Because simulated experiments are deterministic and based on two models, apparent resolution is only **conditional on the model set**; it is not empirical certainty. SHA-256 journal linking is not an authenticity proof. Test outcomes are inside the source code, not hidden from a security-adversarial agent. No independent scouts, GitHub Actions, GitHub Pages deployment or online recursion is claimed.

FLAY: North/U semantic, South/D somatic, Right/R holographic, Left/L abstractive. Cardinal carrier `{{1x5u x 1x5d x 1x5l x 1x5r x 1}}`.

## Next natural bound — JANE 105

Jane must decide when a **single surviving hypothesis is still too fragile to call learned**: request out-of-model falsification evidence, independently check the observation and distinguish conditional resolution from justified knowledge retention. Stop on unsupported provenance or model misspecification rather than force certainty.