#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
remember.py — TOPH CORTEX · the WRITE path (gated).

The battery (a model) is ALLOWED here, but write is gated:
  - EPISODIC entries append directly to the agent's own append-only log.
  - SEMANTIC changes are STAGED to memory/_staging/ as a diff — never straight
    to main memory. A validation script or human review stands between staging
    and commit (the Closure Loop: extend -> verify -> commit lineage).
Every write appends a row to the ledger with a content hash.

Usage:
  python bin/remember.py --agent beta --episodic --session s4 \
      --item "read [[battery-location]] via recall (no model)" --item "built X"
  python bin/remember.py --agent beta --semantic --topic caching --session s4 \
      --body "the cache is redis, decided by the sovereign" --confidence 0.8
"""
import os, sys, json, time, hashlib, argparse, datetime

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MEM = os.path.join(ROOT, "memory")
LEDGER = os.path.join(MEM, "ledger.jsonl")

def H(s):
    return "sha256:" + hashlib.sha256(s.encode("utf-8")).hexdigest()[:16]

def now():
    return datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")

def append_ledger(row):
    os.makedirs(MEM, exist_ok=True)
    with open(LEDGER, "a", encoding="utf-8", newline="\n") as f:
        f.write(json.dumps(row) + "\n")

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--agent", required=True)
    ap.add_argument("--session", required=True)
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--episodic", action="store_true")
    g.add_argument("--semantic", action="store_true")
    ap.add_argument("--item", action="append", default=[], help="episodic bullet (repeatable)")
    ap.add_argument("--topic")
    ap.add_argument("--body")
    ap.add_argument("--confidence", default="0.7")
    ap.add_argument("--note", default="")
    a = ap.parse_args()
    date = datetime.date.today().isoformat()

    if a.episodic:
        d = os.path.join(MEM, "episodic", a.agent)
        os.makedirs(d, exist_ok=True)
        path = os.path.join(d, "%s-%s.md" % (date, a.session))
        rel = os.path.relpath(path, ROOT).replace("\\", "/")
        if not os.path.exists(path):
            open(path, "w", encoding="utf-8", newline="\n").write(
                "---\nagent: %s\nsession: %s\ndate: %s\n---\n\n" % (a.agent, a.session, date))
        body = "".join("- " + it + "\n" for it in a.item)
        with open(path, "a", encoding="utf-8", newline="\n") as f:
            f.write(body)
        append_ledger({"ts": now(), "agent": a.agent, "action": "write", "layer": "episodic",
                       "path": rel, "hash": H(body), "session": a.session, "note": a.note or "episodic append"})
        print("EPISODIC appended -> %s (%d items) · ledger updated" % (rel, len(a.item)))
        return

    # semantic -> STAGE a diff, do not touch main
    assert a.topic and a.body, "semantic write needs --topic and --body"
    stg = os.path.join(MEM, "_staging", "semantic")
    os.makedirs(stg, exist_ok=True)
    path = os.path.join(stg, a.topic + ".md")
    rel = os.path.relpath(path, ROOT).replace("\\", "/")
    fm = ("---\ntopic: %s\ntags: []\nconfidence: %s\nwritten_by: %s\nsession: %s\n"
          "supersedes: none\nupdated: %s\nstatus: STAGED\n---\n\n" % (a.topic, a.confidence, a.agent, a.session, date))
    open(path, "w", encoding="utf-8", newline="\n").write(fm + a.body + "\n")
    append_ledger({"ts": now(), "agent": a.agent, "action": "stage", "layer": "semantic",
                   "path": rel, "hash": H(a.body), "session": a.session, "note": a.note or "staged, awaiting validation"})
    print("SEMANTIC STAGED -> %s · ledger updated" % rel)
    print("  gate: nothing enters main memory until a validation script passes or you review the diff.")

if __name__ == "__main__":
    main()
