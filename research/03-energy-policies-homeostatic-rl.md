# 03 - Energy-based policies + homeostatic RL (research seat R1)

Date: 2026-10-13. Scope: the creature brain F_θ(x,a), its learning rule, the drive-reduction reward, credit assignment, temperature, baselines, prior art.

**Provenance tags used below**
- **[V]** = I read the primary text in this session (PDF/XML pulled and grepped).
- **[A]** = abstract or publisher page only.
- **[S]** = secondhand (another paper, a reproduction, or a search summary). Treat as unconfirmed.
- **[M]** = from my own background knowledge, not re-fetched today. Standard, but verify before citing in a paper.
- **[D]** = my own derivation in this note. Check the algebra; it is not from a source.

---

## Q1. Is "RBM free energy as action value / energy-based policy" an established approach?

**Yes. It is a 20-year-old line with a known failure mode (value-based TD diverges) and a known fix (policy gradient).**

### Sallans & Hinton 2004 [V]
Sallans, B. & Hinton, G. E. (2004). Reinforcement learning with factored states and actions. *JMLR* 5:1063-1088.

- **Model.** A product of experts / RBM over binary state s, action a and hidden h. Their eq. (10) gives the free energy as expected energy minus hidden entropy:
  F(s,a) = -Σ_k Σ_i w_ik s_i <h_k> - Σ_k Σ_j u_jk a_j <h_k> + Σ_k [<h_k> log<h_k> + (1-<h_k>) log(1-<h_k>)],
  with <h_k> = σ(Σ_i w_ik s_i + Σ_j u_jk a_j).
  (That is the same thing as the softplus form you use: -Σ softplus(...) plus bias terms.)
- **Value.** Q̂(s,a) = -F(s,a).
- **Learning = SARSA, not a contrastive rule.** Their eq. (4)-(5): E_TD = r_t + γQ̂(s_{t+1},a_{t+1}) - Q̂(s_t,a_t), and Δθ = λ E_TD ∇_θ Q̂.
  Per weight: Δw_ik ∝ E_TD · s_i^t <h_k^t>, and Δu_jk ∝ E_TD · a_j^t <h_k^t>.
- **Action selection.** Boltzmann, p(a|s) ∝ e^{-F(s,a)/T} = e^{Q(s,a)/T}, sampled by Gibbs sampling because their action space is huge (2^40).
  - Temperature was annealed exponentially, e.g. 1.0 → 0.1, and 1.0 → 0.01 in another task.
  - They used 10 Gibbs / annealing iterations.
- **What they found hard:**
  1. "there is no proof of convergence in general for this learning rule"; it is semi-gradient TD.
  2. Gibbs sampling "might not work well for some problems" (local minima in action space).
- **Directly useful for us (growth):** their §8.1 proposes adding hidden units while freezing the existing ones: "Adding and learning parameters for additional hidden variables, while holding the parameters of the pre-existing variables constant, would allow the policy to improve without having to re-learn the entire solution." [V]

### Heess, Silver & Teh 2013 [V]
Heess, N., Silver, D. & Teh, Y. W. (2013). Actor-critic reinforcement learning with energy-based policies. *Proc. EWRL*, PMLR 24:45-58. The author PDF is stamped 2012; it is the same EWRL volume.

- **Model.** π_θ(a;s) = e^{-F(s,a;θ)}/Z(s), with RBM free energy (their eq. 3)
  F_θ(s,a) = -b_s^T s - b_a^T a - Σ_i log(1 + e^{s^T W_si + a^T W_ai + b_hi}).
  **This is structurally identical to our F(x,a).**
- **Their critique of Sallans & Hinton (their name for it: ESARSA):**
  - "TD learning is known to diverge, both in theory and in practice, when using non-linear value functions".
  - "the policy is based on an arbitrary temperature which makes the algorithm hard to tune in practice".
  - Their experiments: ESARSA showed "poor performance in some runs, and sensitivity to initial values".
- **Key equation, their eq. 19.** The compatible features (score function) of an energy-based policy:
  ψ_θ(s,a) = ∇_θ log π_θ(a;s) = φ_θ(s,a) - E_{a'~π}[φ_θ(s,a')], where φ_θ(s,a) = -∇_θ F(s,a).
  - **Their difficulty:** the second expectation "involves a sum over all actions, and is intractable" in high-dimensional action spaces.
  - **With 3 actions this sum is exact and trivial for us.** Their main obstacle does not exist in our setting.
- **Algorithms:**
  - **ENATDAC:** natural actor-critic. It replaces the expectation with K, L sampled actions; K = L = 1 was enough, or 5 on the octopus arm.
  - **EQNAC:** a linear critic Q̂_w = φ_θ(s,a)^T w; the actor follows the natural gradient along w.
  - Both beat ESARSA on all tasks. ENATDAC comes with a two-timescale convergence guarantee (critic slower than actor) to a near-local optimum of average reward.
