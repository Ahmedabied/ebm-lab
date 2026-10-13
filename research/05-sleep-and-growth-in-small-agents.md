# 05 - Sleep and Growth in Small Agents: Exact Rules, Fair Controls

Research seat R3, 2026-10-13. This file goes deeper than `01-ebm-sleep-growth-literature.md` (Parts 2-4). It does not repeat that file. The aim is the exact rules and the controls a numpy creature needs.

## Citation tags

- **[read]**: I read the relevant section of the full text this session. Equations are quoted from it.
- **[abstract]**: I saw only the abstract or landing page this session.
- **[secondhand]**: the claim comes from another paper, a review, a library doc or a press release, not from the source itself.
- **[memory]**: standard textbook material I did not re-check this session. Treat it as needing a check before it goes into code comments.
- **(proposed)**: my own design suggestion. It is not a published result.

## The brain these rules are for

The rules below assume this brain:

- **Free energy:** a conditional RBM, `F(s,a) = -b_a - sum_j softplus(c_j + W_j·s + U_ja)`.
- **Policy:** `pi(a|s) = exp(-F(s,a)) / sum_a' exp(-F(s,a'))`, an exact softmax over 3 actions.
- **Wake update:** weighted by drive reduction `r`: `Δθ = η r [ -∂F(s,a)/∂θ + sum_a' pi(a'|s) ∂F(s,a')/∂θ ]`.

The second term in the wake update is the negative phase, and it is **exact**. Over 3 actions nothing needs to be sampled. Several conclusions below follow from that fact.

---

## Q1. Sleep as offline replay: what is the actual evidence?

### 1.1 Replay helps sample efficiency (well established in RL)

- **Lin 1992**, *Machine Learning* 8(3-4):293-321, doi 10.1007/BF00992699 **[secondhand]**.
  - Introduced experience replay as one of three speed-ups for AHC and Q-learning agents. The other two were learned action models for planning, and teaching.
  - The 1991 ICML precursor's abstract says the extensions "can effectively improve the learning rate and in many cases even the asymptotic performance" **[secondhand]**.
- **Schaul et al. 2016, Prioritized Experience Replay**, arXiv 1511.05952 **[abstract]**.
  - Result: beats uniform-replay DQN "on 41 out of 49 games".
  - Rule [secondhand, consistent across library docs]: sample transition `i` with `P(i) = p_i^α / Σ_k p_k^α`, where `p_i = |δ_i| + ε`.
  - Correction: weight each update by `w_i = (N·P(i))^-β / max_j w_j`, with β annealed toward 1.
  - I did not verify the paper's own α and β values.
- **Fedus et al. 2020, "Revisiting Fundamentals of Experience Replay"**, ICML, arXiv 2007.06700 **[abstract]**.
  - Defines the **replay ratio** as learning updates per unit of experience collected. It is "important across many deep RL algorithms".
  - **This is the control knob for Q1.** A sleep/no-sleep comparison is only fair if the replay ratio is matched.
- **van Hasselt, Hessel, Aslanides 2019, "When to use parametric models in RL?"**, NeurIPS, arXiv 1906.05243 **[abstract]**.
  - Replay can match or beat model-based methods when the model is only used to generate imagined transitions for a model-free update.
  - This is a direct warning for "dreaming" (Q2): a stored cache is a strong baseline for a learned generator.

### 1.2 Replay helps forgetting (well established; interleaving is the active ingredient)

- **Rolnick et al. 2019, CLEAR**, NeurIPS, arXiv 1811.11682 **[abstract]**.
  - On-policy learning (plasticity) plus off-policy learning and behavioural cloning from replay (stability). Reduces forgetting in Atari and DMLab without task labels.
  - A buffer of limited size that discards at random performs "almost as well" as an unbounded one. **This means a small reservoir cache is enough.**
