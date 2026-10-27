#!/usr/bin/env python3
"""Gate 14 / ROOT0 Threaded Persistent Loom.

Independent A/B/C lanes share a causal threaded graph without voting. A single
append-only global SHA chain also has per-thread and per-witness predecessors.
Cross-repository source pointers are public Git blob SHAs, never copied secrets.
COPY and DISTILL preserve exact lowercase 'cubit'; .dlw marks record provenance.
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
import urllib.error
import urllib.parse
import urllib.request

import corpus_spine
import cubit_constant
import temporal_diode
import witness_identity

ROOT=Path(__file__).resolve().parents[1]
LEDGER=ROOT/"memory"/"corpus-spine"/"loom-events.jsonl"
DOMAIN="ROOT0-THREADED-LOOM-v1\n"
VERSION=14
KINDS=("OPEN","WEAVE","LINK","COPY","DISTILL","CHECKPOINT","CLOSE")
PHASES=("PAST_OBSERVES","PRESENT_DESERVES","FUTURE_RESERVES")
THREAD=re.compile(r"^[a-z0-9][a-z0-9._-]{0,63}$")
HEX=re.compile(r"^[a-f0-9]{64}$")
FIELDS={"version","seq","kind","recorded_at","event_on","thread","witness","phase",
        "what","how","why","text","refs","source","corpus_tip","thread_prev",
        "witness_prev","mode","prev","watermark","hash"}
MAX_TEXT=6000
MAX_REFS=16

def day(value:str)->dt.date:
    if not isinstance(value,str):raise ValueError("Invalid ISO calendar date")
    return dt.date.fromisoformat(value)

def recorded(value:str)->dt.datetime:
    if not isinstance(value,str) or not value.endswith("Z"):raise ValueError("Record timestamp must be UTC Z")
    timestamp=dt.datetime.fromisoformat(value.replace("Z","+00:00"))
    if timestamp.utcoffset()!=dt.timedelta(0):raise ValueError("UTC timestamp required")
    return timestamp

def stamp()->str:
    return dt.datetime.now(dt.timezone.utc).isoformat(timespec="milliseconds").replace("+00:00","Z")

def temporal_boundary(phase:str,event_on:str,recorded_at:str)->dt.date:
    """Validate a meaningful subject date against the single recorded UTC instant.

    PAST allows the current UTC calendar date (as well as earlier dates);
    FUTURE cannot be inferred or silently scheduled.
    """
    if phase not in PHASES:raise ValueError(f"Unknown temporal phase: {phase}")
    now=recorded(recorded_at).date()
    when=day(event_on)
    allowed=(when<=now if phase=="PAST_OBSERVES" else
             when==now if phase=="PRESENT_DESERVES" else when>now)
    if not allowed:
        relation=("<=" if phase=="PAST_OBSERVES" else "==" if phase=="PRESENT_DESERVES" else ">")
        raise ValueError(
            f"Temporal boundary violated: phase={phase}, event_on={when.isoformat()}, "
            f"recorded_utc_date={now.isoformat()}; expected event_on {relation} "
            f"recorded_utc_date. For a new OPEN use --event-on auto, or supply a "
            f"historically valid explicit date. Explicit dates are never rewritten."
        )
    return when

def resolve_event_on(phase:str,requested:str,recorded_at:str)->str:
    """Resolve AUTO once; bind it and recorded_at to the same UTC clock instant."""
    if requested is None or not isinstance(requested,str):
        raise ValueError("event_on must be an ISO date or auto")
    supplied=requested.strip()
    if supplied.lower()=="auto":
        if phase=="FUTURE_RESERVES":
            raise ValueError("FUTURE_RESERVES requires an explicit future date; auto cannot reserve it")
        supplied=recorded(recorded_at).date().isoformat()
    return temporal_boundary(phase,supplied,recorded_at).isoformat()

def mark(body:dict)->str:
    return ".dlw:"+hashlib.sha256(DOMAIN.encode("ascii")+corpus_spine.canonical(body)).hexdigest()

def verify(rows:list[dict],corpus:list[dict])->str:
    corpus_spine.verify_rows(corpus)
    heads={e["hash"] for e in corpus}
    if not heads:raise ValueError("Verified v2 corpus anchor required")
    if not isinstance(rows,list):raise ValueError("Expected loom event array")
    prev="GENESIS";threads={};lanes={}
    for idx,e in enumerate(rows,1):
        if not isinstance(e,dict) or set(e)!=FIELDS or e["version"]!=VERSION or type(e["seq"]) is not int or e["seq"]!=idx or e["prev"]!=prev:
            raise ValueError(f"Loom #{idx}: schema or global SHA predecessor invalid")
        if e["kind"] not in KINDS or e["witness"] not in ("A","B","C") or e["phase"] not in PHASES:
            raise ValueError(f"Loom #{idx}: unknown operation, witness or phase")
        if not isinstance(e["thread"],str) or not THREAD.fullmatch(e["thread"]):
            raise ValueError(f"Loom #{idx}: invalid thread ID")
        try:
            temporal_boundary(e["phase"],e["event_on"],e["recorded_at"])
        except ValueError as exc:
            raise ValueError(f"Loom #{idx}: {exc}") from exc
        position=PHASES.index(e["phase"])
        if e["corpus_tip"] not in heads:raise ValueError(f"Loom #{idx}: unverified corpus anchor")
        if e["source"] is not None:corpus_spine.validate_source(e["source"])
        for field in ("what","how","why"):
            if not isinstance(e[field],str) or not 1<=len(e[field])<=1600:
                raise ValueError(f"Loom #{idx}: missing bounded WHAT/HOW/WHY")
        if not isinstance(e["text"],str) or len(e["text"])>MAX_TEXT:
            raise ValueError(f"Loom #{idx}: content size exceeds public metadata boundary")
        if not isinstance(e["refs"],list) or len(e["refs"])>MAX_REFS or any(type(r) is not int or r<1 or r>=idx for r in e["refs"]) or sorted(set(e["refs"]))!=e["refs"]:
            raise ValueError(f"Loom #{idx}: references not unique, sorted, causal or bounded")
        thread=e["thread"]
        current=threads.get(thread)
        lane=(thread,e["witness"])
        earlier=lanes.get(lane)
        if e["kind"]=="OPEN":
            if current is not None or e["refs"] or e["thread_prev"] is not None or e["witness_prev"] is not None or e["phase"]!="PAST_OBSERVES":
                raise ValueError(f"Loom #{idx}: thread already open or genesis malformed")
        else:
            if current is None or e["thread_prev"]!=current["seq"]:
                raise ValueError(f"Loom #{idx}: missing or incorrect thread predecessor")
            if e["witness_prev"]!=(earlier["seq"] if earlier else None):
                raise ValueError(f"Loom #{idx}: incorrect independent witness predecessor")
            if earlier and earlier["kind"]=="CLOSE":
                raise ValueError(f"Loom #{idx}: closed witness lane cannot append")
            if earlier:
                last=PHASES.index(earlier["phase"])
                if position<last or position>last+1:
                    raise ValueError(f"Loom #{idx}: witness phase reverses or skips")
            elif position!=0:
                raise ValueError(f"Loom #{idx}: witness must first observe PAST")
        if e["kind"] in ("COPY","DISTILL"):
            if e["mode"]!=e["kind"].lower() or not e["refs"]:
                raise ValueError(f"Loom #{idx}: transformed content requires source refs and mode")
            original="\n".join(rows[r-1]["text"] for r in e["refs"])
            try:cubit_constant.verify(original,e["text"],e["mode"])
            except cubit_constant.CubitContractError as exc:
                raise ValueError(f"Loom #{idx}: cubit constant violation: {exc}") from exc
        elif e["mode"] is not None:raise ValueError(f"Loom #{idx}: non-transform operation has mode")
        if e["kind"]=="LINK" and (not e["refs"] or not any(rows[r-1]["thread"]!=thread for r in e["refs"])):
            raise ValueError(f"Loom #{idx}: LINK requires a real earlier cross-thread reference")
        if e["kind"]=="CLOSE" and not earlier:
            raise ValueError(f"Loom #{idx}: cannot close a lane with no observation")
        core={k:v for k,v in e.items() if k not in ("watermark","hash")}
        if e["watermark"]!=mark(core):raise ValueError(f"Loom #{idx}: .dlw watermark changed")
        with_mark={**core,"watermark":e["watermark"]}
        if e["hash"]!=corpus_spine.digest(with_mark) or not HEX.fullmatch(e["hash"]):
            raise ValueError(f"Loom #{idx}: SHA chain changed")
        prev=e["hash"];threads[thread]=e;lanes[lane]=e
    return prev

def read(path:Path,corpus:list[dict])->list[dict]:
    if not path.exists():return []
    raw=path.read_text(encoding="utf-8")
    if raw and not raw.endswith("\n"):raise ValueError("Truncated loom JSONL")
    out=[]
    for idx,line in enumerate(raw.splitlines(),1):
        if not line:raise ValueError(f"Blank loom event line {idx}")
        try:out.append(json.loads(line))
        except json.JSONDecodeError as exc:raise ValueError(f"Invalid loom JSONL line {idx}") from exc
    verify(out,corpus);return out

def make(rows:list[dict],corpus:list[dict],*,kind:str,thread:str,witness:str,phase:str,
         event_on:str,what:str,how:str,why:str,text:str="",refs:list[int]|None=None,
         source:dict|None=None,recorded_at:str|None=None)->dict:
    verify(rows,corpus)
    if kind not in KINDS:raise ValueError("Unsupported loom operation")
    same=[r for r in rows if r["thread"]==thread]
    mine=[r for r in same if r["witness"]==witness]
    body={"version":VERSION,"seq":len(rows)+1,"kind":kind,"recorded_at":recorded_at or stamp(),
          "event_on":event_on,"thread":thread,"witness":witness,"phase":phase,
          "what":what,"how":how,"why":why,"text":text,"refs":refs if refs is not None else [],
          "source":source,"corpus_tip":corpus[-1]["hash"],
          "thread_prev":same[-1]["seq"] if same and kind!="OPEN" else None,
          "witness_prev":mine[-1]["seq"] if mine and kind!="OPEN" else None,
          "mode":kind.lower() if kind in ("COPY","DISTILL") else None,
          "prev":rows[-1]["hash"] if rows else "GENESIS"}
    watermark=mark(body)
    event={**body,"watermark":watermark,"hash":corpus_spine.digest({**body,"watermark":watermark})}
    verify([*rows,event],corpus)
    return event

def verify_remote_blob(source:dict)->None:
    """Check a public source's actual Git blob before accepting a new weave."""
    corpus_spine.validate_source(source)
    repo,path=source["repo"],source["path"]
    url="https://api.github.com/repos/"+repo+"/contents/"+urllib.parse.quote(path,safe="/")
    req=urllib.request.Request(url,headers={"Accept":"application/vnd.github+json",
                                            "User-Agent":"ROOT0-threaded-loom/1"})
    with urllib.request.urlopen(req,timeout=20) as resp:doc=json.load(resp)
    if not isinstance(doc,dict) or doc.get("type")!="file" or doc.get("sha")!=source["blob_sha"] or doc.get("size",0)>2_000_000:
        raise ValueError("Remote public Git source blob mismatch or oversized")
    # The blob SHA validates pointer identity at observation time only; subsequent
    # changes are new references, never rewritten source evidence.

