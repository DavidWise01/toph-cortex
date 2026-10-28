#!/usr/bin/env python3
"""Gate19: verify nested SAPPHON components inside the exact cubit constant.

Non-destructive source promotions; no execution, synthetic witness, quorum,
physical qubit claim, added spectral position or replacement of Prime 04/05.
"""
from __future__ import annotations
import argparse
import json
from pathlib import Path
import re
import sys
from urllib.parse import quote

ROOT=Path(__file__).resolve().parents[1]
REGISTRY=ROOT/"memory"/"stochieon"/"cubit-sapphon-promotions-v1.json"
SHA1=re.compile(r"^[a-f0-9]{40}$")
IDENT=re.compile(r"^[a-z][a-z0-9-]{2,95}$")
CANON="{|12|}{|3456|}{|78|}{|910|}{|1112131415||}{|1617|}{|18|}"
EXPECTED_CATEGORIES={"foundation":1,"prime":3,"frozen":2,
                     "spectral":2,"rider":2,"material":4,"visualization":2}
CLASSES={"canonical_symbolic","semantic_source","frozen_software_evidence",
         "executable_source","symbolic_software_manifest",
         "versioned_visual_adapter","browser_visualization"}
ORDER=["STOCHIEON","CORTEX","cubit","SAPPHON"]

def check_source(s:dict)->None:
    if not isinstance(s,dict) or set(s)!={"repo","path","blob_sha","url"}:
        raise ValueError("Exact original public source required")
    if s["repo"] not in ("DavidWise01/oasis","DavidWise01/toph-cortex"):
        raise ValueError("Source outside verified Sapphon repositories")
    path=s["path"]
    if (not isinstance(path,str) or not path or path.startswith("/") or
        "\\" in path or any(part in ("",".","..") for part in path.split("/"))):
        raise ValueError("Unsafe source file path")
    if not SHA1.fullmatch(s["blob_sha"]):
        raise ValueError("Original Git blob SHA-1 missing")
    expected="https://github.com/"+s["repo"]+"/blob/HEAD/"+"/".join(quote(part,safe="") for part in path.split("/"))
    if s["url"]!=expected:
        raise ValueError("Source link does not match its exact pinned Git path")

