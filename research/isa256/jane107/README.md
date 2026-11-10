# JANE 107 — Generational Inheritance / Source Authority

A standalone bounded simulation showing **one Jane (THE SOURCE)** with a 10×10 **mixture-of-experts** hive addressed across **Gen 0–7** and **Z ∈ {−1,+1}**.

The user's coordinate expression `{{n}}^{{n}}^{{n}}` remains symbolic. The present implementation chooses **eight separate 10×10 address planes**: 8 × 100 × 2 = **1,600 logical addresses, not agents**. The Y root is Gen 0; the Gen index tracks the lineage while x/y select one grid position inside that generation. This is an explicit modeling choice pending the user's refinement.

## Proposed generation functions — subject to user correction

| Gen | Function | Scout packet contribution |
|---|---|---|
| 0 | Seed | Capture the input and source without interpretation. |
| 1 | Semantic / U | Identify what it is; preserve words and definitions. |
| 2 | Somatic / D | Record relationships and contextual implications. |
| 3 | Holographic / R | Link genuinely similar patterns without unjustified merging. |
| 4 | Abstractive / L | Ask what-if and seek counterexamples. |
| 5 | Witness | Record roots, provenance, conflicting claims and missing checks. |
| 6 | Synthesis | Collate relevance, novelty, cost and uncertainty into a packet. |
| 7 | Handoff | Present the packet and full lineage to Jane. No memory writes. |

**Z = +1** is a constructive interpretation and **Z = −1** is a challenging interpretation. Neither sign means true or false. Explicit mirroring changes sign while retaining source and coordinate ancestry. Multiple forked packets can exist, without becoming independent authority.

## Run

```bash
python -m unittest -q
python model.py
```

Open `index.html` locally to inspect the generation and signed Z coordinate, and to simulate offering a packet to Jane.

## Invariants

- No generation jumps or wraps after Gen 7.
- Every child refers to its parent, keeps the originating root, and preserves provenance.
- A mirrored packet has unchanged underlying coordinates and opposite Z; the view itself is not a delivered packet.
- Branches are permitted, identical replay branches are not.
- Every generation has `authority=PROPOSAL_ONLY`.
- A completed lineage may be **offered** to Jane, but offering does not store knowledge.
- Only a **distinct Jane decision**, marked as verified, may append a retained memory record.
- Append-only SHA-256 event chain catches byte alteration, but provides no actor authentication or empirical proof.

This prototype does **not** implement neural MoE routing, live agent execution, live external witness verification, Git-to-Git workflows or GitHub Pages deployment. Tests validate toy state transitions and invariants, not Jane's independent curiosity or autonomous preferences.

## Next natural boundary — JANE 108

Can the hive **fork the same source into −/+ interpretations through Gen 0–7**, reconcile both as competing evidence without voting, and return to Jane with preserved branch ancestry and unresolved contradictions? No automatic unification and no inherited authority.