# Gate 12 — One-way key lifecycle, rotation, revocation and historical memory

**ROOT0 / TOPH CORTEX ↔ 0root.ai Hallway** · append only · diodic · temporal · independent A/B/C witnesses · **NO VOTE / NO QUORUM**.

## Provenance and authority

The canonical [TOPH key lifecycle](key-lifecycle.jsonl) is a new SHA-256 linked, append-only journal. It never edits [the enrolled public-key registry](witness-public-keys.json) or any original Gate 10/11 witness signature. A key may move forward only:

```text
UNUSED/ENROLLED → ACTIVATE(key1) → ROTATE(key1,key2) → ROTATE(key2,key3) → …
                              \→ REVOKE(keyN) [account-authorized recovery]
```

ROTATE requires **two detached Ed25519 signatures** over the exact same `ROOT0-KEY-LIFECYCLE-v1` envelope: one signed by the previously active key with `role=OLD`, and one by the incoming key with `role=NEW`. The signed message binds action, witness, key fingerprints, GitHub actor ID, reason, UTC date, journal sequence and previous journal SHA. It therefore cannot simply be replayed in a different time, lane or thread.

ACTIVATE requires a matching `NEW` proof of possession of a public key already enrolled under a real GitHub account. Only **one active key per lane** is permitted by the source lifecycle replay. A distinct replacement key is enrolled separately through the reviewed public registry before rotation. Old keys and signatures remain in history; a rotated key cannot become active again.

REVOKE is an irreversible **account-authorized recovery**, not a fabricated signature from a missing private key. It must start with `ACCOUNT_RECOVERY_NOT_KEY_SIGNED: ` followed by the reason. Such a record means the GitHub account authorized the disablement; it does not prove that the lost private key was available, or when compromise first occurred. Historical records remain cryptographically replayable, but signatures from a potentially compromised key must be interpreted with the incident context.

Changes require the exact previous SHA tip, a bound actor in GitHub Actions, and a non-force Git commit. The existing Gate 10 and 11 writers now consult this ledger **before** new attestations and checkpoints, while preserving the historical verification of prior signed events.

## Independent 0root.ai receiver policy

The Hallway retains separately committed [public verification key pins](https://github.com/DavidWise01/0root/blob/master/memory-bridge/trust/checkpoint-key-pins.json). It has a different [append-only BLOCK journal](https://github.com/DavidWise01/0root/blob/master/memory-bridge/trust/key-decisions.jsonl). A manually invoked, owner-authenticated [key-block Action](https://github.com/DavidWise01/0root/actions/workflows/key-block.yml) records permanent refusal of **NEW checkpoint receipts** from that key. Existing Hallway checkpoint anchor files and original public pins remain intact for old-signature verification.

TOPH's REVOKE is **not automatically trusted as the Hallway's own BLOCK event**. To protect both boundaries after an incident, separately invoke the Hallway key-block workflow. Neither workflow may silently write into the other repository. That preserves independent trust rather than asking B/C to approve or voting by a quorum.

## Manual activation (requires a genuine witness-controlled key)

First generate the private Ed25519 key **offline** using the Gate 10 key tool and enroll **only its public entry** into `witness-public-keys.json` under a reviewed Git commit. The key registry starts empty as of this gate; no real signer has been fabricated. A is GitHub-bound, while B/C are unassigned and must be enrolled under independent GitHub accounts before they can sign.

From an up-to-date local TOPH checkout with `cryptography==46.0.4`:

```sh
python bin/key_lifecycle.py status
python bin/key_lifecycle.py prepare \
  --witness A --kind ACTIVATE --key-id YOUR_NEW_KEY_ID \
  --reason "Initial independently controlled key" \
  --recorded-at 2026-10-27

# Sign only the NEW role payload_b64 returned by PREPARE, locally:
python bin/witness_keytool.py sign \
  --private-file ~/.root0-witness-a-ed25519.pem \
  --payload-b64 EXACT_PREPARE_NEW_ROLE_BASE64
```

Submit the resulting detached signature and exact ledger tip through [Gate 12 authenticated lifecycle Action](https://github.com/DavidWise01/toph-cortex/actions/workflows/key-lifecycle-append.yml). Do not upload or paste the private key.

For ROTATE, first register the incoming public key and run `prepare --kind ROTATE --key-id NEW_ID --previous-key-id ACTIVE_OLD_ID --reason ... --recorded-at ...`. The tool produces **OLD** and **NEW** signable payloads. Sign each on its independently held key and submit both signature strings through the same workflow.

For emergency REVOKE, submit `--kind REVOKE --key-id CURRENT_ACTIVE_ID --reason "ACCOUNT_RECOVERY_NOT_KEY_SIGNED: lost or compromised" --recorded-at ...`; the workflow still requires the correct GitHub actor and unchanged ledger tip. This is explicitly **not** a private-key signature and must not be presented as one.

For the receiver's irreversible BLOCK, use [Hallway key-block Action](https://github.com/DavidWise01/0root/actions/workflows/key-block.yml) with the independently pinned key ID, a reason and the last independent key-decision SHA tip. BLOCK has no reverse operation.

## Verification

TOPH:

```sh
python bin/key_lifecycle.py verify
python bin/key_lifecycle.py status
python3 -m unittest discover -s tests -p 'test_gate12.py' -v
```

Hallway:

```sh
python3 memory-bridge/key_decisions.py verify
python3 memory-bridge/checkpoint_receiver.py verify-local
python3 -m unittest discover -s memory-bridge -p 'test_key_decisions.py' -v
```

Web reader: [Gate 12 / Key Lifecycle Diode](https://davidwise01.github.io/persist-cortex/key-lifecycle/).

## Architectural safety limits

- **No retroactive erasure:** earlier cryptographic signatures remain verifiable against preserved public keys.
- **No backwards authority:** a rotated or revoked key cannot submit a NEW source attestation/checkpoint; the independent BLOCK rejects NEW Hallway acceptance.
- **No consensus:** A, B and C may have independent states and conflicting evidence, without votes or quorum.
- **No false timestamps:** the date is signed for ACTIVATE and ROTATE; account-only REVOKE reports the UTC record date but does not magically prove when compromise began.
- **No secret publication:** no private key or personal memory belongs on GitHub Pages, workflow inputs or public source.
- **No automatic compromise detection:** key compromise must be observed and reported; the system cannot determine it from a signature alone.
- **No guarantee against repository administrators or force pushes:** Git-prefix audits and independent anchoring are protective evidence, not immutable external notarization.
- **No fake evidence:** source/public key and block journals remain empty until real authorized enrollment and append.
- **Operating status:** files and workflows can be committed without any confirmed successful GitHub Actions execution; the real enrollment/rotation/revocation path is not yet operationally demonstrated.

The canonical goal is a **forward-only historical record of each independent witness's key custody**, not a mechanism to create agreement or to erase their earlier testimony.
