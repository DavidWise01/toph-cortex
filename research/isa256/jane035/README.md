# JANE 035 — Travelling Wave Closure

User geometry: one tensor, one Jane, one brace, two waldos `{-()+}`, one box, one toroid, 27 positions. Three ternary register labels (-1,0,+1) account for 27+3=30 counted components, **not** a 30-vertex ring. Wave envelope: `{([111222333444555555444333222111])}`. Seam: 27→27.5→1.

Run `python -m unittest -v` in this directory (26 tests), `python model.py`, or open `index.html` locally. No external dependencies.

**Finding.** With two waldos departing vertex 1 in opposing directions at one vertex per tick, each visits all 27 vertices. The local edge sensor notices an opposite edge swap on edge (14,15) at t=13.5 and swaps two signed wave payload pairs. Neutral components, 27-value stationary fields, waldo identities and total squared amplitudes remain unchanged. The positional state closes after 27 steps, whereas the original full registers return after 54 steps (two exchange events at t=13.5 and 40.5). The numerical squared-amplitude proxy is 741.3125 throughout. The 27.5 seam is an unoccupied transition marker, not a 28th vertex.

**Important caveats.** This is a classic synchronous discrete-event counterrotation model with a local edge sensor; its propagation speeds, swap rules, 27-cycle adjacency and 27/30 accounting are stipulated, not derived from particle dynamics. 'Travelling wave' means a traveling **carrier with a ternary wave register**, not a simulation of a wave equation. The 30-symbol palindrome is not mapped onto 27 positions and 3 register states. Therefore no physical quantum tunneling, self-organized wave propagation or biological homeostasis is established.

Next boundary: permit unequal local clocks, changing amplitudes and partial wave transfer; test conservation and exchange stability without an externally imposed exact one-step synchronization.