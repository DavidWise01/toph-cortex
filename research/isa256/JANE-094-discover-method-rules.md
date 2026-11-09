# JANE 094 — Discover the Method's Rules

**2026-11-09. Local experiment: 32/32 Python tests PASS; browser JS parses; ZIP integrity PASS.**

## Invariant

An apparently correct method is not a justified method if the observed evidence leaves its ordering ambiguous. **Jane must seek discriminating evidence before approving her own proposed method.**

The JANE094 **learner has no preloaded method-dependency graph**. It receives six role names and four binary pairwise observations, constructs a precedence DAG from positive/negative outcomes, and performs deterministic topological sorting. It separately reports uncertainty when more than one node is available at any step.

```text
SCOUT FRAGMENTS (unordered)
         |
     JANE {{j}}
         |
  INFER ORDER EDGES
         |
      AMBIGUOUS?
       /      \
     YES       NO
      |         |
 HOLD_-1     HOLDOUT
      |         |
 CHOOSE PROBE  VERIFIED?
      |         |
 EXTERNAL TEST  YES -> ELIGIBLE
      |         |
  UPDATE DAG   NO -> -1
      |
     REPEAT
```

## Test result

- Frozen six roles: `observe, baseline, contrast, alternative, intervention, replicate`.
- Training: 4 pairwise observations. The first topological ordering *happened* to match the evaluator's reference, but five relative-order questions were unresolved. **First method rejected as `AMBIGUOUS`**, failure journal preserved unchanged and fingerprinted.
- Jane's **programmed** query heuristic selected five subsequent precedence checks. External synthetic evaluator replied PASS/FAIL.
- Final inferred order: `observe -> baseline -> contrast -> alternative -> intervention -> replicate`.
- Final status: `READY_FOR_TEST`; three synthetic holdout labels PASS (motion, crystal growth, algorithm runtime). No contradiction/cycle tolerated; WALL or missing ancestry ignored.
- No automatic retained-memory write, authorized live scout interaction, online reading, physical experiments, or cross-repo handoff occurred.

## Important scope limits

The six role names and the query-selection rule are hard-coded. The hidden toy evaluator is built using the reference order; Jane's learner is not given that graph. The three holdouts share the same six abstract roles and are **not** a test of transfer to an unseen ontology. This is bounded constraint inference, not proof of original causal scientific discovery or autonomous recursive self-improvement. Source ancestry labels are synthetic; hashes do not independently establish authenticity.

The complete runnable source (`model.py`, `test_model.py`, `build.py`), `index.html`, results and SHA-256 manifest are packaged in the conversation artifact `jane_094.zip`; this GitHub record is not a claim the local sources have been separately committed or that Pages deployed.

## Next natural invariant — JANE 095

**Which experiment is worth running?** Jane should choose between competing uncertain hypotheses using packet-supplied evidence, bounded experiment cost, expected information gain and the option to abstain. Freeze an evaluator and test unseen role sets; stop on the first negative transfer.
