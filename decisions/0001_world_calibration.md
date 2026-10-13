# 0001 — World calibration (EXP-00)

**Date:** 2026-10-13, session 02. **Decided by:** Claude, on measurement; Ahmed may override.

## Question
How harsh should the world be? A brain that learns only at night needs a naive creature to reach a few
nights; a world with no pressure teaches nothing. Pre-registered band: the **random** policy survives a
median of **2–5 days**; the **oracle** survives all days.

## Measurement
`uv run python experiments/00_calibration.py` → `experiments/results/00_calibration/results.json`
(8 seeds, day_len 300, E0 0.8, 8-day cap, commit 47d2187). Grid: metabolic ∈ {0.0005, 0.001, 0.002} ×
food_budget ∈ {6, 12, 24}.

| metabolic | food_budget | random days (median [min,max]) | oracle days | random food |
|---|---|---|---|---|
| 0.0005 | 6  | 1.0 [1,2] | 8 [4,8] | 0.14 |
| 0.0005 | 12 | 2.0 [1,3] | 8 [6,8] | 0.34 |
| **0.0005** | **24** | **3.5 [2,5]** | **8 [8,8]** | 1.19 |
| 0.001  | 6  | 1.0 [1,1] | 8 [4,8] | 0.09 |
| 0.001  | 12 | 1.0 [1,2] | 8 [5,8] | 0.23 |
| 0.001  | 24 | 2.0 [1,3] | 8 [8,8] | 0.68 |
| 0.002  | 6  | 0.0 [0,1] | 8 [3,8] | 0.09 |
| 0.002  | 12 | 0.0 [0,1] | 8 [5,8] | 0.15 |
| 0.002  | 24 | 1.0 [0,1] | 8 [8,8] | 0.40 |

Only one cell lands in the band: **metabolic 0.0005, food_budget 24** (random median 3.5 days, oracle 8/8).

**Scent profile** (one food item, mass 2, steady state, note A by distance in cells):
0: 0.213, 1: 0.082, 2: 0.036, 3: 0.018, 4: 0.009, 5: 0.005, 6: 0.0025, 8: 0.0008, 10: 0.0002.
Readable (>0.005) to ~5 cells. With 12 items in 48×48 the mean spacing is ~14 cells, so halo/spacing ≈ 0.36:
food is findable by walking, not from everywhere.

## Decision
Defaults: `BodyConfig.metabolic = 0.0005`, `BodyConfig.E0 = 0.8`, `WorldConfig.food_budget = 24`,
`SimConfig.day_len = 300`. Commit after this decision carries them.

## Caveats
- The random policy with E0 0.8 and these costs starves in 0.8/0.0015 ≈ 533 ticks if it never eats; the
  band is reached because random walkers do bump into food (1.19 mass per life on average).
- Calibrated without sensor noise (random and oracle don't use the antennae), so unaffected by the noise added later.
- This is a calibration, not tuning for the EBM: the EBM was not run in this scan.
