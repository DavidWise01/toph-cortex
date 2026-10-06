#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
clear_view.py — TOPH/Sapphon recursive clear-view marker + auditor.

Canonical invariant:
    NEVER ASK:  "what state is the system in?"
    ALWAYS ASK: "what state is BIODOME X in?"

The recursive walk marks every node with its inherited biodome identity.
A child keeps its parent's biodome unless it explicitly declares a new
biodome boundary. Cross-dome equality is never inferred.

No model calls; deterministic stdlib only.
"""
from __future__ import annotations
from dataclasses import dataclass, asdict
import json
import re
import sys
from typing import Any, Dict, Iterable, List, Optional

CLEAR_VIEW_RULE = 'ALWAYS ASK: "what state is BIODOME X in?"'
FORBIDDEN_GLOBAL_QUERY = 'what state is the system in?'
INSPECTION_TERMS = ("state", "status", "phase", "branch", "provenance", "clock")

SUBSTRATES: Dict[str, str] = {
    "A": "ownership/operator",
    "B": "institutional/access",
    "C": "compute",
    "D": "defense/protection",
    "E": "naming/economic/network-expression",
}

@dataclass(frozen=True)
class Mark:
    biodome_id: str
    substrate: str
    local_path: str
    clear_view_required: bool = True

def normalize_dome(dome: str) -> str:
    d = str(dome).strip().upper()
    if d not in SUBSTRATES:
        raise ValueError("unknown biodome: %r" % dome)
    return d

def scoped_query(query: str) -> Optional[str]:
    """Return referenced biodome A-E, else None."""
    m = re.search(r"\bBIODOME\s+([A-E])\b", query.upper())
    return m.group(1) if m else None

def audit_query(query: str) -> Dict[str, Any]:
    """Mechanical clear-view audit for a state-inspection query."""
    q = " ".join(query.strip().split())
    dome = scoped_query(q)
    asks_state = bool(re.search(r"\bstate\b", q, flags=re.I))
    global_system = bool(re.search(r"\bthe\s+system\b", q, flags=re.I))
    if asks_state and global_system and dome is None:
        return {
            "pass": False,
            "reason": "unscoped global state query",
            "canonical": CLEAR_VIEW_RULE,
            "biodome_id": None,
        }
    if asks_state and dome is None:
        return {
            "pass": False,
            "reason": "state query missing BIODOME A-E scope",
            "canonical": CLEAR_VIEW_RULE,
            "biodome_id": None,
        }
    return {
        "pass": True,
        "reason": "scoped" if dome else "not a state query",
        "canonical": CLEAR_VIEW_RULE,
        "biodome_id": dome,
    }

def mark_recursive(node: Any, biodome_id: str, path: str = "root") -> Any:
    """
    Recursively annotate dict/list trees.

    Explicit boundary convention:
      {"biodome_id": "C", ...}
    changes the inherited dome for that node and all descendants.

    Otherwise descendants inherit the caller's biodome unchanged.
    """
    dome = normalize_dome(biodome_id)

    if isinstance(node, dict):
        explicit = node.get("biodome_id")
        if explicit is not None:
            dome = normalize_dome(explicit)
        mark = asdict(Mark(dome, SUBSTRATES[dome], path))
        out: Dict[str, Any] = {"__clear_view__": mark}
        for key, value in node.items():
            if key == "__clear_view__":
                continue
            child_path = path + "." + str(key)
            out[key] = mark_recursive(value, dome, child_path)
        return out

    if isinstance(node, list):
        return [
            mark_recursive(value, dome, "%s[%d]" % (path, i))
            for i, value in enumerate(node)
        ]

    return node

def collect_marks(node: Any) -> List[Dict[str, Any]]:
    out: List[Dict[str, Any]] = []
    def walk(x: Any) -> None:
        if isinstance(x, dict):
            m = x.get("__clear_view__")
            if isinstance(m, dict):
                out.append(m)
            for k, v in x.items():
                if k != "__clear_view__":
                    walk(v)
        elif isinstance(x, list):
            for v in x:
                walk(v)
    walk(node)
    return out

def verify_marks(node: Any) -> bool:
    """Every marked dict must carry a valid, required clear-view record."""
    marks = collect_marks(node)
    return bool(marks) and all(
        m.get("clear_view_required") is True
        and m.get("biodome_id") in SUBSTRATES
        and m.get("substrate") == SUBSTRATES[m["biodome_id"]]
        and isinstance(m.get("local_path"), str)
        for m in marks
    )

def demo_tree() -> Dict[str, Any]:
    return {
        "biodome_id": "A",
        "referent": {
            "local_state": {
                "phase": "2/5",
                "ternary": 1,
                "provenance": {"source": "local"},
            },
            "crossing": {
                "biodome_id": "C",
                "received": {
                    "phase": "1/5",
                    "ternary": 0,
                },
            },
        },
    }

def selftest() -> Dict[str, Any]:
    # Query gate.
    assert audit_query("what state is the system in?")["pass"] is False
    assert audit_query("what state is BIODOME A in?")["pass"] is True
    assert audit_query("what state is biodome e in?")["biodome_id"] == "E"

    # Recursive inheritance + explicit boundary.
    marked = mark_recursive(demo_tree(), "A")
    assert verify_marks(marked)
    marks = collect_marks(marked)
    assert marks[0]["biodome_id"] == "A"
    assert any(m["biodome_id"] == "C" for m in marks)

    # Before the explicit boundary all nested A nodes remain A.
    local = marked["referent"]["local_state"]
    assert local["__clear_view__"]["biodome_id"] == "A"
    assert local["provenance"]["__clear_view__"]["biodome_id"] == "A"

    # Boundary switches descendants to C.
    crossing = marked["referent"]["crossing"]
    assert crossing["__clear_view__"]["biodome_id"] == "C"
    assert crossing["received"]["__clear_view__"]["biodome_id"] == "C"

    # Exhaustive substrate roots.
    for dome in SUBSTRATES:
        sample = mark_recursive({"x": {"y": {"z": 1}}}, dome)
        ms = collect_marks(sample)
        assert ms and all(m["biodome_id"] == dome for m in ms)

    return {
        "status": "PASS",
        "rule": CLEAR_VIEW_RULE,
        "substrates": SUBSTRATES,
        "recursive_marks": len(marks),
        "seal": "0e / CLEAR-VIEW RULE v1 RECURSIVE AUDIT PASS",
    }

def main() -> None:
    if "--selftest" in sys.argv:
        print(json.dumps(selftest(), indent=2))
        return
    if len(sys.argv) > 2 and sys.argv[1] == "--audit":
        print(json.dumps(audit_query(" ".join(sys.argv[2:])), indent=2))
        return
    print(CLEAR_VIEW_RULE)
    print('Run: python bin/clear_view.py --selftest')
    print(' or: python bin/clear_view.py --audit "what state is BIODOME C in?"')

if __name__ == "__main__":
    main()