- **Kubo, Delanois, Bazhenov 2025, "Toward Lifelong Learning in Equilibrium Propagation: Sleep-like and Awake Rehearsal"**, arXiv 2508.14081 **[read, HTML v1]**.
  - **Setup:** EP-trained convergent RNNs, contrastive update `Δw_ij = (α/β)(ŝ_i ŝ_j − š_i š_j)`. This is the same two-phase shape as our wake rule. Five class-incremental two-class tasks.
  - **Sleep (SRC, from Tadros 2022):**
    - Convert the network to spiking. Drive it with Poisson input at each pixel's mean training intensity.
    - Apply STDP-like steps: `+inc` if the post-synaptic unit spikes at t and the pre-synaptic unit spiked at t−1; `−dec` if post spikes and pre did not.
    - Map the weights back.
  - **Hyperparameters are not reported.** `inc`, `dec`, the thresholds and T were tuned by a genetic algorithm (population 100) on a validation split. **That is a reproducibility red flag.**
  - **Results (MRNN-EP, MNIST average accuracy):**

    | Condition | Accuracy |
    |---|---|
    | Sequential | 24.76 |
    | SRC | 64.68 |
    | 2% awake rehearsal | 31.15 |
    | SRC + rehearsal | 67.77 |
    | Joint training (upper bound) | 96.59 |

  - CIFAR-10 (MRNN-EP): sequential 33.56, SRC 81.30, joint 91.87.
  - To match SRC's gain with rehearsal alone, they needed at least 15% old data.
  - **No seed count is reported.** There were six task-order runs.
  - EWC and SI were not run, "because they underperform without task labels".
- **Tadros et al. 2022** (prior map 2.5): the SRC recipe above is theirs **[secondhand, via 2508.14081]**.
- **SIESTA (Harun, Gallardo, Hayes, Kemker, Kanan; TMLR 2023)**, arXiv 2303.10725 **[abstract]**.
  - **Wake:** rehearsal-free, backprop-free online updates.
  - **Sleep:** "a compute-restricted rehearsal policy".
  - On ImageNet-1K without augmentation, it "matches the performance of the offline learner", using under 2 hours on one GPU.
  - Its efficiency claims are made against REMIND and prior methods. **The abstract does not report a compute-matched sleep vs online-rehearsal comparison.**

### 1.3 Negative and cautionary results

- **Too many updates on early data hurts.**
  - Nikishin et al. 2022, "The Primacy Bias in Deep RL", ICML **[abstract]**: agents overfit to early experience. The fix is to periodically reset the last layers while **keeping the replay buffer**.
  - D'Oro et al. 2023, ICLR **[abstract]**: higher replay ratios only pay off when combined with resets.
  - **For us:** a long night of replay at high learning rate can lock in the first season. "More sleep" is not monotone.
- **Under a compute budget, simple ER beats fancy methods.** Ghunaim et al. 2023, CVPR, arXiv 2302.01047 **[abstract; the identity of the baseline (ER) is secondhand]**. The stream does not pause for training, and in that setting a simple baseline beats state-of-the-art continual-learning methods.
- **Sleep alone is far from joint training, and it can cost the newest task.** In Table 2 of 2508.14081, SRC recovers roughly half of the gap between sequential and joint training on MNIST. Prior map 2.5 records that Tadros saw new-task drops.
- **SRC needs per-dataset genetic-algorithm tuning** (above). At our scale, a sleep rule with 4 tuned constants can overfit the evaluation.

### 1.4 Is "offline" itself special?

**My reading of the evidence** (an inference, not a published finding):

