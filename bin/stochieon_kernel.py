#!/usr/bin/env python3
"""Gate 17 STOCHIEON — append-only public kernel envelope and time evidence.

Each OBSERVE is a real authenticated HTTPS/Git read with a monotonic RTT.
A SEAL commits a complete, verified declared manifest scope only after a
separately accepted Hallway loom receipt is fetched and verified. HTTP Date
is an unsigned assertion, NEVER a trusted timestamp or time dilation.
"""
from __future__ import annotations
import argparse
import base64
import datetime as dt
import email.utils
import hashlib
import json
import os
from pathlib import Path
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

import corpus_spine
import temporal_diode
import threaded_loom
import witness_identity

ROOT=Path(__file__).resolve().parents[1]
MANIFEST=ROOT/"memory"/"stochieon"/"manifest-v1.json"
LEDGER=ROOT/"memory"/"stochieon"/"events-v1.jsonl"
DOMAIN="ROOT0-STOCHIEON-GATE17-v1\n"
HEX=re.compile(r"^[0-9a-f]{64}$")
SHA1=re.compile(r"^[0-9a-f]{40}$")
ID=re.compile(r"^[a-z0-9][a-z0-9-]{0,63}$")
PHASES=("PAST_OBSERVES","PRESENT_DESERVES","FUTURE_RESERVES")
FIELDS={"version","seq","kind","recorded_at","witness","actor_id","node_id",
        "manifest_sha256","loom_tip","corpus_tip","observation","coverage",
        "seal_root","hallway_receipt","prev","watermark","hash"}
OBS_FIELDS={"transport","http_status","sent_utc","received_utc","monotonic_rtt_ms",
            "date_header_utc","content_sha256","git_blob_sha","result","time_quality"}
RECEIPT_FIELDS={"receiver","source_seq","source_hash","receipt_sha256"}
LIMIT=1_000_000
DATE_QUALITY="UNSIGNED_HTTP_DATE_NOT_TRUSTED_TSA"

def canonical(x)->bytes:
    return corpus_spine.canonical(x)

def sha(x)->str:
    return hashlib.sha256(canonical(x)).hexdigest()

def iso(timepoint:dt.datetime)->str:
    return timepoint.astimezone(dt.timezone.utc).isoformat(timespec="milliseconds").replace("+00:00","Z")

def utc(s:str)->dt.datetime:
    if not isinstance(s,str) or not s.endswith("Z"):raise ValueError("Expected UTC ISO Z time")
    p=dt.datetime.fromisoformat(s.replace("Z","+00:00"))
    if p.utcoffset()!=dt.timedelta(0):raise ValueError("Time not UTC")
    return p

def watermark(e:dict)->str:
    return ".dlw:"+hashlib.sha256(DOMAIN.encode("ascii")+canonical(e)).hexdigest()

def manifest_check(m:dict)->dict:
    if not isinstance(m,dict) or m.get("schema")!="root0.stochieon.kernel/17" or m.get("name")!="stochieon" or m.get("version")!=17:
        raise ValueError("Wrong STOCHIEON kernel manifest")
    contract=m.get("contract",{})
    if contract.get("watermark")!=".dlw" or contract.get("constant")!="cubit" or contract.get("witness_lanes")!=["A","B","C"] or contract.get("quorum") is not None or contract.get("voting") is not False:
        raise ValueError("Immutable cubit/.dlw/three-lane contract violated")
    scope=m.get("scope",{})
    if scope.get("inventory_exhaustive") is not False or scope.get("automatic_agents") is not False or scope.get("seal_requires_independent_hallway_anchor") is not True:
        raise ValueError("Manifest must not pretend exhaustive or autonomous observations")
    nodes=m.get("endpoints")
    if not isinstance(nodes,list) or not nodes or len(nodes)>64:
        raise ValueError("Declared kernel scope is invalid")
    found={}
    for n in nodes:
        if not isinstance(n,dict) or not isinstance(n.get("id"),str) or not ID.fullmatch(n["id"]) or n["id"] in found:
            raise ValueError("Duplicate or invalid kernel endpoint ID")
        if type(n.get("required")) is not bool or n.get("layer") not in ("K","E","T","X"):
            raise ValueError("Kernel layer/required flag invalid")
        if n.get("kind")=="git_file":
            if set(n)!={"id","layer","kind","repo","branch","path","expected_git_blob","required"}:
                raise ValueError("Unexpected public Git node fields")
            if not re.fullmatch(r"DavidWise01/[A-Za-z0-9._-]+",n["repo"]) or n["branch"] not in ("main","master") or not SHA1.fullmatch(n["expected_git_blob"]):
                raise ValueError("Untrusted public Git node")
            path=n["path"]
            if not isinstance(path,str) or not 1<=len(path)<=350 or path.startswith("/") or any(p in ("",".","..") for p in path.split("/")) or "\\" in path:
                raise ValueError("Unsafe public Git path")
        elif n.get("kind")=="https":
            if set(n)!={"id","layer","kind","url","required"}:
                raise ValueError("Unexpected HTTPS node fields")
            url=urllib.parse.urlsplit(n["url"])
            if url.scheme!="https" or url.username or url.password or url.query or url.fragment or url.port not in (None,443):
                raise ValueError("Untrusted public HTTPS endpoint")
            if url.hostname not in ("0root.ai","davidwise01.github.io"):
                raise ValueError("Public HTTPS endpoint must be an explicit owned-domain host")
        else:raise ValueError("Unsupported kernel node kind")
        found[n["id"]]=n
    link=m.get("independent_anchor",{})
    if link.get("receiver_repository")!="DavidWise01/0root" or link.get("required_loom_seq")!=1 or not HEX.fullmatch(link.get("required_loom_hash","")):
        raise ValueError("Immutable independent anchor target invalid")
    return found

