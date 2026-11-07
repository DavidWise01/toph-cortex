# STOICHEION ISA-256.031 — Self/Other Discovery and Remembrance

Date: 2026-11-07. **One agent, one NES nursery**. Historical ISA constitution and 49,152-address lattice unchanged.

## Natural invariant

**Motion is not self. Repeated action-dependent evidence may establish a controlled-region candidate, but memory alone must not certify present control.**

The visual model starts in CONTROL UNKNOWN. It restores one emulator snapshot for three 8-frame counterfactual trials: NONE, LEFT, RIGHT. It compares direction-specific coarse 16x15 screen differences against no-action, rejects missing, diffuse or spatially unrelated effects, and proposes a candidate bounding box only for overlapping localized differences. Two consistent probe outcomes are necessary to display a purple **JANE?** candidate box; this is not yet validated player identity.

Orange GOAL appears **only** after the operator marks a location on the NES screen. The earlier practice of treating maximum pixel motion as an inferred objective is removed.

The agent preserves a per-ROM local control-candidate history and user-marked goal. On reload, previously recorded geometry enters **REMEMBERED / UNVERIFIED**, with no premature purple overlay. Live re-probing can independently reconfirm a candidate. Historic screen corpus, title/defeat recovery and START behavior remain available. When the screen corpus identifies FIGHT, the local agent may schedule periodic control probes, not on TITLE/GAME_OVER.

## Local executable verification

- New self-discovery model: **12/12 Node tests PASS**
- Preserved semantic recovery: **16/16 Node tests PASS**
- Five inline scripts extracted and individually checked with Node syntax checker: PASS
- Browser end-to-end boot/Punch-Out!! probing remains **unverified** (sandbox browser navigation blocked or timed out; JSNES core not accessible).

The downloadable conversation package `jane_self_031.zip` contains `index.html`, `self031.js`, the two test modules, the retained semantics module and an SHA256 manifest. No copyrighted game ROM is published, and the full executable is not deployed by this specification commit.

## Critical epistemic boundary

A button-response region is a **candidate**, not confirmed ownership or object identity; camera scroll, HUD updates, animation, and coarse sampling may confound. A stronger follow-up must track sprite displacement, compare multiple fresh states, and reject global camera motion explicitly.

Next natural invariant: **ISA-256.032 — Persistent Object Identity and Active Control Disambiguation**. Pair frame-to-frame object tracks with causal probes, distinguish world movement from camera/HUD motion, and remember the identity as a defeasible hypothesis rather than a permanent label.