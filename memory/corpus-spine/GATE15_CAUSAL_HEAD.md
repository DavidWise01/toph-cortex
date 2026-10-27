# Gate 15 — Causal head lock / Threaded Persistent Loom

**Snapshot time:** 2026-10-27. This is a read-only operational protocol, NOT another witness event.

## Why

A valid event may arrive after another witness or GitHub writer changes a thread. An old form must not be silently applied to a new head. Gate 15 protects the **exact observed causal predecessor** while retaining the original append-only ledger, the temporal diode, `.dlw` and lowercase `cubit`.

### Verified starting point

- Canonical thread: **`tessy-1`** (digit one), first real `OPEN` at `seq=1`.
- Witness: `A`; phase: `PAST_OBSERVES`.
- Head event SHA-256: `9368d3921ec95ad4c1ba02ce79f4bdde89516a1449d69a8f81dfbc1fa3e53780`.
- Proposed next operation: `WEAVE` / `PRESENT_DESERVES` / `event_on=auto`.
- **Mandatory existing-workflow input:** `refs=1`. If the actual thread has moved to event #2 (or later), stale `refs=1` is rejected, not reinterpreted. For unrelated concurrent thread updates, the current global Git tip remains separately CAS-checked.

## Two supported guards

**1. Existing GitHub Actions form:** `loom-append.yml` already accepts user-supplied `refs`. For any non-`OPEN` event, the writer now checks that those refs explicitly include the latest committed event number on the exact named thread. The canonical Git SHA chain binds that numeric event number to recorded bytes. For the *next* event on `tessy-1`, set:

```text
operation: WEAVE
thread: tessy-1
witness: A
phase: PRESENT_DESERVES
event_on: auto
refs: 1
what:  [witness supplies]
how:   [witness supplies]
why:   [witness supplies]
content: [witness supplies]
```

A `WEAVE` without the current thread head in `refs` now fails closed. `OPEN` is still permitted with empty `refs`, but cannot reopen an existing thread.

**2. Strict direct CLI:** The writer additionally understands paired `--expect-thread-head` and `--expect-witness-head` arguments. Both must be present together. They accept a full 64-character lowercase SHA-256 (or `GENESIS` if the respective thread/lane has no earlier event). When supplied, the script rejects any mismatch with the actual thread and A/B/C lane heads. The existing GitHub form has **not** been changed to expose these two SHA fields because its update was blocked. Do not claim that form enforces the SHA pair directly; it enforces the causal `refs` fallback.

Independent lane and causal predecessor checks still run on the final record. A/B/C do not vote; a disagreement or silence never closes a different lane.

## Read-only planner

```sh
python3 bin/loom_next.py status
python3 bin/loom_next.py prepare --thread tessy-1 --witness A
python3 -m unittest discover -s tests -p 'test_gate15.py' -v
```

The planner's JSON includes `refs`, `expected_thread_head_sha`, and `expected_witness_head_sha`. It never writes witness WHAT/HOW/WHY, never copies private memory, and does not submit GitHub Actions runs. Treat a plan as stale whenever its observed thread head differs from the current public ledger. The actual append must be an authenticated human-witness operation through the existing workflow.

## Technical limits

- An ordinary GitHub branch history is still controlled by repository administration; independent Hallway receipts strengthen detectable historical preservation, not absolute immutability.
- The code tests are committed; successful GitHub Actions execution after these changes has **not** yet been verified.
- Causal-head checking protects the relevant thread. The global Git push additionally prevents overwriting concurrent commits.
- `cubit` remains the lowercase constant for every copy/distill transformation; `.dlw` remains a separate provenance watermark.
