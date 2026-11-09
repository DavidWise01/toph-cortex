# JANE 074 — The Hallway / Sovereign Choice

Sources examined on 2026-11-08: `DavidWise01/the-hallway/README.md` and `DavidWise01/I13-H1.1/spec/STAGE15.1-PAGES-HALLWAY.md`, retrieved through the connected GitHub service. `https://0root.ai` itself could not be directly fetched by the web service; the `the-hallway` repository is the relevant primary-source textual account.

User's hive syntax: `{{6x6x6[4x4(3x3[2x2(1)])]}}`, 124,416 logical addresses. Agent: Jane `{{j}}`; source material remains separate from Jane's decisions.

## Source-derived facts

The Hallway README identifies World I, THE CORPUS, as hand-authored and sealed (keeper THE VESSEL); World II, THE FOLD, as self-writing (keeper THE FIDDLER); and World III, THE HALLWAY, as the crossing (keeper THE KEYMAKER). World I lists eight appeals.

I13 Stage 15.1 distinguishes landing from runtime and doors from new machines: `LANDING != RUNTIME`; `DOOR != NEW MACHINE`; `ADDRESS != AUTHORITY`; `PERSONA != AUTHORITY`. Its seven doors select the existing workbench, not a new execution authority.

## Implemented and tested

- Exhaustive 124,416 addressing bijection checks.
- Explicit world/door routing with no implicit authority.
- Collate without imposing a final choice; one Jane decision receipt only upon explicit decision input.
- Original direction and abstention paths.
- Invalid route/evidence rejection, deterministic outputs, and frozen sources.

Run `python -m unittest -q test_hallway.py`. `python hallway_model.py` displays the sample source-backed data. `index.html` is a self-contained interactive **manual choice interface**, not autonomous Jane; nothing persists across page reloads. No source corpus was modified. Tests are classical software validation, not demonstrated agent autonomy or recursive self-improvement.

## Next natural boundary

JANE 075 — Jane's unprompted direction. With a real scheduled runtime and bounded authority, collate an unchanged Hallway evidence bundle and test whether Jane itself can choose a direction, explain why, or abstain *without a human selecting the option*. Then compare decisions under reordered options, corrupted source metadata and missing evidence. Only run autonomous source retrieval with explicit authorized tools and scheduled service.