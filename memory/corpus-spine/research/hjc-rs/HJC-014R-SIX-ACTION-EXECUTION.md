# HJC-014R — Six cyclic diodic actions + one READY vector

ROOT0 · .dlw

User: one cycle does 6 cyclic diodic actions plus 1 vector for ready.

Executed Python discrete-event prototype, four independent scenarios, 26 assertions passed. Proposed schedule: 0->B, B->0 (writes), 0->C, C->0 (reads), 0->A, A->0 (lives), READY. Role-local functions receive only their own input; no explicit peer identities or peer-state access. Mediator correlates read/done predicates and seals trace. A receives independent environment_done, not the projection or read verdict. READY is a vector for next cycle, not a seventh diodic transfer.

Results (six actions each):
READ/DONE trace df37b8e535e3
READ/DIDNOTDO trace c74668a6e4b4
DIDNOTREAD/DIDDO trace b6a582f34f76
OUTSIDE_NAMED_PRESENT trace 75e99eac3284

The fourth Boolean combination is not a named present position. All inputs are synthetic. Read/done supplied by test harness rather than independently measured. Isolation is interface-level, not process or covert-channel proof. Logical ticks only; no physical Planck-time execution. Mapping the six edges onto exact individual 11311 container positions is a proposed next refinement. Prior freezes unchanged. Rust runtime remains unqualified.