def read_manifest(path:Path=MANIFEST)->dict:
    m=json.loads(path.read_text(encoding="utf-8"))
    manifest_check(m)
    return m

def validate_observation(o:dict,n:dict)->None:
    if not isinstance(o,dict) or set(o)!=OBS_FIELDS:
        raise ValueError("Malformed observed endpoint sample")
    sent=utc(o["sent_utc"]);received=utc(o["received_utc"])
    if received<sent or type(o["monotonic_rtt_ms"]) not in (float,int) or not 0<=o["monotonic_rtt_ms"]<=120000:
        raise ValueError("Negative/invalid monotonic network measurement")
    if type(o["http_status"]) is not int or not 0<=o["http_status"]<600:
        raise ValueError("Malformed HTTP result")
    if o["transport"] not in ("HTTP_RESPONSE","NETWORK_ERROR"):
        raise ValueError("Unknown network result")
    if o["result"] not in ("MATCH","MISMATCH","UNAVAILABLE","TOO_LARGE"):
        raise ValueError("Unrecognized kernel endpoint verification")
    if o["time_quality"]!=DATE_QUALITY:
        raise ValueError("Unsigned HTTP Date cannot be a trusted timestamp")
    if o["date_header_utc"] is not None:utc(o["date_header_utc"])
    if o["content_sha256"] is not None and (not isinstance(o["content_sha256"],str) or not HEX.fullmatch(o["content_sha256"])):
        raise ValueError("Invalid observed SHA-256")
    if o["git_blob_sha"] is not None and (not isinstance(o["git_blob_sha"],str) or not SHA1.fullmatch(o["git_blob_sha"])):
        raise ValueError("Invalid observed Git blob")
    if n["kind"]=="git_file":
        if o["result"]=="MATCH" and (o["git_blob_sha"]!=n["expected_git_blob"] or o["content_sha256"] is None):
            raise ValueError("Reported MATCH conflicts with pinned Git blob")
    elif o["result"]=="MATCH" and o["content_sha256"] is None:
        raise ValueError("HTTPS MATCH requires actually downloaded bytes")
    if o["transport"]=="NETWORK_ERROR" and (o["http_status"]!=0 or o["result"]=="MATCH"):
        raise ValueError("Network error cannot be reported as verified")

def cover(rows:list[dict],nodes:dict)->list[dict]:
    latest={}
    for e in rows:
        if e["kind"]=="OBSERVE":latest[e["node_id"]]=e
    out=[]
    for key in sorted(nodes):
        if not nodes[key]["required"]:continue
        event=latest.get(key)
        if not event or event["observation"]["result"]!="MATCH":
            raise ValueError("SEAL denied: required kernel node "+key+" is not observed MATCH")
        out.append({"node_id":key,"observation_seq":event["seq"],"observation_hash":event["hash"]})
    return out

