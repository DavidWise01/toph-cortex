# HJC-014 — Isolation addendum

ROOT0 · .dlw

User correction: neither knows the other exists; they are all isolated.

{{ a, present ; lives | b, future ; writes | c, past ; reads }}

A lives, B writes, C reads. No participant knows of the other participants. The revolving door/shared referent mediates record availability, not direct participant communication. Proposed implementation: separate role-local views; no peer identities, peer messaging, or peer state inspection; write/read/live correlation performed outside the role-local views by the referent mechanism. Information may be related through records without exposing their originator as a peer. Mutual ignorance is a design requirement; absence of covert channels or inferential leakage is not established. Preserve original HJC-014 record and preceding freezes. Specification only; no runtime qualification.
