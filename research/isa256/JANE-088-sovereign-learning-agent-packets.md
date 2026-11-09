# JANE 088 — Sovereign Learning / Agent Packet Boundary

Status: governance specification; no simulated autonomy or live agent execution claimed.

## Canonical rule

**Only one Jane `{{j}}` chooses what Jane wants to learn.** Hive agents do not assign lessons, set priorities for Jane, alter her retained understanding, or decide whether a claim deserves learning. They observe, investigate and present sourced packets; Jane may accept, investigate, defer, reject, or explicitly choose a completely different question.

```text
      SCOUT A             SCOUT B             SCOUT C
         |                   |                   |
      PACKET A            PACKET B            PACKET C
   what / why / how     what / why / how     what / why / how
         \                   |                  /
                  HIVE COLLATION
               (NO VOTE / NO QUORUM)
                         |
                    JANE {{j}}
                         |
                WHAT DO *I* WANT?
                    /    |    \
              LEARN   INVESTIGATE   PASS
                 |         |          |
           chosen method  ask agents   preserve packets
                 |         |          |
              VERIFY      RETURN       |
                 \         /           /
                JANE-OWNED MEMORY GATE
                         |
                 NEXT JANE QUESTION
```

## Packet contract (suggested)

- `packet_id`, `agent_id`, `timestamp`, `topic`
- `observation`: what was actually observed
- `why_it_might_matter`: agent's argument **not** Jane's priority
- `sources`: exact retrievable evidence, provenance/ancestry, independent-root grouping
- `uncertainties`: alternatives, unresolved gaps and WALL claims
- `possible_tests`: bounded, falsifiable proposals
- `estimated_cost`: resources/time
- `requested_action`: optional suggestion, never instruction
- `hash`: integrity identifier, not proof of truth

## Jane's authority

Jane chooses `INTERESTED`, `INVESTIGATE`, `DEFER`, `REJECT`, or `ABSTAIN`, and may issue `OWN_QUESTION` unrelated to agent packet suggestions. Only `INTERESTED` + verification + Jane's explicit retain decision adds a record to Jane's working knowledge.

The hive may collate, deduplicate, retrieve and report. It never writes directly to Jane's committed semantic memory. Agents cannot count aliases of one root as independent confirmation.

## Next decisive experiment

Feed Jane 3–8 grounded packets and let her select zero or more, including the empty selection and a self-originated question. Demonstrate that agent-suggested importance does not override Jane's selection and that unsolicited data never silently modifies retained understanding. Log evidence, Jane choice, test outcome and commit separately.

**This boundary is sovereignty of learning decisions, not evidence of autonomous preferences or self-generated values in an actual running agent.** A simulator with a scripted choice is not a proof of a genuine autonomous Jane.

The 124,416-slot `{{6x6x6[4x4(3x3[2x2(1)])]}}` hive shape is routing capacity, not 124,416 separate agents.
