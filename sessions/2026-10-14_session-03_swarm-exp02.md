# Session 03 — 2026-10-14 — the swarm, EXP-02, and the proof of possibility

**Ahmed's instruction (verbatim):** "ok lets try it but lets try a deffrent approach youll be the
orchestrator with a hayracical structured subagents, a swarm, every time one of them provides an
interresting conclusion you put out 2 hostile refferries, meanwhile while the swarm does what it does
you go on a spree trying to find out in math and biology itself for proof this could be possible and
verify it". Lever chosen the turn before: 4 (decompose tabular Q's advantages), as a decomposition
experiment with a ceiling arm.

## Sequence (commits in order)
1. `2e30295` pre-registration + interface contract, before any code.
2. Builders (Opus, worktrees): senses+acting `99bc2a2`; harness `0b7eca7`; learners `d953731`/`5906e74`.
3. Referees on builders (4): found the clipped behaviour ratio is a biased estimator with possibly
   wrong sign (bandit counterexample); silent dotted overrides; pairing is starting-conditions only;
   meta.json dim wrong; viewer cut-off; P1 power 14–24%.
4. Learners builder found my contract's 100× online-step confound → A14; re-pilot.
5. Merge `9dd8c14` with the unclipped-ratio fix; prereg addendum `73e7e6a`.
6. Fix branches (harness2 `ab4e680`, export2 `864a950`, learners2 `93d6f9a`) merged.
7. Referees on learners (2): critic timing exact (hand calc); Q offset at birth breaks ε-greedy
   (blocks-run) → A16 centred Q; shipped tabular Q not textbook → A17 `tabular_q_next`.
8. Referees on `research/07` (2): reversed citation (Schroll 2006), Keramati–Gutkin scope,
   Sallans–Hinton SARSA, "innate prior" wording, E. coli; night-1 bias r = −0.49 (my r = 0.006 was
   the wrong night), policies flip overnight (gravity-well reading retracted), step measured 8–16×,
   lr/T² one knob, B carries signal, 2-weight construction, Mei scope. All rewritten in place.
9. Re-pilot alpha_q on centred Q → 0.3 by the declared rule; addendum 13. Main run `112e957`
   (results `bd81d7e`).
10. Referees on the result (2): no leak; fresh-seed and frozen-brain confirmation; `ebm-all` is a
    step-size casualty; hidden units not needed in linear; no poison avoidance anywhere; td ≈ Q, not >;
    reversed ranking does not survive Holm; P3 criterion wrong (difference test used).
11. `findings/02` `b042371`; STATE/HANDOFF/journal/README/memory.

## Orchestrator's own track (`research/07`)
M1 existence by construction (2 weights suffice; 5250 on 20/20; xor survivable by an A-chaser),
M1b ES search (xor; ceiling hit in gen 1; held-out pending at close), M2 SNR (≈ 1.8–1.9/day, right
sign 96%), M3 resting bias (0.53 vs 0.014; r = −0.49 with survival). Literature via WebSearch
(Firecrawl out of credits).

## Lessons for the method
- Two hostile referees per conclusion paid for themselves every single time. The orchestrator's own
  claims needed them most (two retractions, one reversed citation).
- Interface contracts written by the orchestrator can carry bugs that only a builder's pilot or a
  referee's counterexample finds; pre-run addenda keep that honest.
- A pilot selection rule should be declared with its grid AND its extension rule, and should not be
  shared across arms whose stability differs (the `ebm-all` lesson).
- Cost: ~16 Opus agent runs + the orchestrator. Heavy, as Ahmed asked; next sessions should be one
  lever, one experiment, two referees.


## Locked for the next session (2026-10-15): the teaching video
Ahmed asked for a YouTube lesson (Manim + ElevenLabs v4 soft female voice) teaching the concepts with
real-life analogies, the math from the beginning, the EBM and its training rule symbol by symbol, the
experiment step by step, and the code, with many moving visualisations: "be the teacher i never could
find". The verbatim prompt (key redacted), facts, syllabus and pipeline: `video/BRIEF.md`.
