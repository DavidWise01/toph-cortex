#!/usr/bin/env python3
"""Gate 13 / ROOT0: referenced provenance watermarks and observed Internet delay.

Immutable WHAT/HOW/WHY ledger. Cryptographic hashes prove record integrity under
a trusted checkpoint, NOT authorship, article truth, or physical time dilation.
No internet probe occurs without an explicitly initiated authenticated append.
"""
from __future__ import annotations
import argparse
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
import witness_identity

ROOT=Path(__file__).resolve().parents[1]
LEDGER=ROOT/"memory"/"corpus-spine"/"referent-events.jsonl"
DOMAIN="ROOT0-WATERMARK-v1"
FIELDS={"version","seq","kind","recorded_at","witness","github_actor_id","referent_id",
        "referent_uri","basis","what","how","why","claimed_author","content_sha256",
        "source_seq","sample","prev","watermark","hash"}
KINDS=("REGISTER","SAMPLE","CORRECT")
BASES=("OBSERVED","REPORTED","INFERRED","DISPUTED","UNKNOWN")
HEX=re.compile(r"^[0-9a-f]{64}$")
URI_HOSTS={"www.scientificamerican.com","scientificamerican.com","tech.yahoo.com",
    "openai.com","www.openai.com","github.com","api.github.com",
    "raw.githubusercontent.com","davidwise01.github.io","0root.ai",
    "www.quantamagazine.org","www.claymath.org"}
SAMPLE_FIELDS={"sent_utc","received_utc","rtt_ms","http_status","server_date_utc","transport_result"}

def utc(s:str)->dt.datetime:
    if not isinstance(s,str) or not s.endswith("Z"):raise ValueError("UTC must end with Z")
    try:parsed=dt.datetime.fromisoformat(s.replace("Z","+00:00"))
    except ValueError as exc:raise ValueError("Invalid ISO UTC") from exc
    if parsed.utcoffset()!=dt.timedelta(0):raise ValueError("UTC offset required")
    return parsed

def fmt_utc(value:dt.datetime)->str:
    return value.astimezone(dt.timezone.utc).isoformat(timespec="milliseconds").replace("+00:00","Z")

def uri_ok(uri:str)->str:
    if not isinstance(uri,str) or not 1<=len(uri)<=1800:
        raise ValueError("Invalid referent URI length")
    parsed=urllib.parse.urlsplit(uri)
    if parsed.scheme!="https" or parsed.username or parsed.password or parsed.fragment:
        raise ValueError("Referent must be a canonical HTTPS URL with no credentials or fragment")
    if parsed.hostname not in URI_HOSTS or parsed.port not in (None,443):
        raise ValueError("Source host not on explicit public allowlist")
    if not parsed.path.startswith("/") and parsed.path!="":
        raise ValueError("Invalid URI path")
    if any(ord(ch)<32 for ch in uri):raise ValueError("Control character in source URL")
    return uri

def rid(uri:str)->str:
    return hashlib.sha256(uri_ok(uri).encode("utf-8")).hexdigest()

def mark(body:dict)->str:
    return hashlib.sha256((DOMAIN+"\n").encode("ascii")+corpus_spine.canonical(body)).hexdigest()

def validate_sample(sample:dict)->None:
    if not isinstance(sample,dict) or set(sample)!=SAMPLE_FIELDS:
        raise ValueError("Invalid network sample schema")
    sent=utc(sample["sent_utc"]);received=utc(sample["received_utc"])
    if received<sent:raise ValueError("Local receive time before send")
    rtt=sample["rtt_ms"]
    if type(rtt) not in (float,int) or not 0<=rtt<=120000:
        raise ValueError("Invalid monotonic RTT duration")
    if type(sample["http_status"]) is not int or sample["http_status"] not in range(0,600):
        raise ValueError("Invalid HTTP status (0 means no HTTP response)")
    if sample["transport_result"] not in ("HTTP_RESPONSE","NETWORK_ERROR"):
        raise ValueError("Unknown transport classification")
    if sample["transport_result"]=="NETWORK_ERROR" and sample["http_status"]!=0:
        raise ValueError("Network error cannot carry HTTP response code")
    if sample["transport_result"]=="HTTP_RESPONSE" and sample["http_status"]<100:
        raise ValueError("HTTP response code missing")
    if sample["server_date_utc"] is not None:utc(sample["server_date_utc"])
    # Date headers are server assertions, not externally verified synchronized clocks.

