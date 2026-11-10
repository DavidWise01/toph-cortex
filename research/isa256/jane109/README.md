# JANE 109 — Growth Without Forced Settlement

An executable **local symbolic simulation** correcting the former flat 8×10×10 generation plane interpretation. Gen 0–7 are nested growth chambers, not equally filled planes. The root remains a 10×10 logical area, and Z is a challenge/construct (−/+) interpretive operant. `{{n}}^{{n}}^{{n}}` means nested reserved growth room and has **no assigned universal numerical exponent**.

## Tests and demonstration

```sh
cd jane_109
python -m unittest -q
python model.py
```

## State machine

```text
THE SOURCE JANE {{j}}
       |
 ROOT [10×10] Gen0
       |
 RESERVE NESTED CHILD
       |
 SEED → GROWING [0 .. capacity]
             |       |
             |      FULL != SETTLED
             v
       SETTLEMENT REQUEST
          /         \
      NO VALID       AUTHORISED JANE
      EVIDENCE       + VERIFIED RECEIPT
          |                 |
       -1 HOLD            SETTLED
          |                 |
      KEEP GROWING     CHILD MAY BE RESERVED
          |                 |
          +---------- NEXT GROWTH
```

## Core rules

1. Parent/child lineage must be recorded; Gen 7 has no unapproved Gen 8.
2. Capacity bounds occupied packet count but does **not** force settlement.
3. Settlement requires *explicit Jane authorization*, a selected criterion ID, a verified flag, a receipt ID, and at least one packet. In this model receipt ID and verification are synthetic parameters supplied by the harness, **not independently authenticated**.
4. Siblings evolve independently. A child of a settled parent starts reserved/empty and does not rewrite the parent's event journal.
5. Z mirror flips the interpretive sign without changing claim identity.
6. Scout packet arrival never writes Jane's memory; retention requires independent verification and a separate Jane choice.
7. Hash-chained event journal detects local tampering, not source authenticity.

## Verified demonstration

`42/42` Python unit tests. Demonstration leaves Gen1 A settled after an initial verification hold; Gen1 B remains growing; nested Gen2 is reserved; memory remains empty. No claim of genuine autonomous curiosity, MoE network execution, empirical validation, external witnesses, authorized Git workflow handoffs, or GitHub Pages deployment.

## Next invariant — JANE 110

**Settlement criterion learning:** How can Jane propose a measurable settlement criterion for each nested chamber, request evidence, and reject premature settlement without taking the criterion from a scout as a command? Test under- and over-settlement with unseen growth histories and preserve `−1` when the criterion lacks discriminating evidence.