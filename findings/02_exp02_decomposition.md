# Finding 02 — EXP-02: which of tabular Q's advantages explains its lead over the EBM?

**Date:** 2026-10-14 (session 03). **Status:** pre-registered result, scored; two hostile referees on the
result (leak hunt; statistics), their corrections applied to the wording below.
**Re-derive:** `uv run python experiments/02_main.py linear` and `... xor` (seeds 200–219, 15 days,
commit `112e957`, source hash `e2ae83c2b53faf80`), then `uv run python experiments/report_exp02.py`
(saved as `experiments/results/02_main_report.md`) and `experiments/plot_exp02.py`.
Pre-registration incl. the pre-run addendum: `experiments/EXP-02-prereg.md`.
Raw: `experiments/results/02_main_{linear,xor}/results.json`. Plots: `02_main_ticks.png`, `02_main_gap.png`.
Pilot for the two new step sizes (seeds 20–27): `experiments/results/02a_pilot_alpha/results.json`.

## The headline, as the referees allow it to be said
**Trained as a value function (Q = −F, ε-greedy acting, Q-learning target, online + nightly replay), the
energy-based brain learns to forage by smell within one life.** `ebm-td` lived 4113 [3210, 5014] ticks
in the linear world and 3876 [2955, 4780] in xor; 15/20 and 14/20 lives reached the 15-day ceiling.
The same model trained by policy gradient at EXP-01's step size (`ebm-dn`, 1145) did not. The win is
not a leak or a world artefact: it reproduces on 10 fresh seeds (4803, 9/10 at ceiling; referee rerun on
seeds 1100–1109), a day-5 brain frozen with learning OFF still lives 5250 on 15/15 fresh lives, and the
same brain with mirrored antennae dies (530–980). The learner **reaches tabular Q's level; superiority
is not shown** (paired `ebm-td − tabular_q` = +1230 [−187, 2552] linear; log-rank p = 0.10; against the
textbook `tabular_q_next` it is a tie: +194 [−1200, 1698]). This is the lab's first positive
within-life learning result, and it is the paradigm, not the energy model's hidden units, that
carries it (see §Limits).

## The numbers (ticks alive, mean [95% bootstrap CI], 20 seeds; food = lifetime total)

| arm | linear ticks | linear food | xor ticks | xor food | censored at 5250 (lin / xor) |
|---|---|---|---|---|---|
| random | 1175 [993, 1367] | 0.90 | 1175 [993, 1367] | 0.90 | 0 / 0 |
| tabular_q (pre-registered target) | 2882 [1963, 3827] | 5.51 | 3124 [2269, 3986] | 5.83 | 9 / 9 |
| ebm-nolearn | 1147 [989, 1310] | 0.92 | 1161 [1003, 1321] | 0.92 | 0 / 0 |
| ebm (EXP-01 config) | 1102 [853, 1417] | 1.20 | 1185 [854, 1626] | 1.81 | 0 / 0 |
| ebm-dn (B0: + online PG) | 1145 [865, 1496] | 1.39 | 1403 [970, 1910] | 1.94 | 0 / 0 |
| ebm-dn-sign | 1963 [1404, 2600] | 5.50 | 1966 [1322, 2641] | 4.55 | 1 / 2 |
| ebm-dn-greedy | 1127 [897, 1397] | 1.28 | 1354 [1076, 1650] | 1.72 | 0 / 0 |
| ebm-dn-critic | 1457 [1064, 1947] | 3.17 | 1296 [968, 1772] | 2.24 | 1 / 1 |
| **ebm-td** | **4113 [3210, 5014]** | **9.08** | **3876 [2955, 4780]** | **9.01** | **15 / 14** |
| ebm-all (td + sign features) | 2076 [1437, 2771] | 2.67 | 2131 [1547, 2825] | 2.78 | 2 / 2 |
| tabular_q_next (exploratory, textbook) | 3919 [3025, 4803] | 9.82 | 4175 [3268, 4879] | 10.72 | 14 / 15 |

Gap fraction G = (arm − ebm-dn)/(tabular_q − ebm-dn), paired bootstrap (denominator 1737 [739, 2744] linear):
sign 0.47 [0.06, 1.31] · greedy −0.01 [−0.50, 0.19] · critic 0.18 [−0.18, 0.65] · **td 1.71 [0.92, 4.13]** ·
all 0.54 [0.14, 1.15]. Against the textbook target: td 1.07 [0.63, 1.84], all 0.34 [0.08, 0.70].
The G upper bounds are ratio artefacts near the ceiling (8% of resamples give G > 3); the paired
differences above are the honest companion.

## Predictions, scored
- **P1 (ceiling arm G ≥ 0.75, lo > 0.5): FAILED** (0.54 [0.14, 1.15]). But see §Limits 1: the arm ran
  at a step size that is unstable for it; this failure is uninformative about sign features + Q.
- **P2 (greedy > sign > critic, greedy > 0.4): FAILED.** Greedy alone ≈ 0. The observed order
  (sign > critic > greedy) is post-hoc: of the six pairwise contrasts (3 × 2 worlds), none survives
  Holm correction (smallest adjusted p 0.17); greedy < sign holds in the linear world only, uncorrected
  (p = 0.028). Reported as exploratory.
- **P3 (replication): HELD.** `ebm` = 1102 vs EXP-01's 973: difference +129 [−193, 486]; CIs overlap;
  `ebm − ebm-nolearn` = −45 [−309, 257] linear, +24 [−354, 505] xor. (The prereg's "inside EXP-01's CI"
  criterion was the wrong test, a new mean lands inside an old CI only ~84% of the time if nothing
  changed; the difference test is what is reported.)