def verify(rows:list[dict])->str:
    prev="GENESIS";registered={}
    if not isinstance(rows,list):raise ValueError("Expected JSONL event list")
    for i,e in enumerate(rows,1):
        if not isinstance(e,dict) or set(e)!=FIELDS or e["version"]!=1 or type(e["seq"]) is not int or e["seq"]!=i or e["prev"]!=prev or e["kind"] not in KINDS:
            raise ValueError(f"Event {i}: broken chain or schema")
        utc(e["recorded_at"])
        if e["witness"] not in ("A","B","C") or not isinstance(e["github_actor_id"],str) or not e["github_actor_id"].isdigit():
            raise ValueError(f"Event {i}: witness identity missing")
        uri=uri_ok(e["referent_uri"])
        if e["referent_id"]!=rid(uri) or e["basis"] not in BASES:
            raise ValueError(f"Event {i}: referent or basis mismatch")
        for name in ("what","how","why"):
            if not isinstance(e[name],str) or not 1<=len(e[name])<=2000:
                raise ValueError(f"Event {i}: missing {name}")
        if e["claimed_author"] is not None and (not isinstance(e["claimed_author"],str) or len(e["claimed_author"])>200):
            raise ValueError(f"Event {i}: author attribution malformed")
        if e["content_sha256"] is not None and (not isinstance(e["content_sha256"],str) or not HEX.fullmatch(e["content_sha256"])):
            raise ValueError(f"Event {i}: content digest malformed")
        if e["kind"]=="REGISTER":
            if e["source_seq"] is not None or e["sample"] is not None or e["referent_id"] in registered:
                raise ValueError(f"Event {i}: duplicate/incomplete referent registration")
            registered[e["referent_id"]]=e
        else:
            parent=registered.get(e["referent_id"])
            if not parent or type(e["source_seq"]) is not int or e["source_seq"]!=parent["seq"] or uri!=parent["referent_uri"]:
                raise ValueError(f"Event {i}: source registration not found")
            if e["kind"]=="SAMPLE":
                validate_sample(e["sample"])
                if e["content_sha256"] is not None:raise ValueError("HEAD transport sample cannot claim article content digest")
            elif e["sample"] is not None:raise ValueError("Correction must not fabricate network sample")
        core={k:v for k,v in e.items() if k not in ("hash","watermark")}
        if e["watermark"]!=mark(core):
            raise ValueError(f"Event {i}: provenance watermark mismatch")
        plus={**core,"watermark":e["watermark"]}
        if e["hash"]!=corpus_spine.digest(plus):
            raise ValueError(f"Event {i}: SHA-256 mismatch")
        prev=e["hash"]
    return prev

def read(path:Path=LEDGER)->list[dict]:
    if not path.exists():return []
    raw=path.read_text(encoding="utf-8")
    if raw and not raw.endswith("\n"):raise ValueError("Truncated referent JSONL")
    result=[]
    for n,line in enumerate(raw.splitlines(),1):
        if not line:raise ValueError(f"Blank referent event {n}")
        try:result.append(json.loads(line))
        except json.JSONDecodeError as exc:raise ValueError(f"Invalid event JSON {n}") from exc
    verify(result);return result

def write(rows:list[dict],*,kind:str,witness:str,actor_id:str,uri:str,basis:str,
          what:str,how:str,why:str,author:str|None,content_sha:str|None,
          source_seq:int|None,sample:dict|None,observed_at:str|None=None)->dict:
    verify(rows)
    body={"version":1,"seq":len(rows)+1,"kind":kind,
          "recorded_at":observed_at or fmt_utc(dt.datetime.now(dt.timezone.utc)),
          "witness":witness,"github_actor_id":actor_id,
          "referent_id":rid(uri),"referent_uri":uri,"basis":basis,"what":what,
          "how":how,"why":why,"claimed_author":author,
          "content_sha256":content_sha,"source_seq":source_seq,"sample":sample,
          "prev":rows[-1]["hash"] if rows else "GENESIS"}
    m=mark(body);e={**body,"watermark":m,"hash":corpus_spine.digest({**body,"watermark":m})}
    verify([*rows,e]);return e

