# Referee 1 (mathematics and numbers) on video/script/00-09 + FACTS.md

Date: 2026-10-15. Brief: break the script. Every spoken number was checked against the replay dump
(`video/data/life203.npz`), `runs/exp02-linear/203-ebm-td/run.json`, `experiments/results/02_main_linear/results.json`,
`video/data/frozen_brain_test.json`, `findings/01`, `findings/02`, `research/07`, `DESIGN-AMENDMENTS.md`,
`experiments/EXP-02-prereg.md`, `decisions/0002` and `creature/*.py`. Check commands were run with
`cd /home/abied/ebm-lab && uv run python -c "..."`; the key values are quoted inline below.

Severity: BLOCKER = false or forbidden; MAJOR = misleading or overclaim; MINOR = imprecise.
Items are grouped by severity, then in script order. Nothing in the script was modified.

## What checked out (so the writer knows what not to touch)

Tick 14 (E after 0.82675, D before 0.04915, D after 0.03002, r +0.01914); tick 192/193 (X 0.025 / 0.0495,
r −0.00079 / −0.00202); 91% of waking ticks r < 0 (0.9076); r range −0.0038 … +0.0350; 267 food bites,
30 poison bites, 13.35 / 1.5 mass; birth x and birth Q; tick 3693 x and Q (+0.00109, −0.00234, −0.00157),
greedy LEFT, taken LEFT; softmax at T 0.3 (0.336, 0.332, 0.333), T 0.05 (0.347, 0.324, 0.329), T 0.001
(0.907 on LEFT); b after night 14 (0.0047, 0.0021, 0.0057); w_norm 0.0956 after night 0 → 0.0781 after
night 14; H 4 → 5 on night 1, no later surprise above 0.005 (closest 0.0048); explore fraction 5.0–7.3%;
action shares day 0 0.187/0.293/0.520, day 10 0.480/0.357/0.163; B pair positive on 100% of ticks;
day-mean steering pairs in FACTS (A −0.030/+0.0005/+0.0061/+0.0017/+0.0024; B +0.0255/+0.0168/+0.0126/
+0.0034/+0.0024; C −0.0079/−0.0128/−0.0009); tick 1231 Q 0.00734, y 0.00767, td +0.00033; frozen test
(5250 15/15; mirrored mean 1012.6, 0/15, 640–1603; birth 1419.3, 2/15); all EXP-02 arm means and CIs;
all EXP-01 numbers; the softmax, exp, log1p (0.693 / 2.398 / 4.615), softplus (0.0486 / 0.693 / 3.049),
4·log 2 = 2.773, 0.9^20 = 0.122, 0.9^50 = 0.0052, 0.99^20 = 0.818; the 2-D explicit 4-neighbour
diffusion bound (amplification 1 − 8α on the checkerboard mode, so |g| ≤ 1 iff α ≤ 0.25; at 0.25 the
cell lands exactly on the neighbour average; at 0.30 g = −1.4 and the checkerboard grows); softplus as the
log of e^0 + e^z; slope of softplus = sigmoid; the policy-gradient positive/negative split; the toy
"praise without comparison" (positive phase alone with constant R: E[Δb_a] ∝ π(a), so the gap b_i − b_j
grows whenever π_i > π_j and the policy sharpens onto whichever action is currently most chosen; with both
phases E[onehot − π] = 0); the Q target; gradient of a weighted sum; the drive formula; the 64–69% A16
number; the mirrored-antennae logic (mirroring flips contrast only; mean, change, body, bias are symmetric
in L and R even with noise, because noise is added to L and R before the symmetric mean). No forbidden
phrase is used as a current claim: "cannot unlearn" appears only as quoted, retracted history (07 p02);
"beats tabular Q" and "avoids poison" appear only under "not shown" (09 p02).

## BLOCKERS

