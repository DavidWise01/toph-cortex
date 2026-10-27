# ROOT0 / Temporal Diode v1

**PAST OBSERVES → PRESENT DESERVES → FUTURE RESERVES**

This is the append-only, one-way temporal boundary above the [verified Corpus Spine v2](events-v2.jsonl).

- **A, B, C are independent witness lanes**, not roles with votes or majority authority.
- Each `(thread, witness)` lane begins at PAST. It can append more past observations, advance to PRESENT, then advance to FUTURE. It cannot skip or move backward. Another witness can begin in PAST even after A has reserved the future.
- **PAST / observes:** the referenced event date is not later than the record date.
- **PRESENT / deserves:** the referenced date equals the record date. “Deserves” records that witness's present assessment, not system authorization or moral truth.
- **FUTURE / reserves:** the referenced date must be later than the record date. This is an intentional reservation statement, **never an automation or promise of execution**.
- Three witnesses may all disagree, be silent, or appear at different phases. No quorum, consensus, vote, promotion or agreement is computed.
- A later correction or changed observation is **another appended event**, either at the current phase (where allowed) or on a distinct new thread; no retroactive mutation.
- WHAT, HOW and WHY are recorded separately for every witness.
- Each event has global `prev` SHA-256, a per-witness `anchor` to the prior event in its lane, a verified Corpus Spine v2 tip, and a public Git source blob SHA.
- Appends require compare-and-swap against BOTH the global temporal tip and the current validated corpus tip.

The [temporal-events.jsonl](temporal-events.jsonl) file starts **empty**, because we do not invent witness testimony. Empty means no claims have been made, not that any witness agrees with another.

## Trust boundary

The initial [legacy corpus ledger](events.jsonl) contained five incorrect event digests and is preserved as a historical artifact. The [validated successor](events-v2.jsonl) anchors the legacy Git blob without granting its events verified status. The Temporal Diode refuses to attach to an unverified corpus tip.

## Read, replay, then append

```sh
python3 bin/corpus_spine.py verify
python3 bin/temporal_diode.py verify
python3 bin/temporal_diode.py status
python3 -m unittest discover -s tests -p 'test_temporal_diode.py' -v
```

The [manual authenticated append workflow](https://github.com/DavidWise01/toph-cortex/actions/workflows/temporal-diode-append.yml) accepts a single witness and event. It requires public Git blob verification and attempts a non-force Git push. GitHub Pages remains strictly read-only.

## Topology

```
              ROOT0 CORPUS SPINE v2 (valid SHA chain)
                                |
                     TEMPORAL GLOBAL SHA
                                |
                    ┌───────────┼───────────┐
                    A           B           C
                    |           |           |
         past → present → future [each lane independently]
                    |           |           |
              No votes, no quorums, no retroactive writes

          0root.ai ↔ GitHub Pages Gate 08 (read only)
                     TOPH CORTEX Git (writer)
```

This system does not establish who controls a witness label. That requires separately authenticated witness signatures/identities; a label alone is not an attestation of physical independence. Public-source metadata only; never post secrets or private records.