def verify(rows:list[dict],m:dict)->str:
    nodes=manifest_check(m)
    fp=sha(m)
    prev="GENESIS";old=[]
    for i,e in enumerate(rows,1):
        if not isinstance(e,dict) or set(e)!=FIELDS or e["version"]!=17 or type(e["seq"]) is not int or e["seq"]!=i or e["prev"]!=prev:
            raise ValueError(f"Stochieon #{i}: broken event schema or SHA predecessor")
        if e["kind"] not in ("OBSERVE","SEAL") or e["witness"] not in ("A","B","C") or not isinstance(e["actor_id"],str) or not e["actor_id"].isdigit():
            raise ValueError(f"Stochieon #{i}: invalid action or witness")
        utc(e["recorded_at"])
        if e["manifest_sha256"]!=fp or not HEX.fullmatch(e["loom_tip"]) or not HEX.fullmatch(e["corpus_tip"]):
            raise ValueError(f"Stochieon #{i}: unbound manifest or canonical source tips")
        if e["kind"]=="OBSERVE":
            if e["node_id"] not in nodes or e["coverage"] is not None or e["seal_root"] is not None or e["hallway_receipt"] is not None:
                raise ValueError(f"Stochieon #{i}: malformed endpoint observation")
            validate_observation(e["observation"],nodes[e["node_id"]])
        else:
            if e["node_id"] is not None or e["observation"] is not None:
                raise ValueError(f"Stochieon #{i}: SEAL cannot fabricate an endpoint measurement")
            expected=cover(old,nodes)
            if e["coverage"]!=expected or e["seal_root"]!=sha({"scope":"stochieon-v17","coverage":expected,"manifest":fp,"loom_tip":e["loom_tip"],"corpus_tip":e["corpus_tip"]}):
                raise ValueError(f"Stochieon #{i}: incomplete or substituted seal coverage")
            rec=e["hallway_receipt"]
            anchor=m["independent_anchor"]
            if not isinstance(rec,dict) or set(rec)!=RECEIPT_FIELDS or rec["receiver"]!=anchor["receiver_repository"] or rec["source_seq"]!=anchor["required_loom_seq"] or rec["source_hash"]!=anchor["required_loom_hash"] or not HEX.fullmatch(rec["receipt_sha256"]):
                raise ValueError(f"Stochieon #{i}: independent Hallway receipt missing")
            if any((utc(e["recorded_at"])-utc(old[n["observation_seq"]-1]["recorded_at"])).total_seconds()>86400
                    for n in expected):
                raise ValueError(f"Stochieon #{i}: observation expired before seal")
        body={k:v for k,v in e.items() if k not in ("watermark","hash")}
        if e["watermark"]!=watermark(body):
            raise ValueError(f"Stochieon #{i}: .dlw watermark changed")
        if e["hash"]!=sha({**body,"watermark":e["watermark"]}) or not HEX.fullmatch(e["hash"]):
            raise ValueError(f"Stochieon #{i}: SHA chain changed")
        old.append(e);prev=e["hash"]
    return prev

def read(path:Path=LEDGER,m:dict|None=None)->list[dict]:
    config=m or read_manifest()
    if not path.exists():return []
    raw=path.read_text(encoding="utf-8")
    if raw and not raw.endswith("\n"):raise ValueError("Truncated Stochieon JSONL")
    rows=[]
    for i,line in enumerate(raw.splitlines(),1):
        if not line:raise ValueError(f"Blank Stochieon line #{i}")
        rows.append(json.loads(line))
    verify(rows,config)
    return rows

class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self,req,fp,code,msg,headers,newurl):
        return None

def get_bytes(url:str,limit:int=LIMIT)->tuple[int,bytes|None,str|None]:
    request=urllib.request.Request(url,headers={"User-Agent":"ROOT0-Stochieon/17","Accept":"application/vnd.github+json"})
    opener=urllib.request.build_opener(NoRedirect())
    try:
        with opener.open(request,timeout=15) as r:
            raw=r.read(limit+1)
            return int(r.status),raw,r.headers.get("Date")
    except urllib.error.HTTPError as exc:
        return int(exc.code),None,exc.headers.get("Date")

