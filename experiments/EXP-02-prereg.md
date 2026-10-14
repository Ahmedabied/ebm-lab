# EXP-02 — pre-registration (written BEFORE any code, 2026-10-14, session 03)

**Question.** Tabular Q beat the EBM by 3× in EXP-01. Q has four advantages the EBM lacks:
(1) hand-built sign features, (2) ε-greedy argmax action, (3) TD bootstrapping, (4) learning every
tick. **Which of these explains the gap?** Give the EBM each advantage alone, then all together
(the "ceiling" arm, which is Sallans & Hinton 2004's free-energy-as-Q learner). If the ceiling arm
still loses to Q, the bottleneck is the energy parameterisation itself, not the learning paradigm.

**Fixed before running.** Commit recorded in results.json. **Main seeds 200–219** (20 per arm, both
worlds, 15 days, day_len 300). **Pilot seeds 20–27** may be used ONLY to pick the step sizes of the
two new components (critic lr `alpha_v`; Q-mode lr `alpha_q`), and those pilots are reported.
Seeds 0–7 and 100–119 are burned. Nothing is re-tuned after the main run.

## Arms

| arm | what it is | decomposition role |
|---|---|---|
| `random` | uniform actions | floor |
| `tabular_q` | EXP-01's Q learner (sign state, ε=0.1 greedy, TD γ=0.9, online) | target |
| `ebm-nolearn` | EBM, learning off | zero |
| `ebm` | EXP-01's EBM exactly (night-only replay) | replication on fresh seeds |
| `ebm-dn` | `ebm` + `day_learning=True` (online REINFORCE + nightly replay) | **B0**, the decomposition baseline (advantage 4 alone) |
| `ebm-dn-sign` | B0 + `sense.sign_features=True` | advantage 1 alone |
| `ebm-dn-greedy` | B0 + `brain.act_mode="egreedy"` (ε=0.1), IS-corrected PG | advantage 2 alone |
| `ebm-dn-critic` | B0 + `learner="ac"`: linear critic V(x), lesson = TD error δ (γ=0.9) | advantage 3 alone |
| `ebm-td` | `learner="q"`: Q(x,a) = −F(x,a), ε-greedy, Q-learning target γ=0.9, online + replay; raw features | advantages 2+3+4 (Q's paradigm) |
| `ebm-all` | `ebm-td` + `sense.sign_features=True` | **ceiling**: all four |

All EBM arms keep EXP-01 defaults otherwise (T 0.3, lr 1.0, clip 1.0, replay 3 days × 3 epochs,
downscale 0.01, surprise growth, H0 4, init_scale 0.01).

## Metrics
**Primary:** `ticks_alive`. **Secondary:** food, poison, mean_drive.
**Gap fraction** G(arm) = (mean(arm) − mean(ebm-dn)) / (mean(tabular_q) − mean(ebm-dn)), with a
**paired bootstrap** over seeds (resample seed indices, recompute all three means jointly), 95% CI.
Every arm reported, including losers. Per-night instruments (entropy, clip_frac, w_norm; for
critic/Q arms also the TD error magnitude) logged as before.

## Predictions (falsifiable, in the linear world unless stated)
- **P1 (ceiling):** G(ebm-all) ≥ 0.75 with CI lower bound > 0.5. *If false:* the free-energy
  parameterisation (or its learning dynamics) is itself a bottleneck; that becomes the next question.
- **P2 (ranking of single advantages):** G(greedy) > G(sign) > G(critic), and G(greedy) > 0.4.
  Reason: the single-life diagnosis (right sign, too weak to act on; entropy 0.97 of 1.10) is
  exactly what argmax removes; a critic needs more ticks than a 3–4 day life gives to fit V.
- **P3 (replication):** `ebm` on seeds 200–219 lands inside EXP-01's CI [806, 1167] and does not
  beat `ebm-nolearn` (CI of the difference includes 0).
- **P4 (xor):** G(sign) in xor < G(sign) in linear: single-note signs cannot express "A and B
  together". No prediction for `ebm-all` in xor (the conjunction needs hidden units to learn it).
- **P5 (paradigm):** G(ebm-td) ≥ G(ebm-dn-greedy): greedy+TD together ≥ greedy alone.

**Decision rule.** Report the table and the CIs as they come. No new seeds, no changed bars.
Surprises go into `findings/02` as findings, not fixes.

## Interface contract (so three builders can work in parallel without talking)

- `SenseConfig.sign_features: bool = False`, `SenseConfig.dead: float = 0.02`. When on, x gains
  3 dims appended before the bias: s_k = sign(left_k − right_k) · [|left_k − right_k| > dead], on the
  same noisy log readings tabular Q discretises. `Senses.dim` property (12 or 15). `Life` builds the
  brain with `dim = senses.dim`. This is a fixed sense-organ nonlinearity; it carries no valence
  (it never says which note is good) and so stays inside DESIGN §0.
- `BrainConfig.act_mode: str = "softmax"` | `"egreedy"`, `BrainConfig.eps: float = 0.1`.
  `Brain.act` returns `(a, Fx, logp_behaviour)`; for egreedy, logp = log((1−ε)+ε/A) on the argmin-F
  action and log(ε/A) otherwise. Learning stays the softmax policy gradient at T; both the online
  rule and replay weight each sample by the clipped ratio π_T(a|x)/β(a|x) (A2's machinery, now also
  applied online). Ties in argmin broken by the first index (deterministic).
- `SimConfig.learner: str = "pg"` | `"ac"` | `"q"`, `SimConfig.gamma: float = 0.9`,
  `SimConfig.alpha_v: float` (critic lr), `SimConfig.alpha_q: float` (Q-mode lr), both set from the
  seeds-20–27 pilot and recorded here when chosen.
  The cache stores transitions `(x, a, r, logp, x_next, done)`; `x_next` = next waking sensation;
  the last tick of a day has `done=True` (no bootstrap).
  - `"ac"`: V(x) = v·x (x already carries a bias dim). δ = r + γ(1−done)V(x') − V(x). Critic:
    v += alpha_v · δ · x (TD(0)). Actor lesson = δ standardised by a running scale (EMA of δ²), in
    place of the day-return R; online with the eligibility trace, and at night on replayed
    transitions with δ recomputed from the current V (IS-clipped as before).
  - `"q"`: Q(x,a) = −F(x,a). Target y = r + γ(1−done)·max_a' Q(x',a'). θ += alpha_q · (y − Q(x,a)) ·
    ∂(−F(x,a))/∂θ (new `Brain.grad_negF(X, a)`: like `grad_logpi` with coef = onehot, no /T).
    Acting is ε-greedy on Q (`act_mode` forced to egreedy). Online every tick, and nightly replay
    of cached transitions (3 days × 3 epochs, shuffled; no IS weighting: Q-learning is off-policy).
    No standardisation: Q regresses raw r, as tabular Q does. Downscaling and growth unchanged
    (v = 0 birth is still Q-neutral).
- Growth, downscale, cache_days, batch, sleep modes: unchanged and shared.
- Every new piece gets a law test: sign features carry no valence (permuting note identities permutes
  features); egreedy logp is the true behaviour prob; critic TD(0) on a known 2-state chain converges
  to the analytic V; Q-mode gradient matches finite differences; `done` stops the bootstrap;
  determinism per seed for every learner.

## Method for this session (the swarm)
Tier 0: orchestrator (writes this file, merges, runs the main experiment, writes findings/02).
Tier 1: three builders in separate git worktrees (senses+acting; learners; harness+paired bootstrap).
Tier 2: **two hostile referees per interesting conclusion**, briefed to break it: on each builder's
"done", on the main result, and on the orchestrator's own proof-of-possibility notes
(`research/07`). A conclusion stands only after both referees have had their shot and every
objection is either fixed or recorded as a limitation.
