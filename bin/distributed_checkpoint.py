#!/usr/bin/env python3
"""Gate 11: one-way, individually signed four-stream checkpoints.

Checkpoint records are append-only sidecars; original corpus, temporal, delivery,
and witness attestations are never rewritten. Signing keys never enter Git.
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
import delivery_receipt
import witness_attestation
import witness_identity

ROOT=Path(__file__).resolve().parents[1]
LEDGER=ROOT/"memory"/"corpus-spine"/"checkpoints.jsonl"
DOMAIN="ROOT0-CHECKPOINT-v1"
STREAMS=("CORPUS","TEMPORAL","DELIVERY","ATTESTATION")
FIELDS={"version","seq","kind","recorded_at","witness","github_actor","github_actor_id",
        "key_id","state","prev","payload_sha256","signature_b64","hash"}
HEX64=re.compile(r"^[a-f0-9]{64}$")

def sources()->dict:
    corpus=corpus_spine.read_rows()
    temporal=temporal_diode.read_rows(temporal_diode.LEDGER,corpus)
    delivery=delivery_receipt.read_rows(delivery_receipt.LEDGER,temporal)
    keys=witness_attestation.public_keys()
    attests=witness_attestation.read_rows(witness_attestation.LEDGER,
        {"TEMPORAL":temporal,"DELIVERY":delivery},keys)
    return {"CORPUS":corpus,"TEMPORAL":temporal,"DELIVERY":delivery,"ATTESTATION":attests}

def snapshot(streams:dict)->dict:
    return {s:{"count":len(streams[s]),
               "tip":streams[s][-1]["hash"] if streams[s] else "GENESIS"} for s in STREAMS}

def valid_state(state:dict, streams:dict)->bool:
    if not isinstance(state,dict) or set(state)!=set(STREAMS):return False
    for name in STREAMS:
        entry=state[name];rows=streams[name]
        if not isinstance(entry,dict) or set(entry)!={"count","tip"}:return False
        n=entry["count"]
        if type(n) is not int or n<0 or n>len(rows):return False
        expected=rows[n-1]["hash"] if n else "GENESIS"
        if entry["tip"]!=expected:return False
    return True

def envelope(*,witness:str,key_id:str,recorded_at:str,seq:int,prev:str,state:dict)->bytes:
    msg={"domain":DOMAIN,"witness":witness,"key_id":key_id,
         "recorded_at":recorded_at,"checkpoint_seq":seq,
         "previous_checkpoint":prev,"state":state}
    return corpus_spine.canonical(msg)

def verify_rows(events:list[dict],streams:dict,keys:dict)->str:
    if not isinstance(events,list):raise ValueError("Checkpoint journal not an array")
    prev="GENESIS";per_lane={}
    for i,e in enumerate(events,1):
        if not isinstance(e,dict) or set(e)!=FIELDS or e["version"]!=1 or e["seq"]!=i or e["kind"]!="CHECKPOINT" or e["prev"]!=prev:
            raise ValueError(f"Checkpoint {i}: schema/chain invalid")
        try:dt.date.fromisoformat(e["recorded_at"])
        except (ValueError,TypeError) as exc:raise ValueError(f"Checkpoint {i}: invalid UTC calendar date") from exc
        k=keys.get(e["key_id"])
        if not k or k["witness"]!=e["witness"] or k["github_actor_id"]!=e["github_actor_id"]:
            raise ValueError(f"Checkpoint {i}: witness public key not registered")
        actor=witness_identity.read_registry()["lanes"].get(e["witness"])
        if not actor or actor["state"]!="BOUND" or actor["github_actor_id"]!=e["github_actor_id"] or actor["github_login"].casefold()!=e["github_actor"].casefold():
            raise ValueError(f"Checkpoint {i}: witness actor binding mismatch")
        if not valid_state(e["state"],streams):raise ValueError(f"Checkpoint {i}: stream tip/count does not exist")
        last=per_lane.get(e["witness"])
        if last and any(e["state"][s]["count"]<last["state"][s]["count"] for s in STREAMS):
            raise ValueError(f"Checkpoint {i}: witness rollback forbidden")
        payload=envelope(witness=e["witness"],key_id=e["key_id"],
                 recorded_at=e["recorded_at"],seq=e["seq"],prev=e["prev"],state=e["state"])
        if e["payload_sha256"]!=hashlib.sha256(payload).hexdigest():
            raise ValueError(f"Checkpoint {i}: signed payload hash mismatch")
        try:
            pub=witness_attestation.decode64(k["public_key_b64"],32)
            signature=witness_attestation.decode64(e["signature_b64"],64)
            Ed25519PublicKey.from_public_bytes(pub).verify(signature,payload)
        except InvalidSignature as exc:raise ValueError(f"Checkpoint {i}: invalid Ed25519 signature") from exc
        if not isinstance(e["hash"],str) or not HEX64.fullmatch(e["hash"]) or corpus_spine.digest({k:v for k,v in e.items() if k!="hash"})!=e["hash"]:
            raise ValueError(f"Checkpoint {i}: SHA-256 chain mismatch")
        per_lane[e["witness"]]=e;prev=e["hash"]
    return prev

def read_rows(path:Path,streams:dict,keys:dict)->list[dict]:
    if not path.exists():return []
    raw=path.read_text(encoding="utf-8")
    if raw and not raw.endswith("\n"):raise ValueError("Truncated checkpoint JSONL")
    rows=[]
    for i,line in enumerate(raw.splitlines(),1):
        if not line:raise ValueError(f"Blank checkpoint line {i}")
        try:rows.append(json.loads(line))
        except json.JSONDecodeError as exc:raise ValueError(f"Malformed checkpoint line {i}") from exc
    verify_rows(rows,streams,keys)
    return rows

def create(rows:list[dict],streams:dict,keys:dict,*,witness:str,key_id:str,
           signature_b64:str,recorded_at:str,actor:dict)->dict:
    verify_rows(rows,streams,keys)
    if witness not in ("A","B","C") or key_id not in keys or keys[key_id]["witness"]!=witness:
        raise ValueError("No enrolled key for witness lane")
    if actor["witness"]!=witness or actor["github_actor_id"]!=keys[key_id]["github_actor_id"]:
        raise ValueError("Authenticated actor/key mismatch")
    dt.date.fromisoformat(recorded_at)
    state=snapshot(streams);prev=rows[-1]["hash"] if rows else "GENESIS"
    payload=envelope(witness=witness,key_id=key_id,recorded_at=recorded_at,
                     seq=len(rows)+1,prev=prev,state=state)
    try:
        pub=witness_attestation.decode64(keys[key_id]["public_key_b64"],32)
        sig=witness_attestation.decode64(signature_b64,64)
        Ed25519PublicKey.from_public_bytes(pub).verify(sig,payload)
    except InvalidSignature as exc:raise ValueError("Invalid checkpoint signature") from exc
    body={"version":1,"seq":len(rows)+1,"kind":"CHECKPOINT","recorded_at":recorded_at,
          "witness":witness,"github_actor":actor["github_actor"],
          "github_actor_id":actor["github_actor_id"],"key_id":key_id,
          "state":state,"prev":prev,
          "payload_sha256":hashlib.sha256(payload).hexdigest(),"signature_b64":signature_b64}
    record={**body,"hash":corpus_spine.digest(body)}
    verify_rows([*rows,record],streams,keys)
    return record

def main(argv=None)->int:
    p=argparse.ArgumentParser(description="Gate11 / individually signed corpus checkpoint")
    commands=p.add_subparsers(dest="cmd",required=True)
    for name in ("verify","status","tip"):commands.add_parser(name)
    for name in ("prepare","append"):
        a=commands.add_parser(name)
        a.add_argument("--witness",choices=("A","B","C"),required=True)
        a.add_argument("--key-id",required=True)
        a.add_argument("--recorded-at",required=True,help="UTC day YYYY-MM-DD, must be supplied for stable signing")
        if name=="append":
            a.add_argument("--signature-b64",required=True)
            a.add_argument("--expect-tip",required=True)
            a.add_argument("--expect-state-sha256",required=True)
    args=p.parse_args(argv)
    try:
        streams=sources();keys=witness_attestation.public_keys()
        rows=read_rows(LEDGER,streams,keys);tip=verify_rows(rows,streams,keys)
        if args.cmd=="verify":print(f"PASS | signed_checkpoints={len(rows)} | tip={tip}")
        elif args.cmd=="tip":print(tip)
        elif args.cmd=="status":
            print(json.dumps({"schema":"root0.checkpoint/1","records":len(rows),
              "tip":tip,"current_state":snapshot(streams),
              "registered_keys":len(keys),"votes":False,"quorum":None},indent=2))
        else:
            import key_lifecycle
            lifecycle=key_lifecycle.replay(key_lifecycle.read_rows(key_lifecycle.LEDGER,keys),keys)
            if lifecycle["active"].get(args.witness)!=args.key_id:
                raise ValueError("Witness signing key inactive, rotated, or revoked")
            if args.key_id not in keys or keys[args.key_id]["witness"]!=args.witness:
                raise ValueError("No independently registered witness signing key")
            day=dt.date.fromisoformat(args.recorded_at)
            state=snapshot(streams)
            state_hash=hashlib.sha256(corpus_spine.canonical(state)).hexdigest()
            if args.cmd=="prepare":
                payload=envelope(witness=args.witness,key_id=args.key_id,
                    recorded_at=day.isoformat(),seq=len(rows)+1,prev=tip,state=state)
                print(json.dumps({"domain":DOMAIN,"signable_b64":base64.b64encode(payload).decode(),
                    "payload_sha256":hashlib.sha256(payload).hexdigest(),
                    "state_sha256":state_hash,"expected_tip":tip,
                    "recorded_at":day.isoformat()},indent=2))
            else:
                actor=witness_identity.authorize(args.witness,os.environ.get("GITHUB_ACTOR",""),
                    os.environ.get("GITHUB_ACTOR_ID",""),"checkpoint-append.yml")
                if args.expect_tip!=tip or args.expect_state_sha256!=state_hash:
                    raise ValueError("Compare-and-swap conflict: source state or ledger advanced")
                record=create(rows,streams,keys,witness=args.witness,key_id=args.key_id,
                    signature_b64=args.signature_b64,recorded_at=day.isoformat(),actor=actor)
                if verify_rows(read_rows(LEDGER,streams,keys),streams,keys)!=tip:
                    raise ValueError("Checkpoint journal changed before writing")
                temporal_diode.write(LEDGER,record)
                verify_rows(read_rows(LEDGER,streams,keys),streams,keys)
                print(f"APPENDED LOCAL checkpoint #{record['seq']} / {record['hash']}")
                print("Git commit/push required; no cross-repo action triggered.")
        return 0
    except (ValueError,TypeError,OSError,json.JSONDecodeError,KeyError) as e:
        print("HALTED: "+str(e),file=sys.stderr);return 1

if __name__=="__main__":raise SystemExit(main())
