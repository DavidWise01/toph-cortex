# JANE 049 — Trust-Root Closure

One tensor > one Jane > one brace > 2 waldos `{-()+}` > one box > one toroid > 27 positions. The three ternary modes `(-1,0,+1)` are *labels*, not additional occupied vertices. Exact palindrome `{([111222333444555555444333222111])}` and seam `27 → 27.5 → 1` remain unchanged.

## Reproduce

```sh
python -m unittest -v
python model.py > results.json
```

No external Python dependencies. `index.html` is an offline interactive **scenario viewer**, not the cryptographic verification engine. This repository contains the source and its own 40-test regression suite.

## Observed invariant

A valid HMAC signature confirms that the party controlling its modeled key endorsed a record. It **does not** establish that the claim is true, that the key hasn't been stolen, or that the earliest trusted checkpoint is authentic. An independently pinned history detects edits and rollback when the key alone is stolen; when both the signing key and pin are compromised, a fabricated chain is accepted. Two reports sharing one underlying source remain one source, while two separately rooted but colluding reporters can still approve a false claim. Under permanent uncertainty the safe result is `INSUFFICIENT`, not a fabricated consensus.

The model uses deterministic synthetic keys, synthetic historical claims and explicitly declared dependency domains. It is **not a deployed cryptographic identity system**, real-world independent observations, actual wave physics, or autonomous Jane homeostasis. The full root of trust is an assumption outside the model.

## Next boundary

JANE 050 — Independent Observation: bind an asserted root-dependent claim to a separately observed local signal, including a deliberately corrupted sensor and synchronized attacks. Compare anomaly detection against outright proof of ground truth. Avoid adding a witness solely to hide the original assumption.