def status(rows:list[dict])->dict:
    by_thread={};lanes={}
    for e in rows:
        obj=by_thread.setdefault(e["thread"],{"first":e["seq"],"last":e["seq"],"events":0,"witnesses":{}})
        obj["last"]=e["seq"];obj["events"]+=1
        obj["witnesses"][e["witness"]]={"phase":e["phase"],"last":e["seq"],
            "closed":e["kind"]=="CLOSE"}
    return {"schema":"root0.threaded-loom/14","threads":by_thread,"events":len(rows),
            "tip":rows[-1]["hash"] if rows else "GENESIS","watermark":".dlw",
            "constant":"cubit","quorum":None,"votes":False,"automatic_execution":False}

def cli(argv=None)->int:
    p=argparse.ArgumentParser(description="Append-only three-witness, causal ROOT0 threaded memory loom")
    subs=p.add_subparsers(dest="cmd",required=True)
    for name in ("verify","status","tip"):subs.add_parser(name)
    a=subs.add_parser("append")
    a.add_argument("--kind",choices=KINDS,required=True)
    a.add_argument("--thread",required=True)
    a.add_argument("--witness",choices=("A","B","C"),required=True)
    a.add_argument("--phase",choices=PHASES,required=True)
    a.add_argument("--event-on",default="auto",help="ISO date, or auto for PAST/PRESENT bound once to the runner UTC clock")
    for field in ("what","how","why"):a.add_argument("--"+field,required=True)
    a.add_argument("--text",default="")
    a.add_argument("--refs",default="",help="Comma-separated earlier event numbers")
    a.add_argument("--source-repo")
    a.add_argument("--source-path")
    a.add_argument("--source-blob")
    a.add_argument("--expect-tip",required=True)
    a.add_argument("--expect-corpus-tip",required=True)
    args=p.parse_args(argv)
    try:
        corpus=corpus_spine.read_rows()
        rows=read(LEDGER,corpus);tip=verify(rows,corpus)
        if args.cmd=="verify":print(f"PASS / events={len(rows)} / tip={tip}")
        elif args.cmd=="tip":print(tip)
        elif args.cmd=="status":print(json.dumps(status(rows),indent=2))
        else:
            actor=witness_identity.authorize(args.witness,os.environ.get("GITHUB_ACTOR",""),
                    os.environ.get("GITHUB_ACTOR_ID",""),"loom-append.yml")
            if args.expect_tip!=tip or args.expect_corpus_tip!=corpus[-1]["hash"]:
                raise ValueError("Loom or corpus compare-and-swap tip mismatch")
            pieces=[x for x in args.refs.split(",") if x]
            if any(not re.fullmatch(r"[1-9][0-9]*",x) for x in pieces):
                raise ValueError("Loom refs must be positive integer IDs")
            refs=[int(x) for x in pieces]
            source_parts=(args.source_repo,args.source_path,args.source_blob)
            if any(source_parts):
                if not all(source_parts):raise ValueError("Source requires repo, path and blob SHA")
                source={"repo":args.source_repo,"path":args.source_path,
                        "blob_sha":args.source_blob,"visibility":"public"}
                verify_remote_blob(source)
            else:source=None
            observed_at=stamp()
            bound_date=resolve_event_on(args.phase,args.event_on,observed_at)
            print(f"TEMPORAL INPUT / phase={args.phase} / requested={args.event_on} "
                  f"/ resolved={bound_date} / recorded_at={observed_at}",flush=True)
            event=make(rows,corpus,kind=args.kind,thread=args.thread,witness=actor["witness"],
                       phase=args.phase,event_on=bound_date,what=args.what,how=args.how,
                       why=args.why,text=args.text,refs=refs,source=source,recorded_at=observed_at)
            if read(LEDGER,corpus)!=rows:raise ValueError("Loom changed before appending")
            temporal_diode.write(LEDGER,event)
            verify(read(LEDGER,corpus),corpus)
            print(f"APPENDED LOCAL / thread={event['thread']} / seq={event['seq']} / {event['watermark']}")
            print("Git commit/push still required; nothing was executed in another repo.")
        return 0
    except (ValueError,KeyError,OSError,TypeError,json.JSONDecodeError,urllib.error.URLError) as exc:
        print("LOOM HALTED: "+str(exc),file=sys.stderr);return 1

if __name__=="__main__":raise SystemExit(cli())
