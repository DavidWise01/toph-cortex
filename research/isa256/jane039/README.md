# JANE 039 — Durable Seam Recovery

A **two-waldo classical state transaction** at the symbolic `27 → 27.5 → 1` seam. Canonical primitive: one tensor, one Jane, one brace, two waldos `{-()+}`, one box, one toroid, 27 occupied positions. `−1,0,+1` are three register labels; 27+3=30 *counted components* rather than 30 occupied vertices. Preserved palindrome: `{([111222333444555555444333222111])}`.

## Run

```sh
python -m unittest -q
python model.py > results.json
```

The model uses **per-node append-only JSON Lines files**, flushing and fsyncing every appended record. Participants persist `PREPARED`, `COMMITTED` or `ABORTED` records, while the coordinator persists the immutable `COMMIT` or `ABORT` decision. Restart reconstructs the phases and wave payloads from journal history. Duplicate COMMIT is idempotent because the final ternary register is calculated from immutable original payloads rather than toggled repeatedly. No extra spatial vertex is allocated.

## Findings

- 40/40 tests PASS.
- 200/200 CLOSED at 0%, 10%, 20%, and 40% simulated message loss under bounded retries and reconnection.
- 200/200 remained IN_DOUBT with 100% message loss: the recorded ABORT cannot reach both waldos.
- 200/200 partial-commit cases at each nontrivial run temporarily depart from the initial global squared-amplitude total.
- At full closure, squared amplitude is **741.3125**; with only the left waldo committed it is **802.3125**.
- A network partition after one party commits blocks atomic closure; no false completion is reported.

**Caveats:** Tests restart by constructing fresh Python objects over the same intact journal files. They do not simulate torn writes, corrupted storage, fsync lying, lost media, simultaneous independent process crashes, malice, hardware wave propagation or quantum tunneling. A centralized coordinator remains; 2PC may block permanently. Norm is a classical *proxy*, not a measured physical energy. The dashboard is an interactive demonstration of these rules, not the actual filesystem-backed model.

**Next boundary:** JANE 040 — journaled exchange with no single permanently available coordinator; test peer reconciliation and demonstrate the blocking/consensus boundary explicitly, without claiming indefinite-partition liveness.