1. **06 p09 and FACTS "TD example, tick 3693".** Spoken: "Tick three six nine three: Q was minus zero
   point zero zero one two, the lesson was six hundred-thousandths, the best next Q was minus zero point
   zero zero one five, so y is minus zero point zero zero one two five, and the miss is one
   hundred-thousandth."
   Truth: those numbers are at **array index 3693 of the dump, which is tick 4293 (day 12)**, not tick
   3693. At tick 3693 (dump index 3193, day 10) the same brain has Q(x, LEFT) = **+0.00109** (the value
   the script itself speaks in 02 p06 and 05 p13 for this tick), r = **−0.00026**, recorded y_target =
   **+0.00089**, miss = **−0.00020**. At index 3693 (tick 4293): x = (0.034, 0.207, 0.331, 0.251, 0.352,
   0.134, −0.070, −0.129, −0.044, 0.996, 0.046, 1), Q = (−0.00120, −0.00350, −0.00189), r = +0.00006,
   y = −0.00122, miss = −0.000014. Source: `life203.npz` keys t, Q, r, y_target, td; `t[3693] = 4293`.
   FACTS also labels tick 3693 "day 12"; tick 3693 is day 10 (3693 // 350 = 10). The chapter therefore
   quotes two different ticks under one label and the Q spoken here contradicts the Q spoken for the
   same tick two chapters earlier.
   Replacement (keeping the real tick 3693): "Tick three six nine three: Q for left was plus zero point
   zero zero one one, the lesson was minus twenty-six hundred-thousandths, the best next Q was about
   plus zero point zero zero one three, so y is plus zero point zero zero zero nine, and the miss is
   minus two ten-thousandths. Small, and the knobs barely move." (Or relabel the example as tick 4293,
   day 12, and fix FACTS to match.)

2. **03 p02.** Spoken: "Each cell moves a fraction alpha of the way toward the average of its four
   neighbours."
   Truth: `physics.diffuse` computes f + α·(sum of 4 neighbours − 4f) = f + **4α**·(neighbour average − f).
   At α = 0.18 the cell moves 72% of the way to the average, not 18%. The script's own next sentence
   ("exactly four times the difference between the neighbour average and the cell") contradicts the
   first. The viz "α = 0.25: a cell takes exactly the neighbour average" (03 p03) is right only with 4α.
   Replacement: "Each cell moves four alpha of the way toward the average of its four neighbours. At
   alpha one quarter it lands exactly on that average."

3. **05 p06 and FACTS (EXP-01 block, "Capacity").** Spoken: "two knobs, plus three on the left move's A
   contrast and minus three on the right move's, and nothing else, live the full fifteen days on twenty of
   twenty held-out seeds."
   Truth: `research/07` §1.1: the **20/20 on seeds 320–339** was the five-number construct (A pair, C pair
   and b[FORWARD], k = 3). The **two-knob** A-pair-alone result is the referee ablation on **fresh seeds
   340–349, 10/10**. FACTS merges the two ("2 non-zero weights ... 5250 on 20/20 held-out seeds").
   09 p02 ("with two knobs") is fine; only the seed count is wrong.
   Replacement: "two knobs, plus three on the left move's A contrast and minus three on the right
   move's, and nothing else, live the full fifteen days on ten of ten fresh seeds; with two more knobs
   against C it is twenty of twenty."

4. **02 p09.** Spoken: "Near a food source the smell is a hundred times stronger than two cells away."
   Truth: from the dump's fields, the ratio of the A peak to the value two cells away is **4.8–5.8×**
   at every sampled tick (e.g. tick-index 3000: 0.214 → 0.083 → 0.038 → 0.020 → 0.012 at 0–4 cells; 18× at
   four cells). Source: `life203.npz` key fields. The "whisper and a shout" point survives on the full map
   range, but the spoken ratio is false.
   Replacement: "Two cells from a food source the smell is already five times weaker, and four cells
   away twenty times weaker; across the map it spans well over a hundredfold."

5. **02 p02 and 05 p05.** Spoken: "twelve products, one total. Tiny numbers, about a thousandth" and
   "Pull out the row for left, multiply by the real readings of tick three six nine three, add up: a total
   of about a thousandth."
   Truth: w[LEFT]·x at tick 3693 = **0.0142** with that tick's weights and **0.0147** with the night-14
   weights; the two biggest products are body_E (0.919 × 0.0094 = 0.0086) and the constant (0.0034). The
   final Q_LEFT = +0.0011 only after adding b_LEFT (+0.0040) and the committee's centred share (−0.0172).
   Source: `life203.npz` theta_w, x; `run.json` brain[14].w. Fourteen thousandths is not "about a
   thousandth", and the audience will see the sum on screen.
   Replacement: "...add up: about fourteen thousandths, most of it from the energy reading and the
   constant. The committee's share and the resting preference then bring the final Q for left down to
   about a thousandth."