- **P4 (sign's gain smaller in xor): NOT SUPPORTED.** ΔG = 0.14 [−0.51, 1.39].
- **P5 (td ≥ greedy): HELD**, strongly: ΔG = 1.72 [0.88, 4.55]; alive at day 15: 15/20 vs 0/20.

## What the decomposition says
- **No single ingredient closes the gap.** Greedy acting with an importance-corrected policy gradient
  does nothing; a linear critic adds little (+330 [−132, 944] over greedy, linear); sign features help the
  policy-gradient learner in the linear world (+818 [121, 1561] ticks, p = 0.04; xor +563 [−273, 1431],
  not shown).
- **The value-learning paradigm does.** TD on Q with greedy acting, online plus replay (`ebm-td`), is
  the combination that forages; the design has no TD-without-greedy arm, so the paradigm cannot be split
  further here.
- **Why greedy + policy gradient fails (referee trace):** the behaviour ratios were applied (up to 11.6),
  the weights moved (w_norm 1.1–1.9 after night 0), and the policy collapsed on night 0 (entropy
  ≤ 0.036); after that the learning policy puts ≈ 1 on the greedy action, explored actions carry weight
  ≈ 0, and nothing is learned from exploration. This is the same night-0 collapse `research/07` measured
  for plain policy gradient (step 8–16× the initial norm). So "policy gradient does not learn" holds
  **at EXP-01's step size**; the policy-gradient arms were never re-tuned in this experiment.
- **What `ebm-td` learned:** w[LEFT, contrast_A] − w[RIGHT, contrast_A] turns positive after night 1 and
  stays small (0.01–0.023; argmax needs only the sign); turns toward the higher-A antenna rise from
  0.45–0.52 on day 1 to 0.73–0.82 by day 10.
- **Shipped tabular Q is not textbook** (A17: s′ from the pre-move sensation). The textbook variant
  lived longer (+1036 [−77, 2175] linear, +1050 [100, 2003] xor). EXP-01's target was the weaker learner.

## Limits (every one found by a referee)
1. **`ebm-all` is a step-size casualty, not a feature result.** The stability argument in the prereg
   addendum used α|x|² and ignored the hidden-unit gradient paths; the exact per-sample gain
   α·|∂Q/∂θ|² exceeds 2 on 54% of day-0 ticks for `ebm-td` and 60% for `ebm-all`, which blows up on
   night 0 (w_norm 16–72, td_abs 1.3–5.3). On fresh seeds `ebm-all` at α = 0.1 lives **4806** (9/10 at
   ceiling) vs 1194 at 0.3. The two-arm pilot rule picked a value unstable for one arm. Whether sign
   features help or hurt Q-learning is **not identified** by this design.
2. **The hidden units do not carry the win (linear world).** Frozen day-5 `ebm-td` brains with v = 0
   (hidden units cannot distinguish actions) still reach 5250 on 15/15; the hidden part alone lives
   919–1054. A linear Q on raw senses inside the energy model does the foraging. The RBM's contribution
   in xor was not tested.
3. **No arm learned to avoid poison, in either world.** Per-tick poison rate vs random: `ebm-td` −0.011
   (p = 0.84), `tabular_q` −0.022 (p = 0.70). Survivors live by eating more food. The xor conjunction
   ("A and B together is food, either alone is poison") was never shown to be learned by anyone, and
   `research/07` §1.3 explains why nothing forced it: at toxicity 0.5 a pure A-chaser survives xor.
4. **Censoring.** 15/20 `ebm-td` and 9/20 `tabular_q` lives hit 5250; means are restricted-mean survival
   times to 15 days and squeeze strong arms together. On uncensored metrics the td-vs-PG claim survives
   (food +7.7 [5.0, 10.1]; food per 1000 ticks +0.98 [0.38, 1.49]; alive at day 15 15/20 vs 0/20), the
   td-vs-Q claim does not (Fisher p = 0.105; log-rank p = 0.098).
5. **`ebm-td` succeeds or starves:** its 5 failed linear lives ate 0–1.05 food; a birth brain under
   ε-greedy argmax lives 618 (< random). Day-15 frozen brains transfer worse than day-5 ones
   (1016, 2057): late brains seem to need ongoing learning (unexplained).
6. **Pairing** shares the starting world and heading only (addendum 5). **Multiple comparisons:** none
   applied; P1–P5 confirmatory, all else exploratory.
7. Policy-gradient step sizes were EXP-01's; α_q and α_v came from pilot seeds 20–27 (now burned).

## What it points to (for Ahmed to choose; nothing here is started)
1. **Fix the step and re-ask the sign-feature question:** a per-sample normalised step (α/|∂Q/∂θ|²)
   or α = 0.1 for the 15-dim arm, pre-registered on fresh seeds.
2. **Re-ask policy gradient at a sane step** (`research/07`: lr/T² is one knob; night step 8–16× the
   initial norm) with an entropy bonus, so "PG cannot learn this" is tested rather than assumed.
3. **Make the xor world bite** (raise toxicity or let poison deplete energy) so the conjunction is
   required, then test whether the hidden units earn their keep: that is the first real test of the
   "small EBMs that make connections" idea.
4. **Sleep now has something to consolidate.** `ebm-td` learns; the matched-update sleep arms of EXP-01
   can be re-run on it (replay vs today vs noise vs none) as the first meaningful sleep test (H1).
5. **Generations:** a learner that reaches competence in ~5 days is a learner whose priors (step size,
   ε, innate valence) can be inherited; EXP-03's genome question is now live (R4, `research/06`).
