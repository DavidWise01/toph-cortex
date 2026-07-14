# TOPH CORTEX

**A multi-agent swarm memory hub.** The substrate that oversees, manages, and learns
from a swarm's shared memory — built on one principle: *the model is the battery, so
confine it to write time and make read time fully mechanical.* Model writes, grep
reads, git remembers.

> Which is, not coincidentally, just **AKASHA with hooks bolted on**. The pattern was
> already there; Claude Code adds the automation seams (CLAUDE.md auto-load, session
> hooks, skills-as-procedural-memory) so the loop closes without hand-carrying context.

---

## The battery, found first
In any "self-evolving memory" system the LLM is the battery — you can't remove it,
because deciding *what's worth keeping* and *abstracting patterns into skills* genuinely
need judgment. What you **can** do is move the battery to **write time only** and make
**read time fully mechanical**. Systems that need the model to read their own memory
(a model call inside the retrieval score) are hiding the battery and calling it
perpetual motion. TOPH CORTEX names it and confines it.

## Substrate — plain files in a git repo
No database, no server. Every node is human-readable, diffable, and useful with the power out.
```
memory/
  semantic/      facts, one .md per topic (YAML frontmatter) — shared truth
  episodic/      append-only session logs, per agent (episodic/<agent>/) — cite [[topic]]
  procedural/    distilled skills — these ARE Claude Code skills (SKILL.md)
  ledger.jsonl   append-only: who wrote what, when, from what session, hash
  cortex_state.json   the overseer's learned maturity record
```

## Read path — **zero LLM**
`bin/recall.py` is BM25 over the memory, stdlib-only by construction — no model call
anywhere. Deterministic, offline, same query → same results forever. `CLAUDE.md` is
auto-loaded, so every agent starts already knowing where memory lives, with no
retrieval call.

## Write path — model allowed, but **gated**
`bin/remember.py`: episodic entries append directly; **semantic changes STAGE a diff**
to `memory/_staging/`, never straight to main. Nothing enters committed memory without
a validation script passing or your review — the Closure Loop: extend → verify → commit
lineage. The `SessionEnd`/`Stop` hook fires this automatically.

## Referee — deterministic, not a nested agent
`bin/referee.py` measures only what a script can measure:
- **hit-rate** — did a later session cite this memory (`[[topic]]`), and how many *distinct* agents (cross-agent ≥ 2 = earned its keep swarm-wide);
- **staleness** — a fact contradicted/superseded by a newer entry → **flagged, never silently rewritten**;
- **skill invocations**; **per-agent** contribution and citations earned.
The convergence signal is "diffs got small" — `git log` on a memory file is its maturity
curve, for free. No embedding-drift mysticism.

## Consolidation — offline for real
`bin/consolidate.py` clusters episodic entries **mechanically** (token-Jaccard, no model),
then spends the battery **once per cluster** to draft a procedural `SKILL.md`. The model
call is at write time, its output verifiable by reading it, and the skill works forever
without the model that wrote it — because Claude Code skills are just instructions on disk
any future model instance reads mechanically.

## TOPH CORTEX — the overseer
`bin/cortex.py` is the substrate watching itself: it OVERSEES the swarm (agents, memories,
skills, staged changes), MANAGES the promote/flag decisions, and **LEARNS** — where learning
is stated plainly as *deterministic bookkeeping*: `--learn` appends a snapshot to
`cortex_state.json` recording which memories/skills have earned their keep. **No weights,
no battery** in the learning; it is a git-backed record the whole swarm can trust cold.

## The swarm shape
Each agent keeps its own episodic log; **semantic facts and procedural skills are shared**.
Cross-agent citation is the learning signal: when agent β cites a fact agent α wrote, that
fact earned its keep swarm-wide. A new agent joins already knowing the swarm's memory cold.

## Run it
```
python bin/recall.py "battery read path"      # mechanical read
python bin/remember.py --agent me --session s5 --episodic --item "cited [[substrate]]"
python bin/consolidate.py                      # cluster -> stage skill drafts
python bin/referee.py                          # deterministic metrics
python bin/cortex.py --learn                   # overseer dashboard + maturity snapshot
```

## The honest limit, stated plainly
You still need a model for the two genuinely cognitive operations — deciding what's worth
keeping, and abstracting patterns into skills. No architecture eliminates that; anyone
claiming otherwise is hiding the battery. What this design guarantees instead is that the
**artifact never depends on the battery after commit**: internet dies, you still have a
greppable, verifiable, git-lineaged corpus the next session — or the next model, or you
with your eyeballs — can use cold.

David Lee Wise (ROOT0) / TriPod LLC, with AVAN.
