#!/usr/bin/env python3
"""ROOT0 Gate 12: append-only Ed25519 key lifecycle and recovery revocations.

ACTIVATE: new-key possession signature; one active key per witness.
ROTATE: signatures by BOTH existing and incoming keys, no voting.
REVOKE: explicit account-authorized emergency event; no forged lost-key signature.
All previous signatures retain historical verification, with compromise warnings.
"""
from __future__ import annotations
import argparse
import base64
import datetime as dt
import hashlib
import json
import os
from pathlib import Path
import re
import sys

from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey

import corpus_spine
import temporal_diode
import witness_attestation
import witness_identity

ROOT=Path(__file__).resolve().parents[1]
LEDGER=ROOT/"memory"/"corpus-spine"/"key-lifecycle.jsonl"
DOMAIN="ROOT0-KEY-LIFECYCLE-v1"
FIELDS={"version","seq","kind","recorded_at","witness","key_id","previous_key_id",
        "github_actor_id","reason","new_signature_b64","old_signature_b64",
        "prev","hash"}
HEX=re.compile(r"^[0-9a-f]{64}$")
ACTIONS=("ACTIVATE","ROTATE","REVOKE")
RECOVERY="ACCOUNT_RECOVERY_NOT_KEY_SIGNED"

def payload(*,kind:str,witness:str,key_id:str,previous_key_id:str|None,
            actor_id:str,reason:str,recorded_at:str,seq:int,prev:str,role:str)->bytes:
    msg={"domain":DOMAIN,"kind":kind,"witness":witness,"key_id":key_id,
         "previous_key_id":previous_key_id,"github_actor_id":actor_id,
         "reason":reason,"recorded_at":recorded_at,"seq":seq,"prev":prev,"role":role}
    return corpus_spine.canonical(msg)

def signature(key:dict, sig:str, data:bytes)->None:
    try:
        pub=witness_attestation.decode64(key["public_key_b64"],32)
        sign=witness_attestation.decode64(sig,64)
        Ed25519PublicKey.from_public_bytes(pub).verify(sign,data)
    except InvalidSignature as exc:raise ValueError("Invalid Ed25519 lifecycle signature") from exc

def replay(rows:list[dict],keys:dict)->dict:
    if not isinstance(rows,list):raise ValueError("Lifecycle ledger not list")
    prev="GENESIS";active={};disabled=set();history={}
    for i,e in enumerate(rows,1):
        if not isinstance(e,dict) or set(e)!=FIELDS or e["version"]!=1 or type(e["seq"]) is not int or e["seq"]!=i or e["prev"]!=prev:
            raise ValueError(f"Lifecycle event {i}: schema or previous link invalid")
        if e["kind"] not in ACTIONS or e["witness"] not in ("A","B","C"):
            raise ValueError(f"Lifecycle event {i}: action/witness invalid")
        if not isinstance(e["reason"],str) or not (1<=len(e["reason"])<=500) or not isinstance(e["github_actor_id"],str) or not e["github_actor_id"].isdigit():
            raise ValueError(f"Lifecycle event {i}: reason/identity invalid")
        try:dt.date.fromisoformat(e["recorded_at"])
        except (ValueError,TypeError) as exc:raise ValueError(f"Lifecycle event {i}: date invalid") from exc
        key=keys.get(e["key_id"]);lane=e["witness"]
        if not key or key["witness"]!=lane or key["github_actor_id"]!=e["github_actor_id"]:
            raise ValueError(f"Lifecycle event {i}: key not registered for witness")
        former=active.get(lane)
        if e["kind"]=="ACTIVATE":
            if former is not None or e["key_id"] in disabled or e["key_id"] in history or e["previous_key_id"] is not None or e["old_signature_b64"] is not None:
                raise ValueError(f"Lifecycle event {i}: invalid activation")
            signature(key,e["new_signature_b64"],payload(kind=e["kind"],witness=lane,
                key_id=e["key_id"],previous_key_id=None,actor_id=e["github_actor_id"],
                reason=e["reason"],recorded_at=e["recorded_at"],seq=i,prev=prev,role="NEW"))
            active[lane]=e["key_id"];history[e["key_id"]]="ACTIVE"
        elif e["kind"]=="ROTATE":
            old=keys.get(e["previous_key_id"])
            if former is None or e["previous_key_id"]!=former or not old or e["key_id"]==former or e["key_id"] in disabled or e["key_id"] in history:
                raise ValueError(f"Lifecycle event {i}: invalid rotation source/new key")
            if old["witness"]!=lane or old["github_actor_id"]!=e["github_actor_id"]:
                raise ValueError(f"Lifecycle event {i}: rotated key is not same witness")
            for role,pub,sig in (("OLD",old,e["old_signature_b64"]),("NEW",key,e["new_signature_b64"])):
                signature(pub,sig,payload(kind=e["kind"],witness=lane,
                    key_id=e["key_id"],previous_key_id=former,actor_id=e["github_actor_id"],
                    reason=e["reason"],recorded_at=e["recorded_at"],seq=i,prev=prev,role=role))
            disabled.add(former);history[former]="ROTATED";active[lane]=e["key_id"];history[e["key_id"]]="ACTIVE"
        else:
            if former!=e["key_id"] or e["previous_key_id"] is not None or e["new_signature_b64"] is not None or e["old_signature_b64"] is not None:
                raise ValueError(f"Lifecycle event {i}: revoke requires active key and no false key signature")
            if not e["reason"].startswith(RECOVERY+": "):
                raise ValueError(f"Lifecycle event {i}: recovery must disclose account-only authorization")
            disabled.add(e["key_id"]);history[e["key_id"]]="REVOKED";active.pop(lane,None)
        if not isinstance(e["hash"],str) or not HEX.fullmatch(e["hash"]) or corpus_spine.digest({k:v for k,v in e.items() if k!="hash"})!=e["hash"]:
            raise ValueError(f"Lifecycle event {i}: SHA mismatch")
        prev=e["hash"]
    return {"tip":prev,"active":active,"disabled":disabled,"history":history}

