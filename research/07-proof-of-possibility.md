# Research 07 — Proof of possibility: can a body-taught energy-based brain learn to forage at all?

**Date:** 2026-10-14 (session 03). **Author:** the orchestrator (Fable), while the swarm built EXP-02.
**Status:** revised after two hostile referees (session 03). Referee 2 (biology/theory) found a reversed
citation (Schroll 2006) and six over-claims; all rewritten in place with the referee's sourced wording.
Referee 1 (mathematics) retracted two claims (2.3's correlation was computed on the wrong night; "cannot
unlearn" is contradicted by the trajectories) and sharpened four; all rewritten in place, with the
retracted wording quoted so the correction is visible.
Scripts and raw json: `research/07-proof-of-possibility/` (seeds 300–339, declared proof seeds; not used
for tuning any learner). Commit at the runs: see each json's `commit` field.

The question Ahmed set: *is this possible, in the mathematics and in biology?* "This" = a creature that is
not told what food is, whose body's drive change is the only teacher, with an energy-based brain, learning
within a life and across generations. Three sub-questions, each answered below with a measurement or a source:

1. **Capacity.** Does the EBM's model class even contain a foraging policy? (If not, no learner can find it.)
2. **Signal.** Does the body's lesson carry enough information per day for a gradient learner to find it?
3. **Precedent.** Do real organisms of comparable size do this, and with what ingredients we lack?

## 1. Capacity: the class contains the solution (M1)

**By construction.** Braitenberg's rule can be written directly into the energy: `w[LEFT,cA]=+k`,
`w[RIGHT,cA]=−k`, `w[LEFT,cC]=−k`, `w[RIGHT,cC]=+k`, `b[FORWARD]=0.05k`, everything else zero, no hidden
units, no learning, no sleep. `m1_existence.py construct`, 20 held-out seeds 320–339, 15 days:

| world | arm | ticks alive (mean [95% CI]) | food | poison |
|---|---|---|---|---|
| linear | braitenberg (raw L−R, dead zone) | 4223 [3526, 4874] | 26.7 | 0.01 |
| linear | **ebm, hand-set k=3** | **5250 [5250, 5250]** (ceiling) | 24.0 | 0.01 |
| linear | ebm, hand-set k=10 / k=30 | 5250 / 5250 | 24.6 / 25.0 | 0.00 |
| linear | ebm, untrained | 1176 [999, 1379] | 0.95 | 0.31 |
| xor | braitenberg | 2775 [2248, 3342] | 14.6 | 4.10 |
| xor | **ebm, hand-set k=3** | **5250 [5250, 5250]** | 23.0 | 3.43 |
| xor | ebm, untrained | 1219 [1060, 1386] | 1.00 | 0.26 |

**Claim 1.1.** The linear world is solved by a point in the EBM's parameter space with **2 non-zero
numbers**: referee ablation on fresh seeds 340–349 shows the A-contrast pair alone reaches 5250 in both
worlds; the C-aversion pair is not needed and costs food (24.7 with it vs 37.2 without, linear), and
b[FORWARD] makes no difference. (First draft said "3 numbers" and offered an untested explanation for
beating Braitenberg; both withdrawn.) EXP-01's failure is therefore a failure of *learning*, not of
capacity.

**Claim 1.2 (unplanned, important).** 5250 = 15 × (300 + 50) is the **ceiling** of `ticks_alive` at
15 days. A good arm in EXP-02 will be censored at it; the gap fraction is then a lower bound. (Pre-registered
days are not changed; the censoring is recorded here before the run.)

**Claim 1.3 (unplanned, important).** The **xor world does not force the conjunction**: a true
A-chaser (A weights only; the k=3 arm's C weights only react to sensor noise in xor, where nothing
emits C) eats **6.15 poison** per life with 34 food and still lives the full 15 days on 10/10 seeds
(referee rerun; the first draft's 3.4 was the k=3 arm), because at toxicity 0.5 the poison is paid for
by the food. P4's premise ("single-note signs cannot solve xor") is about
representation, and still stands; but the xor world as calibrated does not *punish* the linear solution
enough to make the conjunction necessary for survival. This is a world-design decision for Ahmed
(raise toxicity, or make poison deplete energy directly) and must not be changed inside EXP-02.

**By search (M1b).** An evolution strategy over the full θ with 4 hidden units (103 parameters;
population 24, elite 6, 40 generations; search seeds 300–303, held-out 320–339), xor world:
`m1_search_xor.json`. The best member hit the 5250 ceiling in generation 1, the population mean reached
5250 by generation 39, and the final θ lives **5250 on 20/20 held-out seeds** (food 13.7–21.5 on the
first five). Consistent with 1.3: the xor world is easy for an A-chaser, so search finds a survivor at
once and the result says nothing about the conjunction. Provenance note: the process imported the
creature code at launch (commit `2e30295`) and ran for 52 min across later merges; the json's `commit`
field (`3866e04`) was stamped at write time. No file it depends on for a frozen, non-learning life
(`physics`, `world`, `body`, `senses`, `Brain.F` with centre off) changed in between.

## 2. Signal: the lesson is informative; the step is the problem (M2, M3)

**M2 (`m2_snr.py`).** For an untrained creature's first three days, the per-sample contribution to the
one weight direction that matters most ("turn toward more A": `w[LEFT,cA] − w[RIGHT,cA]`) is
d_i = R_i · ∂logπ/∂w. Batch-means standard errors (blocks of 30 ticks, because R is λ-credited with
~20-tick memory), 20 seeds, 51 creature-days (linear) / 53 (xor):

| world | block-means SNR per day (mean [CI]) | days with SNR > 2 | sign correct | days to SNR 3 (median, IQR) | SNR for "toward C" |
|---|---|---|---|---|---|
| linear | **1.92 [1.56, 2.37]** | 39% | **96%** of days | 3 (1–8) | −0.11 (correctly ≤ 0) |
| xor | 1.59 [1.38, 1.79] | 38% | 98% | 4 (2–9) | −0.37 |

**Claim 2.1.** The body's lesson is *not* data-starved for the key direction: one day of random
walking gives a batch gradient that points the right way with ~2 standard errors (referee re-analysis:
lag-1 autocorrelation of d_i is +0.09 and ~0 from lag 5, so 30-tick blocks are conservative; pooled
SNR 1.78 linear / 1.50–1.67 xor; blocks of 60/100 give 1.9–2.1 pooled). Projected onto the full
hand-set direction the pooled SNR is 1.41–1.67 because the C half is noise, and the per-day batch
gradient has cosine only 0.20 (linear) / 0.17 (xor) with that direction. The A coordinate was chosen
with hindsight, but the ablation in 1.1 shows A alone suffices. "A learner that moved only this
direction would learn within a life" is an inference, not a measurement, and the SNR is from
untrained creatures' days. This corrects `findings/01`'s diagnosis (see its CORRECTION block).

**M3 (`m3_bias.py`).** What the actual learner does with that signal, EXP-01 `ebm` configuration,
seeds 300–319: the resting turning bias |π(LEFT|x0) − π(RIGHT|x0)| at a featureless sensation

| arm | after night 1 (mean [CI]) | last night | corr(|bias|, days survived) | days |
|---|---|---|---|---|
| ebm (learning) | **0.533 [0.341, 0.747]** | 0.698 | **−0.49** (night-1 bias; t = −2.35, n = 20, p ≈ 0.03) | 2.50 |
| ebm-nolearn | 0.014 [0.009, 0.020] | 0.014 | n/a (bias ≈ 0 throughout) | 2.95 |

(First draft reported r = 0.006: that was `m3_bias.py`'s correlation with the *last*-night bias, which is
two clusters and uninformative. Retracted by referee 1; the night-1 value above is read from the same
`m3_bias.json`. The resting bias at x0 is representative: 0.550 at the empirical mean sensation.)

and end-of-night policy entropy on seeds 300–303 after night 1: 0.028, 0.092, 0.004, 0.139 (max 1.099).

**Claim 2.2 (rewritten after referee 1).** One night at T = 0.3, lr = 1.0 turns a near-uniform policy
into a near-deterministic one (entropy < 0.15) with a large resting turn bias. **The step is measured,
not asserted:** on night 1 |Δθ| = 0.68–1.39 against |θ₀| = 0.087–0.093 (8–16× the whole initial
norm; each of the ~15 batch steps is 0.08–0.19, already the size of θ₀). The gradient is not "≈ 0 on the
other ~100 directions": over all 103 parameters the median |SNR| is 0.82 (0.67 if pure noise), 7.3%
exceed 2, and the **B-contrast pair carries SNR +1.40/−1.38** (food outnumbers poison, so B, which
both emit, is informative; the world comment "B carries no information" is wrong for the gradient).
And **the committed policy does unlearn, violently**: in `m3_bias.json` seed 313 goes +0.99 → −1.00
overnight, seed 318 +0.64 → −1.00, seed 307 FORWARD 0.99 → LEFT 0.99, seed 316 FORWARD → LEFT → FORWARD.
The first draft's "once committed … cannot unlearn" and the gravity-well reading are **retracted**:
this is step-size instability (lurching between corners), not a stall. Lowering lr to 0.1 or raising T
to 1.0 each keep night-1 entropy at 0.68–0.94; a logit-equivalent rescaling (T 1, lr 11.1, init 0.033)
collapses identically, so "too large a step" and "too low T" are **one knob** (lr/T²), not two fixes.

**Claim 2.3 (rewritten).** The night-1 resting bias *does* predict days survived within the learner
group (r = −0.49, exploratory, n = 20; lives that collapse onto FORWARD have bias ≈ 0 while just as
collapsed). So acquired turning bias is one route by which the oversized step kills, not the only one.

**Theory it rests on (sources checked 2026-10-14).**
- The learning rule is REINFORCE for a Boltzmann policy (Williams 1992; Sutton et al. 2000). Unbiased,
  high variance; the day-return standardisation makes the step scale-free but not the variance.
- Mei et al. ICML 2020, *On the Global Convergence Rates of Softmax Policy Gradient Methods*: with
  **exact gradients and tabular softmax** (one logit per state-action, μ(s) > 0), unregularised softmax PG
  converges at O(1/t) with initialisation-dependent constants, and **entropy regularisation gives a linear
  rate toward the regularised (biased) optimum** for general MDPs (Theorem 6; the first draft's "bandit
  only" was wrong, and its "our setting is close" over-claimed). No theorem in either Mei paper covers our
  case: shared linear + hidden-unit parameters over a continuous context, stochastic REINFORCE on ~300
  samples, λ-credit, clipping, per-day standardisation. What they honestly supply: a reason to expect
  entropy regularisation to help and a warning about sensitivity to initialisation. R1's entropy-bonus
  recommendation (`research/03`) stands on that, and on the one-knob finding in 2.2 (lr/T²).
- Sallans & Hinton, JMLR 5 (2004): state-action values as **negative free energies** of a product of
  experts (an RBM with the hidden units summed out, the same function class as our F), learned by
  **SARSA with Boltzmann exploration** (on-policy, actions by Gibbs sampling); they note there is no
  convergence proof for the rule in general. EXP-02's `ebm-td`/`ebm-all` arms use the **same function
  class** (Q = −F) but **off-policy Q-learning with ε-greedy acting**, so they are a close relative, not
  the same learner (referee correction, session 03). Heess, Silver & Teh 2012 and Elfwing et al. 2013
  extend the family. So "an EBM that forages by value learning" has precedent; EXP-02 asks which of Q's
  ingredients our policy-gradient EBM is missing.
- Keramati & Gutkin, eLife 2014: with reward defined as the reduction of a drive D(h) = distance of the
  internal state from its setpoint, their Proposition states that **for deterministic trajectories that
  end at the setpoint, with γ < 1, maximising the discounted sum of drive reductions equals minimising
  the discounted sum of drive** (a telescoping identity, SDR = D₀ + (γ−1)·SDD, valid for any drive
  function), and that any discounting selects the shortest path to the setpoint. Our body's
  r = D_before − D_after is their reward and our D fits their class. But our runs end at death or at a
  day boundary, our world is stochastic, and the EXP-01 learner optimises a standardised λ-return, so
  the theorem **motivates** the objective and does not prove that maximising lessons keeps the body alive
  (referee correction). "The body teaches it" is well-posed as an objective; its sufficiency is empirical.

## 3. Precedent: biology does this, with two ingredients we lack

**Within-life learning of odour valence from an internal body signal exists in ~300-neuron and
~10,000-neuron nervous systems.**
- *C. elegans* (302 neurons): after exposure to pathogenic bacteria, worms learn to **avoid the odour**
  of that bacterium; serotonin rises in the ADF chemosensory neurons and acts through the MOD-1
  channel in interneurons, and the authors *propose* that this serotonin increase is the negative
  reinforcer of infection (Zhang, Lu & Bargmann, *Nature* 438:179, 2005; the abstract hedges with "may
  represent", and ingestion itself is not shown to be required). An internal-state signal retunes a
  sense: that is the creature's law §0 in a real animal. Worms also lose their NaCl attraction after
  NaCl is paired with the **absence of food** (Saeki, Yamamoto & Iino, *J Exp Biol* 2001: associative,
  "not merely adaptation or habituation"; a serotonin food signal partly blocks it, so whether the
  teacher is sensed absence of food or metabolic state is not resolved). Later Iino-lab work located
  the switch in insulin/PI3K signalling at ASER synapses (Ohno et al., *Science* 345, 2014).
- *Drosophila* larva (~10k neurons): sugar reward, signalled by **taste and by nutrient value separately**
  (arabinose is only sweet, sorbitol only nutritious; both teach), drives the **dopaminergic pPAM
  neurons** that teach an odour's value at the mushroom body; pPAM are necessary for odour–sugar
  learning and their optogenetic activation is sufficient as a reward (Rohwedder et al., *Curr Biol*
  26:661, 2016; **not** Schroll 2006, which found dopaminergic activation aversive and octopaminergic
  appetitive in the larva: a citation error in the first draft, caught by a referee). Saumweber et al.
  (*Nat Commun* 2018) give the single-cell map and functional screen of the larval mushroom body's
  input and output neurons. Larvae learn an odour–sugar association from **a single pairing**
  (Weiglein et al., *Learn Mem* 26:109, 2019).

**Claim 3.1.** Valence learning taught by an innate reinforcer (sugar taste or nutrient, infection,
absence of food), in a life, in a tiny brain, is an experimental fact. "Body-taught" in the strict sense
of *energy state as teacher* is supported for the larva's nutrient route and is unresolved for the worm.

**But every one of these animals has two things our v0 creature lacks.**
- **An innate reinforcer and innate attractions.** E. coli's attractant preferences are genetically
  fixed; its only within-life memory is a ~4 s methylation-based comparison (CheR/CheB) that tracks recent
  concentration and assigns no value (Segall, Block & Berg, *PNAS* 1986); associative anticipation in
  E. coli is acquired over generations, not within a life (Tagkopoulos et al., *Science* 2008; Mitchell
  et al., *Nature* 2009). Larvae and worms are born attracted to specific odours and salts. In every
  case found, **the reinforcer's value is innate** (sugar, malaise, hunger) and **the plasticity sites are
  fixed**; the value of the *predicting* stimulus can be learned from neutral (Schroll 2006: "a positive
  or negative value is assigned to a previously neutral stimulus"). Our creature has the first (the innate
  drive) and lacks the second. This is the biological argument for lever 2 (generations supply the
  prior) and for A7's finding that the uniform start is itself a trap.
- **A structural prior on *where* learning happens.** In the larva the plasticity is at one synapse class
  (KC→MBON), gated by dopamine in a **timing-dependent** way: an odour before a DAN's activation yields
  punishment memory, an odour at its termination yields relief memory (Weiglein et al., *J Comp Neurol*
  2021; Thoener et al., *J Exp Biol* 2022). Our rule updates ~100 parameters with one scalar lesson
  credited over ~20 ticks. That is the ~100-noisy-directions
  problem of Claim 2.2 in biological terms. It is also Ahmed's original idea ("one job: make
  connections"): a growth rule that adds a *specific* connection for a *specific* event, rather than a
  gradient on everything.

**Single cells.** Habituation in *Physarum* and *Stentor* is reproducible; anticipation of periodic stimuli
in *Physarum* (Saigusa et al. 2008) is reported; *associative* learning in *Paramecium* (Gelber 1950s) and
*Stentor* is contested and sample-size-limited (reviews 2019–2023). So the "amoeba" framing is a metaphor
for *size*, not a claim that amoebae learn valence; the honest biological floor for within-life valence
learning is the worm.

## 4. What this proves, and what it does not

- **Proved (by construction, 1.1):** the energy model can represent the forager.
- **Measured (2.1):** the body's lesson carries enough signal per day to find it.
- **Measured (2.2):** the current learner wastes it with a nightly step 8–16× its initial weight norm,
  lurching between near-deterministic policies from night to night; lr/T² is the one knob.
- **Sourced (2, 3):** the objective is well-posed and motivated, not proved sufficient, by Keramati–Gutkin;
  the function class has value-learning precedent (Sallans–Hinton, SARSA); the biology learns stimulus
  value from neutral, but always with an innate reinforcer, fixed plasticity sites, and never with a
  global gradient.
- **Not proved:** that *this* learner, fixed, learns within a life; that is EXP-02's job. Not proved:
  that generations supply a usable prior in our world; that is EXP-03's.
- **Pre-registered consequence for EXP-02:** P2 (greedy helps most) has a candidate mechanism: argmax
  acts on weak correct weights without needing a large logit step, and ε keeps every action sampled. The
  "immune to the gravity well" phrasing is withdrawn with 2.2. P1's ceiling arm may be censored at 5250.

## 5. Sources
- Zhang Y, Lu H, Bargmann CI. Pathogenic bacteria induce aversive olfactory learning in *C. elegans*. Nature 438:179–184 (2005). https://ideas.repec.org/a/nat/nature/v438y2005i7065d10.1038_nature04216.html
- Saeki S, Yamamoto M, Iino Y. Plasticity of chemotaxis revealed by paired presentation of a chemoattractant and starvation in *C. elegans*. J Exp Biol 204:1757 (2001). https://cob.silverchair.com/jeb/article-pdf/204/10/1757/3144282/jexbio_204_10_1757.pdf
- Schroll C et al. Light-induced activation of distinct modulatory neurons triggers appetitive or aversive learning in *Drosophila* larvae. Curr Biol 16:1741 (2006). doi 10.1016/j.cub.2006.07.023
- Rohwedder A et al. Four individually identified paired dopamine neurons signal reward in larval *Drosophila*. Curr Biol 26:661 (2016). doi 10.1016/j.cub.2016.01.012
- Saumweber T et al. Functional architecture of reward learning in mushroom body extrinsic neurons of larval *Drosophila*. Nat Commun 9:1104 (2018). https://pmc.ncbi.nlm.nih.gov/articles/PMC5856778
- Weiglein A et al. One-trial learning in larval *Drosophila*. Learn Mem 26:109–120 (2019). doi 10.1101/lm.049106.118
- Weiglein A et al. J Comp Neurol (2021) doi 10.1002/cne.25037; Thoener J et al. J Exp Biol (2022) doi 10.1242/jeb.244565 (timing-dependent DAN teaching in the larva)
- Ohno H et al. Role of synaptic phosphatidylinositol 3-kinase in a behavioral learning response in *C. elegans*. Science 345 (2014). doi 10.1126/science.1250709
- Segall JE, Block SM, Berg HC. Temporal comparisons in bacterial chemotaxis. PNAS 83:8987 (1986). doi 10.1073/pnas.83.23.8987
- Tagkopoulos I et al. Science 320:1313 (2008) doi 10.1126/science.1154456; Mitchell A et al. Nature 460:220 (2009) doi 10.1038/nature08112 (anticipation evolved over generations)
- Mei J, Xiao C, Szepesvári C, Schuurmans D. On the global convergence rates of softmax policy gradient methods. ICML 2020. https://proceedings.mlr.press/v119/mei20b.html
- Mei J, Xiao C, Dai B, Li L, Szepesvári C, Schuurmans D. Escaping the gravitational pull of softmax. NeurIPS 2020. https://proceedings.neurips.cc/paper/2020/hash/f1cf2a082126bf02de0b307778ce73a7-Abstract.html
- Sallans B, Hinton GE. Reinforcement learning with factored states and actions. JMLR 5:1063 (2004). https://jmlr.org/papers/v5/sallans04a.html
- Keramati M, Gutkin B. Homeostatic reinforcement learning for integrating reward collection and physiological stability. eLife 3:e04811 (2014). https://elifesciences.org/articles/04811
- Single-cell learning reviews: https://scientificamerican.com/article/can-a-cell-remember ; https://pmc.ncbi.nlm.nih.gov/articles/PMC6936043 ; https://www.frontiersin.org/journals/cell-and-developmental-biology/articles/10.3389/fcell.2023.1249165/full
- E. coli chemotaxis mechanism: https://chemotaxis.biology.utah.edu/projects/ecolichemotaxis/ecolichemotaxis.html ; https://pmc.ncbi.nlm.nih.gov/articles/PMC4684286
