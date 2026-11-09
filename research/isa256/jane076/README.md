# JANE 076 — Git-to-Git Recursive Handoff

This repository bundle provides a deterministic **offline protocol simulation**, not a deployed GitHub agent. Execute `python -S -m unittest -q` and `python -S model.py` from this directory. Open `index.html` for an interactive explanation; it does not connect to a GitHub backend.

## Actual source protocol

TOPH's Gate 09 delivery specifies an authenticated, intentional, one-way `OFFER → destination ACK → origin RECEIPT` cross-repository handoff. It explicitly distinguishes OFFER from RECEIPT, permits zero votes/quorums, separates destination authorization, and refuses automatic execution on ACK. See [Gate 09](https://github.com/DavidWise01/toph-cortex/blob/main/memory/corpus-spine/GATE09_WITNESS_DELIVERY.md). The [0root Hallway `llms.txt`](https://github.com/DavidWise01/0root/blob/master/llms.txt) provides routing through five worlds, `LIT/AMBER/WALL` evidence and the authorized build/seal/publish/place/verify process.

## Proposed logical loop

`TOPH Git OFFER → 0root Git ACK → Hallway → bounded hive → Jane {{j}} CHOICE → TOPH Git DECISION → next OFFER`.

One Jane, immutable root payload `{{i}}`, logical hive `{{6x6x6[4x4(3x3[2x2(1)])]}}` (124,416 logical addresses), no hive decision authority. Offer and receipt events form separate append-only journals; event hashes are for integrity only. Every cycle references the previous verified offer; destination ACK does not execute the proposal. A Jane decision creates a next-question candidate, not proof that Jane improves her question-selection mechanism.

## What was tested

- 23 passing local tests: multi-cycle closure, deterministic replay, missing or forged receipt, replay denial, tampering, invalid world, fabricated LIT, no hive-generated decision, explicit Jane choice, no execution authority and capacity.
- Three scripted cycles, with three ACKs and intact append-only journals.
- Failure states halt the simulated local operation rather than creating an unverified new cycle.

## Not yet done

The demo has **not** invoked an authenticated destination-authorized Hallway workflow, created actual Gate 09 OFFER/ACK records, enabled a recurring GitHub Actions runner, deployed a GitHub Page, proven independent witnesses, or demonstrated autonomous question choice and recursive self-improvement. Enabling a real recurrent process requires a separately authorized scheduler/runner, capacity bounds and a non-automatic action review gate. A static GitHub Pages website cannot run a persistent backend.

## Next test

Wire a staged GitHub Actions `workflow_dispatch` runner to the existing verified delivery protocol, with no scheduled auto-writes until the destination ACK and choice authorization are independently checked. Test idempotence and resume-after-crash against separate repositories using intentionally invoked workflows; preserve failures at `−1`.