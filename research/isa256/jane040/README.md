# JANE 040 — Peer-led seam recovery

2026-11-07. Canonical primitive: one tensor → one Jane → one brace → two waldos `{-()+}` → one box → one toroid → 27 occupied positions; `(-1,0,+1)` is a three-label register (27+3 counted components). Closing seam: `27→27.5→1`. Wave envelope `{([111222333444555555444333222111])}`.

**Run:** `python -m unittest -q` (40 tests); `python model.py` (200 seeded trials at each loss rate); open `index.html` locally. No third-party libraries.

**Finding:** If a durable coordinator `COMMIT`/`ABORT` decision copy is present on either peer, it can be forwarded to the other after coordinator disappearance and reconstruction from append-only fsynced journals. Duplicate delivery does not duplicate application. Under eventual reconnection, the pair closes or aborts; without a surviving decision copy, both prepared peers cannot decide correctly and remain `IN_DOUBT`. Permanent partition is also blocking. Contradictory proof is quarantined rather than accepted.

**Crucial limit:** This is peer-*recovery* of an existing coordinator decision, not coordinator-free consensus. Each participant currently stores the full peer's original register to reconstruct exchanged channels; no direct physical amplitude transport is modeled. The intermediate half-committed norm proxy is 802.3125 versus 741.3125 before and after. Local durable writes use flush+fsync but do not model torn writes, disk loss, forged certificates, or power-loss ordering. The `index.html` is an interactive readout of precomputed results, not a live Python execution.

**Next bound:** Remove the coordinator from decision formation, or prove why commit/abort remains ambiguous without additional durable evidence. Test independent peer-led decision rules under simultaneous crashes, partitions, and conflicting memories.