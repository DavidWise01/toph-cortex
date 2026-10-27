#!/usr/bin/env python3
"""Gate 14: prepare, never impersonate, the next authenticated loom witness turn.

Read-only. Derives a causal continuation from committed TOPH memory.
No recorded witness statement is synthesized, signed, or appended.
"""
from __future__ import annotations
import argparse
import datetime as dt
import json
from pathlib import Path
import sys

import corpus_spine
import threaded_loom
import witness_identity

SCHEMA="root0.threaded-loom-continuation/1"
UTC=dt.timezone.utc

def utc_instant(value:str)->dt.datetime:
    parsed=threaded_loom.recorded(value)
    return parsed.astimezone(UTC)

def prepare(rows:list[dict],corpus:list[dict],thread:str,witness:str,as_of:str)->dict:
    """Generate deterministic, tamper-checked workflow inputs, never evidence."""
    threaded_loom.verify(rows,corpus)
    if not threaded_loom.THREAD.fullmatch(thread):
        raise ValueError("Invalid exact thread ID; preserve the existing name")
    if witness not in ("A","B","C"):
        raise ValueError("Unknown witness lane")
    registry=witness_identity.read_registry()
    bound=registry["lanes"][witness]
    if bound["state"]!="BOUND":
        raise ValueError(f"Witness {witness} is unassigned; do not impersonate")
    t=utc_instant(as_of)
    history=[event for event in rows if event["thread"]==thread]
    if not history or history[0]["kind"]!="OPEN":
        raise ValueError(f"Thread {thread} has no authenticated OPEN")
    lane=[event for event in history if event["witness"]==witness]
    latest=lane[-1] if lane else None
    if latest and latest["kind"]=="CLOSE":
        raise ValueError(f"Thread {thread} / witness {witness} is CLOSED")
    if latest and latest["phase"]=="FUTURE_RESERVES":
        raise ValueError("This witness is in FUTURE_RESERVES: explicit future date required; never invent one")
    # An observing witness can advance to PRESENT without a vote. A new
    # witness on a known thread must begin with its own PAST observation.
    phase=("PRESENT_DESERVES" if latest is not None else "PAST_OBSERVES")
    date=threaded_loom.resolve_event_on(phase,"auto",as_of)
    head=history[-1]
    return {
        "schema":SCHEMA,
        "status":"READY_FOR_AUTHENTICATED_HUMAN_DISPATCH",
        "operation":"WEAVE",
        "thread":thread,
        "witness":witness,
        "witness_account":bound["github_login"],
        "phase":phase,
        "event_on":date,
        "recorded_plan_at":as_of,
        "source_global_tip":rows[-1]["hash"] if rows else "GENESIS",
        "source_thread_head_seq":head["seq"],
        "source_thread_head_hash":head["hash"],
        "source_lane_head_seq":latest["seq"] if latest else None,
        "source_lane_head_hash":latest["hash"] if latest else None,
        "corpus_tip":corpus[-1]["hash"],
        "content_constant":"cubit",
        "provenance":".dlw",
        "requires_witness_supplied":["what","how","why","content"],
        "witness_statement_provided":False,
        "may_commit_without_authentication":False,
        "no_quorum":True,
        "votes":False,
        "manual_workflow":"https://github.com/DavidWise01/toph-cortex/actions/workflows/loom-append.yml"
    }

def summarize(rows:list[dict],corpus:list[dict],as_of:str)->dict:
    threaded_loom.verify(rows,corpus)
    threads={}
    for event in rows:
        lane=threads.setdefault(event["thread"],{
            "head_seq":event["seq"],"head_hash":event["hash"],"events":0,"witnesses":{}
        })
        lane["head_seq"]=event["seq"];lane["head_hash"]=event["hash"]
        lane["events"]+=1
        lane["witnesses"][event["witness"]]={
            "phase":event["phase"],"seq":event["seq"],"closed":event["kind"]=="CLOSE"
        }
    return {"schema":SCHEMA,"as_of":as_of,"threads":threads,
            "global_tip":rows[-1]["hash"] if rows else "GENESIS",
            "no_quorum":True,"has_synthetic_witness_events":False}

def main(argv=None)->int:
    p=argparse.ArgumentParser(description="Read-only authenticated loom continuation plan")
    sub=p.add_subparsers(dest="command",required=True)
    sub.add_parser("status")
    a=sub.add_parser("prepare")
    a.add_argument("--thread",required=True)
    a.add_argument("--witness",required=True,choices=("A","B","C"))
    for x in (a,):
        x.add_argument("--as-of",help="UTC ISO Z instant for deterministic offline tests; defaults to current UTC")
    args=p.parse_args(argv)
    try:
        corpus=corpus_spine.read_rows()
        rows=threaded_loom.read(threaded_loom.LEDGER,corpus)
        as_of=getattr(args,"as_of",None) or threaded_loom.stamp()
        if args.command=="status":
            result=summarize(rows,corpus,as_of)
        else:
            result=prepare(rows,corpus,args.thread,args.witness,as_of)
        print(json.dumps(result,sort_keys=True,ensure_ascii=False,indent=2))
        return 0
    except (ValueError,OSError,KeyError,TypeError,json.JSONDecodeError) as e:
        print("NEXT LOOM HALTED: "+str(e),file=sys.stderr)
        return 1

if __name__=="__main__":
    raise SystemExit(main())
