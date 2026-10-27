#!/usr/bin/env python3
"""ROOT0 / TOPH CORTEX corpus-spine: deterministic append-only provenance.
Public metadata and references only. Run from a trusted local checkout or GitHub Action.
No network requests on reads. Existing TOPH memory/ledger.jsonl is unchanged.
"""
from __future__ import annotations
import argparse
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

ROOT = Path(__file__).resolve().parent.parent
LEDGER = ROOT / "memory" / "corpus-spine" / "events.jsonl"
FIELDS = {"version","seq","recorded_at","actor","kind","source","what","how","why","supersedes","prev","hash"}
SRC_FIELDS = {"repo","path","blob_sha","visibility"}
HEX64 = re.compile(r"^[0-9a-f]{64}$")
HEX40 = re.compile(r"^[0-9a-f]{40}$")
REPO = re.compile(r"^DavidWise01/[A-Za-z0-9._-]+$")
ACTOR = re.compile(r"^[A-Za-z0-9._-]{1,60}$")
KINDS = {"ANCHOR","OBSERVATION","CORRECTION"}

def canonical(item: dict) -> bytes:
    return json.dumps(item, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")

def digest(item: dict) -> str:
    return hashlib.sha256(canonical(item)).hexdigest()

def validate_source(source: dict) -> None:
    if not isinstance(source, dict) or set(source) != SRC_FIELDS:
        raise ValueError("source fields are invalid")
    if not REPO.fullmatch(source["repo"]):
        raise ValueError("source repo must be owned by DavidWise01")
    path = source["path"]
    if not isinstance(path, str) or not (1 <= len(path) <= 350):
        raise ValueError("invalid source path")
    if path.startswith("/") or "\\" in path or any(p in ("", ".", "..") for p in path.split("/")):
        raise ValueError("source path must be relative and normalized")
    if not HEX40.fullmatch(source["blob_sha"]):
        raise ValueError("source blob SHA must be 40 lowercase hex digits")
    if source["visibility"] != "public":
        raise ValueError("public spine may never contain private source metadata")

def verify_rows(rows: list[dict]) -> str:
    prev = "GENESIS"
    for index, item in enumerate(rows, 1):
        if not isinstance(item, dict) or set(item) != FIELDS:
            raise ValueError(f"row {index}: unexpected fields")
        if item["version"] != 1 or item["seq"] != index or item["prev"] != prev:
            raise ValueError(f"row {index}: broken sequence or previous link")
        if not isinstance(item["recorded_at"], str):
            raise ValueError(f"row {index}: invalid date")
        try:
            dt.date.fromisoformat(item["recorded_at"])
        except ValueError as exc:
            raise ValueError(f"row {index}: invalid date") from exc
        if not isinstance(item["actor"], str) or not ACTOR.fullmatch(item["actor"]):
            raise ValueError(f"row {index}: invalid actor")
        if item["kind"] not in KINDS:
            raise ValueError(f"row {index}: invalid kind")
        validate_source(item["source"])
        for field in ("what","how","why"):
            value = item[field]
            if not isinstance(value, str) or not 1 <= len(value) <= 2000:
                raise ValueError(f"row {index}: invalid {field}")
        sup = item["supersedes"]
        if item["kind"] == "CORRECTION":
            if type(sup) is not int or not 1 <= sup < index:
                raise ValueError(f"row {index}: correction must reference older event")
            former = rows[sup - 1]
            if former["source"]["repo"] != item["source"]["repo"]:
                raise ValueError(f"row {index}: correction must refer to same repository")
        elif sup is not None:
            raise ValueError(f"row {index}: non-correction cannot supersede")
        hash_value = item["hash"]
        if not isinstance(hash_value, str) or not HEX64.fullmatch(hash_value):
            raise ValueError(f"row {index}: invalid digest")
        calculated = digest({k:v for k,v in item.items() if k!="hash"})
        if calculated != hash_value:
            raise ValueError(f"row {index}: SHA-256 mismatch")
        prev = hash_value
    return prev

def read_rows(path: Path = LEDGER) -> list[dict]:
    if not path.exists():
        return []
    text = path.read_text(encoding="utf-8")
    if text and not text.endswith("\n"):
        raise ValueError("unterminated JSONL line; refusing append")
    rows = []
    for n, line in enumerate(text.splitlines(), 1):
        if not line:
            raise ValueError(f"blank JSONL line {n}")
        try:
            rows.append(json.loads(line))
        except json.JSONDecodeError as exc:
            raise ValueError(f"JSONL parse error on line {n}") from exc
    verify_rows(rows)
    return rows

def verify_public_file(source: dict) -> None:
    """Verify a PUBLIC default-branch file via unauthenticated GitHub Contents API."""
    validate_source(source)
    repo, path = source["repo"], source["path"]
    encoded = urllib.parse.quote(path, safe="/")
    url = "https://api.github.com/repos/" + repo + "/contents/" + encoded
    request = urllib.request.Request(url, headers={"Accept":"application/vnd.github+json","User-Agent":"ROOT0-corpus-spine-v1"})
    with urllib.request.urlopen(request, timeout=20) as response:
        payload = json.load(response)
    if not isinstance(payload,dict) or payload.get("type") != "file" or payload.get("sha") != source["blob_sha"]:
        raise ValueError("source SHA mismatches public default-branch GitHub file")

def append_row(rows: list[dict], *, actor: str, kind: str, source: dict,
               what: str, how: str, why: str, supersedes: int | None,
               date: str | None = None) -> dict:
    verify_rows(rows)
    body = {"version":1,"seq":len(rows)+1,"recorded_at":date or dt.datetime.now(dt.timezone.utc).date().isoformat(),
            "actor":actor,"kind":kind,"source":source,"what":what,"how":how,"why":why,
            "supersedes":supersedes,"prev":rows[-1]["hash"] if rows else "GENESIS"}
    new = dict(body, hash=digest(body))
    verify_rows([*rows,new])
    return new

def write_append(path: Path, row: dict) -> None:
    path.parent.mkdir(parents=True,exist_ok=True)
    # local exclusive append. Git history and non-force git push are the remote concurrency gate.
    fd=os.open(str(path),os.O_WRONLY|os.O_APPEND|os.O_CREAT,0o644)
    try:
        with os.fdopen(fd,"a",encoding="utf-8",newline="\n") as out:
            out.write(json.dumps(row,ensure_ascii=False,separators=(",",":"))+"\n")
            out.flush()
            os.fsync(out.fileno())
    except BaseException:
        raise

def main(argv=None) -> int:
    p=argparse.ArgumentParser(description="TOPH CORTEX corpus-wide append-only source memory")
    p.add_argument("--ledger",type=Path,default=LEDGER,help="test/alternate ledger")
    sub=p.add_subparsers(dest="cmd",required=True)
    sub.add_parser("verify")
    sub.add_parser("tip")
    sub.add_parser("status")
    a=sub.add_parser("append")
    a.add_argument("--expect-tip",required=True)
    a.add_argument("--actor",default="root0")
    a.add_argument("--kind",choices=sorted(KINDS),default="OBSERVATION")
    a.add_argument("--source-repo",required=True)
    a.add_argument("--source-path",required=True)
    a.add_argument("--source-sha",required=True)
    a.add_argument("--what",required=True)
    a.add_argument("--how",required=True)
    a.add_argument("--why",required=True)
    a.add_argument("--supersedes",type=int)
    a.add_argument("--verify-public-source",action="store_true")
    a.add_argument("--date",help="UTC calendar date YYYY-MM-DD, default today")
    args=p.parse_args(argv)
    try:
        rows=read_rows(args.ledger);head=verify_rows(rows)
        if args.cmd=="verify":
            print(f"PASS | events={len(rows)} | tip={head}")
        elif args.cmd=="tip":
            print(head)
        elif args.cmd=="status":
            print(json.dumps({"schema":"root0.corpus-spine/1","events":len(rows),"tip":head,
                              "source_repositories":sorted(set(x["source"]["repo"] for x in rows))},indent=2))
        elif args.cmd=="append":
            if args.expect_tip!=head:
                raise ValueError("CAS conflict: expected tip does not match on-disk tip")
            source={"repo":args.source_repo,"path":args.source_path,"blob_sha":args.source_sha,"visibility":"public"}
            validate_source(source)
            if args.verify_public_source:
                verify_public_file(source)
            if args.date:
                dt.date.fromisoformat(args.date)
            row=append_row(rows,actor=args.actor,kind=args.kind,source=source,
                           what=args.what,how=args.how,why=args.why,supersedes=args.supersedes,date=args.date)
            write_append(args.ledger,row)
            verify_rows(read_rows(args.ledger))
            print(f"APPENDED LOCAL | seq={row['seq']} | tip={row['hash']}")
            print("NOT GIT SYNCED: commit and push this updated ledger (no force push).")
        return 0
    except (ValueError, OSError, urllib.error.URLError) as exc:
        print(f"HALTED: {exc}",file=sys.stderr)
        return 1

if __name__=="__main__":
    raise SystemExit(main())
