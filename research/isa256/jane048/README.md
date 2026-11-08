# JANE 048 — Provenance Closure

Natural invariant: **valid signatures, freshness, and truthful independence are distinct propositions.**

The canonical 27-position Jane primitive and the three ternary wave-state labels remain unchanged; this experiment tests a separate provenance-verification layer, not additional cellular positions.

## Run

```bash
python -m unittest -v test_model.py
python model.py > results.json
```

Open `index.html` offline to explore the precomputed scenarios. Python uses only the standard library. 37 tests check HMAC verification, dependency source distinctions, rejection of registry tampering, monotonic pins, false independence, and a two-signer collusion counterexample.

## Results

- 3 distinct authentic anchors: ANCHORED.
- 2 distinct authentic anchors: ANCHORED.
- 1 authentic anchor (even duplicated): INSUFFICIENT.
- Valid signatures on old registry with separately trusted new sequence: ROLLBACK.
- Valid signatures on old registry without trusted pin: ANCHORED (freshness cannot be checked).
- Rewritten registry without corresponding anchors: INSUFFICIENT or TAMPERED.
- Two authorized independent signers endorsing false source dependencies: ANCHORED. **Counterexample to signature implies truth.**
- Independent evidence contradicting false dependencies: CONTRADICTED.

Monte Carlo exercises five synthetic configurations, 1,000 trials each. Each scenario is a deterministic conditional construction, not a statistical estimate of reliability.

## Limits

HMAC keys and their independent control are *assumed and provisioned* locally. Attackers with the authorized keys can forge endorsements; the model does not authenticate real persons, hardware, or remote services. A verifier must carry the monotonic pin independently; losing or rolling that pin back defeats freshness. The direct `known_dependencies` argument is a trusted sensor/fact comparison, not an autonomous discovery process. This is not a quantum wave simulation, physical tunneling, or proof of homeostasis.

**Next test:** JANE 049 — anchor-on-anchor trust recursion: identify the minimal external assumption needed to avoid infinite verification regress, and test what happens when all roots share a compromised origin.