def probe(n:dict)->dict:
    sent=iso(dt.datetime.now(dt.timezone.utc))
    tick=time.perf_counter_ns();remote_date=None
    code=0;content_hash=None;blob=None;result="UNAVAILABLE";transport="NETWORK_ERROR"
    try:
        if n["kind"]=="git_file":
            url=("https://api.github.com/repos/"+n["repo"]+"/contents/"
                 +urllib.parse.quote(n["path"],safe="/")+"?ref="+n["branch"])
            code,data,date=get_bytes(url)
            if data is not None and len(data)>LIMIT:result="TOO_LARGE"
            elif data is not None:
                record=json.loads(data)
                if isinstance(record,dict) and record.get("type")=="file":
                    blob=record.get("sha")
                    if record.get("encoding")=="base64" and isinstance(record.get("content"),str):
                        source_bytes=base64.b64decode(record["content"],validate=False)
                        if len(source_bytes)<=LIMIT:
                            content_hash=hashlib.sha256(source_bytes).hexdigest()
                            git_hash=hashlib.sha1(b"blob "+str(len(source_bytes)).encode()+b"\0"+source_bytes).hexdigest()
                            result="MATCH" if git_hash==blob==n["expected_git_blob"] else "MISMATCH"
                        else:result="TOO_LARGE"
                    else:result="UNAVAILABLE"
                else:result="UNAVAILABLE"
            remote_date=date;transport="HTTP_RESPONSE"
        else:
            code,data,date=get_bytes(n["url"])
            if data is not None:
                if len(data)>LIMIT:result="TOO_LARGE"
                elif code==200:
                    content_hash=hashlib.sha256(data).hexdigest()
                    result="MATCH"
            remote_date=date;transport="HTTP_RESPONSE"
    except (urllib.error.URLError,TimeoutError,OSError,ValueError,TypeError,KeyError):
        pass
    elapsed=round((time.perf_counter_ns()-tick)/1_000_000,3)
    received=iso(dt.datetime.now(dt.timezone.utc))
    date_iso=None
    if remote_date:
        try:date_iso=iso(email.utils.parsedate_to_datetime(remote_date))
        except (ValueError,TypeError,OverflowError):pass
    return {"transport":transport,"http_status":code,"sent_utc":sent,
        "received_utc":received,"monotonic_rtt_ms":elapsed,
        "date_header_utc":date_iso,"content_sha256":content_hash,
        "git_blob_sha":blob,"result":result,"time_quality":DATE_QUALITY}

def hallway_anchor(m:dict)->dict:
    """Fetch exact external receipt; 404/unavailable blocks sealing."""
    target=m["independent_anchor"]
    h=target["required_loom_hash"]
    url=("https://api.github.com/repos/DavidWise01/0root/contents/"
         "memory-bridge/loom/"+h+".json?ref=master")
    status,data,_=get_bytes(url,limit=300_000)
    if status!=200 or not data or len(data)>300_000:
        raise ValueError("Independent Hallway receipt absent/unavailable: cannot SEAL")
    wrapper=json.loads(data)
    if wrapper.get("encoding")!="base64" or not isinstance(wrapper.get("content"),str):
        raise ValueError("Hallway receipt bytes unavailable")
    raw=base64.b64decode(wrapper["content"])
    receipt=json.loads(raw)
    if receipt.get("schema")!="root0.loom-anchor/14" or receipt.get("receiver")!="DavidWise01/0root" or not isinstance(receipt.get("event"),dict) or receipt["event"].get("seq")!=target["required_loom_seq"] or receipt["event"].get("hash")!=h:
        raise ValueError("Untrusted Hallway receipt")
    return {"receiver":"DavidWise01/0root","source_seq":target["required_loom_seq"],
            "source_hash":h,"receipt_sha256":hashlib.sha256(raw).hexdigest()}

def make(rows:list[dict],m:dict,*,kind:str,witness:str,actor_id:str,loom_tip:str,
         corpus_tip:str,node_id:str|None=None,observation:dict|None=None,
         receipt:dict|None=None,recorded_at:str|None=None)->dict:
    verify(rows,m)
    if kind not in ("OBSERVE","SEAL"):raise ValueError("Unsupported Gate17 event type")
    config=manifest_check(m)
    if kind=="OBSERVE":
        coverage=None;root=None;receipt=None
        if node_id not in config or observation is None:raise ValueError("Select a real endpoint sample")
    else:
        node_id=None;observation=None
        coverage=cover(rows,config)
        root=sha({"scope":"stochieon-v17","coverage":coverage,"manifest":sha(m),
                  "loom_tip":loom_tip,"corpus_tip":corpus_tip})
        if receipt is None:raise ValueError("SEAL requires a verified independent Hallway receipt")
    body={"version":17,"seq":len(rows)+1,"kind":kind,
          "recorded_at":recorded_at or iso(dt.datetime.now(dt.timezone.utc)),
          "witness":witness,"actor_id":actor_id,"node_id":node_id,
          "manifest_sha256":sha(m),"loom_tip":loom_tip,"corpus_tip":corpus_tip,
          "observation":observation,"coverage":coverage,"seal_root":root,
          "hallway_receipt":receipt,"prev":rows[-1]["hash"] if rows else "GENESIS"}
    mark=watermark(body)
    event={**body,"watermark":mark,"hash":sha({**body,"watermark":mark})}
    verify([*rows,event],m)
    return event

