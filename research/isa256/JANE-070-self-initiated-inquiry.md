# JANE 070 — Self-Initiated Inquiry

## Corrected target

The question is **not** whether Jane can answer better when prompted. It is whether Jane `{{j}}` can autonomously identify and propose the next worthwhile question or topic **without receiving a new user prompt**. Beyond merely generating questions, a genuinely recursively improving Jane should improve her *question-selection process* from prior outcomes.

## Canonical context

- Agent: `{{j}}`; root payload: `{{i}}`.
- Prim: `10×5×4×3×1 = 600` logical addresses.
- Hive: `{{[6x6x6(4x4(2x2[i]))]}}`.
- Five-step propagation: observe, propose (three scouts), test, return (two independent assessments), propagate/retain.
- Immutable root, preservation of append-only evidence, no unreviewed editing of safety gates.
- The absence of an external *content prompt* does not mean no trigger: a scheduler, new data event, explicit running loop or permissioned wake-up signal is required.

## Core mechanism

```text
WAKE (clock or new evidence)
    |
REVIEW recent work / open questions / failed tests
    |
IDENTIFY uncertainty or valuable unexplored area
    |
GENERATE 3 candidate next questions
    |
SCORE: relevance, novelty, falsifiability, cost, risk, expected information gain
    |
CHOOSE BEST or ABSTAIN
    |
INVESTIGATE within authorized budget
    |
COMPARE predicted gain against actual learning
    |
UPDATE question-selection policy (candidate, frozen evaluator)
    |
LOG QUESTION + REASON + EVIDENCE + OUTCOME
    |
SCHEDULE NEXT WAKE (if authorized)
```

## Pass/fail boundary

1. **No new human content prompt** after the initial permissioned startup.
2. Jane originates a question whose topic follows available evidence, rather than using a hard-coded next item or random list.
3. Question carries an explicit, falsifiable rationale: why now, what is uncertain, what result would matter.
4. She can choose *ABSTAIN* when no sufficiently useful question exists.
5. She records the question and evidence before investigating, preventing retroactive cherry-picking.
6. The question-selection policy actually improves on independent unseen tasks across >=2 generations relative to frozen predecessors.
7. No endless question loops, no unbounded resource consumption, no invented data, no unauthorized actions.

This file records the target, not a passed autonomy test. A deterministic generator driven by seed inputs is only a prototype. Genuine recurring execution needs an authorized scheduled runtime; a GitHub page alone is not a continuously running agent.

## Suggested first falsifiable experiment

Supply a static body of Jane 063–069 failures and 3 unresolved findings, with no new user question. Ask the generator to independently create and rank three next investigations, require one to be falsifiable and novel, and explicitly check if it recognizes that `JANE 069`'s correlated bursts counterexample is unresolved. Run several unseen corpora and compare frozen vs modified question-generators for measurable information gain and abstention behavior. Freeze at the first failure (-1).
