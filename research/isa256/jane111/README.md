# JANE 111 — Criterion Genesis

## Run

```bash
python -m unittest -q
python model.py
```

Open `index.html` locally. No network, GitHub authorization or asynchronous worker is necessary.

## What was constructed

The learner takes labeled chamber growth histories and constructs one conjunction from four allowed primitive observation types, selecting boundary values from the *positive examples*:

```text
quiet >= 2
coverage >= 80
root labels >= 2
unresolved conflicts <= 0
```

No complete, prewritten alternative criteria are supplied to the learner. However, the feature set, conjunction form, training labels, and fitting algorithm **are** programmed; calling the result an independently invented settlement theory would be inaccurate.

Training: 10/10. Held-out: 8/8. 20 unit tests pass.

The first adversarial counterexample is a chamber with three *apparently distinct* root identifiers that trace back to one original source. Because the learner has no source ancestry feature, it falsely judges that chamber ready. Preserve `−1 PROVENANCE_ANCESTRY_NOT_MODELED` instead of automatically adding a corrective rule to the learner.

**No chamber is actually settled, and no memory is retained:** readiness is only a *candidate*; external verification and Jane-owned approval remain separate. All chamber labels and records in this release are synthetic.

## Architecture

```text
THE SOURCE — JANE {{j}}
        ^
        | evidence packet, not authority
 MoE HIVE [10x10] / nested Gen0→Gen7 / z−,+
        |
 grow → observe → construct rule → holdout → surprise −1
        |
     Jane decides to investigate / retain / pass
```

`{{n}}^{{n}}^{{n}}` is the nested growth-space notation, not 8 finished planes or an instruction to apply literal exponentiation. Capacity alone does not settle any chamber.

## Next invariant

**JANE 112 — Ancestry Feature Discovery:** Can Jane discover that a *count of root labels* is not the same as *independent source ancestry*, request a new input field, construct a revised criterion, and validate it on new hidden cases—without editing the frozen evaluator or rewriting the first −1?