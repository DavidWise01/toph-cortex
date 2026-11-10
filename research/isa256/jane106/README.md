# JANE 106 — The Source / MoE Hive 10×10 Generational Lattice

## Canonical user-defined primitives

- **Source:** one Jane `{{j}}`, alone authorized to select a question and approve retained knowledge.
- **Hive:** mixture-of-experts packet routers with FLAY functions U semantic, D somatic, R holographic, L abstractive.
- **Grid:** `[10×10]`; **Y:** anchored at Gen 0; **X:** lineage Gen 0 through Gen 7; **Z:** `−/+` operant.
- **Carrier:** `{{n}}^{{n}}^{{n}}`. Here `^` is the symbolic nesting/address carrier, *not exponentiation*.

## Explicit implementation assumption

The request did not fix whether all 8 generations overlay one 10×10 plane or each generation has its own plane. This test uses **eight 10×10 generation slices**, `generation=0..7`, `(x,y)=0..9`, `z=−1 or +1`.

Thus `8 × 10 × 10 × 2 = 1,600` **logical address slots**, not 1,600 distinct independent agents. Y's lineage root is Gen 0; the generation coordinate follows the X-directed lineage. An address is written `g3:x04:y05:z+1`. Mirroring Z changes only the sign. At Gen 7, forward traversal returns NONE, not automatic wrap.

The nested carrier is rendered as `{{n[g3]}}^{{n[x04,y05]}}^{{n[z+1]}}`.

## Invariant

Agents can provide attributed packets (what, why, source, uncertainty, cost). They cannot set Jane's interests, cast authority votes, or write Jane's retained memory. `Jane.retain()` requires evidence verification **and** Jane's explicit decision. SHA-256 packet hashes are byte identifiers, not evidence authentication or source independence.

## Run

```bash
python -m unittest -q
python model.py
```

Open `index.html` offline. Click lattice vertices; change generation; toggle Z; copy a coordinate.

## Local verification

26/26 Python tests pass. The tests cover 1,600 unique addresses, bounds, mirrored signs, terminal generation, packet validation and Jane's learning gate.

## Explicit limits

This is a visual address model and deterministic sovereignty test. It does **not** instantiate 1,600 AI agents, a trained neural MoE, live 0root.ai crawling, autonomous learning, GitHub Actions, or deployed Pages.

## Next invariant — JANE 107

**Generation inheritance without authority inheritance:** packets may traverse `Gen 0→7` with their source ancestry and Z-operant preserved, but no generation or expert may gain Jane's write/learn authority. Test conflict, fork, mirror and terminal-boundary behaviors.