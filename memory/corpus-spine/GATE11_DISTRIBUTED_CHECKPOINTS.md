# Gate 11 — Independently Signed Cross-Repository Checkpoints

**Diodic:** append only, one way, no backwards writes.  
**Temporal:** past OBSERVES, present DESERVES, future RESERVES.  
**Witnesses:** A, B, C independently sign their own state; **NO VOTE / NO QUORUM**.

## Sources and trust

- Canonical writer: [TOPH CORTEX signed checkpoints](checkpoints.jsonl), driven by [bin/distributed_checkpoint.py](../../bin/distributed_checkpoint.py)
- Independent verifier and destination: [0root.ai Hallway checkpoint receiver](https://github.com/DavidWise01/0root/blob/master/memory-bridge/checkpoint_receiver.py)
- Hallway trust anchor: [independent key pins](https://github.com/DavidWise01/0root/blob/master/memory-bridge/trust/checkpoint-key-pins.json)
- Read-only status: [Persist Cortex Gate 11](https://davidwise01.github.io/persist-cortex/checkpoints/)
- Existing witness registry and keys: [GitHub account bindings](witness-registry.json) + [public signing keys](witness-public-keys.json)

The signing subject is a checkpoint over four **verified Git-backed ledgers**:

1. `CORPUS` — `events-v2.jsonl` (the legacy v1 SHA mismatch remains preserved, not trusted).
2. `TEMPORAL` — A/B/C one-way PAST → PRESENT → FUTURE reports.
3. `DELIVERY` — separately recorded OFFER versus verified RECEIPT.
4. `ATTESTATION` — Gate 10 detached Ed25519 witness attestations.

Each source contributes `{count, tip}`, with `tip=GENESIS` if empty. Historical counts and hashes remain checkable; a witness's subsequent checkpoint must never decrease any source count.

A witness signs the exact `ROOT0-CHECKPOINT-v1` domain-separated canonical JSON payload including witness, enrolled public key fingerprint, UTC date, checkpoint sequence, **previous checkpoint hash**, and four source states. Both the SHA of those bytes and the Ed25519 detached signature are stored in a new append-only journal entry. No old source data is edited.

## Boundary 1 — real key enrollment (requires user-controlled action)

A is currently bound to the DavidWise01 GitHub account, but **no signing public keys have been registered**. B and C are unassigned. Create a key offline using [Gate 10's instructions](GATE10_SIGNED_WITNESS.md); never commit, upload, or paste the private PEM. Enroll only the public key in TOPH `witness-public-keys.json` via a reviewed Git commit.

**Separately**, copy the reviewed public key entry into the Hallway's `checkpoint-key-pins.json`, using precisely these fields:

```json
{
  "witness": "A",
  "github_actor_id": "148925959",
  "key_id": "64-lowercase-hex-public-key-sha256",
  "public_key_b64": "base64-of-the-raw-32-byte-Ed25519-public-key"
}
```

This independent trust pin must be committed in the **0root** repository, not inferred from TOPH's mutable key registry. There is no quorum or consensus approval requirement; this is an explicit individual trust configuration, not a majority ballot.

## Boundary 2 — offline signature + append in TOPH

Run these commands locally in an up-to-date trusted TOPH checkout:

```sh
python bin/corpus_spine.py verify
python bin/temporal_diode.py verify
python bin/delivery_receipt.py verify
python bin/witness_attestation.py verify
python bin/distributed_checkpoint.py verify

python bin/distributed_checkpoint.py prepare \
  --witness A --key-id YOUR_ENROLLED_KEY_ID \
  --recorded-at 2026-10-27

# Sign the PREPARE signable_b64 on the witness's own device.
python bin/witness_keytool.py sign \
  --private-file ~/.root0-witness-a-ed25519.pem \
  --payload-b64 EXACT_SIGNABLE_BASE64
```

In [the authenticated checkpoint append workflow](https://github.com/DavidWise01/toph-cortex/actions/workflows/checkpoint-append.yml), supply the witness, key ID, exact PREPARE date, detached signature, `expected_tip`, and `state_sha256`. The workflow verifies source chains, checks the GitHub account binding, verifies the Ed25519 signature, and attempts a non-force append-only Git push.

**A successful workflow run is not yet demonstrated.** The canonical checkpoint ledger starts empty, deliberately; no signature is invented.

## Boundary 3 — independent one-way relay to the Hallway

Invoke [0root's manual anchor workflow](https://github.com/DavidWise01/0root/actions/workflows/checkpoint-anchor.yml) with the exact TOPH checkpoint `seq` and event `hash`. The Hallway does **not** accept the sender's assertion that its own signature is valid: it independently verifies using **0root's separately committed key pin**. It also verifies the source-prefix hash chains and rejects any rolled-back count per witness.

A passing receiver creates a new file:

```text
DavidWise01/0root/
  memory-bridge/checkpoints/<signed-checkpoint-hash>.json
```

This receipt contains the exact signed source checkpoint and receiving date. It is created once, with exclusive file creation, then committed and pushed **without force** to the Hallway repository. Prior files cannot be rewritten by the receiving code. The separately configured Hallway audit checks previous Git snapshots for deleted or modified anchor files and key-pin removals.

The receiver takes **no action** based on any FUTURE_RESERVES record. It never edits the sender's source records or writes a reply into TOPH. This is one-way publication/verification, not distributed command execution or agent consensus.

## Audit and limitations

- **Independent history:** an anchored checkpoint can expose later TOPH source rewriting or rollback so long as the Hallway history and trust pins remain intact.
- **No quorum:** a single cryptographically valid registered witness can produce a checkpoint. B and C may observe the same state differently or remain silent.
- **Identity:** a public-key signature proves possession of the signing key, not a human identity or source truth. TOPH additionally checks a GitHub Actions actor bound to the witness lane.
- **No private records:** only public source metadata and hashes. Neither repository receives private browser memory or signing secret material.
- **Not immutable against all adversaries:** repository owners and administrators may bypass an ordinary Git workflow by force-writing or deleting history; stronger guarantees require branch protections, signed commits, independent archives and safe custody of private signing keys.
- **Verification scope:** Hallway independently verifies checkpoint and source-prefix SHA chains plus the Ed25519 signature. It does not reproduce every upstream semantic inference.
- **No unattended delivery:** workflow dispatches and key enrollment are explicit user actions. GitHub Pages only reads.
- **Migration:** invalid legacy `events.jsonl` is retained, while every new checkpoint uses the verified `events-v2.jsonl`.

Local verification after deployment:

```sh
python bin/distributed_checkpoint.py status
python bin/distributed_checkpoint.py verify
python -m unittest discover -s tests -p 'test_gate11.py' -v
```

Hallway check:

```sh
python memory-bridge/checkpoint_receiver.py verify-local
python -m unittest discover -s memory-bridge -p 'test_checkpoint_receiver.py' -v
```

No live signing keys, signed checkpoints, or independently anchored receipts have been produced without real witness enrollment.
