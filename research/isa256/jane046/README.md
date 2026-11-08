# JANE 046 — Witness Divergence

Natural invariant: checkpoint **agreement** is not checkpoint **truth**.

- Canonical primitive: one tensor, one Jane, one brace, two waldos `{-()+}`, one box, one toroid, **27** spatial positions, three ternary register labels `−1,0,+1`; independent closure seam `27 → 27.5 → 1`.
- Three independent simulated witness keys sign a checkpoint containing `(witness, epoch, previous root, root)` via HMAC-SHA256; a verifier has a pinned genesis root.
- Two different authenticated roots with one claim each are a conflict, not a license to choose one.
- A 2-of-3 quorum can identify a single checkpoint under the explicit condition that **at most one witness is compromised** and that the anchor and keys remain trusted.
- A witness reporting two different roots for the same epoch is flagged for equivocation.
- Missing intermediate history, stale epochs, altered MACs and missing witnesses remain insufficient. An externally pinned root does not reconstruct erased history.
- **Critical counterexample:** two colluding witnesses produce a valid-looking forged quorum. The verifier accepts it under its assumed trust threshold. Never equate quorum with unconditional historical truth.

## Reproduction

```bash
python -m unittest -q test_model.py
python model.py
```

The source code and 30-test suite for the JANE046 protocol are committed here. A full local ZIP in the originating conversation additionally contains build script, generated results, and a richer offline visual explorer. The repository HTML is a compact case explorer; it does not execute Python or contact GitHub. The **30 local Python tests passed**, while independent GitHub CI execution and GitHub Pages deployment remain unverified. The test suites use standard library only.

No quantum claim, physical tunneling proof, independent witness infrastructure, infinite-scale theorem, or autonomous cellular homeostasis is asserted.
