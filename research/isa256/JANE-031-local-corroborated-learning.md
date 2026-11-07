# JANE 031 — Locally Corroborated Distributed Learning

**2026-11-07. Status: 19/19 local tests PASS. Runnable Python module, tests, and minimalist HTML monitor are now committed to this repository** under `research/isa256/jane031/`, in addition to the packaged ZIP linked from the originating conversation.

## Natural invariant

**Received information is only a hypothesis until a primitive can corroborate it with its own experience.**

The lesson from a neighbor cannot directly overwrite stored local knowledge. An empty recipient starts with one observation of each transition (insufficient for the standalone threshold of three); a source starts with four observations. With a source report showing three or more consistent observations, one matching local observation promotes the relation into cellular slot-pair memory. A contradictory report is retained in provenance/conflict records without being learned. A replayed message ID is rejected, while delayed out-of-order messages are allowed. Message digests are unkeyed and not authentication.

## Geometry

One Jane; each primitive retains two arrays of 72 positions = 144 classical values. 57 cross-cell signed position pairs encode up to three records containing one valid bit, a 9-bit antecedent, and a 9-bit consequent. The previous 19-position body, symbolic GAP, fixed ISA-256 identities and 49,152-coordinate topology are unchanged. Records are encoded in the current two-cell state, not loaded as initial memorized output.

## Reproducible experiment

Three transition lessons are 17→68, 68→130, 130→17. Source sees 4 examples each; recipient and isolated control see 1 example each. Evaluate without updates. Run 100 separate seeds per message-loss rate:

| Message loss | Mean recipient correct / 3 | Mean isolated correct / 3 |
|---:|---:|---:|
| 0% | 3.00 | 0.00 |
| 15% | 2.51 | 0.00 |
| 50% | 1.48 | 0.00 |
| 100% | 0.00 | 0.00 |

19 local Python tests pass, covering two-cell shape, read/write physical differential encoding, blank memory, local threshold, untrusted neighbor report, corroboration, conflicting report, corruption/replay, out-of-order delivery, restart restoration, capacity, total loss, deterministic seeds and no-leakage baseline. The official unit command is `cd research/isa256/jane031 && python -m unittest -q test_jane031.py`.

## Limits

This is a **controlled classical learning model**, not a demonstration of emergent general intelligence or completely local nearest-neighbor cellular learning. Inputs come from a synthetic observation generator; an external test harness knows the target pattern, but the primitive's learning rule only sees its local examples and messages. A single misleading local observation can corroborate a forged report; checksums do not authenticate real senders. No asynchronous independent clock was integrated into this learning prototype. The online message source has learned its records first, so the recipient gains a specifically defined sample-efficiency advantage, not a general learning-to-learn advantage.

The offline dashboard in `index.html` displays precomputed experiment results, not a running learner. The exact complete local package with build script, JSON outcome data, and source integrity manifest was delivered in conversation as `jane_031.zip`.

## Next meaningful boundary — JANE 032

**False Corroboration / Self-Correction.** Inject wrong local observations and forged neighbor messages, then compare error detection, contradiction preservation and revision from later direct experience. Do not allow a checksum to masquerade as trustworthy evidence, and do not replace a learned memory without a transparent revision record.