def probe(uri:str)->dict:
    uri_ok(uri)
    start=fmt_utc(dt.datetime.now(dt.timezone.utc))
    tick=time.perf_counter_ns()
    status=0;server_date=None;transport="NETWORK_ERROR"
    try:
        request=urllib.request.Request(uri,method="HEAD",headers={"User-Agent":"ROOT0-referent-delay/1"})
        class NoCrossHostRedirect(urllib.request.HTTPRedirectHandler):
            def redirect_request(self,req,fp,code,msg,headers,newurl):
                return None
        opener=urllib.request.build_opener(NoCrossHostRedirect())
        with opener.open(request,timeout=15) as resp:
            status=resp.status;date_hdr=resp.headers.get("Date");transport="HTTP_RESPONSE"
    except urllib.error.HTTPError as exc:
        status=exc.code;date_hdr=exc.headers.get("Date");transport="HTTP_RESPONSE"
    except (urllib.error.URLError,TimeoutError,OSError) as _:
        date_hdr=None
    duration=round((time.perf_counter_ns()-tick)/1e6,3)
    end=fmt_utc(dt.datetime.now(dt.timezone.utc))
    if date_hdr:
        try:server_date=fmt_utc(email.utils.parsedate_to_datetime(date_hdr))
        except (TypeError,ValueError,OverflowError):server_date=None
    return {"sent_utc":start,"received_utc":end,"rtt_ms":duration,
            "http_status":status,"server_date_utc":server_date,"transport_result":transport}

def main(argv=None)->int:
    p=argparse.ArgumentParser(description="Public referent integrity watermark and network RTT evidence")
    sub=p.add_subparsers(dest="cmd",required=True)
    for n in ("verify","tip","status"):sub.add_parser(n)
    a=sub.add_parser("append")
    a.add_argument("--kind",choices=KINDS,required=True)
    a.add_argument("--expect-tip",required=True)
    a.add_argument("--witness",choices=("A","B","C"),required=True)
    a.add_argument("--uri",required=True)
    a.add_argument("--basis",choices=BASES,required=True)
    a.add_argument("--what",required=True)
    a.add_argument("--how",required=True)
    a.add_argument("--why",required=True)
    a.add_argument("--claimed-author")
    a.add_argument("--content-sha256")
    a.add_argument("--source-seq",type=int)
    args=p.parse_args(argv)
    try:
        rows=read();tip=verify(rows)
        if args.cmd=="verify":print(f"PASS / events={len(rows)} / tip={tip}")
        elif args.cmd=="tip":print(tip)
        elif args.cmd=="status":print(json.dumps({"schema":"root0.referent-watermark/1",
            "events":len(rows),"tip":tip,"referents":len({x["referent_id"] for x in rows}),
            "time_samples":sum(x["kind"]=="SAMPLE" for x in rows),
            "no_quorum":True,"physical_time_dilation_measured":False},indent=2))
        else:
            actor=witness_identity.authorize(args.witness,os.environ.get("GITHUB_ACTOR",""),
                os.environ.get("GITHUB_ACTOR_ID",""),"referent-append.yml")
            if tip!=args.expect_tip:raise ValueError("Ledger compare-and-swap tip conflict")
            samp=probe(args.uri) if args.kind=="SAMPLE" else None
            event=write(rows,kind=args.kind,witness=args.witness,
                actor_id=actor["github_actor_id"],uri=args.uri,basis=args.basis,
                what=args.what,how=args.how,why=args.why,
                author=args.claimed_author,content_sha=args.content_sha256,
                source_seq=args.source_seq,sample=samp)
            if read()!=rows:raise ValueError("Concurrent referent append")
            temporal_diode.write(LEDGER,event)
            verify(read())
            print(f"APPENDED LOCAL / seq={event['seq']} / watermark={event['watermark']}")
            print("No remote Git persistence until commit/push.")
        return 0
    except (ValueError,TypeError,KeyError,OverflowError,OSError,urllib.error.URLError) as exc:
        print("HALTED: "+str(exc),file=sys.stderr);return 1

if __name__=="__main__":raise SystemExit(main())
