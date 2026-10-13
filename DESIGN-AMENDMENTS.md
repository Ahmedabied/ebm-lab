# DESIGN amendments (append-only; the reason and the source for every change to DESIGN.md)

| # | Date | Change | Why | Source |
|---|---|---|---|---|
| A1 | 2026-10-13 | World defaults: metabolic 0.0005, E0 0.8, food_budget 24, day_len 300 | Pre-registered calibration band (random median 2–5 days) met by exactly one grid cell | `decisions/0001`, EXP-00 |
| A2 | 2026-10-13 | Sleep replay is importance-corrected: cache stores log π_old(a\|x); update weighted by clip(π/π_old, 1±clip). `clip_frac` logged per night | The cache holds actions chosen by yesterday's policy; uncorrected replay is biased | R1 `research/03` §Q2 (Degris 2012; Schulman 2017) |
| A3 | 2026-10-13 | New hidden units are born with v = 0 (policy-neutral); downscaling touches w, u, v only, not b or c | A unit with v = 0 adds the same energy to every action: the policy is unchanged at birth. Decaying b pulls toward uniform; decaying c shifts offsets | R1 §Q5 (Elfwing 2013) |
| A4 | 2026-10-13 | Credit: λ 0.9 → 0.95; the day's tail is bootstrapped with mean r continuing (mean_r/(1−λ)); R standardised per day (zero-variance day → R = 0) | Truncated returns credited the last ticks of a day as if drift had stopped; raw lessons are O(0.01) vs energy gaps O(1) | own derivation + R1 §Q4; pilot 01 |
| A5 | 2026-10-13 | Second world `blend_mode="xor"`: food = A+B together, poison = A alone or B alone | In the linear world B carries no information; a linear rule solves it from A and C. XOR needs the hidden units: the world where "chemistry blends" matters | R2 `research/04` §Q7 |
| A6 | 2026-10-13 | Antenna noise σ = 0.02 (log units) | Without noise steering is trivially easy | R2 §Q3 (Berg & Purcell 1977) |
| A7 | 2026-10-13 | Brain init_scale 0.1 → 0.01 | A persistent turning bias traps an untrained creature in loops; a near-uniform start explores like a random walk | pilot 01 |
| A8 | 2026-10-13 | unit_cost 2e-4 → 1.25e-5 (4 units = 10% of resting metabolism) | The brain cost more than the body; untrained creatures starved in ~350 ticks | pilot 01, `findings/01` |
| A9 | 2026-10-13 | Senses: per note, contrast (L−R)/(\|L\|+\|R\|+ε), mean, change (DIM unchanged = 12) | Raw L−R is ~0.15 log units; a decisive turn would need weights ~13. Opponent coding is what sensory systems do | pilot 01c arithmetic; R2 (raw L/R) partially overridden, reason recorded |
| A10 | 2026-10-13 | Growth trigger reads the std of the day's raw lessons (drive units), threshold 0.005 | After A4 the normalised \|R\| no longer measures surprise | own |
| A11 | 2026-10-13 | `ebm-sleep-matched` arm (today-only, 1 epoch): each sample replayed once, like online | A sleep claim must beat matched updates; "more updates" is not "sleep" | R3 `research/05` §Q1 |
| A12 | 2026-10-13 | Eligibility trace reset on growth | Bug found by pilot: trace shape stale after add_units | pilot 01 crash |

## Adopted in principle, not yet implemented (next session)
- **R3**: growth by *candidate units trained against the policy residual*, inserted only if they beat a permutation null; dormancy instead of deletion; fixed-at-final-size and random-insertion controls. `research/05` §Q4, (a).
- **R3**: fast + slow weights (Hinton & Plaut 1987) for two-speed forgetting (Genesis report 22). `research/05` §Q5.
- **R3**: a real "dream" needs the model to generate sensations (v0.1); the action-side negative phase is exact and is not a dream. `research/05` §Q2.
- **R4**: genome = {log lr, log T, λ, H₀, growth threshold, + one unwired placebo gene}, NOT θ₀ (106 floats is too many for Ne ≈ 6). Nulls: `severed`, `random-parents`, common-garden re-tests on held-out worlds. Lamarckian only as an ablation. Child starts at its own H₀ with fresh weights. `research/06`.
- **R4**: a 2×2 with the smell→effect mapping fixed vs redrawn each life, or evolution hard-wires the answer and learning becomes optional.
- **R1**: linear critic (actor-critic) for variance reduction once v0 works; entropy bonus β as the future gene; Keramati–Gutkin n > m > 1 as an ablation.
- **R2**: `braitenberg-learned-sign` baseline (3 learned numbers) as the smallest learner the EBM must beat; primary metric (agent − random)/(oracle − random) on net food rate; a sensor-limited oracle that knows valences but only smells.
| A13 | 2026-10-13 | Defaults T 0.3, lr 1.0, clip 1.0, day_lr 1/64 | Pilots 01c/01d/01e on seeds 0–7 (burned). T 0.1 collapses; clip 0.2 throttled learning (clip_frac 0.5) | `experiments/results/01{c,d,e}_*` |
