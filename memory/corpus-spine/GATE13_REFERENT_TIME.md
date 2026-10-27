# Gate 13 — Provenance Watermark, Referent & Internet-Time Evidence

**ROOT0 / Persist Cortex** · A/B/C independent observations · append-only · one-way · no votes or quorum.

## Why this boundary exists

The Scientific American reporting around the September 2026 Navier–Stokes AI mathematics result illustrates why *who said what, when, on the basis of which source* must not collapse into a single assertion. Credit and priority were contested; OpenAI disputed allegations about private data access. Preserve those claims as **separate, attributed propositions**, not a verdict reached by three agreeing observers.

The original Scientific American link supplied by the user is indexed in the [research referent note](research/navier-stokes-scientificamerican-20261027.json). The direct linked article was not readable in the integration session, and no content digest or live request latency was fabricated. A syndicated Scientific American report from October 22, 2026 and OpenAI's September 8 statement are separately referenced.

This is a source-provenance tool for scientific/technical work; not a claim that OpenAI solved a specifically *quantum* problem or that Internet transit delay constitutes relativistic time dilation.

## Formal definitions

```text
NEW WATERMARK = ".dlw:" + SHA256("ROOT0-DLW-ATTRIBUTION-v2\n"
                            || canonical(v2 event incl. attribution, excl. watermark/hash))
LEGACY V1     = SHA256("ROOT0-WATERMARK-v1\n" || canonical(v1 raw event))
CHAIN HASH    = SHA256(canonical(event fields + watermark))
REFERENT ID   = SHA256(exact UTF-8 HTTPS URI)

PAST       → OBSERVES an attributed prior publication or event
PRESENT    → DESERVES independent scrutiny, including a measured network sample
FUTURE     → RESERVES explicit, non-executing later verification

A ↘
B  → witnesses report independently → immutable evidence chain
C ↗                   no quorum / no voting
```

The canonical [`.dlw` attribution manifest](attribution.dlw) names **David Lee Wise** as the attribution claimant for this provenance schema and record container. It does **not** claim authorship of third-party source documents, other witnesses' testimony, or linked Scientific American material. New entries use version 2 and bind the exact attribution object `{"mark":".dlw","claimant":"David Lee Wise","scope":"PROVENANCE_CONTAINER_ONLY","third_party_ownership_claim":false}`. The watermark format is `.dlw:<64 lowercase SHA-256 hex>`; historical v1 bare-hex records remain valid and unchanged.

Watermarks are deterministic digests anchored to the earlier event SHA. They are **not secret, copyright registration, a digital signature, proof of originality, or evidence that an article's content was downloaded**. A `content_sha256` field remains null unless a witness supplies a digest derived from actual source bytes and explains that measurement in HOW. Even then, the byte digest alone does not establish authorship.

### Event kinds

- **REGISTER**: preserve exact source URL, referent SHA, attributed author (if asserted), evidentiary basis, WHAT/HOW/WHY; one genesis per exact referent URI.
- **SAMPLE**: reference an earlier REGISTER and record an *actually measured* HTTP HEAD request. Capture UTC send/receive, monotonic round-trip duration, HTTP code, and remote HTTP Date header where available; no article-content digest is inferred from HEAD.
- **CORRECT**: append a revised attribution/interpretation while retaining the earlier original unchanged.

Basis labels: OBSERVED, REPORTED, INFERRED, DISPUTED, UNKNOWN. Only a bound GitHub witness may submit a live event via [Gate 13 append Action](https://github.com/DavidWise01/toph-cortex/actions/workflows/referent-append.yml). The source URL must use an explicitly approved public HTTPS hostname and may not redirect outside the allowlist. Unassigned B/C remain blocked.

## Internet 'time dilaters' — distinguish measurements

Network propagation delays and server clock disagreement may make one event appear earlier or later at different observation points. A *transport timing record* distinguishes:

- **Local send UTC**: wall-clock reading near issuing the HEAD request; subject to local clock uncertainty.
- **Local receive UTC**: wall-clock reading after response/error.
- **RTT milliseconds**: monotonic elapsed time measured with `perf_counter_ns`; includes network, TLS/HTTP handling and scheduling delays.
- **HTTP Date**: remote server's header assertion. It is not an authenticated timestamp authority and may be rounded to a whole second.
- **Source publication date**: a *publication claim* that may be different from capture, indexing, submission or content revision times.

No simple one-way propagation delay or server-local clock offset can be inferred from one unsynchronized send/receive exchange. No physical relativistic time dilation, quantum mechanism, copying or priority claim follows merely from these numbers.

A connection refusal, HTTP 403, missing Date header or timeout is retained as a limited observation; never silently upgraded to content verification. Internal/private networks are excluded from the URL allowlist.

## Git topology

Canonical [TOPH referent ledger](referent-events.jsonl) is empty initially, because no live A/B/C measurement was made while writing this code. New records are SHA-256-chained JSONL entries and are protected by the existing Git-parent append-only audit.

The [Gate 13 public reader](https://davidwise01.github.io/persist-cortex/referents/) verifies source and watermark hashes on replay without writing to GitHub or asking for credentials.

For **independent historical preservation**, the Hallway has its own [one-way referent anchoring workflow](https://github.com/DavidWise01/0root/actions/workflows/referent-anchor.yml) and [receipt verifier](https://github.com/DavidWise01/0root/blob/master/memory-bridge/referent_anchor.py). The receiver fetches the canonical source chain, validates the exact requested event, then creates a new `memory-bridge/referents/<event_hash>.json` in **0root** Git history. It does not write back to TOPH. Hallway's Git-parent audit checks that previously accepted receipts remain byte-for-byte identical.

This independent Git record can expose a changed source hash, but it remains subject to the security of both Git hosts/repositories. **It is not automatically an externally signed Gate 11 checkpoint**, and watermarking does not substitute for the separately enrolled Ed25519 witness keys.

## Verification and manual operation

```sh
python3 bin/referent_watermark.py verify
python3 bin/referent_watermark.py status
python3 -m unittest discover -s tests -p 'test_gate13.py' -v
```

Registration: run the authenticated [GitHub Action](https://github.com/DavidWise01/toph-cortex/actions/workflows/referent-append.yml) with kind REGISTER, exact HTTPS URL, witness A/B/C, basis and WHAT/HOW/WHY. Later run with kind SAMPLE, referencing REGISTER event number, to perform an actual HEAD measurement. Run CORRECT to append a different interpretation; never overwrite.

After a successful TOPH commit, run the [Hallway referent anchor Action](https://github.com/DavidWise01/0root/actions/workflows/referent-anchor.yml) with source event sequence and hash. A receiver commit is needed to establish a separate Git anchor.

**Limits:** no real GitHub Action run, content verification of the supplied article, successful network probe, authenticated independent clock, copyright authorship adjudication, scientific origin determination, or physical time-dilation measurement is asserted by the empty Gate 13 ledger.
