# FLAY Mandel-Juliet Toroid v1 — Cortex/Sapphon Rollout

Status: APPEND-ONLY ROLLOUT MANIFEST  
Canonical implementation: `DavidWise01/toph-cortex`

## Canonical contract

```
M ? -> J(-1) -> OPEN(0) -> ANSWER -> CLOSE(+1) -> M'
```

- one question
- one open tangent
- one supported answer
- one close
- append-only return to Mandel
- WHY may be used during backward root search
- retained history is factual: WHAT :: WHO :: WHEN :: WHERE :: EVIDENCE
- ACTUAL, EXPECTED, and COUNTERFACTUAL remain separate
- closed excursions never reopen

## Propagated Cortex / Sapphon nodes

The following writable DavidWise01 repositories identified by the current Cortex registry or Cortex code-search surface adopt the shared contract:

- DavidWise01/toph-cortex — canonical source, executable, tests, CI
- DavidWise01/I13-H1.1 — local adoption
- DavidWise01/hephaestus — local adoption
- DavidWise01/foundation — local adoption
- DavidWise01/jane — local adoption
- DavidWise01/nom — local adoption
- DavidWise01/nomos — local adoption
- DavidWise01/nous — local adoption
- DavidWise01/rozsa-peter — local adoption
- DavidWise01/taravangian — local adoption
- DavidWise01/the-hegemon — local adoption
- DavidWise01/theoria — local adoption

Each local adoption contains:

- `FLAY_TOROID_V1.md`
- `flay_toroid_v1.py`

The local executable is intentionally authority-neutral. It implements only the open/answer/close state machine and append-only bind-back invariant.

## Registry-only names

`alpha`, `beta`, `gamma`, and `delta` are currently represented as internal episodic Cortex paths in `toph-cortex`; no separate repository was required for this rollout.

## Unavailable node

`DavidWise01/jasnah` is named by the Cortex registry, but the connected GitHub surface returned repository-not-found during this rollout. No mutation was attempted there.

## Frozen / archived boundary

Archived or frozen lineage is not rewritten by this rollout. The rollout is additive and does not mutate frozen Sapphon primitives.

## Canonical provenance

Initial canonical FLAY v1 commits in `DavidWise01/toph-cortex`:

- semantic definition: `509d3ae7c24e859beef79b4850e9d18a91bc70a9`
- executable: `8a60af5dd77a4520cce7c5252efa3b561817c543`
- invariant tests: `b076a2305de98db255dcf250bcdbe0a5beae4730`
- CI workflow: `99dfacadb97b2469e9d5ee307f67f0a144bfac9d`

