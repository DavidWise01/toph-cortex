#!/usr/bin/env python3
"""ROOT0 Gate 10: append-only Ed25519 attestations of existing Git events.
Uses externally held private keys; never reads/stores private keys in the repository.
No quorum or automatic actions. Requires 'cryptography' for Ed25519 verification.
"""
from __future__ import annotations
import argparse
import base64
import binascii
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
import witness_identity

ROOT=Path(__file__).resolve().parents[1]
REGISTRY=ROOT/"memory"/"corpus-spine"/"witness-public-keys.json"
LEDGER=ROOT/"memory"/"corpus-spine"/"witness-attestations.jsonl"
DOMAIN="ROOT0-ATTESTATION-v1"
STREAMS={"TEMPORAL":"temporal-events.jsonl","DELIVERY":"delivery-events.jsonl"}
FIELDS={"version","seq","kind","recorded_at","witness","source_stream","source_seq",
        "source_hash","key_id","signature_b64","signed_payload_sha256","prev","hash"}
KEY_FIELDS={"witness","github_actor_id","public_key_b64","key_id","enrolled_on"}
HEX64=re.compile(r"^[a-f0-9]{64}$")

def decode64(text:str, length:int)->bytes:
    if not isinstance(text,str):
        raise ValueError("Expected strict base64 string")
    try:raw=base64.b64decode(text,validate=True)
    except (ValueError,binascii.Error) as exc:raise ValueError("Invalid base64") from exc
    if len(raw)!=length:raise ValueError(f"Expected {length} bytes")
    if base64.b64encode(raw).decode("ascii")!=text:raise ValueError("Non-canonical base64")
    return raw

def public_keys(path:Path=REGISTRY)->dict:
    data=json.loads(path.read_text(encoding="utf-8"))
    if data.get("schema")!="root0.witness-keys/1" or not isinstance(data.get("keys"),list):
        raise ValueError("Wrong key registry format")
    witness_registry=witness_identity.read_registry()
    keys={}
    for entry in data["keys"]:
        if not isinstance(entry,dict) or set(entry)!=KEY_FIELDS:raise ValueError("Key entry malformed")
        lane=entry["witness"];binding=witness_registry["lanes"].get(lane)
        if not binding or binding["state"]!="BOUND" or entry["github_actor_id"]!=binding["github_actor_id"]:
            raise ValueError("Key has no registered matching witness actor")
        raw=decode64(entry["public_key_b64"],32)
        expected=hashlib.sha256(raw).hexdigest()
        if entry["key_id"]!=expected or entry["key_id"] in keys:raise ValueError("Duplicate or incorrect public key fingerprint")
        try:dt.date.fromisoformat(entry["enrolled_on"])
        except (ValueError,TypeError) as exc:raise ValueError("Invalid key enrollment date") from exc
        keys[expected]=entry
    return keys

def source_ledgers()->dict:
    corpus=corpus_spine.read_rows()
    temporal=temporal_diode.read_rows(temporal_diode.LEDGER,corpus)
    delivery=delivery_receipt.read_rows(delivery_receipt.LEDGER,temporal)
    return {"TEMPORAL":temporal,"DELIVERY":delivery}

def message(witness:str,stream:str,seq:int,source_hash:str,key_id:str)->bytes:
    if witness not in ("A","B","C") or stream not in STREAMS or type(seq) is not int or seq<1:
        raise ValueError("Invalid signable attestation subject")
    if not isinstance(source_hash,str) or not HEX64.fullmatch(source_hash) or not isinstance(key_id,str) or not HEX64.fullmatch(key_id):
        raise ValueError("Invalid subject or key hash")
    envelope={"domain":DOMAIN,"witness":witness,"source_stream":stream,"source_seq":seq,
              "source_hash":source_hash,"key_id":key_id}
    return corpus_spine.canonical(envelope)

