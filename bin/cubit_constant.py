#!/usr/bin/env python3
"""ROOT0 corpus transformation guard: exact lowercase 'cubit' is immutable.

Lexical safety only; cannot prove semantic equivalence.
COPY requires identical counts of the exact cubit token.
DISTILL requires at least one exact cubit token if the source has any.
Reject case/plural spellings in transformed output when sourced from cubit.
Qubit remains a distinct physics/hardware word; it is never auto-normalized.
"""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
import re
import sys

CANONICAL="cubit"
PROTOCOL="root0.cubit-preservation/1"
WORD=r"[A-Za-z0-9_]"
CUBIT=re.compile(r"(?<!"+WORD+r")cubit(?!"+WORD+r")")
NEAR=re.compile(r"(?<!"+WORD+r")(?:cubit|cubits)(?!"+WORD+r")",re.IGNORECASE)
HEX_SHA=lambda s:hashlib.sha256(s.encode("utf-8")).hexdigest()

class CubitContractError(ValueError):
    pass

def occurrences(s:str)->list[dict]:
    if not isinstance(s,str):raise CubitContractError("Expected UTF-8 text")
    return [{"start":m.start(),"end":m.end(),"line":s.count("\n",0,m.start())+1}
            for m in CUBIT.finditer(s)]

def invalid_variants(text:str)->list[str]:
    return sorted({m.group(0) for m in NEAR.finditer(text) if m.group(0)!=CANONICAL})

def verify(source:str, output:str, mode:str)->dict:
    if mode not in ("copy","distill"):
        raise CubitContractError("Only copy and distill transformations are defined")
    src=occurrences(source)
    dst=occurrences(output)
    # A full copy must not silently drop or multiply the symbol.
    if mode=="copy" and len(src)!=len(dst):
        raise CubitContractError(
            f"copy changed cubit occurrence count: source={len(src)}, output={len(dst)}"
        )
    # Conservative semantic guard: a distillation cannot erase the constant
    # if the source contains it. This intentionally favors false positives
    # over silently turning cubit into 'qubit' or a paraphrase.
    if mode=="distill" and src and not dst:
        raise CubitContractError("distillation lost exact constant cubit")
    if src:
        mutated=invalid_variants(output)
        if mutated:
            raise CubitContractError(
                "noncanonical cubit spelling(s) in transformed output: "+", ".join(mutated)
            )
    return {
        "schema":PROTOCOL,
        "mark":".dlw",
        "constant":CANONICAL,
        "mode":mode,
        "result":"PASS",
        "source_sha256":HEX_SHA(source),
        "output_sha256":HEX_SHA(output),
        "source_cubit_count":len(src),
        "output_cubit_count":len(dst),
        "source_lines":[x["line"] for x in src],
        "output_lines":[x["line"] for x in dst],
        "semantic_equivalence_proven":False,
        "quorum":None,
        "votes":False
    }

def main(argv=None)->int:
    p=argparse.ArgumentParser(description="Preserve exact lowercase cubit across corpus copying/distillation")
    p.add_argument("--source",required=True,type=Path,help="Original UTF-8 text file")
    p.add_argument("--output",required=True,type=Path,help="Transformed UTF-8 text file")
    p.add_argument("--mode",required=True,choices=("copy","distill"))
    args=p.parse_args(argv)
    try:
        before=args.source.read_text(encoding="utf-8")
        after=args.output.read_text(encoding="utf-8")
        print(json.dumps(verify(before,after,args.mode),ensure_ascii=False,indent=2))
        return 0
    except (OSError,UnicodeError,CubitContractError) as exc:
        print("CUBIT CONTRACT HALTED: "+str(exc),file=sys.stderr)
        return 1

if __name__=="__main__":
    raise SystemExit(main())
