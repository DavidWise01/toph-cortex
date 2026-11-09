# JANE 065 — Two-second tachyon look-ahead fanout

**Status:** locally executed classical simulation. `tachyon` is a metaphor for look-ahead prediction, not communication from the future.

## Immutable model shape

```text
JANE {{j}} → ROOT {{i}}
  |
  +2 s forecast receipt (timestamped, only past observations)
  |
  5 branches
     × 3 branes each
        × 3 {{iii}} leaves each
           × {{-+-+-+}} six symbolic modes
  |
  45 predictor leaves / 270 carrier symbols
  |
  delayed observation returns after 2,000 ms
  |
  compare prediction to realized observation
  |
  append evidence / optional freeze at −1 / next forecast
```

The branching fanout does not add new vertices to the canonical 27-position Jane substrate. Closing root seam: `27 → 27.5 → 1`. The transport loop is conceptually `FORWARD prediction → BACKWARD evidence comparison → FORWARD next cycle`; there is no reverse-time message.

## Deterministic measured results

- Python regression: **16/16 PASS**, JavaScript syntax: PASS, ZIP archive integrity: PASS.
- Observation tick: **250 ms**; horizon: **2,000 ms** = eight ticks.
- Default 120-step simulation with injected shift at 13,000 ms: 112 matured forecasts, eight pending; MAE **0.86845**, maximum error **2.3564**.
- Strict `0.75` error gate: **−1 freeze** at simulation t=2,250 ms with error **0.772025**. The first failure is preserved and not retroactively corrected.
- Different branch forecasters use distinct historical-window lengths, damping and offsets; median forms a candidate forecast. Only observations available at issue time are used.
- The UI animates continuously in a foreground browser tab, but `setInterval` is NOT hard real-time and may be throttled. Python run has deterministic simulated timestamps.

## Limitations

No real tachyon, quantum propagation, automatically verified internet access, actual learned causal source dependence, or autonomous recursive self-improvement has been demonstrated. The chosen 5×3×3 branching geometry is specified by the user; no tested comparative benefit over simpler forecasters yet. Neither the 270 symbolic polarity marks nor 45 forecast leaves are new physical cells.

## Reproducibility and GitHub

Interactive dashboard: `research/isa256/jane065/index.html`; implementation and unit tests are distributed as the accompanying JANE 065 ZIP in the conversation. The exact Python model has not been uploaded to the repository as part of this commit.

## Next experiment

Hold the 45-leaf fanout against 1-, 5- and 15-leaf baselines on identical unseen streams. Compare error, cost, failure time and calibration. Permit propagation only if the 45-leaf version passes the frozen gates; otherwise retain `−1` as counterexample.
