# Decision 0002 — Goal pivot (Ahmed, 2026-10-15, after EXP-02)

**Ahmed's words:** "lets piviot the goal, the experment goal is build the smallest possible creature
with braincells similar to humans, the EBM goal (memic how braincells learn, connect, fucntion, die
and get born)".

## The two goals from now on
1. **Experiment goal:** build the smallest possible creature whose brain is made of cells that
   behave like human brain cells.
2. **EBM goal:** each small energy-based model mimics how a brain cell learns, connects, functions,
   dies and gets born.

The previous framing (`RESEARCH-PLAN.md` §1, H1–H5; `IDEA.md`) is not deleted: it is the parent idea
and the long arc. The hypotheses are to be re-derived from the two goals above before EXP-03.

## Verdict on EXP-02 under the new goals (what it established)
- **Learn:** demonstrated. The weights change with experience and the changed weights carry the skill
  (frozen day-5 brain forages; birth brain starves; mirrored antennae kill it). `findings/02`.
- **Function:** demonstrated (three actions driven by energies over smells).
- **Connect:** present in the code (u: sense→unit, v: unit→action) but not needed by the current
  world; the linear weights carried the win. Needs a world that requires a conjunction.
- **Get born:** placeholder only (v = 0 units added on eventful days; A3/A10).
- **Die:** not implemented.
- Limits that carry over: learning is not monotone with experience (day-15 brains transfer worse than
  day-5); the policy-gradient rule changes weights without learning.

## What the new goals change next (for Ahmed to confirm)
- The unit of study becomes the **cell** (one small EBM) and its lifecycle, not the whole policy.
- Growth and death need real rules with controls (R3's candidate-unit rule, dormancy, permutation
  null; `research/05`), and a world where units are necessary (`research/07` §1.3).
- "Similar to human brain cells" needs a written list of which properties are meant (local plasticity,
  eligibility/dopamine-like gating, synaptic scaling in sleep, neurogenesis/pruning, …) with sources,
  so each can be a falsifiable test. That list is the first deliverable of the next session.