- **Failure mode they saw:** some ENATDAC runs got "trapped in suboptimal maxima where the arm moves only in one direction".
  - **Expect the analogous thing in our creature: a policy that always turns one way.** It is a local optimum of policy gradient.

### Haarnoja, Tang, Abbeel & Levine 2017 [V, partial read]
Haarnoja, T. et al. (2017). Reinforcement learning with deep energy-based policies. *ICML*, PMLR 70 (arXiv:1702.08165).

- **Objective.** Maximum entropy: π* = argmax Σ_t E[r(s_t,a_t) + α H(π(·|s_t))].
- **Optimal policy.** π*(a|s) = exp((Q*_soft(s,a) - V*_soft(s))/α), with V_soft(s) = α log ∫ exp(Q_soft(s,a')/α) da'.
- **Soft Bellman:** Q*_soft(s,a) = r + γ E_{s'}[V_soft(s')].
- **EBM reading.** (1/α)Q_soft is the negative energy and (1/α)V_soft the log-partition. So **-F(x,a)/T plays the role of Q_soft/α, and T is the entropy weight α.**
- **What was hard:** the soft backup and sampling are intractable for continuous actions. They need importance sampling for V and an amortised Stein variational gradient descent (SVGD) sampler network.
  - **With 3 discrete actions, V = T·log Σ_a exp(-F(x,a)/T) is exact**, and soft Q-learning is a one-liner.

### Also in this line [V for the Elfwing abstract via the Frontiers page]
**Free-energy RL (FERL)** comes out of Doya's group:
- Otsuka, Yoshimoto & Doya 2010: partially observable MDPs (POMDPs). [S]
- Elfwing, Otsuka, Uchibe & Doya 2010: vision-based navigation. [S]
- Elfwing, Uchibe & Doya 2013, *Frontiers in Neurorobotics* 7, "Scaled free-energy based RL...". [V via publisher page]

**Elfwing 2013 found that the "magnitude of the initial free-energy grows with the size of the network".**
- Their fix: Q = -F/Z, with Z = √(number of state nodes).
- This is equivalent to rescaling the learning rate by 1/Z², the reward by Z, and the softmax temperature τ' = Zτ.
- They call the choice of Z "quite arbitrary".
- **Consequence for growth:** adding hidden units changes the effective temperature. See Recommendations.

**Verdict.** "RBM free energy as negative action value, with a Boltzmann policy" is established (Sallans & Hinton 2004).
- The policy-gradient version is exactly Heess et al. 2013.
- The max-entropy reading is Haarnoja et al. 2017.
- Our novelty is not the brain form. It is the homeostatic reward, the sleep replay, and the growth.

---

## Q2. Is the proposed gradient REINFORCE? Baseline, sign, variance, "negative phase", "dream"

### Derivation [D, consistent with Heess eq. 19 [V] and Williams 1992 [M]]
Policy: π(a|x) = exp(-F(x,a)/T) / Σ_{a'} exp(-F(x,a')/T).

