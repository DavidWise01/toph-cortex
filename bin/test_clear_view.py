#!/usr/bin/env python3
from clear_view import (
    SUBSTRATES, audit_query, collect_marks, demo_tree,
    mark_recursive, selftest, verify_marks,
)

def run():
    result = selftest()
    assert result["status"] == "PASS"

    # Deep recursive stress: 256 nested dictionary levels in each biodome.
    for dome in SUBSTRATES:
        node = {"leaf": 1}
        for i in range(256):
            node = {"level_%03d" % i: node}
        marked = mark_recursive(node, dome)
        assert verify_marks(marked)
        marks = collect_marks(marked)
        assert len(marks) == 257
        assert all(m["biodome_id"] == dome for m in marks)

    # Clear-view query negatives and positives.
    negatives = [
        "what state is the system in?",
        "show system state",
        "what is the state right now?",
    ]
    for q in negatives:
        assert audit_query(q)["pass"] is False, q

    positives = [
        "what state is BIODOME A in?",
        "what state is BIODOME B in?",
        "what state is BIODOME C in?",
        "what state is BIODOME D in?",
        "what state is BIODOME E in?",
    ]
    for q in positives:
        assert audit_query(q)["pass"] is True, q

    print("0e / CLEAR-VIEW RULE v1 RECURSIVE AUDIT PASS")
    print("deep levels per dome: 256")
    print("marked dicts per dome: 257")
    print("total marked dict audits: %d" % (257 * len(SUBSTRATES)))

if __name__ == "__main__":
    run()