def verify_rows(rows:list[dict],sources:dict,keys:dict)->str:
    if not isinstance(rows,list):raise ValueError("Attestation ledger not a list")
    prev="GENESIS"
    for i,e in enumerate(rows,1):
        if not isinstance(e,dict) or set(e)!=FIELDS or e["version"]!=1 or e["seq"]!=i or e["kind"]!="ATTEST":
            raise ValueError(f"Attestation {i}: malformed")
        if e["prev"]!=prev or e["witness"] not in ("A","B","C") or e["source_stream"] not in STREAMS:
            raise ValueError(f"Attestation {i}: chain, witness or source failure")
        try:dt.date.fromisoformat(e["recorded_at"])
        except (TypeError,ValueError) as exc:raise ValueError(f"Attestation {i}: invalid record date") from exc
        subject=sources[e["source_stream"]]
        if type(e["source_seq"]) is not int or not 1<=e["source_seq"]<=len(subject):
            raise ValueError(f"Attestation {i}: source not present")
        original=subject[e["source_seq"]-1]
        if original["hash"]!=e["source_hash"] or original["witness"]!=e["witness"]:
            raise ValueError(f"Attestation {i}: source hash or witness mismatch")
        key=keys.get(e["key_id"])
        if not key or key["witness"]!=e["witness"]:raise ValueError(f"Attestation {i}: key not enrolled for witness")
        signed=message(e["witness"],e["source_stream"],e["source_seq"],e["source_hash"],e["key_id"])
        if e["signed_payload_sha256"]!=hashlib.sha256(signed).hexdigest():
            raise ValueError(f"Attestation {i}: signed envelope mismatch")
        signature=decode64(e["signature_b64"],64)
        try:Ed25519PublicKey.from_public_bytes(decode64(key["public_key_b64"],32)).verify(signature,signed)
        except InvalidSignature as exc:raise ValueError(f"Attestation {i}: invalid Ed25519 signature") from exc
        body={k:v for k,v in e.items() if k!="hash"}
        if not isinstance(e["hash"],str) or not HEX64.fullmatch(e["hash"]) or corpus_spine.digest(body)!=e["hash"]:
            raise ValueError(f"Attestation {i}: chain SHA mismatch")
        prev=e["hash"]
    return prev

def read_rows(path:Path,sources:dict,keys:dict)->list[dict]:
    if not path.exists():return []
    raw=path.read_text(encoding="utf-8")
    if raw and not raw.endswith("\n"):raise ValueError("Truncated attestation journal")
    out=[]
    for i,line in enumerate(raw.splitlines(),1):
        if not line:raise ValueError(f"Blank attestation line {i}")
        try:out.append(json.loads(line))
        except json.JSONDecodeError as exc:raise ValueError(f"Invalid attestation JSON #{i}") from exc
    verify_rows(out,sources,keys)
    return out

def append(rows:list[dict],sources:dict,keys:dict,*,witness:str,stream:str,seq:int,
           key_id:str,signature_b64:str,recorded_at:str|None=None)->dict:
    verify_rows(rows,sources,keys)
    if stream not in sources or type(seq) is not int or seq<1 or seq>len(sources[stream]):
        raise ValueError("Referenced event missing")
    subject=sources[stream][seq-1]
    if subject["witness"]!=witness:raise ValueError("Cannot sign a different witness's record")
    if key_id not in keys or keys[key_id]["witness"]!=witness:raise ValueError("Witness key unassigned")
    signed=message(witness,stream,seq,subject["hash"],key_id)
    try:Ed25519PublicKey.from_public_bytes(decode64(keys[key_id]["public_key_b64"],32)).verify(decode64(signature_b64,64),signed)
    except InvalidSignature as exc:raise ValueError("Invalid Ed25519 signature") from exc
    body={"version":1,"seq":len(rows)+1,"kind":"ATTEST",
          "recorded_at":recorded_at or dt.datetime.now(dt.timezone.utc).date().isoformat(),
          "witness":witness,"source_stream":stream,"source_seq":seq,
          "source_hash":subject["hash"],"key_id":key_id,"signature_b64":signature_b64,
          "signed_payload_sha256":hashlib.sha256(signed).hexdigest(),
          "prev":rows[-1]["hash"] if rows else "GENESIS"}
    event={**body,"hash":corpus_spine.digest(body)}
    verify_rows([*rows,event],sources,keys)
    return event

