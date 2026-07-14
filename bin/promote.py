#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
promote.py — TOPH CORTEX · the GATE (validate + promote).

The automated half of the Closure Loop: validate a STAGED semantic fact and, only
if it passes, move it into main memory and append a ledger row. Validation is
DETERMINISTIC — no model. A human can also just review the staged diff and move it
by hand; this script is the scriptable gate the write path promises.

Checks (all mechanical):
  - frontmatter parses and carries topic + written_by + confidence
  - confidence is a float in [0, 1]
  - body is non-empty
  - if a committed fact on this topic already exists and differs, refuse unless
    the staged fact declares `supersedes: <topic>` (no silent overwrite)

Usage:
  python bin/promote.py --list
  python bin/promote.py <topic>
"""
import os, re, sys, json, hashlib, datetime, glob

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MEM = os.path.join(ROOT, "memory")
STG = os.path.join(MEM, "_staging", "semantic")
DST = os.path.join(MEM, "semantic")
LEDGER = os.path.join(MEM, "ledger.jsonl")

def fm_of(text):
    m = re.match(r"---\s*(.*?)\s*---", text, re.S)
    d = {}
    if m:
        for line in m.group(1).splitlines():
            if ":" in line:
                k, v = line.split(":", 1); d[k.strip()] = v.strip()
    body = re.sub(r"^---.*?---", "", text, count=1, flags=re.S).strip()
    return d, body

def validate(text):
    fm, body = fm_of(text)
    errs = []
    if not fm.get("topic"): errs.append("missing topic")
    if not fm.get("written_by"): errs.append("missing written_by")
    try:
        c = float(fm.get("confidence", "x"))
        if not (0.0 <= c <= 1.0): errs.append("confidence out of [0,1]")
    except ValueError:
        errs.append("confidence not a number")
    if not body: errs.append("empty body")
    return fm, body, errs

def main():
    if "--list" in sys.argv or len(sys.argv) < 2:
        staged = sorted(glob.glob(os.path.join(STG, "*.md")))
        print("staged semantic (awaiting the gate): %d" % len(staged))
        for p in staged:
            print("  - " + os.path.splitext(os.path.basename(p))[0])
        print("\npromote one:  python bin/promote.py <topic>")
        return
    topic = sys.argv[1]
    sp = os.path.join(STG, topic + ".md")
    if not os.path.exists(sp):
        print("no staged fact '%s' (see --list)" % topic); sys.exit(1)
    text = open(sp, encoding="utf-8").read()
    fm, body, errs = validate(text)
    if errs:
        print("REJECTED '%s' — validation failed (deterministic gate):" % topic)
        for e in errs: print("   ✗ " + e)
        sys.exit(1)
    dst = os.path.join(DST, topic + ".md")
    if os.path.exists(dst):
        cur = open(dst, encoding="utf-8").read()
        _, curbody = fm_of(cur)
        if curbody.strip() != body.strip() and fm.get("supersedes", "none") in ("none", ""):
            print("REFUSED '%s' — a committed fact exists and differs. Set `supersedes: %s` to replace it "
                  "(no silent overwrite)." % (topic, topic)); sys.exit(1)
    # promote: strip status:STAGED, write to main, ledger it
    out = re.sub(r"^status: STAGED\s*$", "status: committed", text, flags=re.M)
    open(dst, "w", encoding="utf-8", newline="\n").write(out)
    os.remove(sp)
    row = {"ts": datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
           "agent": fm.get("written_by", "?"), "action": "promote", "layer": "semantic",
           "path": os.path.relpath(dst, ROOT).replace("\\", "/"),
           "hash": "sha256:" + hashlib.sha256(body.encode("utf-8")).hexdigest()[:16],
           "session": fm.get("session", "?"), "note": "validated + promoted past the gate"}
    with open(LEDGER, "a", encoding="utf-8", newline="\n") as f:
        f.write(json.dumps(row) + "\n")
    print("PROMOTED '%s' -> memory/semantic/%s.md (validation passed) · ledger updated" % (topic, topic))

if __name__ == "__main__":
    main()
