# EXP-01 — pre-registration (written BEFORE the run, 2026-10-13, session 02)

**Question.** Does the energy-based brain learn to forage from its body's lessons alone, within one
life, and how does it compare with the baselines? Does sleep (offline replay) matter? Do hidden units
matter in the world where blends matter?

**Fixed before running.** Commit of `creature/` at the run (recorded in results.json). Defaults after
amendments A1–A13. **Seeds 100–119** (20 per arm; seeds 0–7 were used for tuning and are excluded).
15 days, day_len 300. Both worlds: `linear` and `xor`.

**Arms.** random · braitenberg · tabular_q · oracle · ebm · ebm-nosleep (online, per-sample lr matched:
day_lr = 1.0/64) · ebm-sleep-matched (today, 1 epoch) · ebm-sleep-today (today, 3 epochs) ·
ebm-sleep-noise · ebm-nolearn · ebm-nogrowth · ebm-linear (H0 = 0, no hidden units).

**Primary metric.** `ticks_alive` (lifespan). **Secondary.** food, poison, mean_drive,
`poison_bites_after_first`, and the normalised score (arm − random)/(oracle − random) on food.
All as mean with 95% bootstrap CI over seeds. Every arm reported, including losers.

**Predictions (falsifiable).**
- **P1 (learning works at all):** ebm > ebm-nolearn on ticks_alive, with the bootstrap CI of the
  difference excluding 0, in the linear world. *If false: within-life learning from the body signal
  is not demonstrated in v0.*
- **P2 (honest expectation):** ebm < tabular_q and ebm < braitenberg on ticks_alive in the linear
  world. The EBM is a from-scratch policy-gradient learner with ~1000 samples per life; Q has a
  hand-built state and bootstrapping; Braitenberg is told the answer.
- **P3 (sleep):** no prediction of superiority. R3 (research/05) found no evidence that offline-ness
  itself helps. We report ebm vs ebm-nosleep vs ebm-sleep-matched vs ebm-sleep-today vs ebm-sleep-noise
  and say what we see. A sleep claim would need ebm > ebm-nosleep AND ebm > ebm-sleep-noise with
  CIs excluding 0; we do not expect to make one from this experiment.
- **P4 (blends):** in the xor world, braitenberg eats poison (it is wired to approach A) and its
  lifespan drops below its linear-world value; ebm-linear (no hidden units) does not beat ebm-nolearn
  there. Whether ebm (with hidden units) beats ebm-linear in xor is the interesting open question;
  no prediction.
- **P5 (growth):** ebm vs ebm-nogrowth: no prediction (the v0 growth rule is a placeholder, A10).

**Decision rule.** Report the table and the CIs as they come. No re-running with new seeds, no
changed bars. Anything surprising goes into findings/01 as a finding, not a fix.