6. **07 p01.** Spoken: "Tabular Q, the standard textbook learner, lived three thousand two hundred."
   Truth: A17 (`DESIGN-AMENDMENTS.md`, `baselines.TabularQ` docstring): the shipped `tabular_q` builds
   s′ from the pre-move sensation and "is not textbook Q-learning"; the script itself says so in 07 p03
   ("the textbook baseline was not textbook"). Calling it "the standard textbook learner" eleven
   sentences earlier is the exact claim the referee struck.
   Replacement: "Tabular Q, the classic table-based learner as it was then written, lived three
   thousand two hundred."

## MAJOR

7. **05 p11.** Spoken: "the learner that worked compares Q to a target near zero, and starting all three
   at two point eight meant every learning step pulled only the taken move down."
   Truth: the target is y = r + 0.9 · max Q′ (`sim.q_targets`). With every Q ≈ 2.8 the target is ≈ 2.5,
   not near zero; the TD error is ≈ −0.28 on every tick ("large and negative in every state",
   `brain.learn_q` docstring). The direction is right, the mechanism as spoken is wrong: it is the
   discount that makes an unanchored positive constant decay, one taken action at a time.
   Replacement: "the target is the lesson plus nine tenths of the next Q, so with every Q sitting at two
   point eight the target is always about a quarter below it, and every step pulled only the taken move
   down."

8. **07 p09 and FACTS ("Turns toward the higher-A side").** Spoken: "This particular seed was a lucky
   starter and turned toward A from day zero." FACTS lists 0.81 (day 0), 0.80 (day 5), 0.83 (day 10),
   0.82 (day 14).
   Truth (same measure, turns with |contrast_A| > 0.3): day 0 **0.81** (n 63), day 1 **0.51** (n 70),
   day 2 0.79, day 3 0.73, day 4 0.77, day 5 0.80, day 10 0.83, day 14 0.82. Day 1 is at chance and is
   omitted. On days 0–1 the A pair itself was at its most negative (−0.030, −0.019); the day-0 0.81 is
   carried by the B pair, because A and B contrasts co-vary at food. Source: `life203.npz` a, x,
   theta_w. The selective list makes the ratio look flat when it dipped to a coin toss.
   Replacement: "This seed turned toward A on four turns in five already on day zero, fell to a coin
   toss on day one, and was back above three quarters from day two. That ratio is noisy, which is why
   the frozen test, not this ratio, is the proof."

9. **06 p09 and FACTS (eat tick 1231).** Spoken: "A tick after a bite, at tick one two three one"; FACTS:
   "r = 0 that tick (the bite landed the tick before)".
   Truth: food[1231] = 0.05, a bite landed **on** this tick (and on 1230); E was **1.0 before and after**,
   so the bite was wasted at the cap (`body.tick`: E = min(E_max, ...)) and the lesson is zero. Source:
   `life203.npz` food, E at index 1081. The explanation given is wrong and misses a teaching point (a
   positive Q of 0.0073 on a tick whose bite buys nothing).
   Replacement: "At tick one two three one it is biting food with a full tank, so the lesson is zero:
   Q zero point zero zero seven three, y zero point zero zero seven seven, miss plus three
   ten-thousandths."

10. **03 p01 against 07 p07.** Spoken (03 p01): "Notice that B is in both. That is on purpose: 'B means
    food' is a wrong lesson the creature can learn." Spoken (07 p07): "In this seed the steering was
    carried by B ... so 'toward B' pays, and the body rewarded it."
    Truth: in the linear world food mass (budget 24) emits three times the B that poison does (4 items ×
    mass 2 = 8), and `research/07` §2.2 measures the B-contrast gradient at SNR +1.40/−1.38 with the right
    sign. "Toward B" is a paying lesson here, not a wrong one. The two chapters contradict each other.
    Replacement (03 p01): "Notice that B is in both. In this world B still points mostly to food, because
    there is three times as much food mass as poison mass. Hold that; it comes back in chapter seven."

