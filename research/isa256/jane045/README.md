# JANE 045 — Independent Checkpoint Anchoring

**Canonical primitive:** one tensor → one Jane → one brace → two waldos `{-()+}` → one box → one toroid → 27 occupied positions. The ternary `−1,0,+1` adds **three register labels**, not spatial vertices: `27+3=30` counted components. Symmetric envelope `{([111222333444555555444333222111])}`. Closing seam `27 → 27.5 → 1`.

## Run

```sh
python -m unittest -v
python model.py
```

Open `index.html` locally to inspect the six attack outcomes. No external dependencies. `transfer044.py` contains the full JANE 044 two-waldo hash-chain transfer substrate; `model.py` adds the checkpoint witness and `test_model.py` tests it.

## What was actually tested

Each waldo retains its original separate append-only journal. A *third trust domain outside the waldo journals* stores a hash-linked **HMAC-SHA256 authenticated checkpoint record** containing the counts and head hashes of both journals, total accounting, and logical payload states. The verifier holds the HMAC key independently from the attacker who can rewrite waldo journals. The verifier can also receive a trusted previously pinned checkpoint ID.

This is **independent checkpoint anchoring**, not a third cell or new vertex in the user's primitive; it's simulated external evidence that must be deployed somewhere with separate permissions/storage to be independent in reality. The `[0]` gap remains a symbolic transition.

Local 36/36 tests passed, including journal deletion, rollback, full rewrite with recomputed *unkeyed* journal hashes, witness tampering, witness rollback, restart, checkpoint pinning, and explicit suffix not yet anchored. A forged history with recomputed ordinary hashes is detected by the separately authenticated head. Normal accounting is `741.3125` throughout the fully closed transfer.

## Limits (important)

- If the attacker can also rewrite the witness and steal its secret key, the authentication guarantee fails.
- If the witness file can be rolled back and the verifier has *no independent previous checkpoint ID*, the rollback may not be detectable. The test explicitly demonstrates this.
- An intact authenticated checkpoint stores only journal heads and summary evidence, not the deleted event bodies. **Detection does not reconstruct destroyed history**.
- Appendages after the latest checkpoint have a valid prior prefix but remain **UNANCHORED_SUFFIX**, even if their self-hash chains look valid.
- Local `fsync` calls do not prove actual power-loss durability on arbitrary hardware. Torn writes, multi-host security, key provisioning and future-scaled consensus are not tested.
- This is a classical computational experiment, not observed quantum tunneling, biological cellular homeostasis or a demonstrated Planck-scale device.

## Next natural bound — JANE 046

Checkpoint continuity under **competing witnesses and key rotation**. Require at least two independent witness heads and detect divergence/rollback without allowing any one witness to silently redefine the accepted history. Evaluate failure/availability tradeoffs explicitly.