∇_θ log π(a|x) = -(1/T)∇_θF(x,a) + (1/T) Σ_{a'} π(a'|x) ∇_θF(x,a')
              = (1/T) [ -∇_θF(x,a) + E_{a'~π}∇_θF(x,a') ].

REINFORCE (Williams 1992, *Machine Learning* 8:229-256 [M]) is Δθ = α (G_t - b(x_t)) ∇_θ log π(a_t|x_t).

**So your rule Δθ ∝ r·[-∂F(x,a)/∂θ + Σ_{a'} π(a'|x) ∂F(x,a')/∂θ] is exactly REINFORCE for a Boltzmann policy.** The constant 1/T is absorbed into the learning rate. Three conditions apply:
1. **r must be the return G_t from step t**, or an advantage. It cannot be the one-step drive change at the moment of acting, because the eat event comes later (see Q4).
2. **The data must be on-policy**, i.e. sampled from the current π.
3. **The expectation must use the same T as acting.**

### Baseline / advantage
- **Correct form:** A_t = G_t - b(x_t), where b may depend on the state x but **not on the action a**. Any such b leaves the gradient unbiased. [M; Sutton & Barto 2018 §13.4]
- **Simplest honest b:** a running mean of G, an exponential moving average (EMA) with a time constant of a few hundred steps.
- **Better b:** a learned state value V_w(x), linear in x, trained by TD(λ). That gives actor-critic, with δ_t = r_t + γV(x_{t+1}) - V(x_t) as the advantage. [M; Sutton & Barto §13.5]
- **Exact for us, no critic needed:** with 3 actions, E_{a'~π}[-F(x,a')] is a free state-dependent quantity. But it is not a valid value baseline: it is in energy units, not return units. Do not use it as b.
- **A free state baseline from the drive [D]:** under the Keramati-Gutkin reward, D(h_t) is itself an exact state baseline. See Q3: the return decomposes as G_t = D(h_t) + (cost-return term).

### Sign pitfalls
1. **The sign of r is meaningful.** Poison gives negative drive reduction.
   - If the implementation weights only the positive phase by r, or clips r ≥ 0, the rule can only reinforce. It can never directly punish turning toward poison.
   - **Keep r signed** and multiply the whole bracket by it.
2. **"Lower F on the taken action" is right only when A_t > 0.** When A_t < 0 the same formula raises F on the taken action. This is not optional.
3. **Weight decay toward 0 is not neutral for the bias b_a.** It pulls the policy toward uniform, which is fine. But decaying c_h changes softplus offsets that are action-independent only when v_{h,a} = 0.

### Variance pitfalls
- REINFORCE variance scales with return variance and episode length. Sparse eat events, seconds after the decisions, are the worst case.
- **Mitigations, in order of cost:**
  1. Running-mean baseline.
  2. Short eligibility window (Q4).
  3. Linear critic.
  4. Normalise advantages within a sleep batch: subtract the mean, divide by the std. [M; common practice, introduces mild bias]
- **Replay during sleep is off-policy.** Cached (x, a) were sampled from π_old, not the sleep-time π.
  - REINFORCE is on-policy, so replaying many epochs without correction biases the gradient. It can also collapse the policy.
  - **Fix:** store π_old(a|x) in the cache and weight by the ratio ρ = π_θ(a|x)/π_old(a|x), clipped (e.g. ρ ∈ [0.8, 1.2]) or truncated. This is the PPO / off-policy actor-critic recipe. [M: Degris, White & Sutton 2012; Schulman et al. 2017]
  - This is the single most likely silent bug in the day/night design.

### Is "negative phase" honest?
- **Structurally yes.** The second term is ∇_θ log Z(x), the gradient of the conditional log-partition function. In RBM maximum-likelihood learning the negative phase is exactly the gradient of log Z.
- **Positive phase:** push down energy on the observed (x,a). **Negative phase:** push up energy where the model puts mass. The analogy is exact.
- **It differs from RBM training in one key way: it is an exact expectation over 3 actions, conditioned on a real x.**
  - It is not sampled.
  - It involves no generated sensory data.
  - It involves no Markov chain.
- **It is also reward-weighted.** With A_t = 0 both phases vanish. In RBM contrastive divergence (CD) the negative phase runs regardless.
- Honest wording: "the score-function gradient of a Boltzmann policy, which has the same positive-minus-model-expectation form as the RBM likelihood gradient".

### When is it legitimately a "dream"?
**It is a dream only when the model generates the sensations x itself**, rather than re-reading cached x. Three ways:
1. A joint energy model over x (and h) is Gibbs-sampled to fantasise x̃, and the policy is then trained or evaluated on x̃. This is the wake-sleep sense: Hinton, Dayan, Frey & Neal 1995, *Science* 268:1158 [M].
2. A learned forward model rolls out imagined trajectories (Dyna-style planning, Sutton 1990 [M]).
3. Persistent fantasy particles, as in persistent CD (Tieleman 2008 [M]).

**Replaying the day's cache is "replay", not "dreaming".** The sleep phase in the current design is experience replay plus weight decay. The paper should call it that. "Dream" can be added later as a separate, ablatable component.

---

## Q3. Homeostatic RL: Keramati & Gutkin 2014 and follow-ups

### Keramati & Gutkin 2014 [V, full text XML]
Keramati, M. & Gutkin, B. (2014). Homeostatic reinforcement learning for integrating reward collection and physiological stability. *eLife* 3:e04811. doi:10.7554/eLife.04811.

- **Drive, eq. 1:** D(H_t) = ( Σ_{i=1}^N |h_i* - h_{i,t}|^n )^{1/m}.
  - The XML flattens it to "∑ |h_i* − h_i,t|^n m"; the standard reading is the outer exponent 1/m.
  - "for the simple case of m = n = 1, the drive function reduces to Euclidian distance". This is their wording. Strictly, m = n = 1 is the L1 distance; m = n = 2 would be Euclidean.
- **Reward, eq. 2:** r(H_t, K_t) = D(H_t) - D(H_{t+1}) = D(H_t) - D(H_t + K_t). K_t is the outcome's effect on the internal state.
- **Constraint:** "Appropriate choice of m and n (n > m > 1)". This yields four properties (eqs. 6-9):
  1. Reward increases with dose: ∂r/∂k_j > 0.
  2. Reward increases with deprivation: ∂r/∂|h_j* - h_j| > 0 ("food will be more rewarding when the animal is hungrier").
  3. Inhibitory effect of irrelevant drives.
  4. Risk aversion, because r is concave in k: ∂²r/∂k² < 0.
- **Overshoot is punished:** "outcomes larger than h* − h_t result in overshooting the setpoint and thus a declining trend of the rewarding value". In a satiation test "the agent stops seeking water when the setpoint is reached".
- **Numbers seen:** one simulation's parameters are "α = 0.4, β = 0.05, γ = 0.9, n = 4". There is also a supplementary run with m = n = 1.
  - **I did not find the m value used in the main simulations.** It sits in the source-data tables, which I did not retrieve.
  - The common recollection "n = 4, m = 3" is **unverified [M]**. Do not cite it.
- **Discounting, eqs. 4-5:** sum of discounted rewards SDR = ∫ γ^t r_t dt. Theorem: "if γ < 1: argmin_π SDD_π(H_0) = argmax_π SDR_π(H_0)", where SDD is the sum of discounted drives.
  - The proof (supplement S3) is over trajectories that end at the setpoint, H_w = H*.
  - They argue discounting is normatively required: "reward seeking without discounting (i.e., if γ = 1) would not lead, and may even be detrimental, to physiological stability".
- **Learning:** state = internal state × external state. The learner is classical TD / Q-learning with softmax choice, per the reviewer-quoted methods text.
- **Their own limitations section:**
  - The model is fully observable. They suggest noisy interoception could model anorexia.
  - **The setpoint is fixed.** They write that "making it adaptive... could explain tolerance... and thus, drug addiction and obesity".
  - The drive function has a restrictive form.
  - The theory only covers rewards that have a regulatory system.

### A useful identity [D]
With Φ(h) = -D(h), the Keramati-Gutkin reward is r_t = D_t - D_{t+1}. Ng-Harada-Russell potential shaping is F_t = γΦ_{t+1} - Φ_t = D_t - γD_{t+1} (Ng et al. 1999, ICML [M]). So

r_t = [D_t - γD_{t+1}] - (1-γ)D_{t+1}

That is, potential-based shaping plus a genuine per-step cost of -(1-γ)D_{t+1}. Summing with discount, the shaping part telescopes, giving

G_t = Σ_k γ^k r_{t+k} = D(h_t) - (1-γ) Σ_{k≥0} γ^k D(h_{t+k+1}).

**Three consequences:**
1. **This is the Keramati-Gutkin theorem in one line:** maximising G is minimising discounted drive.
2. **D(h_t) is an exact state baseline inside G_t.** The policy-relevant signal is only the (1-γ)-weighted cost term.
   - As γ → 1 that signal shrinks to zero relative to the noise. This is why γ = 1 fails, and why the learning signal is weak with long horizons.
3. **For a finite n-step window:**
   Σ_{k=0}^{n-1} γ^k r_{t+k} = D_t - (1-γ)Σ_{k=1}^{n-1} γ^{k-1} D_{t+k} - γ^{n-1} D_{t+n}.
   For γ ≈ 1 this is ≈ D_t - D_{t+n}: **"did drive drop over the next n steps"**. This is an intuitive, cheap credit signal for a creature (see Q4).

Yoshida, Sprekeler & Gutkin (2025) also note that "Yoshida et al (2024) showed how the homeostatic reward definition can be related to reward shaping (Ng 1999)" [V, arXiv:2507.04998]. I did not read the 2024 derivation itself.

### Follow-ups
- **Yoshida, Sprekeler & Gutkin (2025)**, "Linking Homeostasis to Reinforcement Learning: Internal State Control of Motivated Behavior", arXiv:2507.04998. [V] A perspective, not experiments.
  - It restates the Keramati-Gutkin drive with discrete-time SDD/SDR, "for all γ ∈ (0,1)".
  - It notes that "most studies of HRRL so far have focused on value-based RL... policy gradients with actor-critic architectures would be readily applicable".
  - It lists deep-RL extensions: discrete and continuous actions, image input, continuous time (Laurençon et al.), multi-drive decomposition (Dulberg et al.), and a real robot.
  - **Discrepancy:** it writes "Given the we choose m>n>1". eLife says n > m > 1. It also calls m = n = 2 Euclidean.
  - **Trust the eLife original (n > m > 1).** Only that ordering makes D convex in the deviation, since D ~ |dev|^{n/m}.
- **Yoshida, Daikoku, Nagai & Kuniyoshi (2024)**, "Emergence of integrated behaviors through direct optimization for homeostasis", *Neural Networks* 177:106379. [S: citation only, from reference lists]
- **Yoshida, Kanazawa & Kuniyoshi (2024)**, bioRxiv 10.1101/2024.06.03.597087, "Synthesising integrated robot behaviour through RL for homeostasis". [V, methods]
  - A real quadruped learns with homeostatic reward only.
  - Drive: D(x) = τ̄ + (q̄ - 0.8)^K, where τ̄ is a temperature-like variable and q̄ normalised energy with target 0.8. The exponent rendered garbled; it is likely 2. [S]
  - Reward: r ∝ 100·(D_{t-1} - D_t). [V]
  - The agent is an actor-critic MLP with a Beta-distribution policy.
  - **Note: they put temperature in linearly, not as a deviation.** Engineering choices diverge from the Keramati-Gutkin form.
- **Horibe & Yoshida (2024)**, "Emergence of implicit world models from mortal agents", arXiv:2411.12304. [V, intro only] Proposes meta-RL with recurrent networks plus homeostatic RL as a route to intrinsic motivation.
- **Hulme, Morville & Gutkin (2019)**, "Neurocomputational theories of homeostatic control", *Physics of Life Reviews* 31:214-232. [A/S] A review of optimal control, then homeostatic RL, then how survival constraints and active inference might address its challenges.

### Critiques and pitfalls
- **Morville, Friston, Burdakov, Siebner & Hulme**, "The homeostatic logic of reward", bioRxiv 242974. [A]
  - Control-theory and RL accounts of energy homeostasis "rest on implausible assumptions; either via circular definitions, unprincipled drive functions" or by ignoring environmental volatility.
  - They argue active inference avoids these shortcomings.
  - **The "unprincipled drive function" point applies to us:** w_i, n, m and h* are free parameters.
- **"Agent avoids eating to keep drive flat"?** Under r = ΔD this is mostly not a bug.
  - Eating near the setpoint overshoots and is correctly punished (Keramati-Gutkin).
  - The real risk is the reverse: with metabolic drain, D rises every step whatever the action. That creates a large action-independent negative reward stream.
  - It is harmless in expectation but adds variance. **A baseline removes it.**
- **Setpoint drift / wireheading.** If h* is plastic within a lifetime, or the agent can influence its own measurement of h, the cheapest way to reduce D is to move h* or the sensor, not to eat.
  - Keramati and Gutkin themselves flag adaptive setpoints as a model of tolerance and addiction.
  - **Keep h* and w genetic and fixed within a life, and compute D from true h**, not from a learned estimate.
- **Death / termination.** The telescoping identity shows the undiscounted return is D_0 - D_T.
  - If death simply ends the episode with no terminal value, then for γ < 1 an agent in a high-drive spiral loses only the future cost terms it would have paid anyway.
  - **Do not give death a positive or zero-cost "escape" relative to living at high drive.**
  - Simplest: treat death as absorbing at the drive it died with, D_T held for the rest of the window, or apply an explicit terminal cost. [D]
- **Multiple drives and saturation.** With the Keramati-Gutkin n > m > 1 form, the irrelevant-drive inhibition means high toxin damps the reward of food. That is a feature, but it can slow early learning when both drives are off.

---

## Q4. Credit assignment for sparse interoceptive events

**Simple, defensible defaults, in order of increasing machinery:**

1. **Monte-Carlo windowed return (no critic).**
   - G_t = Σ_{k=0}^{n-1} γ^k r_{t+k}. By the identity above this is ≈ D_t - D_{t+n} for γ ≈ 1.
   - Choose n ≈ 1-2× the typical number of steps from "first detectable gradient" to "contact".
   - Advantage A_t = G_t - b̄, with b̄ an EMA of G.
   - Most transparent; this is what the day-cache naturally supports.
2. **Online eligibility trace (GPOMDP / Williams).**
   - e_t = γλ e_{t-1} + ∇_θ log π(a_t|x_t), and Δθ_t = α (r_t - b̄) e_t.
   - Pick the trace time constant τ_e = 1/(1-γλ) to match the approach timescale.
   - Baxter & Bartlett 2001, JAIR 15 (cited in Heess et al. [V]). Form per Sutton & Barto 2018 ch. 12-13 [M].
3. **Actor-critic with traces** (Sutton & Barto 2018 §13.5 [M]).
   - Linear V_w(x) with TD(λ): δ_t = r_t + γV(x_{t+1}) - V(x_t).
   - Updates: w += α_w δ_t z^w_t and θ += α_θ δ_t z^θ_t, with z traces decaying at γλ.
   - The critic learns "being near A-smell predicts drive drop". That turns a sparse eat event into dense TD errors along the approach.
   - **This is the standard answer to sparsity**, and Heess et al. show actor-critic is the robust choice for RBM policies.

**Biological anchor.**
- Three-factor / dopamine-modulated rules use synaptic eligibility traces that last seconds. Izhikevich 2007 (*Cerebral Cortex*, "Solving the distal reward problem through linkage of STDP and dopamine signaling") is the canonical model.
- Reproductions of that model (Brian2, NESTML) use a trace constant of 1000 ms and a dopamine constant of 200 ms. **[S: from reproductions, not the paper's table]**

**Honest defaults:**
- γ = 0.95-0.99 per step.
- λ = 0.9.
- Window or trace length about 20-50 steps, which is 1-2 s if dt ≈ 50 ms. **Tune to your world's actual approach time.**
- **Measure it first:** run the oracle forager (Q6) and histogram "steps from first gradient detection to eating".

---

## Q5. Temperature T and exploration

**Facts:**
- **T scales the learning rate and trades off entropy.**
  - ∇log π carries 1/T.
  - In the soft-RL reading, T is the entropy weight α (Haarnoja 2017 [V]).
  - Heess et al. explicitly complain that ESARSA's "arbitrary temperature... makes the algorithm hard to tune" [V].
- **T is partly unidentifiable from the weights.**
  - For the linear terms (b_a, w_a), scaling them by c equals dividing T by c.
  - The softplus terms do not scale exactly that way, but approximately so in the linear regime. [D]
  - So a learned brain can "choose its own temperature" by growing its weights. Weight decay is what keeps T meaningful.
- **Growth changes effective temperature.** Each hidden unit adds a softplus term to F. Elfwing et al. 2013 found free-energy magnitude grows with network size and needed a size-dependent scale Z (they used √(number of state nodes)), equivalent to τ' = Zτ [V].
  - **A new unit with v_{h,a} = 0 for all a contributes an action-independent term. It is exactly policy-neutral.** Initialise new units that way.
- **Annealing schedules are not free.** Cesa-Bianchi, Gentile, Lugosi & Neu 2017, "Boltzmann exploration done right" (*NeurIPS* 30): for bandits, Boltzmann exploration with any monotone schedule is suboptimal. Their fix needs per-arm rates or problem knowledge. [A/S]
- **Chemotaxis biology.**
  - C. elegans uses two strategies: biased random turning (pirouettes) and gradual steering (weathervane / klinotaxis).
  - Pirouettes: Pierce-Shimomura, Morse & Lockery 1999, *J Neurosci*. Pirouette probability rises when heading down-gradient. [S; exact title unverified]
  - Weathervane: Iino & Yoshida 2009, *J Neurosci* 29:5370-5380. [S]
  - **The noise is state-dependent, not a fixed T.** A Boltzmann policy gets this for free, since F differences scale with gradient inputs. That argues against heavy annealing.

**Should T be a gene?** Yes, but as a fixed-within-life heritable parameter, with three safeguards:
- **(a) Weight decay on.** Otherwise learning absorbs T.
- **(b) Report T together with weight norm,** or report the realised policy entropy H(π) instead.
- **(c) For v0, fix T = 1 and add an explicit entropy bonus β·H(π(·|x)).**
  - Gradient: β·∇H, which is exact over 3 actions.
  - β = 0.01 relative to advantage scale.
  - Make β (not T) the gene in later evolution runs.
  - Entropy regularisation in policy gradient: Williams & Peng 1991 [M].

---

## Q6. Baselines a reviewer will demand

**Shared rules for all controllers:** same world, same seeds, same action set, same sensors unless stated. Metrics:
- food eaten per 1000 steps;
- poison eaten per 1000 steps;
- survival time;
- time-averaged D(h);
- n ≥ 20 seeds, with bootstrap 95% confidence intervals.

1. **Random walk.**
   - (a) Uniform π = (1/3, 1/3, 1/3).
   - (b) **Matched correlated random walk:** fixed p(forward) and p(turn) equal to the trained creature's marginal action frequencies. Without (b), a reviewer will say "it just learned to go forward more".
2. **Braitenberg, hand-wired.** Braitenberg 1984, *Vehicles* [M]. Three variants:
   - **(a) Oracle-valence steering:** s = k_A(A_L - A_R) - k_C(C_L - C_R). Turn left if s > θ, right if s < -θ, else forward. Optionally soft: π ∝ exp(±s/T).
   - **(b) Naive B-seeker:** s = k_B(B_L - B_R). Attracted to both food and poison, because B is shared. **This shows discrimination is required.**
   - **(c) Klinokinesis:** p(turn) = σ(-k·dA/dt). Turn when food smell is falling, after the pirouette strategy.
   - **Tune gains by grid search or CMA-ES on held-out seeds,** and report the tuning budget.
3. **Tabular Q-learning.**
   - State: sign(A_L-A_R), sign(C_L-C_R), sign(dA/dt), sign(dC/dt), each ∈ {-,0,+}, plus energy-low {0,1} and toxin-high {0,1}. That is 3⁴·2·2 = 324 states × 3 actions.
   - Same reward r = ΔD, same γ.
   - Softmax policy with the same T, or ε-greedy.
   - Watkins Q-learning with eligibility traces, Q(λ), at matched λ.
   - **Plus a linear softmax policy gradient on raw x:** the EBM with 0 hidden units, F = -b_a - w_a·x. **This is the critical ablation:** it isolates what the hidden units buy.
4. **Oracle foragers (ceilings, not competitors).**
   - **(a) Omniscient:** knows food and poison positions. Heads to the nearest food while keeping distance from poison, e.g. picks the action minimising angle to the nearest food subject to poison distance > r_safe.
   - **(b) Sensor-limited oracle:** the best Braitenberg 2(a) after tuning, i.e. the best this body can do with these antennae when told the valence.
   - Grimbly et al. 2026 (AffectWorld) likewise report an oracle planner "as a performance ceiling rather than a competing baseline" (0.66 survival in their task). [V]

**Extra controls a sharp reviewer adds:**
- **Valence-swap test:** food emits B+C, poison emits A+B, in a new life. It must be re-learned, which proves nothing is hard-coded.
- **Frozen-at-birth brain:** no learning.
- **Sleep ablation:** same total gradient steps, all online.
- **Growth ablation:** fixed hidden units at the final size.

---

## Q7. Closely related prior work

- **Free-energy RL in embodied / robot settings (Doya lab).** Elfwing et al. 2010 and 2013 used FERL on the simulated Cyber Rodent with camera input.
  - Scaled FERL succeeded in most settings, where plain FERL averaged a 30% success rate.
  - Scaled FERL used all hidden nodes, while FERL "learned a sparse action code with silent hidden nodes". [V, publisher page]
  - **Expect silent hidden units without scaling. That is relevant to "grow where residual is high".**
  - Elfwing, Uchibe & Doya 2016 proposed "expected energy" as a better value than free energy. [S]
- **Embodied evolution of learning for survival:** Elfwing, Uchibe, Doya & Christensen 2011, "Darwinian embodied evolution of the learning ability for survival". [S, citation only] Relevant to "T or β as gene".
- **Active-inference foragers with interoception:**
  - Grimbly et al. 2026, arXiv:2608.04232, "Interoceptive attention as dynamic homeostatic prioritization in a foraging agent" (AffectWorld, a 4-channel gridworld). [V]
    - Reallocating a fixed interoceptive-precision budget to the most-needed channel roughly doubled learning-phase survival: 0.414 vs 0.199 over 11 layouts, 32 seeds each.
    - Aiming precision at the least-needed channel did worse than uniform.
    - They contrast this with homeostatic RL, which "integrates interoceptive state through a hand-designed homeostatic reward".
    - **Lesson for us:** a cheap extension is a gain on body-state inputs scaled by current need.
  - Pezzulo, Rigoli & Friston 2015, "Active inference, homeostatic regulation and adaptive behavioural control", *Progress in Neurobiology*. [M, not fetched]
  - Morville et al. (bioRxiv 242974): the active-inference critique of homeostatic RL. [A]
- **Homeostatic RL in deep agents and robots:** Yoshida et al. 2024 (two papers) and the 2025 perspective (Q3). These are the closest "body teaches the brain" precedents. None uses an energy-based brain.
- **What I did NOT find:**
  - An artificial-life creature with an RBM/EBM brain trained by drive reduction.
  - Any combination of energy-based policy + homeostatic reward + sleep replay + growth.
  - This is absence of evidence from a limited search, not proof of novelty. A dedicated scholar search would be needed before claiming it.

---

## (a) Recommendations for creature v0

**Brain and policy**
- F(x,a) = -b_a - w_a·x - Σ_h softplus(c_h + u_h·x + v_{h,a}), π = softmax(-F/T).
- **T = 1 fixed,** plus an entropy bonus β = 0.01 (exact over 3 actions).
- Weight decay 1e-4 per sleep step on w, u, v. **Not on b_a or c_h.**
- 8 hidden units at birth.

**Reward**
- r_t = D(h_t) - D(h_{t+1}), with D = (Σ_i w_i |h_i* - h_i|^n)^{1/m}.
- Start n = 2, m = 1, which gives an easily-read quadratic. Ablate n > m > 1, e.g. n = 4, m = 2, to get Keramati-Gutkin concavity and risk aversion.
- **h* and w fixed within life.** D computed from true h.

**Credit**
- **v0:** windowed Monte-Carlo return over n = 32 steps, γ = 0.97 (≈ D_t - D_{t+n}). Advantage = G - EMA(G).
- **v0.1:** add a linear critic V(x) with TD(λ = 0.9). Prefer actor-critic once v0 works, per Heess et al.
- **Death:** absorbing at the final D for the rest of the window, no escape.

**Learning rule**
- Δθ = α·A_t·[-∇F(x,a) + Σ_{a'} π(a'|x)∇F(x,a')], **signed A, never clipped.**
- **Sleep replay:** store π_old(a|x). Weight by clip(π_θ/π_old, 0.8, 1.2). At most 4 replay epochs per night.
- Interleave by shuffling episodes across the day, not in temporal order.

**Growth**
- New hidden unit: u_h = small random, c_h = 0, **v_{h,·} = 0** (policy-neutral at birth).
- Optionally freeze old units for K nights (Sallans & Hinton §8.1).
- Track entropy H(π) before and after each growth event, to catch effective-temperature drift (Elfwing 2013).

**Instrumentation:** log policy entropy, |w| norm, fraction of silent hidden units, advantage variance, and the per-night ratio-clip fraction.

**Ablations (each vs full model, ≥ 20 seeds)**
1. 0 hidden units (linear softmax).
2. No sleep: same gradient steps, online only.
3. No importance ratio in sleep.
4. No growth: fixed final size.
5. γ = 1 (expect failure, per the identity).
6. n = m = 1 vs n > m > 1.
7. Unsigned / positive-only reward.
8. T as gene vs β as gene.
9. Valence-swap re-learning.

**Baselines:** the Q6 list, including the matched correlated random walk and the sensor-limited oracle.

## (b) Questions for Ahmed

1. **Step size.** What is dt per step, and roughly how many steps from first smell to contact in your world? This sets the window n and λ. I recommend measuring it with the oracle first.
2. **Death.** Does the creature die, and when (energy = 0, toxin > max)? Is a life one episode, or continuing with respawn? This decides the terminal handling.
3. **Sleep vs dream.** Are you fine calling sleep "replay" in write-ups, and adding true "dreaming" (generated x) later as a separate ablatable feature?
4. **Genes.** Should T be a gene in v0, or do you accept T = 1 plus an entropy bonus, with β as the future gene?
5. **Critic.** Do you want the pure contrastive / REINFORCE story kept (no critic) for conceptual purity, or is a small linear critic acceptable in v0.1?
6. **Interoceptive input.** Should body state h be an input to F at all? If it is, the brain can learn state-dependent foraging (eat only when hungry). If it is not, it cannot express satiety.

---

## Sources
**Primary texts read this session [V]**
- Sallans & Hinton 2004, JMLR 5:1063-1088: https://www.jmlr.org/papers/volume5/sallans04a/sallans04a.pdf
- Heess, Silver & Teh 2013, PMLR 24:45-58: https://proceedings.mlr.press/v24/heess12a.html (PDF: https://proceedings.mlr.press/v24/heess12a/heess12a.pdf)
- Haarnoja et al. 2017, ICML: https://arxiv.org/pdf/1702.08165 (partial read)
- Keramati & Gutkin 2014, eLife 3:e04811: https://pmc.ncbi.nlm.nih.gov/articles/PMC4270100/ (read via the Europe PMC full-text XML)
- Yoshida, Sprekeler & Gutkin 2025: https://arxiv.org/pdf/2507.04998
- Yoshida, Kanazawa & Kuniyoshi 2024, bioRxiv: https://www.biorxiv.org/content/10.1101/2024.06.03.597087.full.pdf
- Horibe & Yoshida 2024: https://arxiv.org/abs/2411.12304 (intro only)
- Grimbly et al. 2026 (AffectWorld): https://arxiv.org/pdf/2608.04232

**Abstract or publisher page only [A]**
- Elfwing, Uchibe & Doya 2013, Front. Neurorobot. 7: https://frontiersin.org/articles/10.3389/fnbot.2013.00003/full (publisher page)
- Morville et al., The homeostatic logic of reward: https://www.biorxiv.org/content/10.1101/242974v1

**Abstract or search summary only [A/S]**
- Hulme, Morville & Gutkin 2019, Phys. Life Rev. 31:214-232: https://hal.archives-ouvertes.fr/hal-02355206
- Cesa-Bianchi et al. 2017: https://arxiv.org/abs/1705.10257

**Secondhand only [S]**
- Izhikevich 2007, trace constants from reproductions: https://brian2.readthedocs.io/en/2.9.0/examples/frompapers.Izhikevich_2007.html
- C. elegans chemotaxis references via search summaries; PMC review: https://pmc.ncbi.nlm.nih.gov/articles/PMC6665864

**Background, not re-fetched [M]:** Williams 1992; Sutton & Barto 2018; Ng, Harada & Russell 1999; Hinton et al. 1995 (wake-sleep); Degris et al. 2012; Schulman et al. 2017; Baxter & Bartlett 2001; Braitenberg 1984; Pezzulo, Rigoli & Friston 2015; Williams & Peng 1991; Tieleman 2008; Sutton 1990.
