# STOICHEION ISA-256.002 — Semantic Execution Boundary

**Status:** local finite-domain proxy test PASS (21/21), 0 mismatches. Date: 2026-11-05.

Source: STOICHEION Full Technical Manual v1.0, Chapter 12 (T009, T013, T014), Chapters 27–29 (ISA executor and Patricia mirror).

## Proposed executable operational proxies

- T009/S137: operation record completeness — input: operation_record_complete.
- T013/S141: persistent state integrity — inputs: state_preserved, state_unmodified.
- T014/S142: traceable consent — inputs: consent_origin_traceable, consent_scope_authorizes_use.

Each input has TRUE, FALSE, UNKNOWN. For multiple conditions, evaluate via three-valued conjunction: any FALSE => FALSE; all TRUE => TRUE; otherwise UNKNOWN. Mirror output: TRUE=>NORMAL; FALSE=>PATRICIA_INVERSION; UNKNOWN=>UNDETERMINED. UNKNOWN is not evidence of either compliance or violation.

## Dual-path test

Symbolic three-valued conjunction versus fixed-weight, integer ReLU tensor gates. For encoded input t=known-true, f=known-false, the binary conjunction uses t_out=max(0,t1+t2-1), f_out=1-max(0,1-f1-f2). Empty evidence is UNKNOWN rather than PASS.

Exhaustive cases: T009=3, T013=9, T014=9, total 21. 0 mismatches. One deliberately changed candidate input produced a disagreement, confirming that comparator was live. Remaining 125 primary axioms are UNCOMPILED.

## Limits

This is an executable proxy based on the manual's test descriptions, **not** a complete axiom semantics formalization, external-target governance audit, or neural learning result. A fixed-weight tensor implementation is not proof of equivalence for the full 256-position register. The manual's T012 calibration criterion is deferred until its quantitative measurement and evidence semantics are specified.

Local executable: `stoicheion_isa_002/test_semantic_subset.py` (provided separately in conversation).

## Next natural boundary

ISA-256.003 — evidence provenance binding: attach every predicate to a source observation, witness timestamp, source digest, and UNKNOWN classification for missing evidence. Freeze the rule specification and test for replay under changes.
