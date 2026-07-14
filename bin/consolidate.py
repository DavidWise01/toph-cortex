#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
consolidate.py — TOPH CORTEX · offline consolidation.

The clustering is MECHANICAL (token-Jaccard, no model): it groups recurring
episodic bullets across the whole swarm. Only THEN is the battery spent — one
model call per cluster, at write time, to abstract the cluster into a procedural
SKILL.md. This script does the mechanical half and STAGES a skill skeleton with
the cluster's evidence; the model fills the body. Output verifiable by reading it,
and the resulting skill works forever without the model that wrote it.

Usage: python bin/consolidate.py [--min 2] [--sim 0.18]
"""
import os, re, sys, glob, argparse, datetime

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MEM = os.path.join(ROOT, "memory")

def tok(s):
    STOP = set("the a of and to in is it for on with as at by my not now did read wrote".split())
    return set(w for w in re.findall(r"[a-z0-9]+", s.lower()) if len(w) > 2 and w not in STOP)

def bullets():
    out = []
    for p in sorted(glob.glob(os.path.join(MEM, "episodic", "**", "*.md"), recursive=True)):
        agent = os.path.basename(os.path.dirname(p))
        for line in open(p, encoding="utf-8"):
            line = line.strip()
            if line.startswith("- "):
                b = line[2:].strip()
                out.append({"agent": agent, "text": b, "toks": tok(b)})
    return out

def jaccard(a, b):
    if not a or not b:
        return 0.0
    return len(a & b) / len(a | b)

def cluster(items, sim):
    clusters = []
    used = [False] * len(items)
    for i in range(len(items)):
        if used[i]:
            continue
        grp = [i]; used[i] = True
        for j in range(i + 1, len(items)):
            if used[j]:
                continue
            if max(jaccard(items[k]["toks"], items[j]["toks"]) for k in grp) >= sim:
                grp.append(j); used[j] = True
        clusters.append(grp)
    return clusters

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--min", type=int, default=2)
    ap.add_argument("--sim", type=float, default=0.18)
    a = ap.parse_args()
    B = bullets()
    cl = cluster(B, a.sim)
    kept = [g for g in cl if len(g) >= a.min]
    print("consolidate: %d episodic bullets -> %d clusters (>=%d): mechanical, no model.\n" % (len(B), len(kept), a.min))
    stg = os.path.join(MEM, "_staging", "procedural")
    os.makedirs(stg, exist_ok=True)
    for gi, g in enumerate(sorted(kept, key=len, reverse=True), 1):
        agents = sorted(set(B[k]["agent"] for k in g))
        common = set.intersection(*[B[k]["toks"] for k in g]) if len(g) > 1 else B[g[0]]["toks"]
        slug = ("-".join(sorted(common))[:40] or "pattern-%d" % gi).strip("-") or ("pattern-%d" % gi)
        print("  cluster %d  (%d bullets, agents: %s)  key: %s" % (gi, len(g), ",".join(agents), " ".join(sorted(common)) or "-"))
        for k in g:
            print("     · [%s] %s" % (B[k]["agent"], B[k]["text"][:80]))
        # STAGE a skill skeleton for the battery to complete
        path = os.path.join(stg, slug, "SKILL.md")
        os.makedirs(os.path.dirname(path), exist_ok=True)
        evidence = "\n".join("- [%s] %s" % (B[k]["agent"], B[k]["text"]) for k in g)
        open(path, "w", encoding="utf-8", newline="\n").write(
            "---\nname: %s\ndescription: [BATTERY fills: when to use this skill]\n"
            "distilled_from: [%s]\nstatus: STAGED-DRAFT\nmaturity: draft\n"
            "battery: ONE model call, at write time, to abstract the evidence below into instructions\n---\n\n"
            "# %s (draft)\n\n## Evidence (mechanical cluster, agents %s)\n%s\n\n"
            "## Instructions\n[BATTERY: the model abstracts the evidence above into steps. "
            "After this one write-time call, the skill runs forever without a model — any agent reads it mechanically.]\n"
            % (slug, ",".join(agents), slug, ",".join(agents), evidence))
        print("     -> staged draft: %s\n" % os.path.relpath(path, ROOT).replace("\\", "/"))
    if not kept:
        print("  (no recurring pattern yet — nothing to distill)")

if __name__ == "__main__":
    main()
