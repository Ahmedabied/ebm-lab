# STATE — EBM lab

Updated 2026-10-15, end of session 04 (the teaching video). Everything below is committed (see `git log`).

## Lesson 01 (session 04)
Built: `video/out/ebm-lab-lesson-01.qh.mp4` with chapters, thumbnail and provenance; script refereed twice
(math + teaching); `video/data/frozen_brain_test.json` re-derives the frozen/mirrored/birth-brain test on
fresh seeds 500–514 (5250 15/15; 1013 0/15; 1419 2/15). One lab-relevant observation from the replay dump
(`video/data/life203.npz`): in seed 203 the steering weight is the contrast-**B** pair (positive all life);
the A pair crosses zero on day 3. `world.py`'s comment "B carries no information" is still wrong for the
gradient (research/07 §2.2). Seeds 500–514 are now used (frozen test, not tuning).

## Goal pivot (2026-10-15, Ahmed): see `decisions/0002_goal_pivot.md`
Experiment goal = the smallest creature with brain cells similar to humans; EBM goal = mimic how a
brain cell learns, connects, functions, dies and is born. Verdict on EXP-02 under those goals is in
the decision file (learn: yes; function: yes; connect: unused; born: placeholder; die: missing).

## Where we are
- **First positive within-life learning result (EXP-02, `findings/02`).** The energy-based brain,
  trained as a value function (Q = −F, ε-greedy, Q-learning target, online + nightly replay: arm
  `ebm-td`), forages by smell: 4113 [3210, 5014] ticks linear, 3876 xor, 15/20 lives at the 15-day
  ceiling; reproduces on fresh seeds; a frozen day-5 brain still forages; mirrored antennae kill it.
  It **reaches tabular Q's level; superiority is not shown.** Policy-gradient training of the same
  model at EXP-01's step size does not learn (night-0 collapse). P1, P2 failed; P3, P5 held; P4 not
  supported. Scored table and referee limits in `findings/02`.
- **Proof-of-possibility note (`research/07`)**, twice refereed: the model class contains the forager
  (2 weights); the body's lesson has per-day SNR ≈ 1.8–1.9 on the key weight; EXP-01's learner failed
  because its nightly step is 8–16× the initial weight norm (lr/T² is one knob), not from data
  starvation; the xor world does not force the conjunction (a pure A-chaser survives it); biology
  precedent (worm, larva) always has an innate reinforcer and fixed plasticity sites.
- **Corrections on record:** `findings/01` CORRECTION block (diagnosis was wrong, then its first
  correction was wrong too); `research/07` quotes every retracted sentence.
- **83 law tests pass** (`uv run pytest`). Code: `creature/` now has sign features, ε-greedy acting with
  unclipped behaviour ratio, learners pg / ac / q, centred Q (A16), `tabular_q_next` (A17),
  `theta_finite`; `experiments/` has `stats.py` (paired bootstrap, gap fraction, cross-world),
  `report_exp02.py`, `plot_exp02.py`, burned-seed guard, strict overrides.
- **Viewer** renders 12- and 15-input brains and the TD instruments. Lives to watch:
  `runs/exp02-linear/203-{ebm-td,ebm-dn-sign,ebm-all,ebm-dn,tabular_q_next}/run.json`,
  `runs/exp02-xor/203-ebm-td/run.json`, plus EXP-01's under `runs/exp01-*`.
  Serve: `cd ~/ebm-lab && uv run python -m http.server 8765` →
  `http://localhost:8765/viewer/?run=runs/exp02-linear/203-ebm-td/run.json`.

## Method this session (the swarm)
Orchestrator (Fable) + 3 builders in worktrees + 2 hostile referees per conclusion (12 referee runs in
all) + the orchestrator's own proof track. Every referee round changed the record: one reversed
citation, two retractions, two blocks-run bugs (clipped behaviour ratio; Q offset at birth), one
baseline defect (tabular Q not textbook), and the reading of the main result narrowed four times.
Amendments A14–A17 in `DESIGN-AMENDMENTS.md`.

## Seeds (burned for tuning, never reuse)
0–7, 20–27 (EXP-02 pilots), 100–119 (EXP-01 main), 200–219 (EXP-02 main), 300–339 (proof),
340–349 and 1000–1114 (referee diagnostics), 500–514 (lesson 01 frozen-brain test; no tuning). `experiments/harness.py` enforces the first four sets.

## Known limitations (do not over-read)
- `ebm-all` ran at a step size unstable for it (α 0.3; at 0.1 it lives 4806 on fresh seeds): sign
  features + Q not identified. Hidden units do not carry the linear-world win. No arm avoids poison.
  Lifespan censored at 5250. Pairing by seed shares only the starting world. No seasons, no
  generations, no entropy bonus, placeholder growth rule.
- `ebm-td` either reaches the ceiling or starves (5/20 failures ate ≤ 1 food).

## Environment
- Laptop venv via `uv` (numpy, pytest, matplotlib). One life ≈ 0.1–0.3 s; the main run ≈ 110 s/world.
- Box unused. No cloud spend. Firecrawl credits exhausted (402); WebSearch works.
