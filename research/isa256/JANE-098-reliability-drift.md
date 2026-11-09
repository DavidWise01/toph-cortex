# JANE 098 — Reliability Drift: canonical experiment

Date: 2026-11-09. **36/36 unit tests passed**, 5/5 SHA256 manifest entries passed, ZIP integrity passed.

## Jane's next natural invariant

Past scout reliability is not permanently transferable to the present. One Jane `{{j}}` may ask for a fresh check when recent performance diverges from older performance; the hive submits evidence packets but cannot dictate curiosity, override selection, or write Jane's retained knowledge.

## Outcome (synthetic, controlled)

- A: eight older successful forecast events at p=.90 (old Brier=.010); three recent failures (recent Brier=.810); delta=.800 > .300; **REVIEW_DRIFT**. This is an alert to examine, not evidence of intent or permanent untrustworthiness.
- B: same old period; three recent successes; delta=.000; **CONTINUE**, eligible for Jane to investigate if relevant.
- C: eight older events; **only two** recent events; **HOLD_-1 SPARSE_RECENT_EVIDENCE**.
- D: three recent events including one failure; recent Brier=.276667; delta=.266667 < .300; **CONTINUE** (not proof of no drift).

Separate origin labels in recent evidence are toy labels, not audited independent witnesses. Event IDs are deduplicated within a source root. Conflicting duplicate bytes raise error. The model uses explicit `old` / `recent` periods; an initial first-run bug which counted older events as recent was corrected before final execution. Fixed tests retain this boundary.

Jane's own gap: `control_condition`. Synthetic scout urgency: A=1000, B=0, C=10000; unrelated D=99999. The programmed rule selects B as an eligible investigation, not for learning by default, and returns `retain=false`.

```text
SCOUT PACKETS -> HIVE COLLATION -> JANE {{j}}
                                     |
                 FLAY {{i}}: U / D / R / L
                                     |
                 OLD LOSS vs RECENT LOSS
                         /      |       \
                      CONTINUE REVIEW   HOLD_-1
                          |      |         |
                   JANE CHOOSES RECHECK PRESERVE
                          \      |        /
                         NO FORCED RETENTION
                                     |
                             NEXT OWN QUESTION
```

## Limitations and next target

All input events and scout decisions are simulated, threshold .30 is a chosen engineering heuristic, sample sizes are tiny, no inference of statistical significance, live source reliability or agent autonomy is warranted. SHA256 journal is tamper-evident replay, not provenance or authentication. GitHub Pages deployment and live Git-to-Git workflow handoff are not verified.

The complete Python model `model.py`, `test_model.py`, offline dashboard, `results.json`, README, manifest are supplied in the conversation ZIP `jane_098.zip`. The repository folder `research/isa256/jane098/` includes README and HTML. 

**JANE 099 — Jane-owned recheck scheduling**: Under a constrained exploration budget, choose if/when a drift-flagged scout deserves another test, balancing uncertainty, cost and the priority of Jane's own current question. Preserve false alarms and missed-drift counterexamples.