11. **06 p14 (spoken and viz).** Spoken: "Rule one scaled every lesson up to size one and then divided
    by the temperature, three point three, so each batch moved the knobs by about a tenth." Viz: "step on
    900 samples".
    Truth: T = 0.3; dividing by 0.3 is a factor of 3.3. As spoken, the temperature is named as 3.3. And
    EXP-01's night 1 had 300 cached samples, not 900 (one day cached; `research/07` §2.2: "each of the
    ~15 batch steps is 0.08–0.19"); 900 is reached from night 3.
    Replacement: "Rule one scaled every lesson up to size one and then divided by the temperature,
    zero point three, a factor of three point three, so each batch moved the knobs by about a tenth."
    Viz: "~300 samples on night 1, ~15 batch steps".

12. **05 p14 and FACTS ("Hidden units ... near-constant bias of ~0.002–0.008").** Spoken: "the fifth unit
    was born with its output knobs at zero, so the committee contributed a bias too, not steering."
    Truth: the committee's share of Q_LEFT − Q_RIGHT over the life has mean **0.0018**, std **0.0030**,
    range **−0.028 … +0.017**; on day 0 its std (0.0039) is a third of the linear share's (0.012); from
    day 10 it is ≈ 0.002 ± 0.0006. Day means run 0.001–0.003, not 0.002–0.008. It is near-constant late,
    not all life, and the reason is not the fifth unit's v = 0 (the four birth units have v_L ≠ v_R); it
    is that |u·x| ≈ 0.01 keeps every sigmoid at ≈ 0.5, so the unit's contribution ≈ ½(v_L − v_R)
    regardless of x. Source: `life203.npz` theta_c/u/v, x.
    Replacement: "In seed two hundred and three the committee's input knobs stayed near a hundredth, so
    every unit sat halfway on, and its left-minus-right share was a small, slowly drifting constant of
    about two thousandths. The steering lived in the three contrast knobs."

13. **01 p03 and 06 p01.** Spoken: "Our creature's brain has one hundred and three knobs. Learning ...
    means one thing: turning knobs. Nothing else ever changes inside the brain." 06 p01 on screen: "103
    knobs".
    Truth: 103 is the birth count (3 + 36 + 4 + 48 + 12). Growth adds a unit with 16 new knobs
    (`brain.add_units`); seed 203 has **119** knobs from night 1 onward (06 p13 describes this growth).
    "Nothing else ever changes" is contradicted by the lesson's own chapter six.
    Replacement: "...one hundred and three knobs at birth. Learning means turning them. The one other
    thing that can change is that on an eventful night the brain grows a new unit with its own knobs."

14. **06 p09.** Spoken: "Only the taken move's knobs move; the other two moves made no promise this tick."
    Truth: `grad_negF` also returns non-zero g["c"] and g["u"] (the committee's thresholds and input knobs
    are shared across moves) and they move on every step; only b, the w row and the v column of the two
    untaken moves stay. Viz "Only the LEFT row of w lights up" is right for w but not for the brain.
    Replacement: "Only the taken move's own knobs move, plus the committee's shared input knobs; the
    rows that belong to the other two moves stay put."

15. **07 p09.** Spoken: "Across all twenty seeds, the fraction of turns toward the side with more A rises
    from about a half on day one to about three quarters by day ten."
    Truth: `findings/02` ("What ebm-td learned") gives 0.45–0.52 → 0.73–0.82 without saying how many
    lives were traced; it is a referee trace, not a 20-seed statistic, and no per-tick dump exists for the
    other 19 seeds (`runs/exp02-linear/` holds seed 203 only). "Across all twenty seeds" is not in any
    source.
    Replacement: "In the lives the referee traced, the fraction of turns toward the side with more A
    rose from about a half on day one to about three quarters by day ten."

