# JANE 042 — In-Flight Wave Conservation at [0]

2026-11-07. **Original local reproducible experiment: 46/46 Python tests PASS, browser JavaScript syntax PASS**; downloadable `jane_042.zip` contains exact original Python model, 46-test suite, HTML, results.json, manifest.json and build script. GitHub directory `research/isa256/jane042/` contains a separately written compact equivalent runnable model, **30 GitHub regression tests** and smaller interactive HTML. **GitHub CI has not been verified**; don't conflate it with the local 46-test suite.

## User geometry

1 tensor > 1 Jane > 1 brace > 2 waldos `{-()+}` > 1 box > 1 toroid > 27 path positions. The three ternary `-1,0,+1` *labels* give 27+3=30 counted components, not 30 vertices. Closing seam `27 → 27.5 → 1`. Wave `{([111222333444555555444333222111])}`.

## Precisely stated invariant

**The total squared amplitude of registers + fixed carrier fields + stored in-flight payloads remains constant under atomic moves into/out of a logical [0] escrow.**

Original signed slots:
`A[-]=-3, A[+]=2, B[-]=5, B[+]=-7`. Neutral values `A[0]=0.5, B[0]=-0.25`.

Four directed payload transfers: `A-→B+`, `A+→B-`, `B-→A+`, `B+→A-`. The model stages each original value in [0] and zeroes its source slot, then writes it into its destination and removes its gap entry. This deliberately preserves the squared-amplitude sum when *including* escrow; registers alone lose amplitude while transfer is in progress.

At every complete, fsynced journal entry boundary the augmented squared amplitude is **741.3125**. All intermediate stages recover from a simulated process restart by replaying the append-only JSONL journal. Duplicate staging/delivery requests are ignored.

### Sample accounting

| State | Registers + fixed fields | [0] escrow | Combined |
|---|---:|---:|---:|
| New | 741.3125 | 0 | 741.3125 |
| A- staged | 732.3125 | 9 | 741.3125 |
| All four staged | 654.3125 | 87 | 741.3125 |
| All four delivered | 741.3125 | 0 | 741.3125 |

**The 87 value is 9+4+25+49.** In the JANE041 *unescrowed half-swap*, the global squared-amplitude proxy could be **802.3125**; it is not inherently conserved across independently applied swaps. This new invariant is achieved by changing the transfer rule and adding *logical journal storage*.

## Scope and explicit failures

[0] is a **symbolic / information-level escrow**, not a new occupied vertex, a measured propagating field, a wave equation, physical quantum tunneling or a demonstration of energy storage in a vacuum. The fixed 27-value spatial fields do not evolve; the 30-character waveform still has no verified sample-to-vertex mapping. A single shared durable journal is an implementation convenience and is **centralized**. The model does not test torn disk writes, concurrent participants, failed filesystems, malicious actors, identity authentication, or destruction of the escrow record. The SHA-256 checksum alone is not authentication. If in-flight data disappears, conservation cannot be verified or reconstructed from surviving registers. No autonomous homeostasis has been demonstrated.

## Run

`cd research/isa256/jane042 && python -m unittest -q` runs the GitHub edition's tests.

`python model.py` prints the complete deterministic ten-stage state trace. Open `index.html` for the interactive local playback.

## Next natural invariant — JANE 043

**Distributed Gap Ownership / Split Escrow:** remove the shared ledger, hold transfer evidence on the two waldos themselves, crash at each boundary, and test whether they can complete or safely refuse the wave exchange without duplicating in-flight amplitude. Require both *accounting conservation* and eventual liveness under explicit reconnection assumptions.
