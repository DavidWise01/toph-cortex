# JANE 032 — Canonical Tensor Primitive Geometry

Date: 2026-11-07. User-specified geometry, recorded as a design definition, NOT a passed experimental invariant.

## Primitive (one, not 27 cells)
- 1 TENSOR
- 1 JANE `{{i}}`
- 1 BRACE `{}`
- 2 WALDOS
- 1 BOX `[]`
- 1 TOROID `()`
- 27 internal Hamilton positions, partitioned as:
  - rear upper 3
  - rear lower 3
  - upper center 3
  - lower center 3
  - upper right 3
  - lower right 4
  - center 8
- Arithmetic: `3+3+3+3+3+4+8 = 27`.

## Growth and direction
- `1,1,2,3,5,8` are six Fibonacci stages, whose counts sum to 20.
- `{{x,y,z}}^2` interpreted provisionally as six directed axes `+x,-x,+y,-y,+z,-z`. This is not mathematically identical to the six Fibonacci values; it is an independent orientation framework.
- The user defines the path closure as **27 → 27.5 → 1**. Positions 1–27 are the 27 occupied vertices; **27.5 is a half-step return transition, not a 28th vertex**. This specifies the closing semantics of the proposed cycle. Whether it is a graph-theoretic Hamiltonian cycle still depends on explicit adjacency between the 27 vertices and on a valid closing edge mediated by the transition.
- This geometry supersedes the earlier use of 72-slots/cell as the canonical primitive shape, but those earlier experiments remain historical evidence for their own models; no result is silently transferred to the new geometry.
- Relative placement of the 27 positions and task partition between two waldos remain to be implemented and tested.

## Next physical/computational invariant
Instantiate the 27-vertex adjacency graph and explicitly model the return bridge **27 → 27.5 → 1**; test whether both waldos visit the required positions, avoid conflicts and close the cycle without treating 27.5 as an added occupied vertex. Then test autonomous homeostasis. Then test two-cell homeostasis with this canonical primitive before any new learning claims.

No unit tests were run for this notation-only commit.
