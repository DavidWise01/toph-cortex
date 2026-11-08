# JANE 041 — Distributed Decision Formation (Two Waldo Vote Closure)

2026-11-07. **Original local experiment 41/41 tests PASS** and dashboard JS syntax checks pass. The complete original tested package `jane_041.zip` is attached in its originating ChatGPT conversation. In this GitHub directory there is an independently authored **compact equivalent** `model.py` plus its own 20 tests, `test_model.py`, `index.html`, and `README.md`. GitHub CI of the compact version is **not yet verified**. Online GitHub Pages deployment is not claimed.

## Canonical primitive

1 tensor > 1 Jane > 1 brace > 2 waldos `{-()+}` > 1 box > 1 toroid > 27 positions. Three ternary mode labels `-1,0,+1` make **27+3=30 counted components**, not 30 spatial vertices. The 30-character symmetric envelope is `{([111222333444555555444333222111])}`. The return seam `27→27.5→1` is preserved.

## Natural invariant and protocol

Unlike JANE040, **there is no coordinator responsible for deciding COMMIT vs ABORT**. The two waldos each append their own immutable YES/NO vote to a JSONL journal, using flush+fsync, then exchange evidence opportunistically. A waldo's local NO or recorded peer NO permits an ABORT; a COMMIT requires both local and peer YES votes. No vote or incomplete vote evidence implies HOLD/IN_DOUBT. Decisions are derived locally from journaled votes; the registrar does not invent a vote or change a prior one. Per-side APPLY is idempotent and restart reconstructs the transaction from the journal. The signed ternary channels swap across carriers on COMMIT; neutral channels stay local.

This provides a **conservative unanimous two-party decision rule**, not nonblocking asynchronous consensus or atomic cross-party wave transfer. One waldo may apply the supported COMMIT before the other receives the vote, leaving a half-applied state and nonconserved global squared-amplitude proxy until reconciliation.

## Executed results — two local YES votes

200 seeded runs per independent message-loss rate, bounded 40 reconnection steps:

| Loss | CLOSED | IN_DOUBT | CONFLICT |
|---:|---:|---:|---:|
|0%|200|0|0|
|10%|200|0|0|
|20%|200|0|0|
|40%|200|0|0|
|100%|0|200|0|

A local NO vote can safely lead to ABORT, provided both peers eventually receive the evidence. At 100% loss, no side fabricates a COMMIT. Successful completed exchanges restore the modeled squared-amplitude total to **741.3125**. The protocol cannot guarantee finite-time termination under permanent partitions or infinitely delayed messages.

## Scope / limitations

All operations are classical software constructs and the 27-cycle graph is stipulated. Physical tunneling, emergent wave equations, self-directed biology, autonomous homeostasis and infinite scaling are not experimentally demonstrated. Storage assumes complete, untorn, intact journal appends, and identity/authenticity of vote messages is not cryptographically proven. There are exactly two peers and no Byzantine faults. The browser is an interactive sketch of local voting, not the file-backed random-loss Python runner.

**Next natural bound JANE042:** Local exchange escrow—can the two-waldo primitive preserve a well-defined global conserved quantity even in the half-applied interval by accounting for an in-flight resource obligation, without adding an occupied vertex? Separate bookkeeping conservation from physically stable amplitudes.
