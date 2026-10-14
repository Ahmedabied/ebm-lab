# Research 07 — Proof of possibility: can a body-taught energy-based brain learn to forage at all?

**Date:** 2026-10-14 (session 03). **Author:** the orchestrator (Fable), while the swarm built EXP-02.
**Status:** draft; every numbered claim below is to be attacked by two hostile referees before it stands.
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

**Claim 1.1.** The linear world is solved by a point in the EBM's parameter space with 3 non-zero
numbers; it beats Braitenberg because the contrast feature steers from far away where Braitenberg's
dead zone is silent. EXP-01's failure is therefore a failure of *learning*, not of capacity.

**Claim 1.2 (unplanned, important).** 5250 = 15 × (300 + 50) is the **ceiling** of `ticks_alive` at
15 days. A good arm in EXP-02 will be censored at it; the gap fraction is then a lower bound. (Pre-registered
days are not changed; the censoring is recorded here before the run.)

**Claim 1.3 (unplanned, important).** The **xor world does not force the conjunction**: a pure
A-chaser eats 3.4 poison per life and still lives the full 15 days, because at toxicity 0.5 the poison it
eats is paid for by the 23 food it finds. P4's premise ("single-note signs cannot solve xor") is about
representation, and still stands; but the xor world as calibrated does not *punish* the linear solution
enough to make the conjunction necessary for survival. This is a world-design decision for Ahmed
(raise toxicity, or make poison deplete energy directly) and must not be changed inside EXP-02.

**By search (M1b).** An evolution strategy over the full θ with 4 hidden units (search seeds 300–303,
held-out 320–339): `m1_search_xor.json` — *(pending; the ES hit the ceiling on the search seeds in
generation 1, consistent with 1.3: the xor world is easy for a linear chaser)*.

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
walking gives a batch gradient that points the right way with ~2 standard errors. Three days would give
SNR 3. A creature lives 3–4 days. So a learner that moved *only* this direction, by a sensible step,
would learn within a life. This corrects `findings/01`'s diagnosis (see its CORRECTION block).

**M3 (`m3_bias.py`).** What the actual learner does with that signal, EXP-01 `ebm` configuration,
seeds 300–319: the resting turning bias |π(LEFT|x0) − π(RIGHT|x0)| at a featureless sensation

| arm | after night 1 (mean [CI]) | last night | corr(|bias|, days survived) | days |
|---|---|---|---|---|
| ebm (learning) | **0.533 [0.341, 0.747]** | 0.698 | 0.006 | 2.50 |
| ebm-nolearn | 0.014 [0.009, 0.020] | 0.014 | 0.348 | 2.95 |

and end-of-night policy entropy on seeds 300–303 after night 1: 0.028, 0.092, 0.004, 0.139 (max 1.099).

**Claim 2.2.** One night at T = 0.3, lr = 1.0 turns a near-uniform policy into a near-deterministic one
(entropy < 0.15) with a large resting turn bias. The policy commits after ~300 samples whose gradient has
SNR ≈ 2 on one direction and ≈ 0 on the other ~100 directions. Once committed, the softmax gradient
vanishes (`tests/test_brain.py` saturation note) and the creature cannot unlearn. This is the
"softmax gravity well" of Mei, Xiao, Dai, Li, Szepesvári & Schuurmans (NeurIPS 2020): convergence of
softmax policy gradient depends strongly on initialisation and can stall near confident wrong policies.

**Claim 2.3 (what M3 does not show).** The bias magnitude does not predict days survived *within* the
learner group (r = 0.006). So "acquired turning bias" is demonstrated, but it is not shown to be the
proximate cause of death; a collapsed policy fails in several ways (bias, wrong note, wrong sign on C).
Recorded as a limitation, not a mechanism.

**Theory it rests on (sources checked 2026-10-14).**
- The learning rule is REINFORCE for a Boltzmann policy (Williams 1992; Sutton et al. 2000). Unbiased,
  high variance; the day-return standardisation makes the step scale-free but not the variance.
- Mei et al. ICML 2020, *On the Global Convergence Rates of Softmax Policy Gradient Methods*: true-gradient
  softmax PG converges at O(1/t) with initialisation-dependent constants; **entropy regularisation gives
  a linear rate** (the conference talk restricts the linear rate to the bandit case; arXiv v3 gives
  O(e^{−ct}) with explicit constant). Our 3-action, near-bandit setting is close to the case where the
  result is strongest. This is the mathematical case for an **entropy bonus** instead of a low T (R1's
  recommendation, `research/03`), and for a smaller nightly step.
- Sallans & Hinton, JMLR 5 (2004): state-action values as **negative free energies** of a product of
  experts, learned by TD. EXP-02's `ebm-td`/`ebm-all` arms are exactly this learner on our features;
  Heess, Silver & Teh 2012 and Elfwing et al. 2013 extend it. So "an EBM that forages by Q-learning" is
  not speculative; the question EXP-02 asks is which of Q's ingredients our policy-gradient EBM is missing.
