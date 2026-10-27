#!/usr/bin/env python3
"""ROOT0 Temporal Diode v1 — append-only three independent witness lanes.
PAST observes -> PRESENT deserves -> FUTURE reserves.
No votes, quorums, merged decisions, backward transitions, or scheduled executions.
"""
from __future__ import annotations
import argparse
import datetime as dt
import json
import os
from pathlib import Path
import re
import sys
import corpus_spine

ROOT=Path(__file__).resolve().parents[1]
LEDGER=ROOT/"memory"/"corpus-spine"/"temporal-events.jsonl"
CANONICAL=ROOT/"memory"/"corpus-spine"/"events-v2.jsonl"
FIELDS={"version","seq","recorded_at","thread","witness","phase","event_on",
        "source","corpus_tip","what","how","why","anchor","prev","hash"}
THREAD=re.compile(r"^[a-zA-Z0-9][a-zA-Z0-9_.-]{0,95}$")
DIGEST=re.compile(r"^[0-9a-f]{64}$")
PHASES=("PAST_OBSERVES","PRESENT_DESERVES","FUTURE_RESERVES")
WITNESSES=("A","B","C")

def to_date(value: str)->dt.date:
    if not isinstance(value,str):
        raise ValueError("Invalid ISO calendar date")
    try: return dt.date.fromisoformat(value)
    except ValueError as e: raise ValueError("Invalid ISO calendar date") from e

def corpus_heads(corpus: list[dict])->set[str]:
    corpus_spine.verify_rows(corpus)
    return {e["hash"] for e in corpus}

def verify_rows(rows: list[dict], corpus: list[dict]) -> str:
    if not isinstance(rows,list): raise ValueError("Temporal ledger is not an array")
    valid_heads=corpus_heads(corpus)
    if not valid_heads: raise ValueError("Canonical corpus ledger must have a verified genesis")
    prev="GENESIS"
    lanes:dict[tuple[str,str],dict]={}
    for index,e in enumerate(rows,1):
        if not isinstance(e,dict) or set(e)!=FIELDS: raise ValueError(f"Event {index}: invalid schema")
        if e["version"]!=1 or type(e["seq"]) is not int or e["seq"]!=index or e["prev"]!=prev:
            raise ValueError(f"Event {index}: global chain/sequence failure")
        if e["phase"] not in PHASES or e["witness"] not in WITNESSES:
            raise ValueError(f"Event {index}: invalid witness or phase")
        if not isinstance(e["thread"],str) or not THREAD.fullmatch(e["thread"]):
            raise ValueError(f"Event {index}: invalid thread")
        corpus_spine.validate_source(e["source"])
        if e["corpus_tip"] not in valid_heads: raise ValueError(f"Event {index}: unknown verified corpus anchor")
        recorded=to_date(e["recorded_at"])
        target=to_date(e["event_on"])
        for field in ("what","how","why"):
            v=e[field]
            if not isinstance(v,str) or not 1<=len(v)<=2000:
                raise ValueError(f"Event {index}: invalid {field}")
        key=(e["thread"],e["witness"])
        last=lanes.get(key)
        phase_idx=PHASES.index(e["phase"])
        if not last:
            if phase_idx!=0 or e["anchor"] is not None:
                raise ValueError(f"Event {index}: independent lane must begin in PAST without a prior anchor")
        else:
            if type(e["anchor"]) is not int or e["anchor"]!=last["seq"]:
                raise ValueError(f"Event {index}: missing or wrong predecessor in witness lane")
            former=PHASES.index(last["phase"])
            if phase_idx<former or phase_idx>former+1:
                raise ValueError(f"Event {index}: diode forbids backward jumps or skipped phases")
        if phase_idx==0 and target>recorded:
            raise ValueError(f"Event {index}: past observation must not refer to future event date")
        if phase_idx==1 and target!=recorded:
            raise ValueError(f"Event {index}: present deserves is dated today")
        if phase_idx==2 and target<=recorded:
            raise ValueError(f"Event {index}: future reservation must carry a future date")
        # A reservation records intent; it never triggers action when its date arrives.
        if not isinstance(e["hash"],str) or not DIGEST.fullmatch(e["hash"]):
            raise ValueError(f"Event {index}: invalid SHA-256")
        body={k:v for k,v in e.items() if k!="hash"}
        if corpus_spine.digest(body)!=e["hash"]:
            raise ValueError(f"Event {index}: SHA-256 mismatch")
        prev=e["hash"];lanes[key]=e
    return prev

def read_rows(path: Path, corpus: list[dict])->list[dict]:
    if not path.exists(): return []
    txt=path.read_text(encoding="utf-8")
    if txt and not txt.endswith("\n"): raise ValueError("Truncated temporal JSONL")
    rows=[]
    for i,line in enumerate(txt.splitlines(),1):
        if not line: raise ValueError(f"Blank temporal line {i}")
        try: rows.append(json.loads(line))
        except json.JSONDecodeError as exc: raise ValueError(f"Malformed temporal JSON line {i}") from exc
    verify_rows(rows,corpus)
    return rows

