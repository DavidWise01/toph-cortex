# STOICHEION ISA-256.024 — Autonomous Counterfactual Agency / JANE IV

Date: 2026-11-06. One agent, one nursery. Freeze the 256 paired-axiom constitution and the existing 49,152 addressing positions; no new independent cryptographic witness stack.

## Natural invariant

`Observe -> Snapshot -> Branch Candidate Actions -> Restore -> Commit Exactly One -> Observe Outcome -> Correct Prediction -> Remember`

An experimental branch and the real game timeline must never be confused.

## Executable implementation

The complete executable bundle is provided as the conversation artifact `jane_isa256_024.zip`: 
- `index.html`: a minimalist black/crimson/amber NES training dashboard inspired by the instrument-heavy Rocky IV training lab aesthetic, with a large 256x240 NES display, simple controls, large live metrics, trace, graph and action rankings.
- `core.js`: deterministic observation, candidate scoring and update rules.
- `test_core.js`: 12 passed model unit tests.
- `browser.js`: extracted browser JavaScript for independent syntax verification.
- `README.md`, `manifest.json`: test caveats and SHA-256.

The dashboard loads user-supplied ROMs locally with JSNES 2.1.0, uses `toJSON/fromJSON` to restore before each candidate, suppresses branch frames from the actual display, and advances the real timeline only for the selected action. Bounds: 2–8 action branches, 3–32 frames/probe, 240 committed decisions/run. Export preserves separate `branch` and `commit` records. A RANGE benchmark world is included for UI testing without a ROM. Local saved learning is loaded only against a coarse ROM fingerprint.

## Tests and caveats

`node test_core.js`: **12/12 PASS**. `node --check browser.js`: **PASS**. Uploaded Punch-Out!! ROM header inspection: iNES, mapper 9, 262,160 bytes. **NES gameplay was not successfully tested in a real browser runtime during this turn**, so no claim of actual gameplay, emulator determinism, or learned fighting performance is made. ROM is user-provided and NOT committed to public GitHub.

Current action ranking favors pixel novelty, including center-region motion. That is a curiosity heuristic, not proof of causal understanding, player health, game progress, or victory. On-screen replay match is a coarse sampled-pixel determinism indicator. Future work should validate browser save-state fidelity and integrate game progress and safety proxies.

## Monitoring

Dashboard metrics: committed decisions, total branch trials, mean prediction error, pixel motion, replay match, visited screen/action memory states, predicted vs witnessed changes, ranked counterfactuals, evidence export. It only runs while the browser tab stays open. There is no background worker, unattended cloud process, or external repository mutation by the page.

## Next natural invariant

ISA-256.025 — measurable causal skill: introduce held-out checkpoint pairs with blinded action selection and a performance outcome independent of raw pixel change, validated against a fixed baseline. Prefer direct play evidence over more cryptographic witnesses.
