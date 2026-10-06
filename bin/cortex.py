#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
cortex.py — TOPH CORTEX · the overseer.

Toph Cortex is the substrate that watches itself. It OVERSEES the swarm's shared
memory, MANAGES the promote/flag decisions, and LEARNS from what happens — where
"learns" is stated honestly: it maintains a deterministic, git-backed record
(cortex_state.json) of which memories and skills have earned their keep (cited,
invoked, un-contradicted). No weights, no model. The learning is bookkeeping the
whole swarm can trust cold.

Usage:
    python bin/cortex.py            # dashboard + management recommendations
    python bin/cortex.py --learn    # also append a snapshot to cortex_state.json
"""
import os, sys, json, glob, datetime, collections

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MEM = os.path.join(ROOT, "memory")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import referee  # deterministic metrics
import toroid5  # exact five-transfer commit timing

STATE = os.path.join(MEM, "cortex_state.json")

def count(glob_pat):
    return len(glob.glob(os.path.join(MEM, glob_pat), recursive=True))

def agents():
    return sorted(os.path.basename(d) for d in glob.glob(os.path.join(MEM, "episodic", "*")) if os.path.isdir(d))

def main():
    r = referee.compute()
    ag = agents()
    n_fact = count("semantic/*.md")
    n_epi = count("episodic/**/*.md")
    n_skill = count("procedural/**/SKILL.md")
    n_staged = count("_staging/**/*.md")
    earned = [t for t, f in r["facts"].items() if f["earned_swarm_wide"]]
    cold = [t for t, f in r["facts"].items() if f["hit_rate_citations"] == 0]

    print("╔══════════════════════════════════════════════════════════════╗")
    print("║  TOPH CORTEX · multi-agent swarm memory · overseer            ║")
    print("╚══════════════════════════════════════════════════════════════╝")
    print("SWARM      %d agents with episodic logs: %s" % (len(ag), ", ".join(ag)))
    rp = os.path.join(MEM, "agents.json")
    if os.path.exists(rp):
        ros = json.load(open(rp, encoding="utf-8"))
        print("ROSTER     %d real git agents, linked to ud0 @ %s :" % (len(ros["agents"]), ros["ud0"]))
        for a in ros["agents"]:
            print("   ◆ %-13s %s" % (a["name"], a["role"][:56]))
    print("SUBSTRATE  %d facts · %d episodic logs · %d skills · %d staged · %d ledger rows"
          % (n_fact, n_epi, n_skill, n_staged, r["ledger_rows"]))
    print("BATTERY    read path = 0 model calls (mechanical) · write path = gated · consolidation = 1 call/cluster")
    print("CLOCK      TOROID-5 .||||. · 5 x 1/5 transfers · commit at 5/5 · exact rational timing")
    print()
    print("LEARNED (earned swarm-wide, cited by >=2 agents):")
    for t in earned or ["  (none yet)"]:
        f = r["facts"].get(t)
        print("   ★ %-26s cites=%d agents=%d" % (t, f["hit_rate_citations"], f["distinct_agents"]) if f else "   " + t)
    print()
    print("MANAGE — recommendations (deterministic):")
    recs = []
    if n_staged:
        recs.append("%d staged change(s) awaiting validation/review before commit (the gate)." % n_staged)
    for s in r["stale_flags"]:
        recs.append("STALE: '%s' (%s) — flagged, not rewritten." % (s["topic"], s["reason"]))
    for t in cold:
        recs.append("COLD: '%s' never cited — keep, but it has not earned its keep yet." % t)
    for n, s in r["skills"].items():
        if s["invocations"] == 0:
            recs.append("Skill '%s' never invoked — candidate for retirement or better indexing." % n)
    for rc in recs or ["  substrate healthy; nothing to escalate."]:
        print("   • " + rc)

    if "--learn" in sys.argv:
        snap = {"ts": datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
                "agents": ag, "n_fact": n_fact, "n_skill": n_skill,
                "earned": earned, "cold": cold,
                "citations": {t: f["hit_rate_citations"] for t, f in r["facts"].items()},
                "invocations": {n: s["invocations"] for n, s in r["skills"].items()}}
        hist = []
        if os.path.exists(STATE):
            try: hist = json.load(open(STATE, encoding="utf-8"))
            except Exception: hist = []
        hist.append(snap)
        json.dump(hist, open(STATE, "w", encoding="utf-8"), indent=1)
        print("\nLEARN — appended snapshot #%d to memory/cortex_state.json (the maturity record; no weights)." % len(hist))

if __name__ == "__main__":
    main()