def read_rows(path:Path,keys:dict)->list[dict]:
    if not path.exists():return []
    raw=path.read_text(encoding="utf-8")
    if raw and not raw.endswith("\n"):raise ValueError("Truncated lifecycle JSONL")
    rows=[]
    for n,line in enumerate(raw.splitlines(),1):
        if not line:raise ValueError(f"Blank lifecycle record {n}")
        try:rows.append(json.loads(line))
        except json.JSONDecodeError as exc:raise ValueError(f"Invalid lifecycle JSON {n}") from exc
    replay(rows,keys)
    return rows

def make(rows:list[dict],keys:dict,*,kind:str,witness:str,key_id:str,
         previous_key_id:str|None,reason:str,
         new_signature_b64:str|None,old_signature_b64:str|None,
         recorded_at:str,actor_id:str)->dict:
    current=replay(rows,keys)
    if kind not in ACTIONS:raise ValueError("Unsupported key operation")
    date=dt.date.fromisoformat(recorded_at).isoformat()
    body={"version":1,"seq":len(rows)+1,"kind":kind,
          "recorded_at":date,"witness":witness,"key_id":key_id,
          "previous_key_id":previous_key_id,"github_actor_id":actor_id,
          "reason":reason,"new_signature_b64":new_signature_b64,"old_signature_b64":old_signature_b64,
          "prev":current["tip"]}
    e={**body,"hash":corpus_spine.digest(body)}
    replay([*rows,e],keys)
    return e

def main(argv=None)->int:
    p=argparse.ArgumentParser()
    sub=p.add_subparsers(dest="cmd",required=True)
    for name in ("verify","status","tip"):sub.add_parser(name)
    for name in ("prepare","append"):
        a=sub.add_parser(name)
        for arg in ("witness","kind","key-id","reason","recorded-at"):
            a.add_argument("--"+arg,required=True)
        a.add_argument("--previous-key-id")
        if name=="append":
            a.add_argument("--expect-tip",required=True)
            a.add_argument("--new-signature-b64")
            a.add_argument("--old-signature-b64")
    args=p.parse_args(argv)
    try:
        keys=witness_attestation.public_keys()
        rows=read_rows(LEDGER,keys);s=replay(rows,keys)
        if args.cmd=="verify":print(f"PASS / lifecycle_events={len(rows)} / tip={s['tip']}")
        elif args.cmd=="tip":print(s["tip"])
        elif args.cmd=="status":
            print(json.dumps({"schema":"root0.key-lifecycle/1","events":len(rows),"tip":s["tip"],
                "active":s["active"],"disabled":sorted(s["disabled"]),
                "history":s["history"],"quorum":None,"votes":False},indent=2))
        else:
            lane=args.witness;kind=args.kind;kid=args.key_id;old=args.previous_key_id
            if kind not in ACTIONS or lane not in ("A","B","C"):raise ValueError("Unsupported kind or witness")
            public=keys.get(kid)
            if not public or public["witness"]!=lane:raise ValueError("Unenrolled signing key")
            day=dt.date.fromisoformat(args.recorded_at).isoformat()
            if args.cmd=="prepare":
                if kind=="REVOKE":
                    print(json.dumps({"kind":"REVOKE","tip":s["tip"],"authorization":RECOVERY,
                        "reason":"ACCOUNT ONLY, no private-key signature claimed"},indent=2))
                else:
                    proofs={}
                    for role in (("OLD","NEW") if kind=="ROTATE" else ("NEW",)):
                        proofs[role]=base64.b64encode(payload(kind=kind,witness=lane,key_id=kid,
                            previous_key_id=old,actor_id=public["github_actor_id"],
                            reason=args.reason,recorded_at=day,seq=len(rows)+1,prev=s["tip"],role=role)).decode()
                    print(json.dumps({"kind":kind,"tip":s["tip"],"payloads_b64":proofs},indent=2))
            else:
                actor=witness_identity.authorize(lane,os.environ.get("GITHUB_ACTOR",""),
                    os.environ.get("GITHUB_ACTOR_ID",""),"key-lifecycle-append.yml")
                if actor["github_actor_id"]!=public["github_actor_id"]:
                    raise ValueError("Authenticated actor differs from key actor")
                if args.expect_tip!=s["tip"]:raise ValueError("Lifecycle CAS tip changed")
                e=make(rows,keys,kind=kind,witness=lane,key_id=kid,previous_key_id=old,
                    reason=args.reason,new_signature_b64=args.new_signature_b64,
                    old_signature_b64=args.old_signature_b64,recorded_at=day,
                    actor_id=actor["github_actor_id"])
                if replay(read_rows(LEDGER,keys),keys)["tip"]!=s["tip"]:
                    raise ValueError("Concurrent lifecycle write")
                temporal_diode.write(LEDGER,e)
                read_rows(LEDGER,keys)
                print(f"APPENDED LOCAL {kind} #{e['seq']} / {e['hash']}")
        return 0
    except (ValueError,OSError,TypeError,KeyError,json.JSONDecodeError) as e:
        print("HALTED: "+str(e),file=sys.stderr);return 1

if __name__=="__main__":raise SystemExit(main())
