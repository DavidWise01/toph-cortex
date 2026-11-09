# JANE 096 — Look Ahead: Adaptive Budget Invariant

Date: 2026-11-09. Local executable experiment: **30/30 unit tests PASS**, JS syntax check PASS, ZIP integrity PASS.

## First distinction

Four equiprobable hypotheses `h0,h1,h2,h3` give initial Shannon entropy `H=2` bits. Total budget = 2 units.

- Cheap-A costs 1; predicts outcome partitions `{h0}|{h1,h2,h3}` yielding `0.811278` bits.
- Balanced-B costs 2; predicts `{h0,h1}|{h2,h3}` yielding `1.000000` bit.
- JANE095 gain-per-cost greedily selects Cheap-A but no further test is affordable. JANE096 finite adaptive planning selects Balanced-B and gains 1.0 expected bit.

## Counter-direction

Add Cheap-C (cost 1) with predicted partitions `{h1}|{h0,h2,h3}`. Full-budget adaptive planning chooses Cheap-A, then Cheap-C **only if** A yielded the remaining three hypotheses.

Expected information: `0.811278 + (3/4)*0.918296 = 1.500000` bits, exceeding Balanced-B's 1 bit. If Cheap-A identifies `h0`, it stops and conserves budget.

Thus neither "always cheap" nor "always expensive" is the invariant. The invariant is **expected total learning achievable under current resources, conditioned on possible outcomes**.

## First preserved -1

Scout packet `unverified-D` provides a two-entry outcome table for a four-hypothesis problem. The planner refuses to forecast `HOLD_-1: INCOMPLETE_OUTCOME_MODEL`. No missing outcomes or source independence are invented.

## Authority and limits

The hive submits packet predictions; **one Jane chooses**, with scout urgency excluded from the optimization objective. Scout packet receipt does not write Jane's retained memory. The model assumes a *uniform prior*, *deterministic outcome predictions* and *correct packet descriptions*; all are synthetic fixtures and not validated external facts. The algorithm is programmed rather than autonomously learned. No live agents, continuous runtime, cross-repo ACK or Github Pages deployment executed.

The offline viewer and README are in `research/isa256/jane096/`. Full executable Python source, 30 tests, JSON result, build script and SHA256 manifest are in the conversation ZIP `jane_096.zip`.

## Next natural invariant — JANE 097

Can Jane identify when a scout's **predicted test outcomes** are wrong, correct its estimate using real observations, and replan without letting the scout redefine Jane's question or force an unverified memory write?
