# JANE 068 — Branch Fitness and Conditional Promotion

2026-11-08. JANE {{j}} / root {{i}} / prim 10×5×4×3×1 = **600 logical addresses**.

## Frozen control and candidate routes

The previous JANE 067 numerical model, identical to JANE 065 baseline predictions, remains frozen. Original 45 mapped addresses; of the 555 previously free addresses, three candidate policies reserve 15 each. **90 mapped / 510 unassigned.** Reservations are logical routing metadata, not independent forecasters or physical cells.

- `scout_0`: blend 35% baseline, 65% latest observation.
- `scout_1`: blend 20% baseline, 80% seasonal observation 2 s prior (when available).
- `scout_2`: robust median-difference short-window extrapolator (clipped).
- Original: 45-leaf median forecast.
- Forecast horizon: **2,000 ms**, sampling **250 ms**, and no future inputs used to make an issued forecast.

## Measured blind-holdout results

Six synthetic scenarios, 30 new holdout seeds, 180 samples each, 5,160 settled forecasts per scenario; training seeds separate from holdout seeds.

| scenario | baseline MAE | scout 0 | scout 1 | scout 2 |
| --- | ---: | ---: | ---: | ---: |
| stationary | 0.081335 | 0.063586 | 0.051752 | 0.113952 |
| periodic | 0.251411 | 0.099491 | 0.062227 | 0.395545 |
| drift | 0.215151 | 0.189666 | 0.230787 | 0.256264 |
| step | 0.157553 | 0.133077 | 0.169900 | 0.179082 |
| bursty | 0.574405 | 0.526024 | 0.459848 | 0.592789 |
| autocorrelated | 0.511991 | 0.457591 | 0.270677 | 0.584351 |

All candidates have a notional 60 units per issued forecast vs baseline 45, a +33.3% budget increase, not a wall-clock runtime measurement. The predeclared promotion gate requires no MAE regression in any of the six environments, at least one MAE improvement >0.01, and at most 60 notional units. `scout_0` is the **sole qualifying candidate**, with no MAE regression across the six synthetic conditions.

Local execution: **13/13 Python tests PASS**, 600/600 prim-address roundtrip, standalone dashboard JS syntax PASS, ZIP integrity and SHA-256 manifest PASS. There is **no independent GitHub CI verification or real-world generalization guarantee**.

## Evidentiary limitation

The test suite itself was written by the developer of these experiments, and the candidate algorithms were specified in advance. This is **not** autonomous recursive self-improvement. The promotion is conditional on this small six-environment synthetic benchmark. No independent source verification, scientific emergence, tachyon communication, 600 real agents, or real-time timing guarantee follows. Stop-on-failure `−1` remains valid when its gate is applied.

## Status

Repository holds dashboard and README and this evidence record. The downloadable conversation archive is the exact locally verified Python source, tests and results.

**Next natural test JANE 069:** independent replication of the winning scout on new distribution shifts and real execution time; freeze and reject if it regresses.
