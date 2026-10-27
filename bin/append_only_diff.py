#!/usr/bin/env python3
"""Compare current memory files against previous Git commit for append-only continuity.
On unprotected branches this is audit evidence, not protection from force-push bypass.
"""
from __future__ import annotations
import json
from pathlib import Path
import subprocess
import sys

ROOT=Path(__file__).resolve().parents[1]
BASE="memory/corpus-spine/"
JOURNALS=("events-v2.jsonl","temporal-events.jsonl","delivery-events.jsonl",
          "witness-attestations.jsonl")
REGISTRY="witness-public-keys.json"

def previous(path:str)->bytes|None:
    cmd=["git","show","HEAD^:"+BASE+path]
    p=subprocess.run(cmd,cwd=ROOT,capture_output=True)
    return p.stdout if p.returncode==0 else None

def validate(old:bytes|None,new:bytes,filename:str)->None:
    if old is None:return
    if filename in JOURNALS:
        if not new.startswith(old):raise ValueError(filename+" rewrites/truncates prior journal bytes")
        if old and not old.endswith(b"\n"):raise ValueError(filename+" had broken historical trailing newline")
        if new and not new.endswith(b"\n"):raise ValueError(filename+" has incomplete appended JSONL")
    elif filename==REGISTRY:
        prior=json.loads(old)
        curr=json.loads(new)
        keys_old=prior.get("keys",[])
        keys_new=curr.get("keys",[])
        if prior.get("schema")!=curr.get("schema") or not isinstance(keys_old,list) or not isinstance(keys_new,list):
            raise ValueError("Key-registry schema changed")
        if len(keys_new)<len(keys_old) or keys_new[:len(keys_old)]!=keys_old:
            raise ValueError("Previously enrolled public keys cannot be removed or rewritten")
        if curr.get("revision",0)<prior.get("revision",0):
            raise ValueError("Key-registry revision regressed")

def main()->int:
    for name in (*JOURNALS,REGISTRY):
        path=ROOT/BASE/name
        old=previous(name)
        if not path.exists():
            if old is not None:raise ValueError("Deleted established memory file: "+name)
            continue
        validate(old,path.read_bytes(),name)
        print("APPEND PASS:",name)
    return 0

if __name__=="__main__":
    try:raise SystemExit(main())
    except (ValueError,OSError,json.JSONDecodeError) as e:
        print("APPEND HALTED: "+str(e),file=sys.stderr);raise SystemExit(1)
