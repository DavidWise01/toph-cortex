#!/usr/bin/env python3
"""Gate 09: GitHub Actions actor-bound witness authorization (no quorum).
No claim of independent cryptographic signatures. Fail closed for unassigned lanes.
"""
from __future__ import annotations
import argparse
import json
import os
from pathlib import Path
import re
import sys

REGISTRY=Path(__file__).resolve().parents[1]/"memory"/"corpus-spine"/"witness-registry.json"
LANES=("A","B","C")
LOGIN=re.compile(r"^[A-Za-z0-9](?:[A-Za-z0-9-]{0,37}[A-Za-z0-9])?$")

def read_registry(path:Path=REGISTRY)->dict:
    data=json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data,dict) or data.get("schema")!="root0.witness-registry/1" or data.get("owner")!="DavidWise01":
        raise ValueError("Untrusted witness registry schema/owner")
    lanes=data.get("lanes")
    if not isinstance(lanes,dict) or set(lanes)!=set(LANES):
        raise ValueError("Registry must contain exactly A, B, C")
    seen=set()
    for lane in LANES:
        entry=lanes[lane]
        if not isinstance(entry,dict) or entry.get("state") not in ("BOUND","UNASSIGNED"):
            raise ValueError("Malformed witness lane "+lane)
        if entry["state"]=="UNASSIGNED":
            if entry.get("github_login") is not None or entry.get("github_actor_id") is not None:
                raise ValueError("Unassigned lane has forged identity")
        else:
            login=entry.get("github_login")
            uid=str(entry.get("github_actor_id",""))
            if not isinstance(login,str) or not LOGIN.fullmatch(login) or not uid.isdigit() or int(uid)<=0:
                raise ValueError("Bound witness must have GitHub login and numeric account ID")
            if uid in seen:raise ValueError("A GitHub account cannot occupy multiple independent witness lanes")
            seen.add(uid)
    return data

def authorize(witness:str, actor:str, actor_id:str, workflow:str,
              environment:dict[str,str]|None=None, registry:dict|None=None)->dict:
    env=dict(os.environ) if environment is None else environment
    config=read_registry() if registry is None else registry
    lanes=config["lanes"]
    if witness not in LANES:raise ValueError("Unknown A/B/C witness")
    binding=lanes[witness]
    if binding["state"]!="BOUND":raise ValueError("Witness "+witness+" is UNASSIGNED; no impersonation")
    if env.get("GITHUB_ACTIONS")!="true" or env.get("GITHUB_REPOSITORY")!="DavidWise01/toph-cortex":
        raise ValueError("Authenticated GitHub Actions context required")
    if env.get("GITHUB_EVENT_NAME")!="workflow_dispatch" or env.get("GITHUB_REF")!="refs/heads/main":
        raise ValueError("Only explicit main-branch workflow dispatch is authorized")
    workflow_ref=env.get("GITHUB_WORKFLOW_REF","")
    expected="/.github/workflows/"+workflow+"@refs/heads/main"
    if not workflow_ref.endswith(expected) or not workflow_ref.startswith("DavidWise01/toph-cortex/"):
        raise ValueError("Wrong workflow identity/ref")
    if not actor or not actor_id or not actor_id.isdigit():
        raise ValueError("Missing authenticated GitHub actor ID")
    if actor.casefold()!=binding["github_login"].casefold() or actor_id!=binding["github_actor_id"]:
        raise ValueError("GitHub actor is not registered to witness "+witness)
    return {"witness":witness,"github_actor":binding["github_login"],
            "github_actor_id":actor_id,"workflow":workflow_ref,"method":"github-actions-actor-binding"}

def main(argv=None)->int:
    parser=argparse.ArgumentParser()
    parser.add_argument("--witness",choices=LANES,required=True)
    parser.add_argument("--workflow",required=True)
    args=parser.parse_args(argv)
    try:
        evidence=authorize(args.witness,os.environ.get("GITHUB_ACTOR",""),
                           os.environ.get("GITHUB_ACTOR_ID",""),args.workflow)
        print(json.dumps({"authorized":True,"attestation":evidence},sort_keys=True))
        return 0
    except (ValueError,OSError,json.JSONDecodeError) as exc:
        print("DENIED: "+str(exc),file=sys.stderr)
        return 1

if __name__=="__main__":
    raise SystemExit(main())
