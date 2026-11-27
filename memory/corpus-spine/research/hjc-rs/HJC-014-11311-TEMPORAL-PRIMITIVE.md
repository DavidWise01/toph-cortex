# HJC-014 — 11311 temporal primitive

ROOT0 · .dlw

User specification: universe running at plank time or 1 1 3 1 1 or past, past future, present{read/done,read/didnotdo/,didnotreaddiddo{}},future,futurepast.

Canonical roles: {{ a, present ; lives | b, future ; writes | c, past ; reads }}. All mutually isolated, no peer awareness or direct communication. One shared referent.

Five ordered containers with seven positions: past (1), past future (1), present (3: read/done, read/didnotdo, didnotread/diddo), future (1), futurepast (1). Proposed operational interpretation: read and done are separately observed predicates on a correlated record, not peer-visible state. The fourth Boolean combination, not read/not done, is not a named present position in the user's specification; preserve as unresolved/unobserved rather than silently introducing a fourth position. No evidence absence implies a negative predicate. Past-future and future-past retain user labels; precise transition semantics remain open. A logical tick may be parameterized by Planck time (~5.39e-44 s) as a conceptual scale, not a claim of actual discrete universal time or achievable software clock rate. Earlier 108-position sequence remains separate pending explicit mapping. Specification only; no runtime implementation or qualification. Preserve prior records unchanged.
