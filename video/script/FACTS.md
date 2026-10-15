# Facts the script may quote (v2, after referee 1). Every number with its source. Ticks are the run's tick numbers
# (t in run.json, 350 per day incl. sleep); "index" means the waking-tick index into life203.npz (300 per day).

## Seed 203, arm ebm-td, linear world (runs/exp02-linear/203-ebm-td/run.json; replay dump video/data/life203.npz, bit-for-bit MATCH)
- Born with E = 0.8, X = 0, D = (1−0.8)² = 0.04. 48×48 torus, centre start, random heading.
- First bite at tick 14. Life: 267 food bites, 30 poison bites, 13.35 food mass, 1.5 poison mass; alive at the ceiling, 5250 ticks.
- Cost of a moving tick: 0.0005 + 0.001 + 1.25e-5 per unit (4 units 0.00155; 5 units 0.0015625). Quiet-tick lesson r ≈ −0.0006.
- Tick 14: D before 0.04915, after 0.03002, r = +0.01914 (show 5 decimals so the subtraction reproduces: 0.04915 − 0.03002 = 0.01913; the dump's r is 0.01914 from unrounded values; show the unrounded on screen).
- Poison tick 192: X 0 → 0.025, r = −0.00079 (D rises by X² = 0.000625 plus the metabolic creep 0.00016); tick 193: X 0.0495, r = −0.00202.
- 91% of waking ticks have r < 0; r range −0.0038 … +0.0350.
- Birth: x[0] contrast (−0.293, −0.041, −0.265), mean (0.009, 0.017, 0.012), change = mean, body (0.8, 0), bias 1; Q = (−0.0029, −0.0024, −0.0105).
- **Worked tick 3693 (day 10, index 3193).** x: contrast_A 0.521, contrast_B 0.328, contrast_C −0.188, mean_A 0.047, mean_B 0.072, mean_C 0.008, change_A −0.022, change_B 0.008, change_C −0.017, body_E 0.919, body_X 0.001, bias 1.
  Weights used at that tick (theta_at(3193)): w[LEFT] = (−0.00207, 0.00874, −0.00304, 0.00592, 0.00258, −0.00757, −0.00195, 0.00391, 0.00557, 0.00940, −0.01731, 0.00288).
  Products w[LEFT]·x: biggest body_E 0.00864, bias 0.00288, contrast_B 0.00287, contrast_A −0.00108; **sum 0.014248** ("fourteen thousandths").
  b_LEFT = 0.004035. Committee: five z for LEFT (−0.0156, −0.0271, −0.0096, 0.0332, −0.0159), sigmoids ≈ 0.50 each, softplus sum 3.4485; minus 5·log 2 = 3.4657 → committee share after centring **−0.017194**.
  Q_LEFT = 0.004035 + 0.014248 − 0.017194 = **+0.001089**. Q = (+0.001089, −0.002344, −0.001573). Greedy LEFT, taken LEFT. Q_L − Q_R = 0.0034.
  Softmax at T 0.3 → (0.336, 0.332, 0.333); T 0.05 → (0.347, 0.324, 0.329); T 0.001 → LEFT 0.907.
  Nudges (recomputed with the real weights): +0.1 on w[LEFT, contrast_A] moves Q_LEFT by +0.0521 (= 0.1 × 0.521); +0.1 on w[LEFT, body_X] moves it by +0.00014. +0.5 on w[LEFT, contrast_A] → Q = (0.2616, −0.0023, −0.0016), a jump of 0.2605.
  TD at this tick: Q(x, LEFT) = +0.001089, r = −0.00026, y = +0.00089, miss = y − Q = **−0.00020**; Δw[LEFT] = 0.3 × miss × x, e.g. −0.000031 on contrast_A, −0.000054 on body_E, −0.000059 on bias.
- **Worked tick 1231 (day 3, index 1081): a bite with a full tank.** food 0.05 on this tick, E = 1.0 before and after (capped), so r = 0. Q(x, LEFT) = +0.007341, y = +0.007669, miss = **+0.000327**. (w[LEFT]·x = 0.030972 here, mean_A 0.947.)
- Weights: w_norm (w, u, v) at birth 0.1012; after night 0 0.0956 → after night 14 0.0781 (14 nights apart; downscaling 1%/night plus learning).
- Steering pairs (w[LEFT,k] − w[RIGHT,k], day means): contrast_B +0.0255 (d0) → +0.0168 (d2) → +0.0126 (d4) → +0.0034 (d10) → +0.0024 (d14), positive on 100% of ticks. contrast_A −0.030 (d0) → +0.0005 (d2) → +0.0061 (d4) → +0.0017 (d10) → +0.0024 (d14); first positive at tick 708 (third day), wanders around zero days 6–9, ends small positive. contrast_C −0.0079 (d0), −0.0128 (d2), −0.0009 (d10).
- Turns toward the higher-A side among turns with |contrast_A| > 0.3, by day: 0.81, 0.51, 0.79, 0.73, 0.77, 0.80, 0.76, 0.73, 0.77, 0.82, 0.83, 0.86, 0.74, 0.86, 0.82 (days 0–14). Day 1 is a coin toss. findings/02 (referee trace, number of lives not stated): 0.45–0.52 on day 1 → 0.73–0.82 by day 10.
- Non-greedy actions 5–7% of ticks (ε = 0.1 over all three moves, so ≈ 1 tick in 15 actually differs).
- Action shares L/R/F: day 0 0.19/0.29/0.52; day 10 0.48/0.36/0.16.
- Hidden units: 4 at birth, 5 from night 1 (one grow event; no later day's std(r) exceeded 0.005). Knobs: 103 at birth (3 b + 36 w + 4 c + 48 u + 12 v), 119 after growth (+16 per unit).
- Committee's share of Q_LEFT − Q_RIGHT: mean 0.0018, std 0.0030 over the life; day-0 std 0.0039 vs 0.012 for the linear part; from day 10 ≈ 0.002 ± 0.0006. Reason: |u·x| ≈ 0.01 keeps every sigmoid ≈ 0.5, so a unit contributes ≈ ½(v_L − v_R) whatever x. Only the three contrast features know left from right (mean, change, body, bias are the same for both antennae, noise included).
- Bites: 267 in 4500 waking ticks ≈ 18 per day.

## Frozen-brain re-derivation (video/data/frozen_brain_test.py → .json; fresh seeds 500–514; commit in file)
- Seed 203's brain after night 4 (day-5 brain), frozen: 5250 on 15/15. Mirrored antennae: mean 1013, 0/15 (640–1603). Birth brain: mean 1419, 2/15 at ceiling.

## EXP-02 (experiments/results/02_main_linear/results.json, commit 112e957, seeds 200–219; findings/02)
random 1175 [993, 1367]; tabular_q 2882 [1963, 3827] (9/20 ceiling); ebm-nolearn 1147; ebm 1102; ebm-dn 1145; ebm-dn-sign 1963 [1404, 2600]; ebm-dn-greedy 1127; ebm-dn-critic 1457; ebm-td 4113 [3210, 5014], 15/20 ceiling, food 9.08; ebm-all 2076 [1437, 2771]; tabular_q_next 3919 [3025, 4803] (14/20). Paired ebm-td − tabular_q +1230 [−187, 2552]; vs tabular_q_next +194 [−1200, 1698]. P1 failed, P2 failed, P3 held, P4 not supported, P5 held.
- No arm avoids poison (ebm-td per-tick poison rate vs random −0.011, p 0.84). ebm-all step-size casualty (α 0.3; at 0.1 on fresh seeds 4806). Hidden units do not carry the linear win (v = 0 frozen brains 5250 on 15/15). ebm-td's 5 failed lives ate 0–1.05 food.
- A16: uncentred Q starts ≈ 2.8 for every move; target y = r + 0.9·maxQ′ ≈ 2.5, so td ≈ −0.28 every tick; each step lowers only the taken move; the greedy move lost its top spot after its own update 64–69% of the time (pilot: ebm-all 627 uncentred vs 3729 centred). A17: shipped tabular_q built s′ from the pre-move reading (not textbook); tabular_q_next added. The alpha_q pilot was re-run after A16 (0.1 → 0.3); the main run was not redone.
- Tabular Q's table: 3 signs (L−R per note, dead zone 0.02) → 27 patterns × 2 hunger states (E < 0.5) = 54 rows × 3 moves.

## EXP-01 (findings/01; results/01_main_linear; seeds 100–119)
ebm 973 [806, 1167] vs ebm-nolearn 1224 [1071, 1399]; tabular_q 3212; braitenberg 4072; oracle 3616; random 1303.
- research/07: night-1 step |Δθ| 0.68–1.39 vs |θ₀| 0.087–0.093 (seeds 300–319); after night 1 the top move's probability is at least 0.996, 0.981, 0.9995, 0.969 on seeds 300–303 (from entropies 0.028, 0.092, 0.004, 0.139 of max 1.099): > 96% on all four, > 99% on two; resting turn bias after night 1 0.533 [0.341, 0.747] vs 0.014 without learning; seed 313 +0.99 → −1.00 overnight. lr/T² is one knob. Block-means SNR 1.92 [1.56, 2.37] per day, right sign 96% of days. EXP-01 night 1 replayed ~300 samples (one day cached), ~15 batch steps of 0.08–0.19 each.
- Capacity (research/07 §1.1): the five-number construct (A pair ±3, C pair, b[FORWARD]) lives 5250 on 20/20 held-out seeds 320–339; the **two-knob** A pair alone lives 5250 on **10/10** fresh seeds 340–349.
- Biology (research/07 §3): worm (302 neurons) learns to avoid the smell of bacteria that made it sick; fly larva learns an odour's value from sugar via four dopamine neurons; every such animal has an innate reinforcer and fixed plasticity sites.

## Design constants
World 48×48; diffusion f + α·(sum of 4 neighbours − 4f) = f + 4α·(average − f), α = 0.18 (72% of the way), stable iff α ≤ 0.25 (checkerboard mode amplification 1 − 8α); keep 0.95; emit 0.05 per tick per unit mass; food budget 24 mass (12 items of 2.0), 4 poison items of mass 2.0 (8 mass); bite 0.05 within radius 1. Blends: food A+B, poison B+C. Food mass is 3× poison mass, so B points mostly to food here. Senses: antennae ±45°, 1.5 cells; log1p(c/0.05); noise σ 0.02; contrast (L−R)/(|L|+|R|+0.05); A9's recorded reason: raw L−R ≈ 0.15 log units would need knobs ≈ 13 for a decisive turn, contrast makes it order one. Smell falloff at index 3000: A peak 0.214, 2 cells 0.038 (5.6× weaker), 4 cells 0.012 (18×); map range ≈ 1000× (A), 840× (B). log1p readings: 0.05 → 0.693, 0.5 → 2.398, 5 → 4.615 (100× louder = 6.7× bigger). softplus(−3) 0.0486, (0) 0.693, (3) 3.049; sigmoid(−3) 0.047, (0) 0.5, (3) 0.953. 4·log 2 = 2.773. 0.9^20 = 0.122, 0.9^50 = 0.0052, 0.99^20 = 0.818, 0.5^3 = 0.125.
Body: E0 0.8, metabolic 0.0005, move 0.001, unit 1.25e-5, toxicity 0.5, toxin decay 0.98, drain 0.01·X; D = w_E·|E_set − E|^n + w_X·|X_set − X|^n with w 1, setpoints 1 and 0, n 2; E capped at 1.0; death at E ≤ 0.
Brain: 3 moves (turn 30° + 1 cell; forward 1 cell), H0 4, T 0.3 (used to act in EXP-01 only), init 0.01, centre on in q mode, ε 0.1, γ 0.9, α_q 0.3 (a different alpha from the diffusion's), λ 0.95 (rule one's credit), day 300, sleep 50, replay 3 days × 3 epochs batch 64, downscale 1%, growth if std(r) > 0.005, max 32.
Rule one: Δθ = lr·R·∂log π/∂θ = (lr·R/T)[−∂F(x,a) + Σ π(a′) ∂F(x,a′)]. Rule two: y = r + γ(1−done)·max Q(x′); θ += α·(y − Q)·∂Q/∂θ via grad_negF (coef onehot: b, the w row and the v column of the taken move, plus the shared c and u).
Expectation example: values 10, −5, 0 with chances 0.5, 0.3, 0.2 → 5 − 1.5 + 0 = 3.5.

## Forbidden/retracted phrasings: "gravity well"; "beats tabular Q"; "3 numbers"; "cannot unlearn" as current truth; "data-starved"; "the hidden units did it"; "avoids poison"; amoebae learn; "standard textbook learner" for the shipped tabular_q.
