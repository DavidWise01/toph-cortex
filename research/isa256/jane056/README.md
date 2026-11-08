# JANE 056 — Hive Memory / Retrieve, Don't Replicate

**Classification:** executable classical architectural experiment, not a deployed internet-connected agent or a proof of recursive self-improvement.

## Natural invariant

Jane can delegate *external factual storage* to a distributed retrieval layer without outsourcing the local state required to remain the same agent: identity, immutable primitive geometry, active policy, a small working cache, and append-only decisions with provenance. When the network is absent, Jane uses a still-fresh cached answer with the status `CACHED_UNVERIFIED`; after its TTL expires she must abstain. Cloned reports with one root are not independent corroboration.

## Geometry preserved

1 tensor > 1 Jane `{{i}}` > 1 brace > 2 waldos `{-()+}` > 1 box > 1 toroid > 27 occupied positions; ternary `(-1,0,+1)` accounts for 27+3=30 counted components. Seam `27 → 27.5 → 1`; palindromic envelope `{([111222333444555555444333222111])}`.

## Five-step propagation

1. OBSERVE local failure and metrics.
2. PROPOSE three candidate retrieval policy variants (3 scouts).
3. TEST under the same training constraints with an isolated frozen baseline (1 stays).
4. RETURN two checks: invariant integrity and held-out performance (2 returns).
5. PROPAGATE a winning *policy only* if it improves scored held-out outcomes without additional false approvals; otherwise retain baseline. All policy changes append evidence.

The model demonstrates a *bounded* threshold optimization. It **does not** demonstrate recursive self-improvement across successive independent tasks. The benchmark's scoring function, quality margin and holdout remain fixed by the evaluator. Its threshold search is hand-specified, and its scoring uses labeled synthetic benchmark cases unavailable to the retrieval-time rule.

## Run

`python -m unittest -q` — 33 tests.

`python model.py` — prints four retrieval cases, offline cache behavior, conservation of identity and the tamper-evident local log.

Open `index.html` locally for the interactive offline dashboard. There is **no live internet search** in the dashboard or Python simulation. A production agent would require configured connectors/APIs, access permissions, throttling, source freshness checks and provider trust evaluation.

## Critical failure cases

- Multiple cloned reports from one dependency root never establish a 2-root quorum.
- Two genuinely separate roots can both be wrong, causing a false majority.
- Offline memory is provisional, not a fresh verified answer; expired cache is not promoted as truth.
- An append-only hash chain detects in-place modification *if its last trusted tip is retained*. Total ledger rewrite with tip replacement is not detectable by this internal chain alone.
- The central simulation and deterministic casebook do not establish the internet as a universally reliable memory substrate.
- The local cache is bounded; the durable evidence trail is conceptually retained on storage and is not necessarily bounded. A finite storage/archive policy would need separate tests.