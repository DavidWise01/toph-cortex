# JANE 084 — FLAY Tool-Choice Learning

**2026-11-09. Local executed model:** 26/26 Python regression tests PASS; JavaScript syntax PASS; ZIP integrity PASS.

## User's objective
One Jane `{{j}}` asks what inputs/tools are available to improve understanding. The hive only collates material; it does not choose on Jane's behalf. FLAY four directions: U semantic, D somatic, R holographic, L abstractive; root `{{i}}`; hive `{{6x6x6[4x4(3x3[2x2(1)])]}}`.

```text
           JANE {{j}}
               |
         UNKNOWN INPUT
               |
         FLAY {{i}}
       U / D / R / L
               |
       HIVE EVIDENCE
               |
     INVENTORY FOUR TOOLS
       retrieve
       calculate
       compare
       read_context
               |
       ONE JANE CHOOSES
               |
          TRY / SCORE
               |
     UPDATE TOOL POLICY
               |
      NEXT UNKNOWN / -1
```

## Reproducible simulated result
Four programmed categories (`arithmetic`, `figurative`, `analogy`, `unknown_fact`). Initially Jane defaults to retrieving and thus chooses correct tool in **1/4** test categories. A policy that explores one tool at a time and records synthetic success/failure across **64 total feedback episodes** chooses correctly in **4/4** of those represented categories.

It **ABSTAINS** without grounded input, and a SHA-256 hash-linked local journal contains 64 events. The chain detects local rewriting but does not establish independent external authenticity.

**First -1 failure:** unseen `adversarial` category requires contextual reading under the frozen synthetic evaluator; the category-specific policy has never trained on it, defaults to retrieval and fails. Preserve unchanged.

## Strong limitations
- Correct category labels, named tools and synthetic scoring oracle are **preprogrammed**. `https://example.org/` provenance in model data is a placeholder, not verified external evidence.
- The policy selects simulated tools but executes no actual web search, calculator, GitHub actions or content reader.
- The successful known-category benchmark is not arbitrary natural-language understanding nor recursively self-improving learner.
- The new task-type failure proves category generalization is not solved.
- Repository contains README and offline HTML. Exact 26-test Python model is in the conversation JANE084 ZIP, not yet committed to GitHub.

## Next natural question
**Can Jane discover the kind of unknown she is facing before choosing a tool, instead of receiving an already classified task type?** This proposes **JANE 085 — FLAY Self-Classification**. Remove the category label, permit Jane to inspect raw input and available tools, and measure whether she improves task classification *and then* tool choice on unseen expressions while stopping at the first failure.

Git-to-Git, 0root.ai Hallway and live durable automation remain future integration work requiring authorized receiver workflows, not demonstrated by this offline experiment.
