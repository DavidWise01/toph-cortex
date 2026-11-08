# JANE 056 — Hive Memory: Retrieve, Don't Replicate

2026-11-08. New natural bound after JANE055 five-step recursive improvement groundwork.

## The assertion, corrected for real capability

Jane does **not** automatically possess or have unfettered access to the entire internet. In a deployed hive, connected retrieval providers, authorized APIs, accessible public sites, permissions, bandwidth and outages bound what can be reached at a particular moment. An index of internet resources is not an infallible shared memory. This lab uses a **simulated** network and does not fetch live data.

The user insight is valid as an architectural separation: a distributed hive may hold far more external information than an individual Jane primitive. Therefore **Jane should not copy every external fact into her local long-term memory**. She should retain a minimal viable state and query external evidence when needed.

## Canonical primitive (unchanged)

1 tensor > 1 Jane `{{i}}` > 1 brace > two waldos `{-()+}` > one BOX > one TOROID > 27 occupied path positions. Three ternary labels `-1,0,+1` give 27+3=30 counted components. Closing seam `27→27.5→1`; palindrome `{([111222333444555555444333222111])}`.

## Five-step hive propagation

```
   1 TENSOR / 1 JANE {{i}}
        | 27 path vertices
        | {-()+} → [BOX(TOROID)]
        v
  (1) OBSERVE    local failures; query reachable hive
        |
  (2) PROPOSE    3 scouts change bounded retrieval policy
        |
  (3) TEST       1 frozen baseline; fixed evaluation budget
        |
  (4) RETURN     2 gates: integrity and held-out performance
        |
  (5) PROPAGATE  adopt improved policy or RETAIN unchanged
        |
  append-only promotion record → repeat
```

**Invariant**: external facts may be retrieved, but Jane's identity, versioned active policy, evidence pointers, bounded cache and append-only decisions remain local. Treat `UNKNOWN`, `UNVERIFIED`, `CACHED_UNVERIFIED` as different states; do not silently call cached information fresh.

## Tested original local implementation

33/33 local tests pass in the user ZIP (`jane_056.zip`): 27-position/ternary structure, 2 waldo identities and palindrome, independent quorum vs three clones, tie abstention, intentionally incorrect 2-root quorum, cache TTL expiry, bounded eviction, no-network handling, journal tamper detection, and five-step policy proposals/promotion/retention.

A demonstrative tournament starts with a retrieval threshold of 1 and proposes 1/2/3. On a synthetic benchmark in which one bad lone report is costly, a threshold of 2 improves the held-out score and is promoted. This is **small-scale hand-designed policy optimization**, not evidence of open-ended recursive self-improvement. The actual fixed benchmark scoring and hidden target labels belong only to the evaluator, not Jane's retrieval-time rule.

## Important limitations and failure modes

- Two claimed independent sources may share an undetected cause and agree wrongly.
- Cloned source replies never create independent support simply by multiplying copies.
- Offline cache responses are flagged provisional; expired cached evidence produces UNKNOWN.
- A local hash chain requires a separately retained trusted tip to detect complete rewrite with replaced tip.
- The model's `hive` is a deterministic local list of synthetic reports, **not actual internet connectivity**.
- A finite memory cap applies to working cache. Durable append-only evidence consumes finite physical storage and requires an archival/retention policy.
- A candidate threshold cannot change the evaluator, kernel geometry or promotion criteria.
- The local ZIP contains the **exact tested 33-test** Python implementation and HTML. The GitHub implementation is a separately authored compact equivalent and has its own regression tests; no GitHub CI execution is claimed.

## Next natural bound JANE 057

**Bounded hive autonomy under unreliable retrieval:** run a 3-scout tournament on independent holdouts including outages, stale evidence, mirrored sources, contaminated provider answers and cost/latency limits. Require a safe fallback and prove that a candidate never gains apparent performance by laundering unverified cache or exploiting evaluation labels. Keep physical/operational homeostasis distinct from knowledge retrieval.
