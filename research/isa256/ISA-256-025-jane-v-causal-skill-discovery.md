# STOICHEION ISA-256.025 — JANE V Causal Skill Discovery

**2026-11-06 | One agent, one NES nursery | Local implementation: 28/28 tests PASS**

## Natural invariant

**An observed screen change is not evidence of a useful action until it is compared with a matched no-action counterfactual.**

`CausalScreenEffect(action,S0,goal) = ScreenProxy(restore(S0);action) - ScreenProxy(restore(S0);NONE)`

The engine restores the same JSNES state for every action and the no-action reference. Branch outcomes remain experiments, while exactly one chosen action is committed to the actual timeline. The 256-axiom constitution and 49,152 lattice addressing positions remain frozen.

## Implemented

The downloadable conversation artifact `jane_isa256_025.zip` includes:
- `index.html` minimalist Rocky-IV-era laboratory telemetry dashboard (no movie assets);
- `core025.js`: no-action baseline, three screen-outcome proxies, causal effect ranking, train/holdout separation and skill retention;
- `test_core025.js`: 16 new passing tests, alongside 12 retained .024 tests;
- `core.js`, `test_core.js`, `browser.js`, `README.md`, test output and per-file hashes.

The dashboard now shows EFFECT / NONE, HOLDOUT WINS and RETAINED SKILLS. Training chooses among matching branches by observed proxy effect. Every fifth decision is a held-out choice from previously learned training effects, **without using current branch trial outcomes to choose the action**. A skill is retained after three positive unique training checkpoints and two distinct positive held-out checkpoints for the same action/goal; evidence cannot be reused across train/holdout. Learning state is keyed to full ROM SHA-256 in local browser storage; the ROM itself is not included.

## Verification and limits

`node test_core.js` 12/12 PASS; `node test_core025.js` 16/16 PASS; `node --check browser.js` PASS.

**Live emulator and browser gameplay NOT verified**: environment policy blocked Chromium navigation even to local files / localhost. No claim of trained Punch-Out!! prowess, win rate, source-accurate progress, or emulator save-state fidelity is supported.

The measured objective is still a **screen-change proxy**, not player health, score, victories or semantic game progress. Three hypotheses are exploration (pixel novelty), stabilization (less motion), and center-screen movement. Positive proxy effect does not necessarily imply improved gameplay. The current holdouts are distinct checkpoints in a session, not independent held-out game runs. Future causal skill evaluation needs a separately calibrated and verified progress signal and independent replays.

## Next natural invariant

**ISA-256.026 — Goal-Grounded Progress and Skill Transfer**: explicitly calibrate health/score/round/terminal screen observations, compare frozen skills with no-action or randomized policies on disjoint save-states and new encounters, and preserve automatic acceptance only upon improved real game outcomes. No new witnesses or axioms required.