- Keramati & Gutkin, eLife 2014: with reward defined as the reduction of a drive D(h) = distance of the
  internal state from its setpoint, **maximising reward is equivalent to homeostasis** (their "physiological
  rationality"), and discounting selects the shortest path to the setpoint. Our body's r = D_before − D_after
  is their reward. The creature's objective is therefore well-posed: a policy that maximises the body's
  lessons is a policy that keeps the body alive. This is the formal content of "the body teaches it".

## 3. Precedent: biology does this, with two ingredients we lack

**Within-life learning of odour valence from an internal body signal exists in ~300-neuron and
~10,000-neuron nervous systems.**
- *C. elegans* (302 neurons): worms that ingest pathogenic bacteria learn to **avoid the odour** of that
  bacterium; the teaching signal is **serotonin released by the ADF chemosensory neurons after infection**,
  acting through the MOD-1 channel (Zhang, Lu & Bargmann, *Nature* 438:179, 2005). A gut-state signal
  retunes a sense: that is the creature's law §0 in a real animal. Worms also learn to avoid NaCl after
  NaCl is paired with **starvation** (Saeki, Yamamoto & Iino, *J Exp Biol* 2001; insulin signalling in
  ASER), i.e. the energy state itself is the teacher.
- *Drosophila* larva (~10k neurons): sugar ingestion drives **dopaminergic pPAM neurons** that teach an
  odour's value at the mushroom body; optogenetic activation of those neurons substitutes for the reward
  (Schroll et al., *Curr Biol* 2006; Saumweber et al., *Nat Commun* 2018, full connectome-level map of
  the larval mushroom body's reward and punishment inputs). Larvae learn an odour–sugar association from
  **a single pairing** (Weiglein et al., *Learn Mem* 2019).

**Claim 3.1.** Body-taught valence learning, in a life, in a tiny brain, is an experimental fact.

**But every one of these animals has two things our v0 creature lacks.**
- **An innate prior.** E. coli's chemotaxis is entirely innate: the run-and-tumble bias and the
  methylation adaptation (CheR/CheB) that makes it a temporal-derivative detector are not learned
  (Berg; reviews listed below). Larvae and worms are born attracted to specific odours and salts; learning
  *retunes* an existing valence. No organism I could find learns food valence from a uniform prior.
  This is the biological argument for lever 2 (generations supply the prior) and for A7's finding that
  the uniform start is itself a trap.
- **A structural prior on *where* learning happens.** In the larva the plasticity is at one synapse class
  (KC→MBON), gated by a dopamine signal with a short eligibility window around the event. Our rule updates
  ~100 parameters with one scalar lesson credited over ~20 ticks. That is the ~100-noisy-directions
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
- **Measured (2.2):** the current learner wastes it by committing after one night.
- **Sourced (2, 3):** the objective is well-posed (Keramati–Gutkin); the learner type is known to work
  (Sallans–Hinton); the biology does it, but never from a uniform prior and never with a global gradient.
- **Not proved:** that *this* learner, fixed, learns within a life; that is EXP-02's job. Not proved:
  that generations supply a usable prior in our world; that is EXP-03's.
- **Pre-registered consequence for EXP-02:** P2 (greedy helps most) now has a mechanism: argmax acts on
  weak correct weights *without* committing the softmax; it is immune to the gravity well. P1's ceiling
  arm may be censored at 5250.

## 5. Sources
- Zhang Y, Lu H, Bargmann CI. Pathogenic bacteria induce aversive olfactory learning in *C. elegans*. Nature 438:179–184 (2005). https://ideas.repec.org/a/nat/nature/v438y2005i7065d10.1038_nature04216.html
- Saeki S, Yamamoto M, Iino Y. Plasticity of chemotaxis revealed by paired presentation of a chemoattractant and starvation in *C. elegans*. J Exp Biol 204:1757 (2001). https://cob.silverchair.com/jeb/article-pdf/204/10/1757/3144282/jexbio_204_10_1757.pdf
- Schroll C et al. Light-induced activation of distinct modulatory neurons triggers appetitive or aversive learning in *Drosophila* larvae. Curr Biol 16:1741 (2006). doi 10.1016/j.cub.2006.07.023
- Saumweber T et al. Functional architecture of reward learning in mushroom body extrinsic neurons of larval *Drosophila*. Nat Commun 9:1104 (2018). https://pmc.ncbi.nlm.nih.gov/articles/PMC6432171
- Weiglein A et al. One-trial learning in larval *Drosophila*. Learn Mem 26 (2019). https://learnmem.cshlp.org/content/31/5/a053726/F1.expansion.html (via search; verify volume)
- Mei J, Xiao C, Szepesvári C, Schuurmans D. On the global convergence rates of softmax policy gradient methods. ICML 2020. https://proceedings.mlr.press/v119/mei20b.html
- Mei J, Xiao C, Dai B, Li L, Szepesvári C, Schuurmans D. Escaping the gravitational pull of softmax. NeurIPS 2020. https://proceedings.neurips.cc/paper/2020/hash/f1cf2a082126bf02de0b307778ce73a7-Abstract.html
- Sallans B, Hinton GE. Reinforcement learning with factored states and actions. JMLR 5:1063 (2004). https://jmlr.org/papers/v5/sallans04a.html
- Keramati M, Gutkin B. Homeostatic reinforcement learning for integrating reward collection and physiological stability. eLife 3:e04811 (2014). https://elifesciences.org/articles/04811
- Single-cell learning reviews: https://scientificamerican.com/article/can-a-cell-remember ; https://pmc.ncbi.nlm.nih.gov/articles/PMC6936043 ; https://www.frontiersin.org/journals/cell-and-developmental-biology/articles/10.3389/fcell.2023.1249165/full
- E. coli chemotaxis mechanism: https://chemotaxis.biology.utah.edu/projects/ecolichemotaxis/ecolichemotaxis.html ; https://pmc.ncbi.nlm.nih.gov/articles/PMC4684286
