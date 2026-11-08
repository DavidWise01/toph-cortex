# JANE 043 — Distributed Gap Ownership

**Date:** 2026-11-08. Canonical single primitive: one tensor, one Jane, brace, 2 waldos `{-()+}`, box, toroid, 27 positions and three ternary labels `-1,0,+1`. The 27→27.5→1 seam is a symbolic transition; no 28th spatial position is created. Wave envelope: `{([111222333444555555444333222111])}`.

## Invariant

Each of four signed payloads has exactly one **logical accounting owner**. Two independent append-only JSONL files store the waldo-local evidence; there is **no shared gap journal**. A payload transitions from origin register → sender escrow → receiver escrow → delivered register, with a durable receiver acceptance preceding a source release. The accepted-but-unreleased receiver copy is **not yet counted as owned**. An idempotent retransmission does not duplicate transfer.

Local Python run: `python -m unittest -q` (41/41 PASS); `python model.py` (100 seeded trials for each loss rate); open `index.html` offline for browser visualization. No external packages. Python serializes the event order in one process. This is a **central simulation harness** observing two distinct local journals, not a genuinely distributed runtime.

## Simulated results

| Per-event drop | Finished / 100 | Conserved accounted total / 100 |
|--:|--:|--:|
| 0% | 100 | 100 |
| 10% | 100 | 100 |
| 20% | 100 | 100 |
| 40% | 100 | 100 |
| 100% | 0 | 100 |

The accounted total is 741.3125: stationary spatial fields + neutral registers + all four signed payloads, regardless of which local journal currently establishes ownership.

## Crucial counterexample

Destroying one journal after an otherwise completed transfer can leave a **numerically unchanged total**, since reconstructed defaults can coincidentally count the payload in the origin instead of the destination. Therefore an explicit cross-journal provenance audit is required: ACCEPTED without source STAGED and CONFIRMED without source RELEASED are invalid. A surviving peer's journal alone does not necessarily determine correct global ownership after permanent data loss. The release includes a failing-history test.

## Limits

The source-owner rule is stipulated, not learned. Both peers' records must be inspected to prove global total; a local node cannot always know whether a remote RELEASE was written. The program assumes atomic JSONL appends and no malicious forged messages, concurrent conflicting writers, power-failure torn writes or storage-media failure except the simulated deletion. Message drops are emulated with a seeded random generator, not network transport. The named 27 spatial regions do not yet have a verified embedding. This is a **classical bookkeeping conservation**, not real tunneling, quantum physics or autonomous homeostasis.

**Next natural invariant:** JANE 044 — local proof of transfer: construct a minimal cryptographically or structurally verifiable receipt sufficient to distinguish an accepted shadow from an owned payload, and test power-loss torn records and inconsistent partner histories. Do not mistake checksum for trustworthy authorship; account for availability under permanent partition.