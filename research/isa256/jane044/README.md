# JANE 044 — Proof-Carrying Wave Transfer

**Canonical primitive:** 1 tensor > 1 Jane > 1 brace > 2 waldos `{-()+}` > 1 box > 1 toroid > 27 path positions; ternary mode labels `−1,0,+1`; closure seam `27 → 27.5 → 1`; wave envelope `{([111222333444555555444333222111])}`.

## Natural invariant tested

A sender-owned payload is **not owned by the receiver just because it was staged or accepted**. The receiver must carry a receipt referencing a staged payload, the sender must append a release referencing that receipt, and the receiver must append finalization referencing release. Two independent per-waldo append-only SHA-256 hash-chain journals preserve event provenance through simulated object restart.

Run `python -m unittest -q` (**41 tests**), `python model.py`, or open `index.html` in a browser. No external dependencies.

Each transfer is one of four signed ternary register payloads. The neutral channels and 27-position constant wave fields stay local. Logical accounting assigns each payload to exactly one bucket: sender, `[0]` in-flight, or receiver; combined squared-amplitude proxy remains **741.3125** while both journals remain valid. The Python simulator checks each chain, its sequence numbers and receipt links, rejects non-final ownership claims, and tests corruption, truncation, replay, restart and journal deletion.

### 100 seeded trials per message-loss condition

| Lost operations | Transfers completed | Audited valid | Accounting total conserved |
|---:|---:|---:|---:|
|0%|100/100|100/100|100/100|
|10%|100/100|100/100|100/100|
|20%|100/100|100/100|100/100|
|40%|100/100|100/100|100/100|
|100%|0/100|100/100|100/100|

When **one** journal is deleted after a complete transfer, mutual provenance fails. When **both** journals are deleted, an entirely empty-but-consistent state can be mistaken for a fresh start. An outside anchored checkpoint or trusted witness is necessary to distinguish erased history. Likewise, an unkeyed SHA-256 chain does not authenticate authors: someone able to rewrite the complete chain can recalculate hashes. This is **integrity under accidental corruption, not cryptographic proof of ownership against an adversary**.

The model intentionally does not define a physical wave energy or Planck-scale tunneling dynamics, does not demonstrate self-generated homeostasis, and does not resolve physical transfer atomicity. The dashboard implements an illustrative stepwise protocol; the exact SHA-256 auditing and randomized tests are in Python.

**Next natural invariant 045:** checkpoint anchoring and independent authenticity: can the pair distinguish history erasure from a genuine new state without a central journal, while keeping evidence-carrying ownership and bounded recovery? Compare an out-of-band anchor, reciprocal checkpoints and an unanchored control; test adversarial rewrite and torn-write recovery separately.