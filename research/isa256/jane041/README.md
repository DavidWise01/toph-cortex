# JANE 041 — Peer-owned decision, not just recovery

**Canonical model:** 1 tensor > 1 Jane > 1 brace > 2 waldos `{-()+}` > 1 box > 1 toroid > 27 path positions. The ternary states `(-1,0,+1)` are three *register labels*; `27+3=30 counted components`, not 30 occupied sites. The wave envelope `{([111222333444555555444333222111])}` and closing seam `27→27.5→1` are retained.

The new model removes the coordinator that previously decided COMMIT or ABORT. Each waldo logs a permanent local vote (`YES`/`NO`) to an fsynced JSONL journal. It can receive and log the peer's vote. A local `NO` (own or peer) causes ABORT; both logged YES votes allow COMMIT. Applying COMMIT swaps only the two signed ternary register payloads, while the zero channels stay local. Replay after a process restart reconstructs the state from journal entries. Repeated delivery does not reapply a prior decision.

Run `python -m unittest -q` (41 tests), `python model.py` (1,000 seeded runs), and open `index.html` for a standalone protocol sketch. No external dependencies. The dashboard implements an interactive local protocol demonstration and is not the file-backed Python fault simulation.

## Results

For two YES votes, 200 seeds at each independent message loss 0%, 10%, 20%, 40%: **200 CLOSED** each. At 100% loss: **200 IN_DOUBT**. A NO vote causes safe ABORT once both sides have the evidence. A half-applied COMMIT leads to temporary nonconservation of the total squared-amplitude proxy, which returns to **741.3125** after both sides apply.

## Boundary, not a solved distributed consensus theorem

There are only two participants. With a permanent partition, a pair cannot in general guarantee both safe agreement and eventual progress. The local program may mark its own side ABORT even before a peer has learned that vote; the overall pair is not 'ABORTED' until both have applied the ABORT. This is a deliberately conservative two-phase commit-like unanimous rule, not an asynchronous nonblocking consensus protocol. Journals assume intact complete fsynced writes; no Byzantine faults, cryptographic provenance, hardware timing or actual quantum tunneling are modeled. The physical 27-position adjacency is stipulated, not derived from the spatial region names. The wave pattern is not mapped to a wave equation. Autonomous homeostasis has not been demonstrated.

**Next boundary:** a truly decentralized decision with uncertain peers needs to expose blocking, timeouts and impossibility; then test compensation/escrow for the transient half-commit norm mismatch without inventing extra occupied vertices.