def verify(data:dict)->dict:
    if not isinstance(data,dict) or data.get("schema")!="root0.stochieon.cubit-sapphon-promotions/1" or data.get("version")!=19:
        raise ValueError("Not an immutable Gate19 Sapphon registry")
    if data.get("mark")!=".dlw" or data.get("constant")!="cubit":
        raise ValueError("Immutable .dlw and lowercase cubit altered")
    if data.get("name")!="STOCHIEON/CORTEX/cubit/SAPPHON" or data.get("promotion_policy")!="NONDESTRUCTIVE_SUBCUBIT_REFERENCE_PROMOTION":
        raise ValueError("Sapphon cannot be promoted beside the cubit")
    relation=data.get("containment",{})
    if relation.get("order")!=ORDER or relation.get("parent")!="cubit" or relation.get("type")!="LOGICAL_INSIDE":
        raise ValueError("Invalid kernel/cortex/cubit/Sapphon nesting")
    if relation.get("not_physical_qubit") is not True or relation.get("not_autonomous_runtime") is not True or relation.get("mutation")!="APPEND_ONLY_SUCCESSOR_REGISTRY":
        raise ValueError("Unsupported physical/runtime claim")
    parent=data.get("parent_cubit",{})
    if parent.get("id")!="cubit" or parent.get("kind")!="LOGICAL_ANALYTICAL_CUBIT":
        raise ValueError("Source cubit parent was replaced")
    check_source(parent.get("source"))
    if (parent.get("source",{}).get("repo")!="DavidWise01/oasis"
        or parent.get("source",{}).get("path")!="n184/analytical-cubit-color-bands-v93/spec.json"
        or parent.get("canonical")!=CANON
        or parent.get("bands")!=7 or parent.get("slots")!=18
        or parent.get("band_lengths")!=[2,4,2,2,5,2,1]):
        raise ValueError("Analytical cubit grammar / seven bands / eighteen positions altered")
    if parent.get("outer_symbolic_anchors")!=["--","++"] or parent.get("outer_anchors_consume_slots") is not False or parent.get("broadband_white_consumes_slots") is not False:
        raise ValueError("Sapphon symbolic anchors cannot consume cubit spectral slots")
    if parent.get("spectral_source_id")!="sapphon-spectrum" or not str(parent.get("slot_policy","")).startswith("Only spectral source bindings consume"):
        raise ValueError("The 18-slot cubit cannot be consumed by non-spectral nodes")
    primes=data.get("prime_ordinal",{})
    if primes.get("declared_total")!=5 or primes.get("found_canonical")!=[1,2,3] or primes.get("unassigned")!=[4,5]:
        raise ValueError("Do not invent Prime 04/05; only 01–03 are sourced")
    scope=data.get("scope",{})
    for name in ("complete_repository_inventory","sources_moved","files_copied","runtime_started"):
        if scope.get(name) is not False:raise ValueError("False exhaustive scan/copy/runtime claim")
    if scope.get("selected_public_git_default_branch_trees") is not True or scope.get("synthetic_witnesses_created")!=0 or scope.get("independent_witness_quorum") is not None or scope.get("records_are_references_not_attestations") is not True:
        raise ValueError("Registry cannot fabricate observations, votes or signatures")
    if data.get("historic_distinction","").find("no votes")<0:
        raise ValueError("Prime03 historical epistemic rule must be distinguished from governance")
    nodes=data.get("nodes")
    if not isinstance(nodes,list) or len(nodes)!=16:
        raise ValueError("Sixteen individually sourced Sapphon child references required")
    counts={cat:0 for cat in EXPECTED_CATEGORIES}
    seen=set();families=set();prime_ids=set()
    for n in nodes:
        if not isinstance(n,dict) or not IDENT.fullmatch(n.get("id","")) or n["id"] in seen:
            raise ValueError("Duplicate / invalid Sapphon child")
        seen.add(n["id"])
        if n.get("kind")!="SAPPHON" or n.get("parent")!="cubit" or n.get("containment")!="INSIDE_CUBIT":
            raise ValueError("Sapphon escaped the parent cubit")
        cat=n.get("category")
        if cat not in counts or n.get("evidence") not in CLASSES:
            raise ValueError("Unknown Sapphon evidence class")
        counts[cat]+=1
        if not isinstance(n.get("name"),str) or not n["name"] or not isinstance(n.get("role"),str) or not n["role"]:
            raise ValueError("Sapphon title and role missing")
        if n.get("runtime_claim")!="SOURCE_ONLY_NOT_ATTESTED":
            raise ValueError("Cannot promote sources into running physical Sapphons")
        binding=n.get("spectral_slot_binding")
        if binding!=("EXACT_PARENT_18" if cat=="spectral" else None):
            raise ValueError("Only spectral Sapphon components can bind 18 cubit slots")
        check_source(n.get("source"))
        families.add(n["source"]["repo"])
        if cat=="prime":
            if n["id"] not in ("sapphon-prime-01","sapphon-prime-02","sapphon-prime-03"):
                raise ValueError("Unverified Prime ordinal")
            prime_ids.add(n["id"])
    if counts!=EXPECTED_CATEGORIES or prime_ids!={"sapphon-prime-01","sapphon-prime-02","sapphon-prime-03"}:
        raise ValueError("Missing supported Sapphon family, or fabricated Prime")
    if seen!={n["id"] for n in nodes} or families!={"DavidWise01/oasis","DavidWise01/toph-cortex"}:
        raise ValueError("Source family provenance incomplete")
    summary=data.get("summary",{})
    if summary!={"nodes":16,"source_repos":2,"categories":counts,
                 "spectral_nodes":2,"prime_nodes":3,"unassigned_prime_ordinals":2}:
        raise ValueError("Source summary/family counts changed")
    preservation=data.get("preservation",{})
    if preservation.get("constant")!="cubit" or preservation.get("watermark")!=".dlw" or preservation.get("source_history")!="UNCHANGED":
        raise ValueError("Provenance, cubit or historical Git source modified")
    if data.get("reference_hierarchy",{}).get("no_flattening_to_cortex_siblings") is not True:
        raise ValueError("Sapphon promotions may not be flattened beside cortex")
    return {"status":"PASS","schema":data["schema"],"child_sapphons":16,
            "inside":"cubit","parent_context":"STOCHIEON/CORTEX","band_count":7,
            "spectral_positions":18,"prime_ordinals":[1,2,3],
            "unassigned_prime_ordinals":[4,5],"categories":counts,
            "physical_qubits_created":0,"new_agents_created":0,
            "quorum":None,"constant":"cubit","watermark":".dlw"}

def main(argv=None)->int:
    parser=argparse.ArgumentParser()
    parser.add_argument("--registry",type=Path,default=REGISTRY)
    args=parser.parse_args(argv)
    try:
        print(json.dumps(verify(json.loads(args.registry.read_text(encoding="utf-8"))),
                         sort_keys=True,indent=2))
        return 0
    except (ValueError,TypeError,OSError,KeyError) as e:
        print("SAPPHON CONTAINMENT HALTED: "+str(e),file=sys.stderr)
        return 1

if __name__=="__main__":raise SystemExit(main())
