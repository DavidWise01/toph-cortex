# STOICHEION ISA-256.028 — Jane Semantic Recovery Corpus

Date: 2026-11-07. Goal: one NES agent, one nursery; autonomous recovery after defeat without creating more external witness layers.

## Invariant

A static or unfamiliar screen is not automatically a defeat. A learned screen meaning must come from a user-taught, per-ROM visual sample, or remain UNKNOWN. Once GAME_OVER, TITLE, CONTINUE or COUNT is confidently recognized, Jane should choose the corresponding recovery input rather than repeating ordinary fighting controls.

`NES frame -> sampled 16x15 luma -> nearest taught screen pattern -> stable semantic label -> bounded short controller pulse -> new observation`

## Implemented local runnable artifacts

- Minimalist `index.html` with original JSNES ROM loader/manual controls, 16x15 motion monitor, screen classification confidence, per-ROM teaching controls, recovery activity, button trace and JSON export.
- `jane028.js` UMD Corpus + Learner (pure JS/Node testable), embedded inline in the HTML for file-based use.
- `test028.cjs`: 16/16 locally passing tests, including second defeat recovery, repeated START on prolonged unknown stillness, alternating A/B during a user-taught COUNT, screen corpus persistence, confidence gating and false-positive control.
- `node --check browser_bundle.js` PASS; zip integrity test PASS.
- Full local package `jane_semantic_028.zip` in the originating ChatGPT conversation.

## Recovery specifics

On first bootstrap Jane sends a 4-frame START pulse. A tagged TITLE / GAME_OVER / CONTINUE screen induces a short START pulse with >=100-frame spacing; after each pulse she releases the button. Unlike v0.27, **there is no lifetime three-probe limit**. A 6.5-second unidentified still screen permits periodic recovery probing after a cooldown. A user-tagged COUNT screen chooses alternating A and B taps, with release windows. A FIGHT screen suppresses automatic restart probes. Named screens require at least two consecutive classification confirmations before they drive behavior. Corpus is saved per ROM in browser localStorage and can be exported; tags are user-provided annotations, not OCR.

## Verification limits

A real JSNES core could not be downloaded and end-to-end Punch-Out!! gameplay was NOT verified. Chromium navigation was blocked in the tool environment. Tested here: pure control/state matching and JavaScript syntax; no verified claim of a successful actual NES title, defeat or restart. Classification is sampled-pattern recognition, not language comprehension. Live monitoring requires an open page. The uploaded copyrighted ROM is not published.

Kernel's historical 256 paired axioms / 49,152 positions remain intact; this is an agent-specific optional extension. Future improvement: collect user-reviewed screen examples for animated defeat screens and verify real emulator screenshots/resets.