16. **07 p03.** Spoken: "Both were found before the main run, so nothing had to be redone."
    Truth: after A16 the alpha_q pilot **was** re-run on the centred code (prereg addendum items 9 and
    13; the first pilot picked 0.1, the re-run picked 0.3). The main run was not redone; the pilot was.
    Replacement: "Both were found before the main run. The step-size pilot was re-run on the fixed code;
    the main run never had to be."

17. **07 p07.** Spoken: "Your own world file once said B carries no information. The referee showed that
    sentence is wrong for the gradient, and it is corrected in the record."
    Truth: `creature/world.py` line 15 **still** says "B carries no information". The correction lives in
    `research/07` §2.2 only. "Once said" implies the file was fixed.
    Replacement: "Your own world file still says B carries no information. The referee showed that is
    wrong for the gradient, and research seven records the correction."

## MINOR

18. **FACTS (seed 203 block).** "Initial w_norm (θ₀) 0.065." Truth: 0.1012 over w, u, v (b and c are
    zero at birth, so the full norm is the same). Source: `life203.npz` theta0_*. Not spoken anywhere;
    fix the sheet. (06 p05's "about 0.09" is research/07's figure for seeds 300–319 and is fine as such.)

19. **07 p07.** Spoken: "The A pair starts negative, turn away from A, crosses zero around the third night,
    and settles small and positive."
    Truth: nightly snapshots −0.0258, −0.0058, +0.0080; per tick it first turns positive at **tick 708**,
    the first minutes of day 2, right after the second night; it then hovers around zero on days 6–9 (day
    means +0.0010, −0.0000, −0.0001, +0.0005), with 59 sign changes in all, before ending at +0.002–0.006.
    "Around the third night" is defensible; "settles" is generous. Viz "crosses zero around night 2–4" is
    fine.
    Replacement: "crosses zero on the third day, wanders around zero for a few days, and ends small and
    positive."

20. **05 p14.** "their knobs can only add a fixed turning bias." The bias scales with the symmetric
    readings (mean, change, E, X), so it varies with smell strength and hunger, just not with side.
    Replacement: "their knobs can only add a turning bias that does not know which side."

21. **03 p07.** The reason given for dividing by the sum (same turn signal near and far) is not the lab's
    recorded reason. A9 / `senses.py`: raw L − R is ~0.15 log units, a decisive turn would need weights
    ~13; contrast makes it O(1). In log units the difference is already scale-free near a source (it is a
    log ratio); it is the far, linear regime where the raw difference shrinks. Also the code divides by
    |L| + |R| + ε (readings can go negative with noise), and the viz example gives 0.066 near vs 0.060
    far, which is "close", not "the same".
    Replacement: "Why divide by the sum? In log units the left-right difference is only about fifteen
    hundredths, so a decisive turn would need knobs of thirteen. Dividing by the total stretches it to
    order one, and knobs of order one are enough."

22. **04 p02.** Reason two: "the sign must not matter. Over the setpoint or under it, the square is the
    same." `body.drive` takes abs() before the power, so sign symmetry does not come from squaring; and E
    is capped at E_max = E_set, so E never sits over its setpoint. Keep reasons one and three; recast two.
    Replacement: "Second, the code takes the absolute distance first, so over or under reads the same,
    and the square then makes the far side steep."

23. **02 p09.** "A hundred times louder is only six times bigger on the reading." 4.615 / 0.693 = 6.7.
    Replacement: "...is under seven times bigger on the reading."

24. **02 p10.** "That is the only knob in the nose." `SenseConfig` also has antenna angle 45°, length 1.5,
    noise 0.02 and the contrast floor 0.05 (two of which the script names in 03 p05–p07).
    Replacement: "That is the only knob in the log."

25. **05 p13.** "On tick three six nine three the highest is left, by a thousandth." Q_L − Q_R = 0.0034,
    Q_L − Q_F = 0.0027. Replacement: "...the highest is left, by about three thousandths."

26. **06 p03.** "when the lesson does not depend on the move, the two phases cancel and nothing moves."
    They cancel in expectation (E[onehot − π] = 0); each sample still moves the knobs, the average drift
    is zero. Replacement: "...the two phases cancel on average and the policy stays where it is."

