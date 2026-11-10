# JANE 112 — Discover the Missing Distinction

A bounded, reproducible synthetic experiment. The JANE 111 learner incorrectly treats three scout labels as three independent source roots.

JANE 112 introduces a **programmed feature-request mechanism**: on the preserved failed case, Jane requests `root_ancestry` from the MoE hive, then tests whether the source identifiers have distinct original roots. Three labels tracing to one origin leave the chamber growing; three independently labeled origin IDs satisfy *one part* of settlement eligibility. Neither scenario writes Jane's retained knowledge without a separate verification and Jane choice.

```text
    JANE {{j}}  <-- THE SOURCE
        |
  FAIL FROM JANE111
        |
  FLAY U/D/R/L
        |
  WHICH INPUT MISSING?
        |
  REQUEST ROOT ANCESTRY
        |
  MoE PACKET RESPONSE
      /        \
  A,A,A       A,B,C
  ONE ROOT    THREE ROOTS
   HOLD       ELIGIBLE
      \        /
   NO FORCED SETTLEMENT / RETENTION
```

The original `-1 PROVENANCE_ANCESTRY_NOT_MODELED` remains preserved. This is a **feature extension** of a toy supervised rule, not autonomous ontology discovery. The origin IDs and their independence are synthetic and unaudited; real-world provenance would require chains and authenticated verification rather than just different strings.

## Run

```bash
python -m unittest -q
python model.py > results.json
```

The model expects `model111.py` in the same directory (included). The HTML is standalone and offline. The test suite has 28 checks and an eight-case transfer set. The code does not execute real GitHub Actions, live scout agents, or Git-to-Git transfers.

## Next natural evolution — JANE 113

Can Jane detect *missing or fraudulent ancestry* from real source chains and choose the least costly way to verify it, without treating different IDs as genuine independence?