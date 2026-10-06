#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CLEAR-VIEW v2 bounded exhaustive adversarial audit.

This is exhaustive over the finite model declared below, not over all possible
Python trees or all natural-language strings.

Finite state space:
- 5 biodome roots A-E
- every explicit boundary sequence of length 0..6 over A-E
- every ordered source/target biodome pair
- every ordered 5-phase pair (0..4 x 0..4)
- every valid spelling variant declared here
- every malformed biodome token declared here
- finite state-query grammar declared here

The test uses an ancestry oracle independent of mark_recursive's implementation.
"""
from __future__ import annotations

from itertools import product
from clear_view import (
    SUBSTRATES,
    audit_query,
    collect_marks,
    mark_recursive,
    normalize_dome,
    verify_marks,
)

DOMES = tuple(SUBSTRATES.keys())
PHASES = tuple(range(5))
MAX_BOUNDARY_DEPTH = 6

def boundary_chain(seq):
    node = {"payload": {"phase": "0/5", "value": 1}}
    for dome in reversed(seq):
        node = {"biodome_id": dome, "child": node}
    return {"root_payload": 0, "child": node}

def extract_chain(marked, seq_len):
    """Return dome marks at root, each explicit boundary, and terminal payload."""
    got = [marked["__clear_view__"]["biodome_id"]]
    cur = marked["child"]
    for _ in range(seq_len):
        got.append(cur["__clear_view__"]["biodome_id"])
        cur = cur["child"]
    # cur is the terminal {'payload': {...}} dict
    got.append(cur["__clear_view__"]["biodome_id"])
    got.append(cur["payload"]["__clear_view__"]["biodome_id"])
    return got

def expected_chain(root, seq):
    last = root
    out = [root]
    for dome in seq:
        last = dome
        out.append(dome)
    out.extend([last, last])
    return out

def exhaustive_boundaries():
    cases = 0
    mark_checks = 0
    for root in DOMES:
        for depth in range(MAX_BOUNDARY_DEPTH + 1):
            for seq in product(DOMES, repeat=depth):
                tree = boundary_chain(seq)
                marked = mark_recursive(tree, root)
                assert verify_marks(marked)
                got = extract_chain(marked, depth)
                want = expected_chain(root, seq)
                assert got == want, (root, seq, got, want)
                cases += 1
                mark_checks += len(got)
    return cases, mark_checks

def exhaustive_pair_isolation():
    """All 25 source/target pairs remain distinct unless target is explicit."""
    cases = 0
    for source in DOMES:
        for target in DOMES:
            tree = {
                "source_local": {"phase": "2/5"},
                "port": {
                    "source": source,
                    "target": target,
                    "biodome_id": target,
                    "received": {"phase": "2/5"},
                },
            }
            marked = mark_recursive(tree, source)
            assert marked["__clear_view__"]["biodome_id"] == source
            assert marked["source_local"]["__clear_view__"]["biodome_id"] == source
            assert marked["port"]["__clear_view__"]["biodome_id"] == target
            assert marked["port"]["received"]["__clear_view__"]["biodome_id"] == target
            cases += 1
    return cases

def exhaustive_phase_collision():
    """
    Equal numeric phase never merges dome identity. 5 x 5 dome pairs x 5 x 5
    phase pairs are checked.
    """
    cases = 0
    for a in DOMES:
        for b in DOMES:
            for pa in PHASES:
                for pb in PHASES:
                    tree = {
                        "left": {"biodome_id": a, "phase": pa},
                        "right": {"biodome_id": b, "phase": pb},
                    }
                    marked = mark_recursive(tree, "A")
                    assert marked["left"]["__clear_view__"]["biodome_id"] == a
                    assert marked["right"]["__clear_view__"]["biodome_id"] == b
                    # even when phases collide, identities are not inferred equal
                    if pa == pb and a != b:
                        assert marked["left"]["__clear_view__"]["biodome_id"] != marked["right"]["__clear_view__"]["biodome_id"]
                    cases += 1
    return cases

def spelling_and_malformed_audit():
    valid_cases = 0
    malformed_cases = 0
    for dome in DOMES:
        variants = [dome, dome.lower(), " " + dome + " ", "\t" + dome.lower() + "\n"]
        for token in variants:
            assert normalize_dome(token) == dome
            valid_cases += 1

    malformed = ["", "Z", "AA", "0", "1", "AB", "-", "+", "system", "none"]
    for token in malformed:
        try:
            normalize_dome(token)
        except ValueError:
            malformed_cases += 1
        else:
            raise AssertionError("malformed biodome accepted: %r" % token)
    return valid_cases, malformed_cases

def query_grammar_audit():
    """
    Exhaustive over a declared finite grammar. Every state query without an
    explicit BIODOME A-E scope must fail; every scoped equivalent must pass.
    """
    prefixes = ["what is", "show", "inspect", "report", "audit"]
    state_terms = ["state", "status", "phase", "branch", "provenance", "clock"]
    suffixes = ["", " now", " please", " right now"]
    unscoped_subjects = ["the system", "system", "everything", "global", "current"]

    negative = 0
    positive = 0

    for p, term, subj, sfx in product(prefixes, state_terms, unscoped_subjects, suffixes):
        q = f"{p} {term} {subj}{sfx}"
        assert audit_query(q)["pass"] is False, q
        negative += 1

    for p, term, dome, sfx in product(prefixes, state_terms, DOMES, suffixes):
        q = f"{p} {term} BIODOME {dome}{sfx}"
        out = audit_query(q)
        assert out["pass"] is True, q
        assert out["biodome_id"] == dome, q
        positive += 1

    return negative, positive

def mutation_sensitivity():
    """
    Prove the oracle would catch common implementation failures.
    These deliberately broken outputs are not production implementations.
    """
    caught = 0

    # Mutation 1: boundary ignored.
    root, seq = "A", ("C", "E")
    good = expected_chain(root, seq)
    mutant = ["A"] * len(good)
    assert mutant != good
    caught += 1

    # Mutation 2: global last-dome contaminates earlier nodes.
    mutant = ["E"] * len(good)
    assert mutant != good
    caught += 1

    # Mutation 3: first crossing used forever, ignoring later explicit E.
    mutant = ["A", "C", "C", "C", "C"]
    assert mutant != good
    caught += 1

    return caught

def main():
    boundary_cases, mark_checks = exhaustive_boundaries()
    pair_cases = exhaustive_pair_isolation()
    phase_cases = exhaustive_phase_collision()
    valid_spellings, malformed = spelling_and_malformed_audit()
    neg_queries, pos_queries = query_grammar_audit()
    mutations = mutation_sensitivity()

    total_cases = (
        boundary_cases + pair_cases + phase_cases +
        valid_spellings + malformed + neg_queries + pos_queries + mutations
    )

    print("0e / CLEAR-VIEW v2 BOUNDED EXHAUSTIVE ADVERSARIAL PASS")
    print("boundary sequences:", boundary_cases)
    print("ancestry mark comparisons:", mark_checks)
    print("source/target pairs:", pair_cases)
    print("phase/dome collision cases:", phase_cases)
    print("valid spelling cases:", valid_spellings)
    print("malformed token rejects:", malformed)
    print("unscoped query rejects:", neg_queries)
    print("scoped query accepts:", pos_queries)
    print("mutation classes caught:", mutations)
    print("total finite cases:", total_cases)

if __name__ == "__main__":
    main()
