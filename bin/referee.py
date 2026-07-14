#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
referee.py — TOPH CORTEX · the DETERMINISTIC referee.

Not a nested agent. It measures only what a script can measure, from the ledger,
the git history, and the citations agents leave in their episodic logs:

  * hit-rate     — how many times a semantic fact was CITED ([[topic]]) by a session
                   OTHER than its author, and by how many distinct OTHER agents
                   (>=2 = earned its keep swarm-wide; self-citation never counts).
  * staleness    — a fact marked `supersedes:` something, or flagged contradicted;
                   FLAGGED, never silently rewritten.
  * invocations  — how often each procedural skill was referenced.
  * per-agent    — writes contributed, citations earned.

Maturity is proxied by the git commit-count on each fact (`git log`); "diffs got
small" is the ideal, approximated here by that count. No embedding-drift mysticism.

Usage: python bin/referee.py [--json]
"""
import os, re, sys, json, glob, subprocess, collections

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MEM = os.path.join(ROOT, "memory")

def read(p):
    return open(p, encoding="utf-8").read()

def frontmatter(text):
    m = re.match(r"---\s*(.*?)\s*---", text, re.S)
    fm = {}
    if m:
        for line in m.group(1).splitlines():
            if ":" in line:
                k, v = line.split(":", 1)
                fm[k.strip()] = v.strip()
    return fm

def ledger():
    p = os.path.join(MEM, "ledger.jsonl")
    if not os.path.exists(p):
        return []
    return [json.loads(l) for l in read(p).splitlines() if l.strip()]

def git_commits(relpath):
    try:
        out = subprocess.run(["git", "-C", ROOT, "log", "--oneline", "--", relpath],
                             capture_output=True, text=True, timeout=8)
        n = len([l for l in out.stdout.splitlines() if l.strip()])
        return n
    except Exception:
        return None

def compute():
    L = ledger()
    # semantic facts + their topics
    facts = {}
    for p in sorted(glob.glob(os.path.join(MEM, "semantic", "*.md"))):
        rel = os.path.relpath(p, ROOT).replace("\\", "/")
        fm = frontmatter(read(p))
        topic = fm.get("topic") or os.path.splitext(os.path.basename(p))[0]
        facts[topic] = {"path": rel, "fm": fm, "citations": 0, "citing_agents": set()}
    # skills
    skills = {}
    for p in sorted(glob.glob(os.path.join(MEM, "procedural", "**", "SKILL.md"), recursive=True)):
        fm = frontmatter(read(p))
        name = fm.get("name") or os.path.basename(os.path.dirname(p))
        skills[name] = {"path": os.path.relpath(p, ROOT).replace("\\", "/"), "invocations": 0}
    # scan episodic for citations [[x]]
    per_agent = collections.defaultdict(lambda: {"writes": 0, "citations_earned": 0})
    for p in sorted(glob.glob(os.path.join(MEM, "episodic", "**", "*.md"), recursive=True)):
        fm = frontmatter(read(p))
        agent = fm.get("agent", "?")
        for ref in re.findall(r"\[\[([a-z0-9\-]+)", read(p).lower()):
            if ref in facts:
                author = facts[ref]["fm"].get("written_by")
                if agent != author:      # self-citation does NOT count toward earning its keep
                    facts[ref]["citations"] += 1
                    facts[ref]["citing_agents"].add(agent)
            if ref in skills:
                skills[ref]["invocations"] += 1
    # per-agent writes from ledger
    for row in L:
        if row.get("action") in ("write", "stage", "consolidate"):
            per_agent[row.get("agent", "?")]["writes"] += 1
    # citations earned per agent (author of the fact)
    for topic, f in facts.items():
        author = f["fm"].get("written_by", "?")
        per_agent[author]["citations_earned"] += f["citations"]
    # staleness + maturity
    stale = []
    for topic, f in facts.items():
        sup = f["fm"].get("supersedes", "none")
        if sup and sup != "none":
            stale.append({"topic": topic, "reason": "supersedes " + sup})
        f["commits"] = git_commits(f["path"])
    report = {
        "facts": {t: {"path": f["path"], "hit_rate_citations": f["citations"],
                      "distinct_agents": len(f["citing_agents"]),
                      "earned_swarm_wide": len(f["citing_agents"]) >= 2,
                      "git_commits": f["commits"]}
                  for t, f in facts.items()},
        "skills": skills,
        "per_agent": {a: v for a, v in per_agent.items()},
        "stale_flags": stale,
        "ledger_rows": len(L),
    }
    return report

def main():
    r = compute()
    if "--json" in sys.argv:
        print(json.dumps(r, indent=1)); return
    print("=== TOPH CORTEX · REFEREE (deterministic) ===\n")
    print("FACTS — hit-rate by citation (cross-agent >=2 = earned its keep):")
    for t, f in sorted(r["facts"].items(), key=lambda kv: -kv[1]["hit_rate_citations"]):
        mark = "★ earned" if f["earned_swarm_wide"] else ("· cited" if f["hit_rate_citations"] else "○ cold")
        gc = "" if f["git_commits"] is None else "  git:%d" % f["git_commits"]
        print("  %-8s  cites=%d  agents=%d%s   %s" % (mark, f["hit_rate_citations"], f["distinct_agents"], gc, t))
    print("\nSKILLS — invocations:")
    for n, s in r["skills"].items():
        print("  %-16s  invoked=%d  (%s)" % (n, s["invocations"], s["path"]))
    print("\nPER-AGENT:")
    for a, v in sorted(r["per_agent"].items()):
        print("  %-8s  writes=%d  citations_earned=%d" % (a, v["writes"], v["citations_earned"]))
    print("\nSTALENESS FLAGS (flagged, never silently rewritten): %s" % (r["stale_flags"] or "none"))
    print("ledger rows: %d" % r["ledger_rows"])

if __name__ == "__main__":
    main()
