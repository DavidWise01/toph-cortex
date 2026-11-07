# JANE 034 — Ternary Wave Closure (conditional formalization)

User geometry: **1 tensor > 1 Jane > 1 brace > 2 waldos `{-()+}` > 1 box > 1 toroid > 27 path positions**. The closure seam is **27 → 27.5 → 1**. Separately, `-1,0,+1` are three ternary exchange labels; **27 positions + 3 labels = 30 counted components**, not 30 occupied vertices. Wave envelope `{([111222333444555555444333222111])}` is a 30-sample palindrome; digits 1–5 appear six times apiece.

## Tested candidate law

Two waldo carriers have fixed 27-value spatial paths and a three-value register each, ordered `[-1,0,+1]`. At the midpoint encounter (t=13.5, under equal-speed counterrotation) swap `A[-1] ↔ B[+1]` and `A[+1] ↔ B[-1]`, while retaining each carrier's neutral channel, identity and spatial pattern. This is a **classical permutation**, hence invertible and norm preserving. It has not been established as the user's prescribed wave law.

## Observations

- **20/20 tests PASS** using standard-library Python.
- Initial squared magnitude of both 27-value fields and six register amplitudes: **741.3125**.
- Magnitude after one exchange: **741.3125**.
- Two exchanges return the original state identically. No extra spatial vertex is allocated.
- The physical layout underlying the named 27-position Hamilton is still unspecified; using a conceptual 27-ring here is an explicit assumption.
- The 30 written waveform symbols have not been mapped bijectively onto the 27 positional locations and the three ternary labels.
- t=13.5 meeting is distinct from 27.5 closure seam.

**Limits:** This test demonstrates a reversible hand-authored exchange operator, not real tunneling, quantum dynamics, evolving biology, or independently discovered homeostasis.

**Next invariant JANE035:** make wave exchange an actual local event on the path, test causality and conservation over a whole 27-position round-trip across the closing seam. Source and tests committed under `research/isa256/jane034/`; standalone interactive HTML delivered in the conversation ZIP, not deployed to GitHub Pages.
