# JANE 043 — Distributed Gap Ownership

Date: **2026-11-08**. **41/41 local Python tests PASS; browser JavaScript syntax PASS**. The complete offline release is `jane_043.zip` in the originating conversation. GitHub source `research/isa256/jane043/model.py` and `test_model.py` were verified against the original local files by identical Git blob SHAs (**1506b9b86e20347fdf15501032e8266ff7ac5bd5** and **0682ac8f223047e75d695de3ebf3423682cf571a**). The HTML and README are also committed, but their Git blobs are not byte-identical to the local copies due to connector text serialization. GitHub CI / Pages deployment is unverified.

## Preserved geometry

One tensor > one Jane > one brace > two waldos `{-()+}` > one box > one toroid > 27 path positions, ternary labels `(-1,0,+1)`: **27 positions + 3 labels = 30 counted components**, not 30 vertices. The wave notation is `{([111222333444555555444333222111])}`. The 27→27.5→1 seam is an unoccupied transition, not a new cell. The bracketed `[0]` gap is conceptual, not a central shared persistence service.

## Invariant tested

Each signed wave payload has one **logical accounting owner** throughout a bilaterally journaled transfer:

1. The sender records STAGED on its own append-only log. It is still owner.
2. The recipient records ACCEPTED on its independent log. Its copy is a shadow, not yet counted as owned.
3. The sender verifies ACCEPTED and records RELEASED, transferring accounting ownership to the recipient.
4. The recipient records CONFIRMED. In-flight escrow becomes a delivered register.

Each phase is idempotent; reopening the same two local journals after restart reconstructs the transfer state. The Python simulator runs both journals in **one orchestrating process**; it is not a decentralized production network, and its code assumes complete atomic JSONL appends with fsync. The combined accounted squared-amplitude proxy stays **741.3125**, including origin registers, sender escrow, recipient escrow, delivered payloads, and fixed fields. Conservation is by deterministic bookkeeping, **not physical wave-energy conservation**.

## Executed fault tests

100 seeded simulations per drop rate; 40 retry rounds with process-object reconstruction after tick 1.

| Loss | Finished all 4 payloads | Accounted total conserved |
|---:|---:|---:|
|0%|100/100|100/100|
|10%|100/100|100/100|
|20%|100/100|100/100|
|40%|100/100|100/100|
|100%|0/100|100/100|

## Newly discovered counterexample: conservation without provenance

Removing waldo A's journal after an otherwise complete transfer leaves all four originally specified payload amplitudes *numerically countable*, so the total can still equal 741.3125, while the reconstructed log history contains four invalid cross-journal dependencies:

- `Aminus:accepted_without_source`
- `Aminus:confirmed_without_release`
- `Aplus:accepted_without_source`
- `Aplus:confirmed_without_release`

Thus **correct numerical accounting is not proof of a valid transfer history**. Global proof requires evidence from both peers; one local waldo may not know if a remote RELEASE has been durably written. Permanent partner or journal loss can make actual ownership unknowable from surviving evidence, even where an aggregate numerical sum appears conserved.

## Boundaries not crossed

No physical quantum tunneling, actual wave equation, autonomous cellular homeostasis, verified graph embedding for the 27 named positions, distributed Byzantine security or infinite-scale result has been demonstrated. The protocol relies on a trusted simulation harness and assumes benign complete writes. Torn records, storage corruption, forged acknowledgments, malicious peers and concurrent conflicting authors are not tested.

## Next natural invariant — JANE 044: Proof-Carrying Wave Transfer

Give each receiver a source-backed, immutable, locally checkable RELEASE receipt that distinguishes a provisional ACCEPTED shadow from an actually owned payload, then simulate torn writes, reordered logs and conflicting receipts. Separate mathematical energy accounting from the availability of decisive ownership proof under permanent partition. Do not confuse a checksum with sender authentication.