def main(argv=None)->int:
    p=argparse.ArgumentParser(description="Offline-verifiable Ed25519 witness attestations; no votes, no quorum")
    sub=p.add_subparsers(dest="cmd",required=True)
    for name in ("verify","status","tip"):sub.add_parser(name)
    prepare=sub.add_parser("prepare")
    submit=sub.add_parser("append")
    for cmd in (prepare,submit):
        cmd.add_argument("--witness",choices=("A","B","C"),required=True)
        cmd.add_argument("--source-stream",choices=tuple(STREAMS),required=True)
        cmd.add_argument("--source-seq",type=int,required=True)
        cmd.add_argument("--key-id",required=True)
    submit.add_argument("--signature-b64",required=True)
    submit.add_argument("--expect-tip",required=True)
    submit.add_argument("--expect-source-tip",required=True)
    try:
        args=p.parse_args(argv)
        sources=source_ledgers();keys=public_keys();rows=read_rows(LEDGER,sources,keys)
        tip=verify_rows(rows,sources,keys)
        if args.cmd=="verify":print(f"PASS | attested={len(rows)} | tip={tip}")
        elif args.cmd=="tip":print(tip)
        elif args.cmd=="status":
            print(json.dumps({"schema":"root0.attestation/1","events":len(rows),"tip":tip,
                "registered_signing_keys":{x:sum(e["witness"]==x for e in keys.values()) for x in ("A","B","C")},
                "quorum":None,"voting":False},indent=2))
        elif args.cmd in ("prepare","append"):
            import key_lifecycle
            lifecycle=key_lifecycle.replay(key_lifecycle.read_rows(key_lifecycle.LEDGER,keys),keys)
            stream=args.source_stream;seq=args.source_seq;lane=args.witness
            if lifecycle["active"].get(lane)!=args.key_id:
                raise ValueError("Signing key inactive, rotated, or revoked under Gate 12")
            if args.key_id not in keys or keys[args.key_id]["witness"]!=lane:
                raise ValueError("No enrolled matching public key for witness")
            if not 1<=seq<=len(sources[stream]):raise ValueError("Referenced event not found")
            subject=sources[stream][seq-1]
            if subject["witness"]!=lane:raise ValueError("Witness mismatch")
            signable=message(lane,stream,seq,subject["hash"],args.key_id)
            if args.cmd=="prepare":
                print(json.dumps({"encoding":"base64","payload_b64":base64.b64encode(signable).decode(),
                    "payload_sha256":hashlib.sha256(signable).hexdigest(),
                    "attestation_tip":tip,
                    "source_tip":sources[stream][-1]["hash"]},indent=2))
            else:
                actor=witness_identity.authorize(lane,os.environ.get("GITHUB_ACTOR",""),
                      os.environ.get("GITHUB_ACTOR_ID",""),"witness-attestation-append.yml")
                if actor["github_actor_id"]!=keys[args.key_id]["github_actor_id"]:
                    raise ValueError("Key actor and GitHub Actions actor mismatch")
                if args.expect_tip!=tip or args.expect_source_tip!=sources[stream][-1]["hash"]:
                    raise ValueError("Compare-and-swap tip conflict")
                item=append(rows,sources,keys,witness=lane,stream=stream,seq=seq,
                    key_id=args.key_id,signature_b64=args.signature_b64)
                if verify_rows(read_rows(LEDGER,sources,keys),sources,keys)!=tip:
                    raise ValueError("Concurrent ledger update")
                temporal_diode.write(LEDGER,item)
                print(f"APPENDED LOCAL ATTESTATION #{item['seq']} | {item['hash']}")
                print("Not Git persistent until commit and successful non-force push")
        return 0
    except (ValueError,OSError,KeyError,json.JSONDecodeError) as exc:
        print("HALTED: "+str(exc),file=sys.stderr);return 1

if __name__=="__main__":raise SystemExit(main())
