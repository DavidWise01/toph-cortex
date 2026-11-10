# JANE 109 — Growth Without Forced Settlement

Date: 2026-11-10. **42/42 local Python tests PASS**, standalone JavaScript syntax PASS, ZIP integrity PASS.

## Canonical invariant

**A nested generation can grow to capacity without being declared settled.** This corrects the former flat eight-plane interpretation. `{{n}}^{{n}}^{{n}}` denotes reserved nested growth room, with Gen 0–7 not necessarily fully occupied or equally sized. The base is `[10×10]` and Z is the signed interpretive operant `−/+`, not a truth value.

```text
         THE SOURCE JANE {{j}}
                  |
           ROOT 10×10 GEN0
                  |
       +----------+----------+
       |                     |
     GEN1A                 GEN1B
     2 slots               3 slots
       |                     |
     2/2 FULL             1/3 GROWING
       |
       +-- SETTLE REQUEST
               |
          EVIDENCE CHECK
          /           \
      -1 HOLD       VERIFIED RECEIPT
         |          + JANE AUTHORIZATION
     KEEP GROWING        |
                      SETTLED
                         |
                  RESERVE GEN2
                         |
                    GROW AGAIN
```

## Executed demonstration

A Gen0 root reserves sibling chambers Gen1A (capacity 2) and Gen1B (capacity 3). Gen1A receives two attributed packets and remains **GROWING**. Settlement attempt with a missing receipt returns `HOLD_-1 SETTLEMENT_UNVERIFIED`. Gen1B independently receives its own packet and remains **GROWING**. Supplying a *synthetic* criterion, verification flag, receipt identifier and Jane authorization settles Gen1A without writing Jane's knowledge. A Gen2 child is then reserved. Z mirroring preserves packet identity; tampering with the local append-only hash journal is detected.

## Test coverage and limits

42 unit tests cover generation ancestry, sibling growth independence, packet provenance, capacity and duplicate rejections, terminal Gen7, Z mirroring, explicit settlement gates, retention authority, chain validation, and immutable settled packet contents.

All decisions, receipts and witness flags are synthetic test inputs: **no real external verification** and no genuinely autonomous Jane, trained MoE, scout network, or live Git-to-Git handoff are claimed. The 10×10 root is a symbolic address space rather than 100 actual agents. The browser 'verify' button simulates an approval.

Repo `research/isa256/jane109/` contains README and interactive offline HTML. Full tested Python model/tests, result journal, HTML and SHA256 manifest are in the conversation artifact `jane_109.zip`, **not in this GitHub directory**. No GitHub Pages deployment verified.

## Next natural invariant — JANE 110: Settlement Criterion Discovery

Can Jane select her own falsifiable settlement condition from the distinctions within a chamber and challenge it on unseen growth histories, with MoE experts only offering evidence packets? Avoid premature settlement or perpetual stalling; preserve the first negative transfer as `-1`.