def append(rows:list[dict],corpus:list[dict],*,thread:str,witness:str,phase:str,event_on:str,
           source:dict,what:str,how:str,why:str,recorded_at:str|None=None)->dict:
    verify_rows(rows,corpus)
    recorded=recorded_at or dt.datetime.now(dt.timezone.utc).date().isoformat()
    previous=next((e for e in reversed(rows) if e["thread"]==thread and e["witness"]==witness),None)
    body={"version":1,"seq":len(rows)+1,"recorded_at":recorded,"thread":thread,
          "witness":witness,"phase":phase,"event_on":event_on,
          "source":source,"corpus_tip":corpus[-1]["hash"],
          "what":what,"how":how,"why":why,"anchor":previous["seq"] if previous else None,
          "prev":rows[-1]["hash"] if rows else "GENESIS"}
    event={**body,"hash":corpus_spine.digest(body)}
    verify_rows([*rows,event],corpus)
    return event

def write(path:Path,record:dict)->None:
    path.parent.mkdir(parents=True,exist_ok=True)
    fd=os.open(str(path),os.O_WRONLY|os.O_APPEND|os.O_CREAT,0o644)
    with os.fdopen(fd,"a",encoding="utf-8",newline="\n") as f:
        f.write(json.dumps(record,ensure_ascii=False,separators=(",",":"))+"\n")
        f.flush();os.fsync(f.fileno())

def summary(rows:list[dict])->dict:
    lanes={}
    for e in rows:
        lane=lanes.setdefault(e["thread"],{})
        lane[e["witness"]]={"phase":e["phase"],"last_seq":e["seq"],
                            "event_on":e["event_on"]}
    return {"schema":"root0.temporal-diode/1","events":len(rows),
            "tip":rows[-1]["hash"] if rows else "GENESIS","witness_lanes":lanes,
            "quorum":None,"voting":False,"auto_execution":False}

def main(argv=None)->int:
    p=argparse.ArgumentParser(description="Independent A/B/C temporal witness append-only diode")
    p.add_argument("--ledger",type=Path,default=LEDGER)
    p.add_argument("--corpus",type=Path,default=CANONICAL)
    sub=p.add_subparsers(dest="command",required=True)
    for n in ("verify","tip","status"):sub.add_parser(n)
    a=sub.add_parser("append")
    a.add_argument("--expect-tip",required=True)
    a.add_argument("--expect-corpus-tip",required=True)
    a.add_argument("--thread",required=True)
    a.add_argument("--witness",choices=WITNESSES,required=True)
    a.add_argument("--phase",choices=PHASES,required=True)
    a.add_argument("--event-on",required=True)
    a.add_argument("--source-repo",required=True)
    a.add_argument("--source-path",required=True)
    a.add_argument("--source-sha",required=True)
    for field in ("what","how","why"):a.add_argument("--"+field,required=True)
    a.add_argument("--verify-public-source",action="store_true")
    args=p.parse_args(argv)
    try:
        corpus=corpus_spine.read_rows(args.corpus)
        rows=read_rows(args.ledger,corpus)
        tip=verify_rows(rows,corpus)
        if args.command=="verify": print(f"PASS | entries={len(rows)} | tip={tip}")
        elif args.command=="tip":print(tip)
        elif args.command=="status":print(json.dumps(summary(rows),indent=2))
        elif args.command=="append":
            if tip!=args.expect_tip:raise ValueError("Temporal CAS tip mismatch")
            if corpus[-1]["hash"]!=args.expect_corpus_tip:raise ValueError("Corpus CAS tip mismatch")
            source={"repo":args.source_repo,"path":args.source_path,
                    "blob_sha":args.source_sha,"visibility":"public"}
            corpus_spine.validate_source(source)
            if args.verify_public_source:corpus_spine.verify_public_file(source)
            row=append(rows,corpus,thread=args.thread,witness=args.witness,phase=args.phase,
                       event_on=args.event_on,source=source,what=args.what,how=args.how,why=args.why)
            # Recheck local file/tip immediately before writing; git push is a second concurrency gate.
            if verify_rows(read_rows(args.ledger,corpus),corpus)!=tip:
                raise ValueError("Temporal ledger changed before append")
            write(args.ledger,row)
            verify_rows(read_rows(args.ledger,corpus),corpus)
            print(f"APPENDED LOCAL | witness={args.witness} | phase={args.phase} | seq={row['seq']} | hash={row['hash']}")
            print("Commit and push (without force) to make this Git-persistent.")
        return 0
    except (ValueError,OSError) as e:
        print("HALTED: "+str(e),file=sys.stderr);return 1

if __name__=="__main__":raise SystemExit(main())
