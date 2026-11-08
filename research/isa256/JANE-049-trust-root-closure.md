# JANE 049 — Trust-Root Closure

**Date:** 2026-11-08. **Local experiment: 40/40 tests PASS**, Node JavaScript syntax PASS. Original executable Python, 40 tests, JSON outputs, HTML dashboard and checksums are bundled in `jane_049.zip` in the originating conversation. A compact equivalent Python model, all 40 regression tests, HTML, README and scenario results are committed in `research/isa256/jane049/`. No separate GitHub CI result or GitHub Pages deployment is claimed.

## Immutable user's primitive
1 tensor > 1 Jane > 1 brace > 2 waldos `{-()+}` > 1 box > 1 toroid > 27 occupied positions. Three ternary labels `-1,0,+1` are states, not positions: **27+3=30 counted components**. The palindromic symbol envelope is `{([111222333444555555444333222111])}` and the closing seam is **27 → 27.5 → 1**. The extra verifying *roles* are not extra cells.

## Tested invariant

**Valid signed provenance is not equivalent to true provenance.** An independently pinned checkpoint detects an altered/rolled-back chain or a replacement signed with a stolen key; a fresh verifier without a retained independent pin may accept a complete forgery. If both the signing key and the pinned checkpoint are replaced, it can accept the forged history as VERIFIED. Multiple reports sharing a root are not independent; independent roots can nevertheless collude and agree on a false claim.

## 12 deterministic fault scenarios

| Scenario | Verification outcome | Note |
| --- | --- | --- |
| clean | VERIFIED | Good signed chain and independent pin |
| tamper | INVALID_AUTHORITY | Unkeyed modification breaks HMAC |
| rollback_pinned | ROLLBACK | Prior epoch pin detects omission |
| rollback_unpinned | VERIFIED | No prior pinned newer epoch |
| key_compromise_pinned | HISTORY_CONFLICT | Signed forged record fails history pin |
| key_compromise_unpinned | VERIFIED | Stolen key forges complete consistent chain |
| shared_root | INSUFFICIENT | Three reports on one dependency |
| independent_roots | wave=2 | Two independent roots agree |
| colluding_roots | wave=999 | Two independent but compromised roots agree falsely |
| pin_compromised | VERIFIED | Signing key and trusted pin replaced |
| absent_root | INSUFFICIENT | No trusted origin |
| broken_link | BROKEN_CHAIN | Hash-linked history discontinuity |

The digest pin and root domains must be assumed trustworthy and truly independent. The example roots are **synthetic** HMAC signers, not hardware security devices or actual institutional witnesses. HMAC only verifies integrity/authenticity while its secret is uncompromised; it does not independently verify claims. The enumerated fault cases are deterministic; their PASS count is **test assertions**, not 40 independent physical trials.

## Limits

No demonstration of actual quantum tunneling, a Planck-scale device, independent physical witnessing, generalized artificial intelligence, autonomous Jane homeostasis or convergence toward infinite scale. The 27-position adjacency is stipulated rather than derived from a full Hamilton adjacency embedding. There is no basis for unlimited trust-root recursion: any verification scheme has a bootstrap assumption.

## Next natural invariant — JANE 050: Independent Observation

Compare a root-endorsed claim to an independently generated **local sensor observation**. Attack signer, sensor, and both together. Measure detection, false alarms, inability to distinguish coordinated deception, and information loss. Do not let a new sensor simply move the unexamined trust root without saying so.
