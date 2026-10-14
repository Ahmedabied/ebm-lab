# Finding 01 — Creature v0: within-life EBM learning did not beat no learning (EXP-01)

**Date:** 2026-10-13 (session 02). **Status:** pre-registered result, negative on the primary prediction.
**Re-derive:** `uv run python experiments/01_main.py linear` and `... xor` (seeds 100–119, 15 days,
commit `bb5b19d`, source hash `5c04ce68aea1ae46`), then `uv run python experiments/plot_exp01.py`.
Pre-registration: `experiments/EXP-01-prereg.md` (written before the run).
Raw: `experiments/results/01_main_{linear,xor}/results.json`. Plots: `01_main_ticks.png`, `01_main_food.png`.

## The numbers (ticks alive, mean [95% bootstrap CI], 20 seeds)

| arm | linear world | xor world |
|---|---|---|
| random | 1303 [1116, 1514] | 1303 [1116, 1514] |
| braitenberg (cheats: told A is good) | **4072** [3342, 4726] | 1909 [1359, 2475], eats 3.5 poison |
| tabular_q | 3212 [2220, 4101] | 3216 [2220, 4147] |
| oracle (sees items) | 3616 [2836, 4346] | 3616 [2836, 4346] |
| **ebm** (sleep replay, 3 days, 3 epochs) | **973** [806, 1167] | 1214 [864, 1654] |
| ebm-nosleep (online, matched step) | 1232 [1052, 1448] | 1280 [1061, 1513] |
| ebm-sleep-matched (today, 1 epoch) | 935 [792, 1103] | 923 [769, 1085] |
| ebm-sleep-today (today, 3 epochs) | 1038 [831, 1277] | 1182 [848, 1620] |
| ebm-sleep-noise (matched-norm noise) | 1109 [928, 1290] | 1012 [812, 1262] |
| **ebm-nolearn** | **1224** [1071, 1399] | 1120 [899, 1391] |
| ebm-nogrowth | 858 [764, 959] | 1074 [807, 1417] |
| ebm-linear (no hidden units) | 1241 [986, 1505] | 1415 [1001, 1942] |

Food eaten tells the same story: ebm 0.73 vs nolearn 1.01 (linear); braitenberg 25.2, oracle 23.8, tabular_q 7.5.

## Predictions, scored
- **P1 (learning works at all): FAILED.** In the linear world the learning EBM lived *less* than the
  same brain with learning off (973 vs 1224; the CIs touch at the edge). In xor, no difference.
- **P2 (EBM < tabular_q, braitenberg): held.** By a factor of 3–4.
- **P3 (sleep): no sleep claim.** No sleep arm beat no-learning. Online ≈ no-learning.
- **P4 (blends): held** for Braitenberg: wired to chase A, it eats 3.5 poison in xor and its lifespan
  halves (4072 → 1909). ebm-linear did not beat ebm-nolearn in a way the CIs support.
- **P5 (growth): no claim.** ebm-nogrowth (858) < ebm (973), CIs overlap at the edge; the v0 growth
  rule is a placeholder.

## The pilot did not replicate (the most important lesson of the day)
Tuning on seeds 0–7 (`01c`, `01d`, `01e`) picked T = 0.3, lr = 1.0, clip = 1.0 and showed
**2178 [1055, 3450]** ticks for the EBM. On 20 fresh seeds the same configuration gave **973 [806, 1167]**.
The pilot's mean was carried by 2–3 lucky seeds; its CI already said so (width > 2000). Genesis's rule
held: numbers from the tuning seeds are not results. Nothing was re-tuned after the main run.

## What the single-life inspection showed (why it fails)
One life (seed 3, before the final defaults) after 3 nights: the LEFT−RIGHT weight on contrast-A was
**+0.42, the correct sign** (turn toward the side with more A), but policy entropy was still 0.97 of a
maximum 1.10: the brain learned the right thing too weakly to act on, then starved while still a
random walker (3-day life). Lowering T to make it decisive (0.3) made confident policies from noisy
gradients; T = 0.1 collapsed completely (pilot 01e). A fully confident softmax policy has a vanishing
policy gradient and cannot unlearn (`tests/test_brain.py`, saturation note).

**Diagnosis (my reading, not measured yet):** a from-scratch policy-gradient learner with ~900 cached
samples and 2–4 meals per day is data-starved; the gradient variance is high; a lifespan of 3–4 days is
not enough nights. Tabular Q escapes this with a hand-built state (sign of L−R per note), greedy argmax
and TD bootstrapping; Braitenberg is told the answer.

## Other things the pilots found (all fixed, all recorded in DESIGN-AMENDMENTS.md)
- The brain's metabolic tax (unit_cost) made the untrained creature cost more than its body (A8).
- Any persistent turning bias traps an untrained creature in loops; a near-uniform start is needed (A7).
- Raw left/right readings differ by ~0.15 log units; a decisive turn would need weights ~13 (A9).
- The eligibility trace did not resize after growth (A12, a crash).
- In the linear blend world, note B carries no information (A5, from R2).
- The day's truncated returns credited the last ticks as if drift had stopped (A4).

## What this does NOT say
- It does not say EBMs cannot learn this. It says *this* learner, from scratch, in one short life, with
  this credit signal, did not. The weights move in the right direction.
- The sleep arms are not evidence against sleep: nothing learned, so there was nothing to consolidate.
- 20 seeds, 15 days, one world size. No seasons, no generations, no critic.

## What it points to (for Ahmed to choose)
1. **Variance reduction:** a linear critic / actor-critic (R1 v0.1), and an entropy bonus instead of a low T.
2. **A prior from generations:** inherit learning-rule genes and innate per-note valences (R4), so a life
   starts from a usable policy and within-life learning fine-tunes. This is the original design's
   "grows over generations", and it is how real creatures work (E. coli is born knowing sugar).
3. **A childhood:** a protected first period (lower metabolic cost / provisioning), so a naive creature
   reaches more nights before the world judges it. All arms would get it.
4. **Match the Q learner's advantages honestly:** give the EBM TD bootstrapping (that is the critic), and
   test whether the hand-built sign features are what makes Q win (an `ebm-signfeatures` arm).

## CORRECTION (2026-10-14, session 03; the original text above is left as written)
The single-life inspection quoted above (seed 3, "right sign, too weak to act on, entropy 0.97 of
1.10") was made BEFORE the final defaults (A13: T 0.3, lr 1.0, clip 1.0). Under the defaults actually
used in EXP-01, one night of replay **collapses** the policy: end-of-night entropy on proof seeds
300–303 was 0.028, 0.092, 0.004, 0.139 (max 1.099), and the resting turning bias
|π(LEFT|x0) − π(RIGHT|x0)| at a featureless sensation jumps from 0.014 (no learning) to 0.53 after the
first night (`research/07-proof-of-possibility/m3_bias.py`, seeds 300–319). So the mechanism in
EXP-01 is not "too weak to act on" but "too confident after one night, then unable to unlearn"
(softmax saturation; Mei et al. 2020's gravity well). The data-starvation reading is also wrong as
stated: the batch gradient on the key weight has block-means SNR ≈ 1.9 per day with the right sign on
96% of creature-days (`m2_snr.py`). The signal is there; the step is far too large and it lands on
~100 noisy directions at once. Full argument: `research/07-proof-of-possibility.md`.
