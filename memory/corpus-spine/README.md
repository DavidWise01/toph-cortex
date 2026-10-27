# ROOT0 Corpus Spine — persistent, reference-only memory

**Canonical write repository:** [DavidWise01/toph-cortex](https://github.com/DavidWise01/toph-cortex)  
**Ledger:** [memory/corpus-spine/events.jsonl](events.jsonl)  
**Read-only UI:** [Gate 07 / Corpus Spine](https://davidwise01.github.io/persist-cortex/spine/)  
**Hallway:** https://0root.ai/  
**Status:** first five public anchors committed on 2026-10-27.

## What this does

One Git-backed append-only source *reference* chain spans OASIS, UD0, 0root.ai, Persist Cortex, and the existing TOPH agent registry. Source documents remain in their own canonical repositories. The OASIS discovery manifest's 2,144 entries are dated **metadata**, not separately verified active workers or current live repositories.

Records have independent WHAT, HOW, and WHY. **No votes, no consensus, no forced agreement.** Corrections are new entries with `supersedes`; originals remain. The chain uses full SHA-256 digests of canonical sorted-key JSON and an explicit previous-event digest. Git branch controls and off-repo witnesses would be needed for stronger tamper resistance.

Only public source references are permitted in this public ledger. Do not publish private repository names, personal memory snapshots, credentials, or sensitive content.

## Read / verify / resume (offline)

```sh
python3 bin/corpus_spine.py verify
python3 bin/corpus_spine.py status
python3 bin/corpus_spine.py tip
```

This reads plain JSONL without an LLM, database, or network access.

## Authenticated append (GitHub UI)

Open [Corpus Memory — append witnessed public reference](https://github.com/DavidWise01/toph-cortex/actions/workflows/corpus-memory-append.yml) while signed into GitHub. Enter a public DavidWise01 repository, a path on its default branch, the current 40-character Git blob SHA, and WHAT / HOW / WHY. The workflow verifies the public source against GitHub, verifies the existing chain, appends one event, commits it, and attempts a non-force push to the canonical repository. It requires Actions enabled with repository contents write permission. A workflow run has **not yet been verified**.

## Trusted local append

```sh
cd toph-cortex
tip=$(python3 bin/corpus_spine.py tip)
python3 bin/corpus_spine.py append \
  --expect-tip "$tip" --actor root0 --kind OBSERVATION \
  --source-repo DavidWise01/oasis --source-path README.md \
  --source-sha YOUR_VERIFIED_40_CHAR_BLOB_SHA \
  --what "Observed X" --how "Observed using Y" --why "Relevant because Z" \
  --verify-public-source
python3 bin/corpus_spine.py verify
git add memory/corpus-spine/events.jsonl
git commit -m "memory(corpus): append witnessed reference"
git push origin main
```

Do not force push. If the branch head advances, fetch and reconcile before extending the chain. A local append is **not persisted to GitHub until a push succeeds**.

## Boundaries

- Public GitHub Pages **only reads**. It does not receive access tokens.
- A record's public Git blob SHA identifies a file version, not its truth.
- Source owners may change their default branch; the original blob SHA remains in the witnessed record.
- A browser-local Gate 06 archive does not automatically become a public record.
- We do not touch any sealed / frozen corpora to add a pointer.
- This supplements, but does not replace, existing TOPH CORTEX memory and `memory/ledger.jsonl`.
- Future secure, private memory requires a dedicated private store or authenticated service, not a public JSONL file.
