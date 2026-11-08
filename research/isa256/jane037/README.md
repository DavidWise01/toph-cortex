# JANE 037 — Clock Jitter and Finite-Width Wave Detection

Canonical primitive: 1 tensor > 1 Jane > 1 brace > two waldos `{-()+}` > one BOX > one TOROID > 27 occupied positions. The ternary labels -1,0,+1 are 3 additional register labels, **not extra vertices**. 27 → 27.5 → 1 remains the symbolic path seam. The exact 30-symbol palindromic envelope `{([111222333444555555444333222111])}` remains unchanged.

This is a **classical discrete stepping experiment**, not physical quantum tunneling. Each waldo moves around a 27-ring with individually sampled uniform speed variation. A finite-width overlap region detects their encounters, with optional sensor-bit errors and dropped exchanges. Unwrapped relative phase supplies a reference crossing counter for *evaluation*, not to the real local detector. The two signed registers exchange by an involutive permutation; the neutral channel and both 27-value stationary fields are retained.

A key boundary: raw overlap causes repeated swaps during a single finite-width pulse; a one-shot latch works when the sensor is clean but is vulnerable to a single false-clear reading. A three-consecutive-sample exit/entry debouncer resists isolated false readings but can still fail when noise persists or an exchange is dropped. Tests cover energy/identity retention, reproducibility, drop, input validation and comparisons.

Run `python -m unittest -q`, `python model.py`, `python build.py`. Open `index.html` without a web server. The HTML is a measured-results viewer, not a live agent.

**Reference results** over 100 seeds, jitter ±12%, width 0.28, step dt 0.02, simulated 50 time units (three reference crossings):

- No sensor noise, raw overlap: mean 48.44 exchanges, 0/100 exact.
- No sensor noise, latch: 3.00, 100/100 exact.
- At 1% sensor flip chance, latch: 27.84 mean, 0/100 exact.
- At 1% sensor flip chance, three-sample debouncer: 3.01 mean, 99/100 exact.
- At 3% sensor flip chance, debouncer: 3.09 mean, 92/100 exact.
- With 10% exchange drops, even otherwise clean latch had only 64/100 exact counts.

Total squared-amplitude proxy = 741.3125 throughout because swaps only permute channel values; it would stay conserved even if the detector makes extra swaps. **Energy preservation is not sufficient for correct exchange count or correct memory.** The full 27-position spatial seam is stipulated rather than independently reconstructed from the seven named positional groups. No autonomous homeostasis is demonstrated.

**Next boundary:** local acknowledgement/sequence marking to detect and retry dropped exchanges without global counting; prove that recovery from a missed exchange does not create a duplicate.