27. **06 p04.** "that third step is exactly where the trouble started." `research/07` §2.2: the knob is
    lr/T²; standardisation makes the step scale-free, and it is the size-one lesson times lr = 1 divided
    by T = 0.3 that is too big. Standardisation alone is not the culprit.
    Replacement: "...and that size-one lesson, multiplied by the learning rate and divided by the
    temperature, is where the trouble started."

28. **06 p12.** "A bite is one tick in three hundred." Seed 203 took 267 bites in 4500 waking ticks, about
    one tick in seventeen (18 per day). True-ish for the dying EXP-01 arms (2–4 meals a day), false for the
    life on screen. Replacement: "A bite is a handful of ticks in a day of three hundred."

29. **06 p13.** "the brain's total knob length slides from zero point zero nine six to zero point zero
    seven eight over fifteen nights." 0.0956 is the value **after** night 0, so fourteen nights separate
    the two numbers, and w_norm covers w, u, v only (not b, c). Replacement: "...slides from zero point
    zero nine six after the first night to zero point zero seven eight after the last."

30. **07 p07.** "the world keeps twenty-four units of food against four poison items." Emission is per
    unit of mass: 24 mass of food against 4 × 2 = 8 mass of poison. Replacement: "...keeps twenty-four
    units of food mass against eight of poison."

31. **04 p06 viz.** "D rises by X²". D rises by X² plus the hunger term: 0.000625 + 0.00016 = 0.00079 at
    tick 192. Replacement in viz: "D rises by X² plus the usual metabolic creep".

32. **00 p02.** "It takes the move with the best number." Nine times in ten (ε = 0.1); the one-in-ten is
    introduced only in 01 p14. Replacement: "Nine times in ten it takes the move with the best number."

33. **01 p06.** "Positive: this reading pushes the score up." In 01 p02 the score is energy, where low
    wins, but a positive w lowers F. The ambiguity is resolved only in 05 p03. Replacement: "Positive:
    this reading adds evidence for the move, so its energy goes down."

34. **06 p01.** "The first is the classic energy-based rule." It is REINFORCE for a Boltzmann policy
    (`brain.py` docstring, Williams 1992); the positive/negative phase form is what makes it look like
    contrastive EBM training. Replacement: "The first is the contrastive policy-gradient rule, the
    energy-based classic."

35. **06 p14 (consistency with Limits).** "One rule's step was sane for its targets and one was not."
    `findings/02` Limit 1: the exact per-sample gain exceeds 2 on 54% of day-0 ticks for `ebm-td` too.
    The following caution sentence covers it; the word "sane" is still too strong for a step the referee
    measured past the bound on half the ticks. Replacement: "One rule's step was small enough for its
    targets, just, and one was not."

## Verdict

The script is built from the right sources and most of its two hundred or so numbers are exact. But it
cannot ship as written. Six spoken statements are false or forbidden: the chapter-six TD worked example is
labelled tick 3693 while its numbers come from tick 4293, so the Q it speaks (−0.0012) contradicts the Q it
spoke for the same tick in chapters two and five (+0.0011); the diffusion rule is stated with α where the
code has 4α; the two-knob forager is credited with 20/20 seeds that belong to the five-number construct;
the "hundred times stronger two cells away" is about five; the LEFT dot product is spoken as "about a
thousandth" when the screen will show fourteen thousandths; and tabular Q is called "the standard textbook
learner" four paragraphs before the script explains that it is not. Eleven further items mislead (the
uncentred-Q mechanism, a cherry-picked turn ratio that hides a day at chance, the tick-1231 explanation,
B as a "wrong lesson" in one chapter and a paying one in another, "divided by the temperature, three point
three", the committee-as-bias reasoning, "nothing else ever changes" against growth, "only the taken move's
knobs move", "across all twenty seeds", "nothing had to be redone", "once said" about a comment that is
still in world.py). The FACTS sheet itself carries three errors (the mislabelled TD tick and its "day 12",
the 20/20 attribution, θ₀ norm 0.065 for 0.101) and one selective list (turn ratios without day 1), and the
script inherited all of them, so the sheet should be fixed first and the chapters re-checked against it.
The underlying mathematics (softmax, softplus as a summed-out free energy, the two-phase gradient, the toy
collapse, the Q target, the stability bound, the drive) is correct throughout.
