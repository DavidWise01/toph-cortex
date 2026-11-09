# JANE 100 — Marginal Information / Overlap

Offline, deterministic simulation. No autonomous agent, live hive, verified source provenance, or actual online self-improvement is claimed.

## Run

```sh
python -m unittest -q
python build.py
```

## Decision invariant

Agents send packets with claims, costs, reason and declared source root. One Jane `{{j}}` asks what **new** distinctions a packet adds to her own question, within a bounded cost. The hive only collates. Packets don't write Jane's memory.

```text
SCOUT A {baseline, contrast} ----+
SCOUT B {baseline, contrast} ----+--> HIVE --> JANE {{j}}
SCOUT C {alternative, replication}+             |
                                                   |
                                            WHAT DO I LACK?
                                                   |
                                            FLAY U / D / R / L
                                                   |
                                         MARGINAL VALUE WITH BUDGET
                                                   |
                                        CHOOSE A+C / RETAIN FALSE
                                                   |
                                        OWN NEXT QUESTION OR HOLD
```

With budget 2: frozen additive packet scores choose A+B and *double count* overlapping evidence for an advertised total of 20; actual distinct coverage is only 10. The marginal planner chooses A+C, distinct coverage 18, while B's marginal information after A is zero.

**Important distinction:** shared *content* and shared *source ancestry* are different questions. Different source roots can duplicate the same fact, and one source root can contain several different facts. Mere root IDs do not prove independence. Weighted coverage scores are arbitrary engineering values, not physical entropy or true information-theoretic bits.

## Preserved first failure

`SYNONYM_ALIAS_UNRESOLVED` / `HOLD_-1`: two differently labeled claims might refer to the same fact; until their semantic equivalence is grounded, the planner must not certify them as distinct information. This is a known limitation, not a claim that the present string-matching model resolves synonyms.

The current `choose` function rejects claim IDs outside its frozen vocabulary. An unsupported alias is held; the next useful experiment learns a defensible equivalence mapping and tests both false merges and false splits.

## Test integrity

37 Python regression tests, reproducible result JSON, SHA-256 file checksums, ZIP integrity. Local SHA-256 chain detects alterations but is not authenticated witness testimony. Offline HTML is an interactive illustration of the same finite packet-coverage rule.

## Next natural invariant — JANE 101: Semantic Equivalence

Can Jane recognize that `baseline` and `control-condition` may describe the same underlying fact **without** incorrectly merging genuinely different claims? Agents propose mappings, Jane evaluates and accepts/rejects on unseen cases; stop at first false merge.