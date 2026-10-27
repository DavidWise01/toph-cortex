#!/usr/bin/env python3
"""Gate 09 / ROOT0: authenticated witness outbox + verified remote receipt.

One-way event references; never remote writes. No quorum or convergence.
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
import urllib.parse
import urllib.request

import corpus_spine
import temporal_diode
import witness_identity

ROOT=Path(__file__).resolve().parents[1]
LEDGER=ROOT/"memory"/"corpus-spine"/"delivery-events.jsonl"
FIELDS={"version","seq","recorded_at","kind","witness","github_actor",
        "github_actor_id","registry_sha256","temporal_seq","temporal_hash",
        "destination_repo","offer_seq","offer_hash","proof","prev","hash"}
PROOF_FIELDS={"path","blob_sha","content_sha256"}
HEX64=re.compile(r"^[0-9a-f]{64}$")
HEX40=re.compile(r"^[0-9a-f]{40}$")
REPO=re.compile(r"^DavidWise01/[A-Za-z0-9._-]+$")

def registry_sha()->str:
    return hashlib.sha256(witness_identity.REGISTRY.read_bytes()).hexdigest()

def validate_rows(rows:list[dict], temporal:list[dict])->str:
    if not isinstance(rows,list) or not isinstance(temporal,list):
        raise ValueError("Expected event arrays")
    by_seq={e["seq"]:e for e in temporal}
    prev="GENESIS"
    offers={}
    confirmed=set()
    for i,e in enumerate(rows,1):
        if not isinstance(e,dict) or set(e)!=FIELDS or e["version"]!=1 or type(e["seq"]) is not int or e["seq"]!=i or e["prev"]!=prev:
            raise ValueError(f"Delivery event {i}: broken global sequence or schema")
        if e["kind"] not in ("OFFER","RECEIPT") or e["witness"] not in ("A","B","C"):
            raise ValueError(f"Delivery event {i}: unknown kind/witness")
        try: dt.date.fromisoformat(e["recorded_at"])
        except (TypeError, ValueError) as exc: raise ValueError(f"Delivery event {i}: bad calendar date") from exc
        if not isinstance(e["github_actor"],str) or not e["github_actor"] or not isinstance(e["github_actor_id"],str) or not e["github_actor_id"].isdigit():
            raise ValueError(f"Delivery event {i}: missing GitHub actor")
        if not isinstance(e["registry_sha256"],str) or not HEX64.fullmatch(e["registry_sha256"]):
            raise ValueError(f"Delivery event {i}: invalid registry provenance")
        temporal_event=by_seq.get(e["temporal_seq"]) if type(e["temporal_seq"]) is int else None
        if not temporal_event or temporal_event["hash"]!=e["temporal_hash"] or temporal_event["witness"]!=e["witness"]:
            raise ValueError(f"Delivery event {i}: no matching temporal witness")
        repo=e["destination_repo"]
        if not isinstance(repo,str) or not REPO.fullmatch(repo) or repo=="DavidWise01/toph-cortex":
            raise ValueError(f"Delivery event {i}: destination must be another DavidWise01 repository")
        if e["kind"]=="OFFER":
            if e["offer_seq"] is not None or e["offer_hash"] is not None or e["proof"] is not None:
                raise ValueError(f"Delivery event {i}: offer cannot assert receipt")
        else:
            ref=e["offer_seq"] if type(e["offer_seq"]) is int else None
            offer=offers.get(ref)
            if not offer or ref in confirmed or offer["hash"]!=e["offer_hash"]:
                raise ValueError(f"Delivery event {i}: missing/duplicate/broken offer")
            if any(e[k]!=offer[k] for k in ("witness","temporal_seq","temporal_hash","destination_repo")):
                raise ValueError(f"Delivery event {i}: receipt contradicts offer")
            proof=e["proof"]
            if not isinstance(proof,dict) or set(proof)!=PROOF_FIELDS or not HEX40.fullmatch(proof["blob_sha"]) or not HEX64.fullmatch(proof["content_sha256"]):
                raise ValueError(f"Delivery event {i}: invalid remote proof")
            corpus_spine.validate_source({"repo":repo,"path":proof["path"],"blob_sha":proof["blob_sha"],"visibility":"public"})
            confirmed.add(ref)
        if not HEX64.fullmatch(e["hash"]):
            raise ValueError(f"Delivery event {i}: invalid hash")
        if corpus_spine.digest({k:v for k,v in e.items() if k!="hash"})!=e["hash"]:
            raise ValueError(f"Delivery event {i}: SHA-256 mismatch")
        if e["kind"]=="OFFER":offers[e["seq"]]=e
        prev=e["hash"]
    return prev

def read_rows(path:Path,temporal:list[dict])->list[dict]:
    if not path.exists():return []
    raw=path.read_text(encoding="utf-8")
    if raw and not raw.endswith("\n"):raise ValueError("Truncated delivery ledger")
    rows=[]
    for i,line in enumerate(raw.splitlines(),1):
        if not line:raise ValueError(f"Blank delivery line {i}")
        try:rows.append(json.loads(line))
        except json.JSONDecodeError as exc:raise ValueError(f"Invalid JSONL event {i}") from exc
    validate_rows(rows,temporal)
    return rows

def build_event(rows:list[dict],temporal:list[dict],identity:dict,kind:str, *,
                temporal_seq:int|None=None,destination_repo:str|None=None,
                offer_seq:int|None=None,proof:dict|None=None,
                date:str|None=None)->dict:
    validate_rows(rows,temporal)
    if kind=="OFFER":
        t=next((t for t in temporal if t["seq"]==temporal_seq),None)
        if not t:raise ValueError("Select a recorded temporal event first")
        witness=t["witness"]
        dest=destination_repo
        ref=None;offer_hash=None;receipt=None
    elif kind=="RECEIPT":
        offer=next((e for e in rows if e["seq"]==offer_seq and e["kind"]=="OFFER"),None)
        if not offer:raise ValueError("Select an existing OFFER")
        witness=offer["witness"];t=next((t for t in temporal if t["seq"]==offer["temporal_seq"]),None)
        dest=offer["destination_repo"];ref=offer["seq"];offer_hash=offer["hash"];receipt=proof
    else:raise ValueError("Unknown receipt event kind")
    if not t:raise ValueError("Temporal reference missing")
    if identity["witness"]!=witness:raise ValueError("Authenticated actor does not control this witness")
    record={"version":1,"seq":len(rows)+1,"recorded_at":date or dt.datetime.now(dt.timezone.utc).date().isoformat(),
            "kind":kind,"witness":witness,"github_actor":identity["github_actor"],
            "github_actor_id":identity["github_actor_id"],"registry_sha256":registry_sha(),
            "temporal_seq":t["seq"],"temporal_hash":t["hash"],"destination_repo":dest,
            "offer_seq":ref,"offer_hash":offer_hash,"proof":receipt,
            "prev":rows[-1]["hash"] if rows else "GENESIS"}
    record["hash"]=corpus_spine.digest(record)
    validate_rows([*rows,record],temporal)
    return record

def verified_recipient_proof(offer:dict,path:str,sha:str)->dict:
    """Fetch receiver's exact public file and verify ACK content before claiming receipt."""
    source={"repo":offer["destination_repo"],"path":path,"blob_sha":sha,"visibility":"public"}
    corpus_spine.validate_source(source)
    url="https://api.github.com/repos/"+source["repo"]+"/contents/"+urllib.parse.quote(path,safe="/")
    request=urllib.request.Request(url,headers={"Accept":"application/vnd.github+json","User-Agent":"ROOT0-temporal-receipt/1"})
    with urllib.request.urlopen(request,timeout=20) as resp: metadata=json.load(resp)
    if metadata.get("type")!="file" or metadata.get("sha")!=sha or metadata.get("encoding")!="base64":
        raise ValueError("Remote public file Git SHA does not match")
    payload=base64.b64decode(metadata["content"],validate=False)
    if len(payload)>32768:raise ValueError("Remote acknowledgement too large")
    obj=json.loads(payload.decode("utf-8"))
    expected={"schema":"root0.delivery-ack/1","offer_hash":offer["hash"],
              "temporal_hash":offer["temporal_hash"],
              "destination_repo":offer["destination_repo"],"received":True}
    if not isinstance(obj,dict) or not all(obj.get(k)==v for k,v in expected.items()):
        raise ValueError("Remote file does not acknowledge this exact offer and temporal event")
    return {"path":path,"blob_sha":sha,"content_sha256":hashlib.sha256(payload).hexdigest()}

