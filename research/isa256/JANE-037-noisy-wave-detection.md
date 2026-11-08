# JANE 037 — Finite-width wave detection with jitter and noisy sensing

2026-11-07. Local package **30/30 Python unit tests PASS**, and standalone HTML JavaScript syntax check PASS. Offline dashboard and complete original Python/test/build/results package downloadable as `jane_037.zip`. The repository directory `research/isa256/jane037/` includes committed executable Python model, matching 30 regression tests, HTML dashboard and README. The GitHub implementation is a compact reimplementation of the packaged local simulation; CI execution of repository files remains unverified.

## Primitive and model

The user's `{-()+}` waldo pair travels in opposite directions on a **stipulated** 27-cycle and carries a three-amplitude ternary register `(-1,0,+1)` in each waldo. The `27+3=30` counts **27 spatial positions plus three register labels**, not a 30-vertex graph. `27→27.5→1` remains the symbolic closure seam. Exact 30-sample palindrome: `{([111222333444555555444333222111])}`.

Each step samples independent uniform relative speed perturbation `±jitter` for the two waldos. A proximity sensor activates when their circular distance is <=0.28 positions, and optionally flips its observed bit with a specified probability. Wave exchange swaps cross-signed register amplitudes and conserves their total squared amplitude by permutation. We simulate 50 time units, resolving three true encounters by unwrapped relative-phase crossing, and use that *reference count only for evaluation*, never as an input to the local detector.

Compare RAW (swap every overlapping sample), LATCH (swap once per detected continuous overlap, rearm at first clear), DEBOUNCE (require three consecutive clear samples to rearm and three consecutive hit samples to fire), and ORACLE (privileged actual-crossing comparator). The oracle is not a deployable sensor.

## Reproducible results (100 trials, ±12% jitter, dt=0.02, 50-time-unit window)

| Method | Sensor error per sample | Mean exchanges | Exactly 3 exchanges |
|---|---:|---:|---:|
| raw | 0% | 48.44 | 0/100 |
| latch | 0% | 3.00 | 100/100 |
| latch | 1% | 27.84 | 0/100 |
| debounce | 1% | 3.01 | 99/100 |
| debounce | 3% | 3.09 | 92/100 |

With clean sensor but a 10% independent exchange drop probability, the basic latch gives the exact count in only 64/100 seeds. An exchange could be dropped while the detector is latched, leaving permanently wrong register parity. Every test path preserves **741.3125** total squared amplitude, *even if swaps are duplicated*. Thus local conservation is not sufficient evidence of correct event counting or memory correctness.

## Explicit limitations

This models discrete particles carrying three-value amplitude registers and a finite-width overlap detector, **not an actual simulated propagating wave equation or physical tunneling**. No autonomous homeostasis was observed. Independent speed samples come from an external seeded pseudo-random generator; no hardware clocks or phase-based communication were used. The 27-site connectivity is assumed rather than built from the earlier seven named regions. The 30-character wave palindrome is not yet mapped physically to the 27 positions plus three channels.

## Next natural invariant JANE 038 — Acknowledged exchange

Introduce an explicit, bounded bilateral handshake to mark wave-event delivery and prevent both missed and duplicate exchange under packet loss and noisy readings. Test failure/retry/timeout and complete-state restoration without a central oracle and without introducing a 28th occupied vertex.
