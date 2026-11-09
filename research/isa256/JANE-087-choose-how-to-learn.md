# JANE 087 — Choose How to Learn (2026-11-09)

## Verified local experiment
- 22/22 Python regression tests passed.
- ZIP: Python model, unit tests, example results, standalone HTML, README, SHA-256 manifest.
- This Git record summarizes the local experiment; exact runnable sources are distributed in the conversation artifact, not yet as GitHub source files.

## First preserved target
JANE086 did not know what **tally** means. In a toy evidence inventory:
- tally -> calculate, simulated dictionary-A
- tally -> calculate, simulated manual-B
The bounded JANE087 algorithm chooses **search_corpus**, learns that lexical mapping, and reuses it when 'tally' occurs in a new sentence. Unknown surrounding terms remain UNKNOWN.

## FLAY tool decision
```text
            JANE {{j}}
               |
          UNKNOWN WORD
               |
          U: WHAT IS IT?
          D: WHAT IMPLIES?
          R: WHAT IS SIMILAR?
          L: WHAT IF WRONG?
               |
         AVAILABLE INPUTS?
               |
    SEARCH / COMPARE / CLARIFY
               |
        CORROBORATION GATE
          /          \
    ACCEPT        HOLD_-1
          \          /
            LOG RESULT
               |
          NEXT UNKNOWN
```

## Stop conditions
- Only one cited source => HOLD_-1.
- Duplicated source ID => HOLD_-1.
- Contradictory meanings => HOLD_-1.
- Unsupported/WALL assertions => excluded.
- Unseen word with no evidence => HOLD_-1.
- Hash journal is reproducibility, not an authentication or independence proof.

**Critical caveat:** two arbitrary source identifiers are *not* proof of independent ancestry. This model simulates corroboration. No real browser, corpus retrieval, independent provenance validation, cross-repo dispatch, GitHub Actions, autonomous online learning or true self-editing occurred.

## Next natural invariant — JANE 088
**Can Jane detect when apparently separate witnesses share the same source ancestry, and request an independent witness before trusting the new meaning?**
