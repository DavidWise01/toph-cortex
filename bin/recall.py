#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
recall.py — TOPH CORTEX · the READ path.

Zero-LLM. Deterministic. Offline. Stdlib only, by construction: there is no model
call anywhere on this path, so the swarm's memory is usable with the power out.
Same query -> same results forever.

Ranks every memory/*.md by BM25 over the query, with a stable path tiebreak.

Usage:
    python bin/recall.py "battery read path"
    python bin/recall.py "referee metrics" -k 3 --layer semantic
"""
import os, re, sys, math, glob, argparse

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MEM = os.path.join(ROOT, "memory")

def tok(s):
    return re.findall(r"[a-z0-9]+", s.lower())

def load_docs():
    out = []
    for p in sorted(glob.glob(os.path.join(MEM, "**", "*.md"), recursive=True)):
        rel = os.path.relpath(p, ROOT).replace("\\", "/")
        if "/_staging/" in rel:      # staged, not yet committed to main memory
            continue
        text = open(p, encoding="utf-8").read()
        layer = ("semantic" if "/semantic/" in rel else
                 "episodic" if "/episodic/" in rel else
                 "procedural" if "/procedural/" in rel else "other")
        out.append({"path": rel, "text": text, "layer": layer, "toks": tok(text)})
    return out

def bm25(query, D, k1=1.5, b=0.75):
    q = tok(query)
    N = len(D)
    if not N or not q:
        return []
    avgdl = sum(len(d["toks"]) for d in D) / N
    df = {}
    for d in D:
        for t in set(d["toks"]):
            df[t] = df.get(t, 0) + 1
    ranked = []
    for d in D:
        tf = {}
        for t in d["toks"]:
            tf[t] = tf.get(t, 0) + 1
        dl = len(d["toks"]) or 1
        s = 0.0
        for t in q:
            if t not in tf:
                continue
            idf = math.log(1 + (N - df.get(t, 0) + 0.5) / (df.get(t, 0) + 0.5))
            s += idf * (tf[t] * (k1 + 1)) / (tf[t] + k1 * (1 - b + b * dl / avgdl))
        if s > 0:
            ranked.append((s, d))
    ranked.sort(key=lambda x: (-x[0], x[1]["path"]))   # deterministic
    return ranked

def snippet(text, n=180):
    body = re.sub(r"^---.*?---", "", text, count=1, flags=re.S).strip()
    body = re.sub(r"\s+", " ", body)
    return body[:n] + ("…" if len(body) > n else "")

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("query", nargs="+")
    ap.add_argument("-k", type=int, default=5)
    ap.add_argument("--layer", choices=["semantic", "episodic", "procedural"], default=None)
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    q = " ".join(a.query)
    D = [d for d in load_docs() if (a.layer is None or d["layer"] == a.layer)]
    hits = bm25(q, D)[:a.k]
    if a.json:
        import json
        print(json.dumps([{"path": d["path"], "layer": d["layer"], "score": round(s, 3)} for s, d in hits], indent=1))
        return
    if not hits:
        print("recall '%s' -> no match (mechanical, no model)." % q)
        return
    print("recall '%s' -> %d hits (BM25, zero-LLM, deterministic)\n" % (q, len(hits)))
    for s, d in hits:
        print("  [%-10s] %-44s  %.3f" % (d["layer"], d["path"], s))
        print("     %s\n" % snippet(d["text"]))

if __name__ == "__main__":
    main()
