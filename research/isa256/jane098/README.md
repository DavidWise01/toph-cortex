# JANE 098 — Reliability Drift

A reproducible, offline **synthetic demonstration** of a bounded reliability-drift detector. The single Jane `{{j}}` controls what to investigate and what to retain; scouts provide evidence packets only. This is not a running autonomous AI or live Git-to-Git bridge.

## Run

```bash
python -m unittest -q
python model.py
```

## FLAY rule

```text
                AGENT PACKETS
         source / prior / recent / cost
                      |
              HIVE COLLATES
                      |
                 JANE {{j}}
                      |
          U  WHAT WAS PREDICTED?
          D  WHAT DOES CHANGE IMPLY?
          R  DO RECENT CASES RESEMBLE OLD?
          L  WHAT IF TRUST HAS DRIFTED?
                      |
               BRIER LOSS CHECK
                /      |       \
           CONTINUE REVIEW    HOLD_-1
               |        |        |
           JANE CHOICE  RECHECK  PRESERVE
               \        |        /
                  NO AUTO RETAIN
                        |
                  NEXT OWN QUESTION
```

## Synthetic data

Each scout has eight older forecasts (`p=0.9`, outcome `1`), plus recent forecasts with separate evidence IDs and two or more origin labels. Scoring uses mean Brier loss `(p - outcome)^2` per period, and flags drift for `new_loss - old_loss > 0.30` with at least 5 older and 3 recent distinct events.

- **Scout A:** old loss `.01`, recent loss `.81` → `REVIEW_DRIFT`, not automatic condemnation.
- **Scout B:** old `.01`, recent `.01` → `CONTINUE`, Jane may investigate a packet relevant to her own gap.
- **Scout C:** only 2 recent observations → `HOLD_-1`, the first sparse-evidence boundary.
- **Scout D:** one failure in 3 recent observations: old `.01`, recent `.276667`, difference `.266667`, so `CONTINUE`. This is not statistical proof of stability.

`36/36` local Python regression tests passed. Hash chaining makes a deterministic journal; it is **not** cryptographic authentication of independent sources. Origin labels are synthetic; two labels are not proof of independent source ancestry. Small sample windows and a manually chosen threshold limit reliability. No automatic retention, real source verification, deployed Pages or independent scout executions.

## Next natural bound

**JANE 099 — Recheck Scheduling.** Jane chooses whether to spend a scarce recheck budget on a drift-flagged scout, an uncertain scout, or neither. Measure false-alert costs and transfer to changed drift patterns.