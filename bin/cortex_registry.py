#!/usr/bin/env python3
"""STOCHIEON cortex reference promotion validator.

PROMOTED_REFERENCE means verified source provenance and central discoverability.
It does NOT execute agents, pass their tests, install code or create B/C witnesses.
"""
from __future__ import annotations
import argparse
import json
from pathlib import Path
import re
import sys

ROOT=Path(__file__).resolve().parents[1]
REGISTRY=ROOT/"memory"/"stochieon"/"cortex-promotions-v1.json"
SHA1=re.compile(r"^[a-f0-9]{40}$")
NAME=re.compile(r"^[a-z][a-z0-9-]{1,96}$")
VALID_CLASSES={"executable_source","symbolic_model","dlw_symbolic_manifest"}
EXPECTED_FAMILIES={"toph","oasis-four-cortex","ud0-i13","atlas-hyper-cortex"}

def source_check(x:dict)->None:
    if not isinstance(x,dict) or set(x)!={"repo","path","blob_sha","uri"}:
        raise ValueError("Source must be exact public Git file pointer")
    repo=x["repo"]
    if repo not in {"DavidWise01/toph-cortex","DavidWise01/oasis","DavidWise01/ud0",
                    "DavidWise01/agent-0root","DavidWise01/atlas","DavidWise01/toroid-kernel"}:
        raise ValueError("Unverified source repository")
    path=x["path"]
    if not isinstance(path,str) or not path or path.startswith("/") or "\\" in path or
        any(piece in ("",".","..") for piece in path.split("/")):
        raise ValueError("Unsafe source path")
    if not SHA1.fullmatch(x["blob_sha"]):
        raise ValueError("Git blob SHA-1 missing")
    if not x["uri"].startswith("https://github.com/"+repo+"/blob/HEAD/"):
        raise ValueError("Provenance URL does not match repository")

def verify(registry:dict)->dict:
    if not isinstance(registry,dict) or registry.get("schema")!="root0.stochieon.cortex-promotions/1":
        raise ValueError("Unknown cortex promotion registry")
    if registry.get("mark")!=".dlw" or registry.get("immutable_constant")!="cubit":
        raise ValueError("Renamed .dlw or lowercase cubit")
    p=registry.get("promotion_policy",{})
    if p.get("method")!="NONDESTRUCTIVE_REFERENCE_PROMOTION" or p.get("source_history")!="UNCHANGED":
        raise ValueError("Promotion cannot alter source Git")
    for key in ("no_quorum","claims_liveness","claims_formal_proof_compile"):
        if p.get(key)!=(key=="no_quorum"):raise ValueError("False quorum, liveness or proof status")
    if p.get("witnesses")!=["A","B","C"] or p.get("independent_witness_claims_created")!=0 or p.get("executable_redeployments")!=0:
        raise ValueError("Unassigned independent witnesses or imaginary deployment")
    nodes=registry.get("promoted")
    if not isinstance(nodes,list) or not nodes:raise ValueError("No promoted source nodes")
    seen=set();families=set();executable=0;symbolic=0;mirror_count=0
    for x in nodes:
        if not isinstance(x,dict) or not NAME.fullmatch(x.get("id","")) or x["id"] in seen:
            raise ValueError("Duplicate/invalid cortex ID")
        seen.add(x["id"])
        if x.get("class") not in VALID_CLASSES or x.get("promotion") not in ("PROMOTED_REFERENCE","PROMOTED_SYMBOLIC"):
            raise ValueError("Wrong evidence class or promotion status")
        if x["class"]=="executable_source":
            if x["promotion"]!="PROMOTED_REFERENCE":raise ValueError("Executable source improperly relabeled")
            executable+=1
        else:
            if x["promotion"]!="PROMOTED_SYMBOLIC":raise ValueError("Symbolic source improperly relabeled")
            symbolic+=1
        if x.get("tier") not in ("K","E","T","X"):raise ValueError("Invalid kernel tier")
        if not isinstance(x.get("role"),str) or not x["role"]:raise ValueError("Cortex role must be explicit")
        if x.get("operational_status") not in (
            "SOURCE_VERIFIED_NOT_EXECUTED_THIS_TURN","SYMBOLIC_NOT_PHYSICAL_VM",
            "MANIFEST_VERIFIED_NO_LIVE_VM_ATTESTATION"):
            raise ValueError("Unverified live cortex claim")
        source_check(x["source"])
        family=x["family"];families.add(family)
        for mirror in x.get("mirrors",[]):
            source_check(mirror)
            if mirror["blob_sha"]!=x["source"]["blob_sha"]:
                raise ValueError("Mirror is a different Git blob, cannot deduplicate")
            mirror_count+=1
        if x.get("shared_source") and x["family"]!="oasis-four-cortex":
            raise ValueError("Improper shared source")
        if family=="oasis-four-cortex" and x.get("carrier")!="{{i}}":
            raise ValueError("VM ladder identity carrier altered")
    if families!=EXPECTED_FAMILIES or set(registry.get("families",[]))!=EXPECTED_FAMILIES:
        raise ValueError("Missing supported cortex family")
    if len([x for x in nodes if x["family"]=="oasis-four-cortex"])!=4:
        raise ValueError("Four-cortex ladder incomplete")
    atlas=[x for x in nodes if x["family"]=="atlas-hyper-cortex"]
    if len(atlas)!=8:raise ValueError("Atlas symbolic family incomplete")
    assert symbolic>=4
    formal=registry.get("supporting_formal_sources")
    if not isinstance(formal,list) or len(formal)!=6:raise ValueError("Six Lean source references required")
    for entry in formal:
        if entry.get("kind")!="lean_source_unverified_compilation":raise ValueError("Proof compilation must not be invented")
        source_check(entry["source"])
        if entry["source"]["repo"]!="DavidWise01/toroid-kernel":raise ValueError("Wrong Lean origin")
    summary=registry.get("summary",{})
    if summary!={"promoted_cortex_nodes":len(nodes),"distinct_source_families":len(families),
                 "distinct_executable_sources":executable,"symbolic_nodes":symbolic,
                 "mirrored_duplicate_sources":mirror_count,"supporting_lean_source_files":len(formal)}:
        raise ValueError("Summary/counts changed")
    if registry.get("preservation",{}).get("cubit","").find("exact lowercase cubit")<0:
        raise ValueError("Distillation constant not preserved")
    return {"status":"PASS","registry":registry["schema"],"promoted":len(nodes),
            "families":sorted(families),"executable_sources":executable,
            "symbolic_nodes":symbolic,"mirrors_deduplicated":mirror_count,
            "formal_source_files":len(formal),"live_agents_created":0,
            "constant":"cubit","watermark":".dlw","quorum":None}

def main(argv=None)->int:
    parser=argparse.ArgumentParser()
    parser.add_argument("--registry",type=Path,default=REGISTRY)
    args=parser.parse_args(argv)
    try:
        print(json.dumps(verify(json.loads(args.registry.read_text(encoding="utf-8"))),
                         sort_keys=True,indent=2))
        return 0
    except (OSError,KeyError,TypeError,ValueError,AssertionError) as exc:
        print("CORTEX PROMOTION HALTED: "+str(exc),file=sys.stderr);return 1

if __name__=="__main__":raise SystemExit(main())
