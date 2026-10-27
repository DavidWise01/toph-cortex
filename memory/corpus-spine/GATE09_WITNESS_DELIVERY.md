# Gate 09 — Witness Identity & Delivery Receipts

**Canonical:** TOPH CORTEX, append-only Git source.  
**Read-only dashboard:** https://davidwise01.github.io/persist-cortex/identity-bridge/  
**Public Hallway receiver:** https://github.com/DavidWise01/0root/tree/master/memory-bridge  
**Mode:** one-way, append-only, WHAT/HOW/WHY, A/B/C independent, zero votes or quorums.

## 1. Authenticated witness bounds

The registry [witness-registry.json](witness-registry.json) binds GitHub account IDs to exactly one witness lane each. As of 2026-10-27:

| Lane | Account | State |
| --- | --- | --- |
| A | DavidWise01 (GitHub ID 148925959) | BOUND |
| B | — | UNASSIGNED, no writes allowed |
| C | — | UNASSIGNED, no writes allowed |

The GitHub Actions `GITHUB_ACTOR_ID`, `GITHUB_ACTOR`, workflow identity and main-branch dispatch context must match the registered lane **before** a temporal or delivery append is accepted. A witness label does not itself authenticate a person; workflow context provides platform-account authorization, not an end-user cryptographic signature.

To enroll B or C, register a **distinct authenticated GitHub account** through an intentional reviewed registry commit. There is no automatic promotion or majority enrollment. Registering three labels under one account is explicitly forbidden.

## 2. One-way cross-repository delivery

1. Witness A/B/C independently appends a public-source temporal record in [Gate 08](https://davidwise01.github.io/persist-cortex/temporal/). A lane moves only PAST_OBSERVES → PRESENT_DESERVES → FUTURE_RESERVES, one phase at a time.
2. Its registered witness runs [TOPH's delivery append workflow](https://github.com/DavidWise01/toph-cortex/actions/workflows/delivery-receipt-append.yml) with `OFFER`, the temporal sequence and a public `DavidWise01/recipient` destination. This appends an **OFFER** event to [delivery-events.jsonl](delivery-events.jsonl). **OFFER does not mean received.**
3. If the destination is `DavidWise01/0root`, an authorized account can invoke [the Hallway receiver workflow](https://github.com/DavidWise01/0root/actions/workflows/temporal-receiver-ack.yml) with the exact OFFER sequence/hash. It checks the Git public offering and temporal event and creates a new, never-overwritten `memory-bridge/receipts/<offer_hash>.json`.
4. The original registered witness runs TOPH's delivery append workflow with `RECEIPT`, the OFFER sequence, the destination ACK file path and **verified Git blob SHA**. The writer fetches and verifies the remote public ACK's exact offer hash, temporal hash and destination. Only then is a RECEIPT event appended.
5. The [Gate 09 dashboard](https://davidwise01.github.io/persist-cortex/identity-bridge/) independently verifies the local hash chains, separately lists offered and acknowledged records, and never treats a pending offer as delivered.

The TOPH writer can only write TOPH. The Hallway receiver can only write its own repository. Cross-repository reception requires an intentionally invoked, destination-authorized workflow; neither page contains a GitHub token.

The same protocol can be installed in another public DavidWise01 repository through its own authenticated receiver writer. No receiver is silently installed account-wide.

## 3. Protocol invariants

- **APPEND-ONLY:** new JSONL event per recorded change; Git push without force, no rewrite of established witness or receipt events.
- **DIODE:** the destination receipt file is created only once, and recorded acknowledgment never triggers execution in the sending corpus.
- **TEMPORAL:** past observes, present deserves, future reserves; all three are witness statements, not objective truth or a timer/automation.
- **THREE WITNESSES:** three independent *lanes*, not three automatically authenticated people. A may progress while B and C remain silent.
- **NO QUORUM:** zero votes, majority, agreement filters, consensus, and inferred authorization from other witnesses.
- **PROVENANCE:** every OFFER references a verified temporal source. Every RECEIPT references exactly one earlier OFFER and includes the destination's public Git blob SHA and SHA-256 content digest.
- **PRIVACY:** only public source metadata. Never publish private snapshots, repo names, keys, health data or other personal records.

## 4. Verification

```sh
python3 bin/corpus_spine.py verify
python3 bin/temporal_diode.py verify
python3 bin/delivery_receipt.py verify
python3 -m unittest discover -s tests -p 'test_gate09.py' -v
```

**Important limits:** Workflow dispatch, correct branch permissions and a successful GitHub Actions run are required for real persistence; source commits alone do not demonstrate deployment. A GitHub user ID is not a separate cryptographic witness signature. An ACK establishes that the referenced file was present and checked at append time; it is not independent scientific evidence or an off-chain pledge. Long-term high-assurance provenance would require signed witness statements and independent history witnesses. The historical invalid corpus-spine v1 remains preserved; all new references use verified v2.

No fabricated witness, OFFER, or ACK has been entered into the canonical ledgers.