def status(rows:list[dict])->dict:
    offered={e["seq"]:e for e in rows if e["kind"]=="OFFER"}
    received={e["offer_seq"] for e in rows if e["kind"]=="RECEIPT"}
    return {"schema":"root0.delivery-ledger/1","events":len(rows),"offers":len(offered),
            "receipts_verified":len(received),"pending":len(offered)-len(received),
            "tip":rows[-1]["hash"] if rows else "GENESIS",
            "voting":False,"quorum":None,"cross_repo_write":False}

def main(argv=None)->int:
    p=argparse.ArgumentParser(description="Gate09 authenticated one-way cross-repository offers and receipts")
    sub=p.add_subparsers(dest="command",required=True)
    for name in ("verify","status","tip"):sub.add_parser(name)
    a=sub.add_parser("append")
    a.add_argument("--kind",choices=("OFFER","RECEIPT"),required=True)
    a.add_argument("--witness",choices=("A","B","C"),required=True)
    a.add_argument("--expect-tip",required=True)
    a.add_argument("--expect-temporal-tip",required=True)
    a.add_argument("--temporal-seq",type=int)
    a.add_argument("--destination-repo")
    a.add_argument("--offer-seq",type=int)
    a.add_argument("--ack-path")
    a.add_argument("--ack-sha")
    args=p.parse_args(argv)
    try:
        corpus=corpus_spine.read_rows()
        temporal=temporal_diode.read_rows(temporal_diode.LEDGER,corpus)
        rows=read_rows(LEDGER,temporal)
        tip=validate_rows(rows,temporal)
        if args.command=="verify":print(f"PASS | records={len(rows)} | tip={tip}")
        elif args.command=="tip":print(tip)
        elif args.command=="status":print(json.dumps(status(rows),indent=2))
        else:
            if tip!=args.expect_tip:raise ValueError("Delivery CAS tip mismatch")
            temporal_tip=temporal[-1]["hash"] if temporal else "GENESIS"
            if temporal_tip!=args.expect_temporal_tip:raise ValueError("Temporal CAS tip mismatch")
            identity=witness_identity.authorize(args.witness,os.environ.get("GITHUB_ACTOR",""),
                os.environ.get("GITHUB_ACTOR_ID",""),"delivery-receipt-append.yml")
            if args.kind=="OFFER":
                if args.temporal_seq is None or not args.destination_repo:raise ValueError("OFFER needs temporal seq + destination")
                target={"repo":args.destination_repo,"path":"README.md","blob_sha":"0"*40,"visibility":"public"}
                corpus_spine.validate_source(target)
                if args.destination_repo=="DavidWise01/toph-cortex":raise ValueError("Cross-repository target required")
                event=build_event(rows,temporal,identity,"OFFER",temporal_seq=args.temporal_seq,destination_repo=args.destination_repo)
            else:
                offer=next((r for r in rows if r["kind"]=="OFFER" and r["seq"]==args.offer_seq),None)
                if not offer or not args.ack_path or not args.ack_sha:raise ValueError("RECEIPT requires OFFER seq and remote ACK file")
                if offer["witness"]!=args.witness:raise ValueError("Cannot receive a different witness's OFFER")
                proof=verified_recipient_proof(offer,args.ack_path,args.ack_sha)
                event=build_event(rows,temporal,identity,"RECEIPT",offer_seq=args.offer_seq,proof=proof)
            if validate_rows(read_rows(LEDGER,temporal),temporal)!=tip:raise ValueError("Ledger concurrently updated")
            temporal_diode.write(LEDGER,event)
            validate_rows(read_rows(LEDGER,temporal),temporal)
            print(f"APPENDED LOCAL | {event['kind']} #{event['seq']} | {event['hash']}")
            print("NOT SYNCED: commit/push this append through GitHub Actions.")
        return 0
    except (ValueError,OSError,KeyError,urllib.error.URLError) as exc:
        print("HALTED: "+str(exc),file=sys.stderr);return 1

if __name__=="__main__":raise SystemExit(main())
