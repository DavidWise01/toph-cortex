# ROOT0 canonical constant: `cubit`

**Canonical token: `cubit`** — lowercase, exact spelling, case-sensitive, atomic. It is not a style preference or an expendable synonym. This is a symbolic constant in the corpus.

The rule is effective at any **copy, distill, compress, summarize, export, import, mirror, bridge, or agent memory handoff** boundary under ROOT0/Persist Cortex.

```text
canonical symbol : cubit
copy             : cubit → cubit      (retain every occurrence)
distill          : cubit → cubit      (compression may collapse repetitions)
rename           : cubit → Cubit      (FORBIDDEN)
pluralize        : cubit → cubits     (FORBIDDEN as a substitute)
substitute       : cubit → qubit      (FORBIDDEN)
drop             : cubit → ∅          (FORBIDDEN when distilling a cubit-bearing source)

.dlw              = provenance mark
cubit             = immutable symbolic constant
A / B / C         = independent reports, no quorum
```

**Distillation does not rewrite terms.** It can remove redundant surrounding explanations, but if `cubit` appears in the source it must remain present as literal `cubit` in the distillate. A copy preserves the count of exact token occurrences. The checker rejects noncanonical case/plural variants in the output of any transformation whose source contains `cubit`.

`qubit` remains a separate, valid term for quantum hardware/physics, not a replacement for the user's `cubit`. Do not globally rename legitimate `qubit` terminology to `cubit` either.

## Operational lexical guard

```sh
python3 bin/cubit_constant.py --source docs/original.md --output docs/copied.md --mode copy
python3 bin/cubit_constant.py --source docs/original.md --output docs/summary.md --mode distill
python3 -m unittest discover -s tests -p 'test_cubit_constant.py' -v
```

The validator prints a deterministic `.dlw`-tagged audit record with source/output SHA-256 digests, token counts and line numbers. It fails closed on loss, casing or plural substitutions. It does **not** claim to prove semantic equivalence or that a token refers to the same concept in every context. More stringent copy equivalence may require byte-for-byte source comparison for the full artifact.

The [manual GitHub check](https://github.com/DavidWise01/toph-cortex/actions/workflows/cubit-constant-check.yml) validates two files from the TOPH checkout with no secret material and no write permissions. The [canonical corpus CI audit](https://github.com/DavidWise01/toph-cortex/actions/workflows/corpus-memory-audit.yml) runs its regression suite on changes.

For other DavidWise01 repositories, treat this [JSON contract](cubit-constant.json) as the interoperability rule. Installing an actual validation job in every repository remains separate work; a policy link alone cannot enforce another repo's CI.

## Attribution

The `.dlw` marker labels provenance and referent records. It is not part of the word `cubit`, does not rename it, and is not an ownership adjudication. The historic Git chain remains append-only; earlier data is not rewritten to enforce a newly declared constant.