- Almost all of the benefit comes from **(i) more updates per experience** and **(ii) interleaving old with new**.
- Doing it at night rather than during the day is not, by itself, shown to matter.
- Offline timing only matters when compute per tick is capped (Ghunaim's setting) or when sleep does something wake cannot do (dreaming, downscaling).

So an honest sleep claim has to beat **awake replay with the same number of updates**.

### 1.5 Smallest experiment that can show a sleep benefit (proposed)

**Environment:**

- Contextual bandit in which s is a 6-8-dim sensation vector, with 3 actions.
- The outcome is drive reduction.
- A **season flip** every D days remaps which action pays in which context.
- Seasons alternate A, B, A, B.

**Agents, all with the same brain and the same total gradient updates per day `U = N_day × k`:**

| ID | Name | What it does |
|---|---|---|
| C0 | online-1 | 1 update per tick on the current episode, no sleep. Fewer updates; it shows the floor. |
| C1 | online-k | k updates per tick on the **current** episode. Matched updates, no replay. |
| C2 | awake-replay | 1 update on the current episode + (k−1) updates per tick from the cache (Lin 1992 style). Matched updates, replay during the day. |
| C3 | sleep-today | 1 update per tick + (k−1)·N_day updates at night on **today's cache only**. |
| C4 | sleep-interleaved | Like C3, but the night samples from a reservoir cache spanning past days (CLS interleaving). |
| C5 | sleep-sham | Like C4, but the night replays episodes with **shuffled outcomes**. Same update count and same weight-change magnitude. It checks whether "any extra perturbation" helps. |

**What counts as a sleep claim:**

- **C4 > C2** on retention after a flip-back is a sleep claim.
- **C4 > C1 but ≈ C2** is only a replay claim. That is still worth having, but it is not sleep.
- **C4 > C3** is an interleaving claim.

**One technical trap (proposed fix):**

- Our wake rule is on-policy, like REINFORCE. Replaying an old `(s,a,r)` under today's policy is off-policy.
- Store `pi_then(a|s)` in the cache and weight replayed updates by the clipped ratio `ρ = min(1, pi_now(a|s)/pi_then(a|s))`.
- CLEAR handles this with V-trace **[memory: CLEAR builds on IMPALA's V-trace; not re-checked]**.
- Without the correction, sleep and awake replay are biased in different amounts, and the comparison is confounded.

---

## Q2. The negative phase as "dreaming"

### 2.1 What exactly is pushed up, and by how much

**Hopfield, Feinstein & Palmer 1983**, *Nature* 304:158-159 **[read, full text]**:

- **Network:** N = 30-1000 ±1 neurons, Hebbian `T_ij = Σ_s μ_i^s μ_j^s`, with n ≤ 0.25N memories.
- **Unlearning:** "choosing starting states at random; when a final equilibrium state μ^f was reached it was weakly unlearned by `ΔT_ij = −ε μ_i^f μ_j^f`, 0 < ε ≪ 1."
- **Figure 1:** 32 neurons, 5 memories, ε = 0.01, about 200 unlearning trials.
- **Effect:** memory accessibility spread from "a factor of 3" down to "a factor of 1.4". The total accessibility of spurious states fell.
- **Mechanism:** what gets pushed up is **the energy of whatever attractor the network falls into from noise.** Deep valleys are also broad, so they get hit most often, which equalises the basins.
- **Failure mode, verbatim:** "**Too much unlearning will ultimately destroy the stored memories.**"
- **Key control:** they tested "clipping the T_ij matrix or a threshold effect" and found these "do not" give equivalent improvement. The reason is that they lack "feedback ... of information about the accessibility of particular states."
  - **This is the published reason that dreaming and synaptic downscaling (Q3) should be tested as separate conditions.**

**Agliari, Barra, Fachechi et al. 2018/2019, "Dreaming neural networks"**, arXiv 1810.12217 **[read, the kernel section]**:

- Replaces open-ended unlearning with a kernel that has a sleep extent `t`: `J_ij = (1/N) Σ_{μ,ν} ξ_i^μ [(1+t)(I + tC)^{-1}]_{μν} ξ_j^ν`, where `C_{μν} = (1/N) Σ_i ξ_i^μ ξ_i^ν`.
- t = 0 gives Hebb. t → ∞ approaches the pseudo-inverse (projection) matrix.
- "The denominator ... yields the remotion of unwanted mixture states, while the numerator ... reinforces the memories." The abstract claims capacity rises from α ≈ 0.14 to the bound α = 1.
- **Lesson:** unlearning is safe when it is paired with reinforcement of real data. Pure unlearning, as in Hopfield 1983, has an optimum and then collapses.

**Wake-sleep (Hinton, Dayan, Frey, Neal 1995)** [memory for the equations; the paper is in prior map 2.1]:

- In sleep nothing is "pushed up." The generative path produces a fantasy, and the **recognition** weights are trained to recover its causes: `Δφ_jk ∝ s_j (s_k − q_k)`.
- **What goes wrong:** wake-sleep does not follow the gradient of any single objective, and when the generative model is poor, the recognition net is trained on bad dreams. This is a known weakness [memory].

**Contrastive divergence (Hinton 2002)** [memory]:

- Rule: `ΔW = ε(⟨v h⟩_data − ⟨v h⟩_k-step reconstruction)`. The negative term pushes energy up on states a short Gibbs chain reaches from the data.
- **What goes wrong:** the negatives sit near the data, so far-away spurious modes are never pushed up. Persistent chains (PCD) partly fix this.
- In unlearning terms, CD has too little exploration, not too much unlearning.

### 2.2 Where a genuine dream could enter OUR brain

**The action-level negative phase is already exact.** `Σ_a' pi(a'|s) ∂F(s,a')/∂θ` is the full expectation, so there is nothing to sample. "Dreaming over actions" would add nothing.

**Our model is conditional:** it defines no distribution over `s`. A genuine dream therefore needs a generator of sensations. There are three options, from most to least defensible (all proposed):

1. **Hopfield-style off-distribution unlearning.**
   - Make the RBM joint over `(s,a)` by adding visible biases on `s`. Then `p(s) ∝ Σ_a exp(−F(s,a))`.
   - At night, Gibbs-sample `s̃` from the model starting from noise. Take `ã = argmin_a F(s̃,a)`.
   - Apply a small push up on `F(s̃, ã)` with ε ≈ 0.01 per dream, paired with replay of real episodes so it cannot run away (the Agliari lesson).
   - **Prediction:** this lowers over-confident action preferences in sensation regions the creature has never visited. It should show up as higher policy entropy on novel sensations and faster re-adaptation after a season flip.
   - **Sham control:** the same number of pushes on uniformly random `s`. **Downscaling control:** shrink the weights by the same total L2 change.
2. **Dyna-style dreams** (Sutton 1990, [abstract]; Dyna integrates "trial-and-error learning and execution-time planning ... operating alternately on the world and on a learned model of the world").
   - Learn a small model of `outcome | s, a` from the cache. At night, sample imagined outcomes and update the policy.
   - van Hasselt 2019 says this must beat **plain cache replay at the same update count**, and usually will not when the cache covers the state space.
3. **World-model dreams (Ha & Schmidhuber 2018; Dreamer).**
   - **World Models** (worldmodels.github.io) **[read]**: the VizDoom controller was trained entirely inside the learned model's "dream" and scored about 1100 time steps in the real game.
   - The same article shows the controller **exploiting** the model's errors: at temperature τ = 0.10 the virtual score was 2086 ± 140 but the real score was 193 ± 58. The best real score, 1092 ± 556, came at τ = 1.15.
   - **DreamerV3** (Hafner et al., *Nature* 640:647-653, 2025, doi 10.1038/s41586-025-08744-2) **[abstract]**: an actor-critic trained on imagined trajectories with one fixed configuration across 150+ tasks.
   - Both are far above our scale. The **exploitation result is the transferable lesson**: dreams sampled too sharply produce policies that look good only in the dream.

### 2.3 What would be a legitimate claim at our scale

> "Nightly self-generated negatives (option 1) improve re-adaptation after a season flip, or calibration on novel sensations, compared with (a) no dreams, (b) the same number of random-input negatives, and (c) matched uniform weight shrinkage, all at the same update budget."

**Not legitimate:**

- "The creature dreams" without control (b).
- Any claim made from the action-level negative phase, which is exact and already in the wake rule.

---

## Q3. Synaptic downscaling (SHY)

### 3.1 The proposed rule and the evidence

**What SHY proposes:** wake is net potentiation, and sleep renormalises synaptic strength. Tononi & Cirelli 2014 (*Neuron* 81:12-34) is in prior map 2.4.

The proposal has two forms:

- **Uniform/proportional scaling,** attributed to Hill et al.'s model **[secondhand, via Nere 2013]**.
- **Selective "down-selection",** the later and preferred form.

**Evidence:**

- **de Vivo et al. 2017**, *Science* 355:507-510 **[abstract]**: 3D electron microscopy of 6,920 synapses in mouse cortex.
  - The axon-spine interface was **about 18% smaller after sleep**, with the reduction **proportional to synapse size** (that is, multiplicative).
  - **The largest synapses were spared.**
- **Diering et al. 2017**, *Science*, doi 10.1126/science.aai8355 **[secondhand, press releases]**: about a **20% drop in synaptic AMPA receptor protein** after sleep, Homer1a-dependent.
- **Critique: Frank 2012**, "Erasing synapses in sleep: is it time to be SHY?", *Neural Plasticity*, PMC3317003 **[abstract]**: SHY "remains an elegant idea" but its mechanisms are "mysterious" and its functional significance unknown.
  - Tononi & Cirelli replied. Frank (2013) answered with "Why I am not SHY".
  - **Treat SHY as contested.**

### 3.2 Implementations with measured effects

- **Nere, Hashmi, Cirelli & Tononi 2013**, "Sleep-dependent synaptic down-selection (I)", *Front Neurol* 4:143, PMC3786405 **[read, the model section]**. Spiking network.
  - **Wake (potentiation only):** `W_i ← W_i + α` if the neuron bursts and its dendritic domain gets **both** feedforward and feedback bursts. α = 0.1 (FF) / 0.05 (FB). Weights are bounded in [0, W_max]. "No long-term depression in wake."
  - **Sleep (down-selection):** `W_i ← W_i − β` if the neuron bursts but the domain gets **only one** pathway. β = 0.01 (FF) / 0.005 (FB).
  - **The depression is activity-dependent and competitive, not uniform.**
  - **Procedural task results (recall % / signal-to-noise):**

    | Condition | Recall % / S/N |
    |---|---|
    | 1 wake | 80 / 4 |
    | 1 wake + sleep | 90 / 9 |
    | 10 cycles | 95 / 19 |
    | Extra wake instead of sleep | 20 / 0.25 |
    | Potentiation during sleep | 25 / 0.33 |

  - **Caveat (the paper's own):** it ran no head-to-head comparison of down-selection against uniform scaling. Constants were chosen empirically, and a different network was used for each task.
- **Olcese, Esser & Tononi 2010**, *J Neurophysiol*, doi 10.1152/jn.00593.2010 **[abstract]**: a corticothalamic STDP model. It gives "exponential, self-limiting renormalization", with higher signal-to-noise, resistance to interference, and "desaturation" of learning.
- **"Sleep improves the variability of motor performance"** (authors unverified) **[secondhand]**: scaling all weights down 15% reduced motor error and variability.
- **Hopfield 1983's negative control** (Q2): uniform clipping did **not** reproduce the benefit of unlearning.

### 3.3 Mapping to a tiny network (proposed)

- **Uniform SHY is weight decay applied once per night:** `W ← (1−δ)W`.
  - Inside a softmax policy, uniform scaling of `W, U` is roughly a **temperature increase**: it flattens action preferences.
  - Part of any "sleep benefit" from downscaling may therefore be **re-exploration after a flip**, not memory.
  - Control: a fixed higher softmax temperature with no downscaling.
- **Selective SHY in the de Vivo / Nere spirit:**
  - Shrink in proportion, but spare the largest or most consolidated weights: `W_f ← (1−δ) W_f`, with the slow weights `W_s` (Q5) untouched.
  - Or shrink only the weights that were active during sleep replay without paying off. For example, `U_ja` gets depressed when unit j fires on replayed episodes where action a had r ≤ 0.
- **Suggested δ:** 0.1-0.2 per night, anchored loosely to the ~18% and ~15% figures above. **This is not a sourced constant for an ANN.**

---

## Q4. Growth of hidden units and connections

### 4.1 Exact published rules

**Cascade-correlation (Fahlman & Lebiere, CMU-CS-90-100 / NIPS 2)** **[read, tech report]**:

- **Start:** no hidden units. Train the outputs until "no significant error reduction has occurred after a certain number of training cycles (controlled by a 'patience' parameter)".
- **Grow or stop:** if the error is still too high, train a **pool of 4-8 candidates**. Each receives all inputs and all existing hidden units, and maximises `S = Σ_o | Σ_p (V_p − V̄)(E_{p,o} − Ē_o) |`, where V is the candidate's output and E the residual error at output o.
  - The paper notes "S is a covariance, not a true correlation", and that the covariance version worked better.
- **Install:** the best candidate is installed and its input weights are **frozen**. Then only the output weights are retrained.
- **Result:** on two-spirals, 100 trials all succeeded, with 12-19 hidden units (mean 15.2).

**Growing neural gas (Fritzke 1995)** [steps quoted from Fritzke's own online description, demogng.de; symbols rendered as images, so the constants are secondhand from the MDP toolkit defaults]:

- **Accumulate:** add the squared distance between input and winner to the winner's error.
- **Insert:** "If the number of input signals generated so far is an integer multiple of a parameter [λ], insert a new unit."
  - Find `q` = the unit with maximum accumulated error, and `f` = its neighbour with maximum error.
  - The new unit `r` gets the interpolated reference vector (midpoint).
  - Connect `r–q` and `r–f`, and remove `q–f`.
  - Multiply the errors of q and f by α, and set r's error from them.
- **Decay:** multiply every unit's error by d.
- **Common defaults [secondhand]:** λ = 100, ε_b = 0.2, ε_n = 0.006, a_max = 50, α = 0.5, d = 0.995.

**NEAT (Stanley & Miikkulainen 2002, *Evol Comput* 10(2))** **[read]**:

- **Add-node:** "an existing connection is split ... The new connection leading into the new node receives a weight of 1, and the new connection leading out receives the same weight as the old connection", chosen "to minimize the initial effect of the mutation".
- **Rates:** "In smaller populations, the probability of adding a new node was 0.03 and the probability of a new link mutation was 0.05. In the larger population [1,000], the probability of adding a new link was 0.3."
- **Other settings:** population 150; species stagnant for 15 generations stop reproducing.

**Growing RBMs (they exist):**

- **Infinite RBM (Côté & Larochelle, arXiv 1502.02476)** **[read, model section]**:
  - Energy: `E(v,h,z) = −vᵀb^v − Σ_{i=1..z} ( h_i(W_i·v + b^h_i) − β_i )`, with `β_i = β·softplus(b^h_i)` and β = 1.01 (it must exceed 1).
  - **Every active unit pays an energy cost.** z is sampled from `P(z|v) ∝ exp(−F(v,z))`.
  - **Growth rule:** if a sampled z exceeds the current trained count l, clamp it to l+1. This adds one unit with zero weights.
  - Weight decay bounds how far the weights can grow to pay the penalty. With β = 1.01, the weights took about 500 epochs to compensate.
  - **This is a published "metabolic cost per unit" inside an energy model.**
- **Kamada & Ichimura 2016/2018 (arXiv 1807.03478)** **[secondhand]**: add a hidden neuron when the energy has not converged and parameter variance is high; remove inactive ones.

### 4.2 Proposed rule for our brain: "add an expert where the residual is high"

**Night growth step (proposed):** a cascade-correlation score on the cache, with NEAT's minimal-disruption insertion.

1. **Residual per cached episode p.** Use `e_{p,a} = ρ_p r_p (1[a = a_p] − pi(a|s_p))`. This is the drive-weighted gradient of log-policy with respect to the 3 action logits, so it is exactly what the current brain cannot yet fit.
2. **Train candidates.** Train a pool of K = 4 candidate units `h̃(s) = sigmoid(w·s + c)` on the cache to maximise `S = Σ_a |Σ_p (h̃_p − h̄)(e_{p,a} − ē_a)|`. Use only the cache; no new experience.
3. **Insertion gate.** Recompute S for the best candidate with episode labels **permuted** (200 shuffles). Insert only if S exceeds the null's 95th percentile **and** the creature's growth budget allows it.
4. **Insert without changing behaviour.** Set the new unit's `W_j = w*` and `c_j = c*`, and set `U_ja = 0`.
   - Note: softplus(x) is never 0, so even with `U_ja = 0` the unit adds a term to F. That term is the same for all 3 actions, so it cancels in the softmax.
   - Behaviour is therefore unchanged at insertion, which follows NEAT's logic. Subsequent replay then trains `U`.
5. **Optional GNG-style variant.** Keep an error accumulator per unit: credit `|e_p|` to the unit most active on episode p. Split the worst unit q by copying `W_q` plus noise and halving its `U` between the two copies.

**Budget against bloat (proposed, following iRBM):**

- **Metabolic cost:** each hidden unit costs κ energy per tick, deducted from the body's energy store, so a unit must earn its keep in food.
- **Insertion cap:** at most one insertion per night.
- **Dormancy instead of deletion:** a unit whose usage `mean_p |h_j|·‖U_j‖` stays below a floor for n nights goes **dormant**. Dormant units pay no cost and are not deleted, in line with the report-22 "never delete" rule; see Q5.
- **Sweep κ:** at κ = 0, growth should bloat. Use that as a positive control that the bloat is real.

### 4.3 Honest controls for growth

1. **No growth:** fixed at the starting size.
2. **Yoked fixed-final:** each seed is fixed **from day 1** at the final size its paired growth seed reached. This matches the parameter count.
3. **Random insertion:** same insertion nights and same zero-U insertion, but the candidate is a random unit instead of the best-S one.
4. **Growth with κ = 0 vs κ > 0,** to show the budget matters.

"It grew" is not a result. The claim is: **directed growth beats yoked fixed-final and random insertion** on post-flip performance per unit of metabolic cost.

---

## Q5. Pruning and forgetting: two speeds, extinction ≠ erasure

**Report 22** (genesis digest C, section 22):

- Ranc et al. 2021 fitted **two** decay rates (value t½ 0.9 d, place t½ 5.6 d), "never totally forgotten".
- Thomson 1996: the update is asymmetric.
- Bouton 2004: extinction is new learning, not erasure.
- PREE: persistence scales with ≈1/p.

**ANN matches:**

- **Hinton & Plaut 1987, "Using fast weights to deblur old memories"** **[read, CMU text]**.
  - Each connection has `w_eff = w_slow + w_fast`. Both receive the same gradient ∂E/∂w, with different learning rates.
  - **After each update every fast weight decays by 1%** toward zero. Slow weights used ε = 0.02, α (momentum) = 0.9. The fast-weight ε and α are not given in the text.
  - **Experiment:** 100 random 10→10-bit associations, then 5 new ones, then retraining on a subset.
  - **Result:** the un-retrained associations improved "nearly as much" as the retrained ones, even when only 10% were rehearsed. **This is a savings result.**
- **Ba, Hinton et al. 2016** (arXiv 1610.06258) **[secondhand]**: modern form `A(t) = λA(t−1) + η h hᵀ`.
- **Benna & Fusi 2016, *Nat Neurosci*** (preprint arXiv 1507.07580) **[read, Methods]**.
  - **Chain of variables:** with n = 2 and α = 1/4,

    `u_i(t+1) = u_i + n^{−2i+2} α (u_{i−1} − u_i) − n^{−2i+1} α (u_i − u_{i+1})`

  - **Input and output:** plasticity events (±1) enter only u_1, and the efficacy *is* u_1. `u_{m+1} = 0` gives a leak.
  - **Scaling:** C_k = 2^{k−1}. The memory signal decays like ~1/√t over a range that grows exponentially with m. Lifetime grows almost linearly with the number of synapses.
  - **Two-variable case (m = 2), worked out by me from that equation:**
    - `u1 += I − (1/8)(u1 − u2)`
    - `u2 += (1/16)(u1 − u2) − (1/32)u2`
- **Kaplanis, Shanahan & Clopath 2018** (arXiv 1802.07239) **[abstract]**: used Benna-Fusi synapses in tabular and deep RL agents. Reports reduced forgetting over two sequential tasks and less "need for an experience replay database". **This is the closest published precedent for our creature.**
- **Extinction as new structure:**
  - **Redish et al. 2007**, *Psych Rev* 114(3):784-805 **[abstract]**: standard TD learning "treat[s] extinction as an unlearning" and cannot produce renewal. Their fix adds situation recognition, which creates new states.
  - **Gershman, Blei & Niv 2010**, *Psych Rev* 117(1):197-209 **[abstract]**: recasts this as inference over an unbounded number of latent causes.
  - **Inference, mine:** in our brain, "infer a new latent cause" = **add a hidden unit** (Q4). The growth rule and the extinction rule can be the **same mechanism**. That is a testable unification.

**Exact rule proposed for v0** (Hinton-Plaut + Benna-Fusi m = 2 + report 22; proposed):

- **State:** each parameter θ has a fast and a slow part, `θ = θ_s + θ_f`.
- **Wake:** `θ_f += η_f g`, where g is the drive-weighted gradient. Every tick, `θ_f *= (1 − λ_f)`, with λ_f ≈ 0.01, as in Hinton & Plaut.
- **Asymmetry:** use a larger η_f for omissions than for gains, following Thomson's direction.
  - The exact ratio is **unsourced**.
  - Count omission *events*, not elapsed ticks (PREE).
- **Sleep (consolidation):** `θ_s += κ θ_f; θ_f *= (1 − κ)`, with κ ≈ 0.1-0.25 (proposed). Apply selective downscaling (Q3) to θ_f only.
- **Floor:** the magnitude of slow weights never decays below a floor, so things are "never totally forgotten".
- **Expected result:** a run of omissions drives θ_f negative, so the behaviour stops fast. If θ_f decays before the next sleep, the old habit returns. That is **spontaneous recovery**, Bouton's signature, and it falls out of the rule.

---

## Q6. Metrics, seeds and CIs for tiny-scale claims

**Per-season metrics** (adapted from Wolczyk et al. 2021, *Continual World*, NeurIPS, arXiv 2105.10919 **[read, metrics section]**):

- **Performance:** `p_i(t)` = mean intake per tick in season i, measured in **frozen evaluation episodes**. No learning during the evaluation.
- **Forgetting:** `F_i = p_i(end of season i) − p_i(T)`.
- **Forward transfer:** `FT_i = (AUC_i − AUC_i^b)/(1 − AUC_i^b)`, where AUC is the normalised area under the season's learning curve and `b` is a fresh single-season learner.
- **Wolczyk's statistics:** "typically 20 seeds", 90% non-parametric bootstrap CIs.

**Savings (proposed operational form):**

- **Return-to-criterion:** ticks to regain 80% of the pre-flip intake when season A returns, divided by the ticks needed the first time A was learned. Lower is better. This is the Hinton-Plaut and Ebbinghaus sense.
- **Day-1 retention:** intake on the first day after the flip-back, before any learning.
- **Spontaneous recovery:** after an extinction run plus a delay with no training, the rebound in choice of the extinguished action.

**Statistics:**

- **Agarwal et al. 2021**, "Deep RL at the Edge of the Statistical Precipice", NeurIPS **[abstract and search snippets]**:
  - Report the **IQM** with **stratified bootstrap 95% CIs**.
  - With **3 runs, bootstrap CIs underestimate** true coverage.
  - The `rliable` library implements this.
- **Colas, Sigaud & Oudeyer 2018**, arXiv 1806.08295 **[abstract]**: choose the seed count by power analysis, using a t-test or bootstrap test.
- **Recommendation for our laptop runs:**
  - **≥ 20 seeds per condition** (cheap at our scale).
  - **Common random numbers:** the same environment seed across conditions, so effects are **paired differences**.
  - A pre-registered primary metric (post-flip savings) and a pre-registered smallest effect of interest.
  - Expect nulls. The genesis digest's selectability floor applies.

---

## (a) Recommendations for creature v0

**Sleep rule (in order each night):**

1. **Replay.** Replay `R = (k−1)·N_day` episodes, sampled from a reservoir cache spanning past days. Use the importance-corrected wake rule, with ρ clipped at 1. Optionally use priority `p ∝ |e|^0.6`.
2. **Consolidate.** `θ_s += κθ_f; θ_f *= (1−κ)`.
3. **Downscale.** Apply `θ_f *= (1−δ)` with δ ≈ 0.15. Keep it switchable.
4. **Dream (v0.1, only after 1-3 work).** Make the brain joint over s, Gibbs-sample s̃, and push up `F(s̃, argmin_a F)` with ε = 0.01, paired with replay.

**Growth rule:**

- At most one unit per night, using the cascade-correlation score on the cache with a permutation-null gate.
- Insert with zero `U`.
- Charge a metabolic cost κ per unit per tick. Low-usage units go dormant rather than being deleted.

**Controls, required before any claim:**

- **Sleep:**
  - C1 online-k (matched updates)
  - C2 awake replay (matched updates)
  - C3 sleep on today only
  - C5 shuffled-outcome sham
  - a temperature-matched control for downscaling
  - a random-input dream control
- **Growth:**
  - no growth
  - yoked fixed-final size from day 1
  - random insertion
  - κ = 0
- **Statistics:** 20 paired seeds, IQM + stratified bootstrap CI, metrics as in Q6.

**Build order:** online-1 → online-k → awake replay → sleep → +consolidation → +downscaling → +growth → +dreams. Add one mechanism per step, and run each against the previous step.

## (b) Questions for Ahmed

1. **What is "the night" competing against?** If daytime compute is unlimited, a sleep benefit collapses into a replay benefit (Q1.4). Do you want a hard per-tick compute cap during the day, so that sleep is where the extra learning has to happen?
2. **Should the cache be bounded,** for example a reservoir of the last M episodes? CLEAR suggests a small random-discard buffer is enough. Or should it hold everything since birth?
3. **Do you want genuine dreams in v0?** They require making the brain model sensations, not just actions given sensations (Q2.2). That changes the architecture. My advice is v0.1.
4. **Is growth within a lifetime (nightly) or across generations (inherited size)?** Your phrase "over generations" could mean either, and the controls differ.
5. **Should the metabolic cost of a hidden unit be a fixed physics constant or an evolvable gene?** The digest warns against evolvable master clocks. I would make it fixed.
6. **Are you willing to pre-register "post-flip savings" as the single primary metric,** before seeing any results?
