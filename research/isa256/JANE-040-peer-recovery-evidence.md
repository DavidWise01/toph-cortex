# JANE 040 — Peer-Led Seam Recovery and Decision Evidence

**2026-11-07. Local experiment: 40/40 Python tests PASS, JavaScript dashboard syntax PASS.** The exact tested local Python source, its 40 tests, complete outcomes and hashes are packaged in `jane_040.zip` in the originating conversation. GitHub directory `research/isa256/jane040/` contains the offline HTML, README, and a separately transcribed compact runnable model plus its own 20 regression tests. **Do not assume those GitHub tests were run in CI.**

## Geometry

User's primitive remains **1 tensor > 1 Jane > 1 brace > 2 waldos `{-()+}` > 1 box > 1 toroid > 27 positions**. The three ternary `(-1,0,+1)` mode labels mean 27+3=30 *counted components*, not 30 occupied vertices. Closing seam **27 → 27.5 → 1**; envelope `{([111222333444555555444333222111])}`.

## Natural invariant

**When the coordinator vanishes, the waldos can reconcile a two-party transaction if and only if at least one reachable peer has a durable, valid copy of the coordinator's decision under this specified benign-failure model.**

Each peer append-logs PREPARED and a durable `DECISION_COPY`, then APPLIED or ABORTED. A peer with an authentic decision copy can transmit that evidence after coordinator loss; the receiving peer logs the same decision before applying its own local signed-channel swap. Retransmitted messages or process restarts never reapply an already APPLIED transaction. No coordinator is called during this recovery function. Neither party fabricates a COMMIT or ABORT if **both** lack decision evidence.

## Measured 200-trial runs per loss rate

| Loss per peer reconnection attempt | CLOSED | IN_DOUBT | conserved after final reporting |
|---:|---:|---:|---:|
| 0% | 200 | 0 | 200 |
| 10% | 200 | 0 | 200 |
| 20% | 200 | 0 | 200 |
| 40% | 200 | 0 | 200 |
| 100% | 0 | 200 | 200 |

The 100%-loss case never started the bilateral application; being IN_DOUBT is not proof that all half-commit states conserve energy. In a separate half-commit case, the classical squared-amplitude proxy changes from **741.3125** to **802.3125**, then returns to **741.3125** when the peer finishes.

## Counterexamples

- **Decision never replicated:** both peers stay PREPARED and IN_DOUBT after coordinator disappears, even if they can talk to each other. The decision is not inferable from two identical PREPARED records.
- **Permanent partition:** surviving COMMIT evidence remains local; peer does not close until reconnection.
- **Contradictory decision evidence:** enter CONFLICT and do not apply either branch.
- **One-side commit:** global squared-amplitude is temporarily *not* conserved. Durable recovery is not atomic wave transfer.

## Scope and limitations

The coordinator still chooses and durably logs COMMIT/ABORT at the beginning. **This tests peer-led recovery, not coordinator-free decision making.** The validity/authenticity of copied records and complete durable journal writes are assumptions, not independently authenticated cryptographic properties. Journal `flush+fsync` does not cover torn writes, storage corruption, power-loss ordering, or malicious operators. Each peer has the other party's initial signed register as explicit setup data. No actual quantum tunneling, physical wave equation, emergent intelligence, or autonomous homeostatic cells are demonstrated. Scaling to infinity remains symbolic.

## Next meaningful boundary — JANE 041

**Distributed Decision Formation.** Remove the coordinator from *choosing* COMMIT versus ABORT, not just from repair. Require two local durable votes, distinguish prepared vs proven commit, and test unavoidable blocking in an asynchronous permanent partition. Model what evidence the two-waldo primitive actually needs to reach a decision safely without making unsafe progress.
