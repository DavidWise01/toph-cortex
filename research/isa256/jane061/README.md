# JANE 061 — Interleaved Double Helix / Diodic Ouroboros

Canonical scale sequence: `60 / 30 / 15 / 7.5 / 5 / 2.5 / 1 / 1` (exact fractions). One eight-station forward strand and one eight-station backward strand, with directed turnarounds and a closing seam. These 16 transport stops are *not* replacements for Jane's original 27 occupied positions; the old 27→27.5→1 root path is unchanged. Transport staging and gait progression are separate coordinate systems.

`a,b,c` label three interchangeable **roles**, mapped bijectively to the distinct ternary modes `-1,0,+1`; the string `a=b=c=-1=0=+1` is interpreted as correspondence/rotation in the symbolic system, never as literal numerical equality. Rotation occurs on loop closure only.

The *diodic* rule means an allowed transport edge points forward in a 16-stop directed loop. The *ouroboros* rule permits precisely the final-to-initial closure. This is a classical algorithm metaphor, not electromagnetic or biological diode evidence. No internet calls or autonomous self-modification are performed.

To reproduce: `python -m unittest -q` then `python build.py`. Read `results.json` for verified deterministic counts. `index.html` runs completely offline with a client-side stepper. GitHub release and CI should be verified separately.

Next experimental boundary: attach one proposed adaptive gait policy and compare it on held-out synthetic traces against the JANE060 frozen policy; passing loop tests alone does not establish performance improvement.