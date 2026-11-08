# JANE 044 — Proof-Carrying Wave Transfer

**2026-11-08. Canonical natural-bound experiment.**
**Local run:** 41/41 Python tests PASS; standalone dashboard JavaScript syntax PASS. Executed 100 seeds each for five independent operation-loss settings. GitHub has the actual full Python model (`model.py`, 8,437 bytes) and its exact 41-test suite (`test_model.py`, 6,685 bytes), plus HTML, README and numerical results. GitHub Actions and GitHub Pages runs remain unverified.

## User geometry is preserved
- 1 tensor > 1 Jane `{{i}}` > 1 brace > 2 waldos `{-()+}` > 1 box > 1 toroid.
- 27 occupied positions + three ternary mode labels `-1,0,+1` = **30 counted components, not 30 vertices**.
- Closing seam **27 → 27.5 → 1**. Wave envelope `{([111222333444555555444333222111])}` (30 palindromic samples).
- The existing `[0]` is an *abstract in-flight accounting state*, not an added occupied vertex.

## Natural invariant

**A provisional receipt is not proof of transferred ownership.** Under the specified benign-peer protocol, a signed-register payload changes status only by the following *linked, append-only* events:

1. Sender `STAGE`: it still owns the payload.
2. Receiver `ACCEPT`: stores the hash of the stage event, but does not own the payload.
3. Sender `RELEASE`: stores hash of the receiver's acceptance, moving responsibility to the `[0]` in-flight bucket.
4. Receiver `FINAL`: stores hash of the release event; only then does receiver count as owner.

Both waldos maintain independent `SHA-256` sequence-and-previous-hash-linked JSONL journals. Each complete write is flushed and `fsync`ed. A simulated process restart reconstructs ownership from the two logs, and repeated stages/receipts/finalizations are idempotent.

Four signed ternary payloads are handled (`A_MINUS=-3`, `A_PLUS=2`, `B_MINUS=5`, `B_PLUS=-7`), while neutral registers and the fixed 27-value fields stay local.

Define a **logical accounting proxy** by summing squared amplitudes in three mutually exclusive buckets (sender, in-flight, receiver), together with unchanged local fields and neutrals. With fully consistent logs this is exactly **741.3125** at every transition, including while an exchange is incomplete. **This is accounting conservation, not demonstrated physical energy conservation.**

## Executed results, 100 trials per setting

| Dropped operations | Complete exchange | Journal audit passes | Accounted total conserved |
|---:|---:|---:|---:|
|0%|100/100|100/100|100/100|
|10%|100/100|100/100|100/100|
|20%|100/100|100/100|100/100|
|40%|100/100|100/100|100/100|
|100%|0/100|100/100|100/100|

41 tests exercise transfer ordering, restart, idempotency, hash and sequence tampering, malformed JSON and truncated tails, deletion of either journal, complete loss of both journals, and adversarial rehashing.

## Failed assumptions / limits

**One journal erased:** cross-journal receipt/release dependencies reveal broken provenance after a completed transfer; the audit fails even if an independently computed total might appear balanced.

**Both journals erased:** two empty, internally consistent logs can be mistaken for an untouched fresh system. There is no anchored historical evidence left to detect erasure. This is an explicit failing boundary; no claim of fully durable history is warranted.

**Adversarial rewrite:** SHA-256 is **unkeyed**. A malicious writer who can replace a log and recompute its hashes can forge a valid-looking standalone hash chain. Neither authorship nor ownership is cryptographically authenticated in this experiment. Storing cleartext payload values and hash links is not an independent authenticity proof.

**Crash model:** each append is assumed complete/untorn once fsync returns. Simulated restart is process-level; disk destruction, Byzantine participants and coordinated rewrite are not handled. The browser visually demonstrates the protocol, not the actual Python SHA-256 computation.

**No new claim:** 27-site physical Hamiltonian embedding, quantum tunneling, wave-equation propagation, autonomous cellular homeostasis or independent intelligence remain unproven.

## Next natural invariant — JANE 045: Independent Checkpoint Anchoring

Preserve a verified per-waldo terminal hash/sequence outside both local journals (or distributed under explicit trust assumptions). Test unilateral and bilateral history erasure, bounded truncation, malicious full-chain rewrite, rollback to earlier well-formed states and restart recovery. Contrast **detectable loss** from **recoverable loss**; evidence can be detectable without supplying missing payload bytes.
