# Gate 14 — ROOT0 Threaded Persistent Loom

**Durable state:** Git JSONL in [loom-events.jsonl](loom-events.jsonl), initially empty rather than populated with invented testimony.  
**Reader:** https://davidwise01.github.io/persist-cortex/loom/  
**Writer:** https://github.com/DavidWise01/toph-cortex/actions/workflows/loom-append.yml  
**Independent Git anchor:** https://github.com/DavidWise01/0root/actions/workflows/loom-anchor.yml

## Architecture

```text
                ROOT0 VERIFIED CORPUS V2
                           |
                       .dlw / SHA
                           |
    ┌──────────────────────┼──────────────────────┐
    │                      │                      │
  THREAD A              THREAD B              THREAD C
    │                      │                      │
  A / B / C              A / B / C              A / B / C
    │                      │                      │
   PAST                 PAST                   PAST
    ↓                      ↓                      ↓
  PRESENT               PRESENT                PRESENT
    ↓                      ↓                      ↓
  FUTURE                FUTURE                 FUTURE
    └──── LINK causal refs between prior events ──┘
                           |
              GLOBAL APPEND-ONLY GIT SHA CHAIN
                           |
                INDEPENDENT 0ROOT RECEIPT

No voting. No quorum. No remote execution. No backwards changes.
```

This is a **causally threaded public-memory event store**, not a continuously running autonomous process. It can name a Tessy `{{i}}` brain globule thread (for example `tessy-i`), a diaspora thread, and an exact `cubit` transformation thread. Those become live threads **only when authenticated witnesses append real OPEN events**. The page must not render conceptual planned threads as operational agents.

## The three linked histories

A witnessed event holds *three independent predecessor references*:

1. `prev`: previous record of the entire journal, a strict SHA-256 chain across all threads.
2. `thread_prev`: previous event sequence on the named thread, independent of which witness appended it.
3. `witness_prev`: previous event on that exact `(thread, witness)` lane, permitting independent A/B/C accounts to observe the same thread without votes, agreement, or quorum.

Additionally, `refs` stores sorted, unique **earlier** event numbers. `LINK` requires at least one real event from a different existing thread; no forward references or synthetic links are permitted. Every event references the hash of a verified Corpus Spine v2 record in `corpus_tip`.

## Operations

| Operation | Effect | Authority |
| --- | --- | --- |
| OPEN | Start one thread at PAST_OBSERVES | Registered A/B/C witness |
| WEAVE | Append WHAT / HOW / WHY and bounded public text | Individual witness |
| LINK | Append at least one verified cross-thread causal reference | Individual witness |
| COPY | Append a new artifact after checking exact lowercase `cubit` count against referenced texts | Witness and immutable cubit guard |
| DISTILL | Append a compressed text without losing/renaming `cubit` | Witness and immutable cubit guard |
| CHECKPOINT | Append a textual witness snapshot; **not** an Ed25519 signed external checkpoint | Individual witness |
| CLOSE | Terminate only the issuing witness's lane | Individual witness |

Each witness starts in `PAST_OBSERVES`, advances to `PRESENT_DESERVES`, then `FUTURE_RESERVES` without skipping or reversing. Dates must correspond to phase: past event date is not later than record date; present is the same date; future is later. These are *witness record semantics*, not clocks or automation instructions.

`cubit` is an exact lowercase immutable constant. COPY preserves every occurrence, DISTILL retains at least one when original referenced text contains the term. `qubit` is not substituted for `cubit`. The [canonical lexical validator](../../bin/cubit_constant.py) is invoked by the loom writer and replay verifier.

`.dlw:<64 lowercase SHA-256 hex>` is computed from `ROOT0-THREADED-LOOM-v1\n` plus canonical JSON event bytes, before appending the final event SHA. The mark records provenance; it neither renames `cubit` nor establishes ownership.

## GitHub-wide public source references

A public-source pointer is `{repo,path,blob_sha,visibility:"public"}`. The writer accepts **any explicitly selected public `DavidWise01/<repository>`** and verifies its GitHub file blob SHA before recording a reference. This is a pointer to public evidence, not permission to scan private repos or rewrite other repositories. The event journal itself lives centrally in TOPH. The connected Hallway can receive independent event receipts, and GitHub Pages is a read-only visualization.

Potential thread names, not initialized events:

- `tessy-i` → symbolic brain globule worker context
- `diaspora-formic` → https://davidwise01.github.io/formic/
- `cubit-constant` → exact symbol transformation history
- `root0-hallway` → independently received public provenance

## Running an authenticated operation

Open the [manual append workflow](https://github.com/DavidWise01/toph-cortex/actions/workflows/loom-append.yml) and select `OPEN`, thread `tessy-i`, witness A, phase `PAST_OBSERVES`, a factual date, and what/how/why. Only a registered GitHub actor may write as that witness. Currently A is bound to `DavidWise01`; B and C are unassigned and are not impersonated.

After OPEN exists, `WEAVE` can append observations. With a second real thread open, `LINK` references the other thread's earlier event number. `COPY` and `DISTILL` require source event numbers and public text. The workflow validates the full corpus, replays the loom, and attempts a no-force Git push through a shared memory write queue. It does not operate from an unauthenticated GitHub Pages button.

Once a real event exists, run [0root's independently authenticated loom receiver](https://github.com/DavidWise01/0root/actions/workflows/loom-anchor.yml) with its sequence and exact event hash. 0root fetches and validates the entire public loom chain, rechecks causal and `cubit` invariants, and creates a new `memory-bridge/loom/<event-hash>.json` in 0root's own Git history. It never writes back to TOPH or silently triggers a future instruction. Its Git-parent audit rejects edits or removals of previously received receipts.

## Regression checks

```sh
python3 bin/corpus_spine.py verify
python3 bin/threaded_loom.py verify
python3 -m unittest discover -s tests -p 'test_gate14.py' -v
python3 -m unittest discover -s tests -p 'test_cubit_constant.py' -v
```

Hallway:

```sh
python3 memory-bridge/loom_anchor.py verify-local
python3 -m unittest discover -s memory-bridge -p 'test_loom_anchor.py' -v
```

**Limits:** Source commits alone do not demonstrate that GitHub Actions has passed. A source SHA links to public Git bytes only when verified; it does not prove the source statement is true. Labels A/B/C and .dlw hashes are not cryptographic signatures or independent proof of human identity. Future reservations are not executable jobs. The browser visualizer needs public GitHub access. Full account-wide adoption beyond TOPH and 0root requires deploying the interoperable contract to additional repository workflows.