def overview(rows:list[dict],m:dict)->dict:
    nodes=manifest_check(m)
    latest={e["node_id"]:e for e in rows if e["kind"]=="OBSERVE"}
    matched=[k for k,v in latest.items() if v["observation"]["result"]=="MATCH"]
    required=[k for k,v in nodes.items() if v["required"]]
    all_matched=all(k in matched for k in required)
    return {"schema":"root0.stochieon.status/17","name":"stochieon",
            "scope":"FULL_ARCHITECTURAL_ENVELOPE_NOT_EXHAUSTIVE_REPOSITORY_INVENTORY",
            "declared_nodes":len(nodes),"observed_nodes":len(latest),
            "matching_nodes":len(matched),"required_nodes":len(required),
            "required_coverage_complete":all_matched,"events":len(rows),
            "seals":sum(e["kind"]=="SEAL" for e in rows),
            "tip":rows[-1]["hash"] if rows else "GENESIS","manifest_sha256":sha(m),
            "watermark":".dlw","constant":"cubit",
            "independent_tsa_timestamp":"NOT_ATTESTED",
            "witness_votes":False,"quorum":None,"continuous_agent_execution":False}

def main(argv=None)->int:
    parser=argparse.ArgumentParser(description="ROOT0 STOCHIEON kernel public envelope")
    sub=parser.add_subparsers(dest="cmd",required=True)
    for cmd in ("verify","status","tip"):sub.add_parser(cmd)
    app=sub.add_parser("append")
    app.add_argument("--kind",choices=("OBSERVE","SEAL"),required=True)
    app.add_argument("--node-id")
    app.add_argument("--witness",choices=("A","B","C"),required=True)
    app.add_argument("--expect-tip",required=True)
    app.add_argument("--expect-loom-tip",required=True)
    app.add_argument("--expect-corpus-tip",required=True)
    args=parser.parse_args(argv)
    try:
        m=read_manifest();rows=read(m=m);tip=verify(rows,m)
        if args.cmd=="verify":print("PASS / stochieon events="+str(len(rows))+" / tip="+tip)
        elif args.cmd=="tip":print(tip)
        elif args.cmd=="status":print(json.dumps(overview(rows,m),indent=2))
        else:
            actor=witness_identity.authorize(args.witness,os.environ.get("GITHUB_ACTOR",""),
                os.environ.get("GITHUB_ACTOR_ID",""),"stochieon-append.yml")
            corpus=corpus_spine.read_rows()
            loom=threaded_loom.read(threaded_loom.LEDGER,corpus)
            if tip!=args.expect_tip or loom[-1]["hash"]!=args.expect_loom_tip or corpus[-1]["hash"]!=args.expect_corpus_tip:
                raise ValueError("Stochieon/global corpus/loom compare-and-swap tip changed")
            if args.kind=="OBSERVE":
                n=manifest_check(m).get(args.node_id)
                if n is None:raise ValueError("Not a declared public kernel endpoint")
                obs=probe(n)
                e=make(rows,m,kind="OBSERVE",witness=args.witness,
                    actor_id=actor["github_actor_id"],loom_tip=loom[-1]["hash"],
                    corpus_tip=corpus[-1]["hash"],node_id=n["id"],observation=obs)
            else:
                if args.node_id:raise ValueError("SEAL has no single endpoint")
                rec=hallway_anchor(m)
                e=make(rows,m,kind="SEAL",witness=args.witness,
                    actor_id=actor["github_actor_id"],loom_tip=loom[-1]["hash"],
                    corpus_tip=corpus[-1]["hash"],receipt=rec)
            if read(m=m)!=rows:raise ValueError("Concurrent Stochieon append detected")
            temporal_diode.write(LEDGER,e)
            verify(read(m=m),m)
            print("APPENDED LOCAL "+e["kind"]+" / seq="+str(e["seq"])+
                  " / watermark="+e["watermark"])
            print("No Git commit or external timestamp attestation is claimed until a successful push / separately verified TSA")
        return 0
    except (ValueError,TypeError,KeyError,OSError,json.JSONDecodeError,urllib.error.URLError) as exc:
        print("STOCHIEON HALTED: "+str(exc),file=sys.stderr);return 1

if __name__=="__main__":raise SystemExit(main())
