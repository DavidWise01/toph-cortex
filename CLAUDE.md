# TOPH CORTEX — swarm memory index (auto-loaded)

You are one agent in a **swarm** that shares this memory. Claude Code auto-loads this
file every session, so you start **already knowing where memory lives** — no retrieval
call needed to find it. The read path below never spends a model call.

## Where memory lives
- `memory/semantic/` — shared facts, one `.md` per topic (YAML frontmatter). The truth the swarm agrees on.
- `memory/episodic/<agent>/` — your own append-only session logs, dated. Cite facts you use with `[[topic]]`.
- `memory/procedural/*/SKILL.md` — distilled skills. These ARE skills: read and follow them mechanically.
- `memory/ledger.jsonl` — append-only write record (who wrote what, when, hash).
- `memory/cortex_state.json` — TOPH CORTEX's learned record of what has earned its keep.

## The loop (do this every session)
1. **RECALL first (no model):** `python bin/recall.py "<task keywords>"` → read the top facts + any skill. You now start knowing what the swarm learned. Follow `recall-first` if it surfaces.
2. **ACT.**
3. **REMEMBER at the end (gated):**
   - `python bin/remember.py --agent <you> --session <sN> --episodic --item "..." --item "cited [[topic]]"`
   - New shared fact? `... --semantic --topic <t> --body "..."` → it **stages** a diff; it does NOT enter main until validated/reviewed.
4. The `SessionEnd`/`Stop` hook (see `.claude/settings.json`) fires the distillation automatically.

## The tools (all stdlib, offline)
- `bin/recall.py` — READ. BM25, zero-LLM, deterministic. Same query → same results forever.
- `bin/remember.py` — WRITE. Episodic appends; semantic stages a diff (Closure-Loop gate).
- `bin/promote.py` — the GATE. Deterministically validates a staged fact and moves it into main memory (or a human just reviews + moves it).
- `bin/referee.py` — deterministic metrics (citation hit-rate, staleness, skill invocations). Flags, never rewrites.
- `bin/consolidate.py` — mechanical clustering of episodic → stages a skill draft (the battery fills the body, once).
- `bin/cortex.py` — the overseer: dashboard + `--learn` to record the maturity snapshot.

## The battery, named
The model is the battery. It is confined to **write time** (deciding what to keep; abstracting clusters into skills) and never touches the read path. After commit, the artifact is a greppable, git-lineaged corpus any future agent — or you with your eyeballs — can use **cold, with the power out**. Anyone claiming a memory system needs no model is hiding the battery.
