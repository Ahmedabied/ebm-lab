# 06 - Generations and inherited priors (research seat R4)

Written 2026-10-13 for `DESIGN.md` §6. Question: what does a generation of the creature inherit, and how do we show, honestly, that inheritance helps? The population is small and runs on a laptop.

**Source tags** (every claim carries one):
- **[read]**: I read the primary text this session (full text, or the relevant section).
- **[abs]**: abstract or metadata only.
- **[2nd]**: secondhand, through a Genesis report or another paper's description. Treat it as unverified.
- **[inf]**: my inference, not a source.

Genesis inputs:
- digest A §1.5-1.6, L-1, L-7, L-8, L-10;
- digest B, report 11 and T5/T7;
- Genesis report 11 (`genesis-archive/docs/research/11-evolving-drives.md`), read directly;
- Genesis report 24 §4 (the severed-inheritance null), read directly.

---

## 1. The Baldwin effect: what was shown, what was overread, and the conditions

**Hinton & Nowlan 1987** ("How learning can guide evolution", *Complex Systems* 1:495-502) **[abs]**:
- Learning reshapes the search space and makes easier paths toward good gene combinations.
- Learning organisms evolve much faster than non-learning ones, though nothing learned is written back into the genotype.
- Setup **[2nd, via Genesis report 11]**: N=1000 haploid individuals, 20 loci, alleles {correct, incorrect, plastic}. Plastic loci get a bounded number of guesses per life. The fitness landscape is a needle in a haystack, and learning turns it into a slope.

**The overreading** (the critique flagged in digest B T7):
- Fontanari & Santos 2017, "The revival of the Baldwin effect", arXiv:1702.08411 **[abs]**. They argue that H&N's simulation showed only that "the learning ability is easily selected for". It did not show the Baldwin effect proper, where a learned behaviour becomes innate.
- They then demonstrate assimilation themselves, with fixation probabilities and waiting times. Learning can raise the fixation probability "by several orders of magnitude", depending on parameters **[abs]**. Genesis report 11 gives "up to six orders of magnitude" **[2nd]**.
- **Lesson for us [inf]:** "the plastic trait spread" and "the learned trait became innate" are two different claims, and each needs its own measurement.

**Ackley & Littman 1991** (*Artificial Life II*, pp. 487-509) **[read, full text]** is the most useful precedent because its setup is close to ours: foraging agents, predators, and a 2-D world.
- **Genome.** It has two parts:
  - initial weights of an *action network*, the innate behaviour;
  - an *evaluation network* that maps sensation to "goodness". Lifetime RL uses it to modify the action network.
- **Inheritance.** Learned action weights are not inherited. "the mechanisms of ERL make direct transmission of acquired characteristics impossible."
- **Baldwin, as observed.** Early on, agents carry learning genes saying "plants are good" and learn to approach plants. Later, action genes "recommend approaching plants right from birth". In the plant domain, "What once had to be acquired, was now inherited by around the 3 million time-step mark."
- **Caveat.** That evidence comes from *hypothetical fitness models* of gene sets ("though plausible, are only hypothetical"). In the carnivore domain, "Our data does not make a strong case for the Baldwin Effect".
- **Shielding.** Their own term: "The well-adapted action network apparently shielded the maladapted learning network from the fitness function". The agents came to *like* carnivores for over a million steps. They name the follow-on hazard "goal regression".
- **Stability condition.** "The Baldwin Effect depends upon the stability of both a problem and its solution."

**Ancel 2000** (*Theor. Pop. Biol.*): **[2nd]** via Genesis report 11 and two later reviews; the abstract was not seen.
- Coined the "Baldwin expediting effect".
- A quantitative-genetic model in which plasticity *slows* genetic evolution by masking genotype differences.
- Norm-of-reaction models in which it speeds evolution.

**Mayley 1996** ("No pain, no gain: landscapes, learning costs and genetic assimilation", Sussex CSRP 409; published as *Evol. Comput.* 4(3):213-234) **[abs]**. Assimilation needs two conditions:
1. **Neighbourhood correlation.** Points near each other in phenotype space must be near each other in genotype space.
2. **A cost of learning.** This supplies the pressure to make the trait innate.

**Fernando et al. 2018**, "Meta-Learning by the Baldwin Effect", arXiv:1806.07917 **[abs]**:
- Evolves the *initial parameters and hyperparameters* of deep learners. Learned weights are not inherited.
- Gets few-shot supervised and RL learners.
- MAML is more data-efficient "in simple cases", but the Baldwin route needs no backpropagation through the inner loop.
- This is the modern "inherit the capacity to learn" result.

**Simpson 1953**, "The Baldwin effect", *Evolution* 7:110-117: I saw it only as reference 24 in Ackley & Littman. **Weber & Depew (eds.) 2003**, *Evolution and Learning: The Baldwin Effect Reconsidered*, MIT Press: I confirmed the bibliography only. **I read neither. Nothing here is attributed to their content.**

**Conditions that make a Baldwin effect appear in simulation** (a synthesis of the sources above **[inf]**):
- A landscape where learning smooths a hard search (H&N).
- A stable problem across generations (Ackley & Littman).
- A real cost to learning, such as time or early-life risk (Mayley).
- Genotype and learned phenotype in correlated spaces (Mayley).
- Learning that is good but not perfect, because perfect learning shields (Ancel; Ackley & Littman).

**Controls that separate it from plain selection:**
1. **Learning-on vs learning-off evolution** (Ackley & Littman's ERL vs E).
2. **Innate performance with learning frozen**, tracked across generations: does what had to be learned become present at birth?
3. **The Baldwin signature from Genesis report 11** **[read]**: "`mean_ticks_to_competence` falls while `asymptotic_error` stays flat".
   - The bar must be fixed once, from generation-1 asymptotic performance, because "a moving bar would contaminate 'does it fall' with 'did the bar move'".
   - Shielding signature: gene variance fails to shrink while time-to-competence also fails to fall.
4. **Fixation statistics over many replicate runs** (Fontanari & Santos), not one trajectory.

## 2. Evolving the prior or evaluator vs the policy, and evolving plasticity

**How each paper measured "evolution adds value on top of lifetime learning":**

- **Ackley & Littman 1991 [read].**
  - **Design:** five strategies, each on 100 random initial populations, recording extinction time up to 10⁶ steps. The strategies were ERL (both), L (learning only), E (evolution only), F (fixed random action networks) and B (Brownian agents that ignore input).
  - **Results:** few runs survived at all: "No more than 18% of all populations reached 10,000 time steps and only 1.8% reached the 1 million time-step simulation limit."
  - The learning arms beat the non-learning arms early. E and F did worse even than brainless B.
  - Only "above about half a million time steps" does "ERL begin to pull away from learning-only (L)". ERL produced seven populations that reached 10⁶ steps.
  - **Their explanation:** "it is easier to generate a good evaluation function than a good action function". One evaluation weight ("energy is good") does the work of "the eight action weights involved in response to plants".
  - **A second measurement worth copying:** gene-segment *substitution rates* compared against drift (their Fig. 11, taken from molecular "functional constraint"). A segment under selection mutates less in the lineage than a neutral one. This is exactly Genesis's placebo-locus idea.

- **Singh, Lewis, Barto & Sorg 2010** (*IEEE TAMD* 2(2):70-82) **[read, relevant sections]**.
  - The optimal reward is `r*_A = argmax_{r∈R_A} E_{E∼P(E)} E_{h∼⟨A(r),E⟩} F(h)`. R_A must contain the *fitness-based reward* r_F.
  - So by construction the best reward never does worse than fitness-as-reward. The empirical question is the size of the margin.
  - **Measurement:** approximately exhaustive search over a reward space, each candidate scored by mean cumulative fitness over **200 sampled environments**. The baseline is "the best fitness-based reward function".
  - **Result:** the best reward outperformed it. It rewarded opening boxes, a distal, "intrinsic" behaviour.
  - **The point for us:** the baseline is not "no evolution". It is the best reward that only re-expresses fitness.

- **Zheng, Oh & Singh 2018** (NeurIPS, arXiv:1804.06459) **[read, via ar5iv]**.
  - **Comparison:** A2C or PPO on extrinsic reward, vs the same with a learned intrinsic reward, plus a "live-bonus" baseline tuned over {0.001, 0.01, 0.1, 1}.
  - **Seeds:** 5 runs on Atari (15 games), 10 seeds on MuJoCo (5 domains).
  - **Results:** better than A2C on all 15 games (>10% on 9). Better in 4 of 5 MuJoCo domains (Ant degraded).
  - **Missing control:** no random-or-fixed intrinsic-reward control is reported.
  - **Follow-up:** Zheng, Oh et al. 2020 (ICML, arXiv:1912.05500) **[abs]**: learned rewards capture "what" to aim for, policies capture "how". So rewards generalise to other agents and changed dynamics. Genesis report 11 adds the detail of transfer from actor-critic to Q-learning **[2nd]**.

**Evolving plasticity rules. What each one inherits:**

- **Soltoggio, Bullinaria, Mattiussi, Dürr & Floreano 2008** (*ALife XI*, pp. 569-576) **[abs]**.
  - Evolution designs networks with standard and *modulatory* neurons for T-mazes whose reward location changes within a life.
  - With modulation enabled, networks learned better than with it disabled, and modulatory neurons evolved on their own.
  - **Inherited:** topology, weights and modulatory gating. The rule's *when and how much* is under genetic control.
  - The broader review is Soltoggio, Stanley & Risi 2018, "Born to Learn" (arXiv:1703.10371) **[2nd, via report 11]**.

- **Najarro & Risi 2020** (NeurIPS, arXiv:2007.02686) **[read, via ar5iv]**.
  - **Inherited:** only per-synapse Hebbian coefficients, `Δw_ij = η_w(A_w o_i o_j + B_w o_i + C_w o_j + D_w)`. Weights are **randomly initialised every episode** from U[−0.1, 0.1].
  - **Key finding:** "Evolving the initial weights alongside the Hebbian coefficients did not improve training efficiency."
  - **Method:** an evolution strategy with population 200 (CarRacing) or 500 (quadruped), σ=0.1.
  - **Results:** CarRacing, 872±11 Hebbian vs 711±16 static.
    - On the seen quadruped morphologies, static weights did *better* (1604 vs 1051 undamaged).
    - On an *unseen* damage, only the Hebbian network solved it (452±95 vs 68±56).
  - **Lesson [inf]:** inherited plasticity pays under within-life change. In a static task, inherited weights can win.

- **Miconi, Clune & Stanley 2018**, "Differentiable plasticity" (ICML, arXiv:1804.02464) **[abs plus secondary description]**.
  - **Each connection:** a fixed weight plus α × a Hebbian trace. Per-connection α and the trace rate are trained.
  - **Inherited** (meta-trained, by gradient descent, not evolution): baseline weights *and* plasticity coefficients.

**Consensus [inf]:** every one of these keeps learned content out of the inheritance. What is inherited is the learner: initial bias, learning rate, plasticity coefficients, or reward. That is Genesis L-1.

## 3. Lamarckian vs Darwinian (Baldwinian) inheritance of weights

- **Whitley, Gordon & Mathias 1994** (*PPSN III*, LNCS 866, pp. 6-15, doi:10.1007/3-540-58484-6_245): **[2nd]** via Benito, Lutzeyer & Doerr 2026; the paper itself was not seen.
  - Baldwinian search "allows for accelerated convergence towards a global optimum" on a moderately deceptive function.
  - Benito et al. summarise the comparative literature: Lamarckian is faster on easy problems but "more susceptible to getting trapped in local optima", while Baldwinian is often slower but more reliable on hard problems.

- **Benito, Lutzeyer & Doerr 2026**, "A Fresh Look at Lamarckian Evolution and the Baldwin Effect" (*PPSN XIX*, LNCS 16988, pp. 459-474; arXiv:2605.28703) **[abs]**:
  - Empirically, both Baldwinian and Lamarckian beat Darwinian on MIS and MaxCut.
  - Theoretically, on DeceptiveLeadingBlocks with block length k, the Baldwinian (1+1) EA's runtime is independent of k, while Lamarckian and Darwinian runtimes grow steeply with k.

- **Castillo et al. 2006** (arXiv:cs/0603004; neural-net evolution) **[abs]**:
  - Lamarckian gave low error and the *smallest* networks.
  - Baldwinian gave the lowest error, but larger networks and slower search.

- **Sasaki & Tokoro 1999/2000** (*KAIS* 2:201-222; LNCS 1999) **[abs of the 1999 paper]**:
  - In *changing* environments, the population with zero inheritance of acquired characters (the Darwinian case) reached the highest adaptation.
  - Lower Lamarckian rates were more stable when the environment changed.

- **Luo, Miras, Longhi, Weissl & Eiben 2024** (arXiv:2403.19545) **[abs]**: the opposite verdict for learning robots. "Lamarckian systems outperform Darwinian ones in adaptability and efficiency, particularly in challenging conditions."

- **Thomsen & Rasmussen 2023** (arXiv:2305.00491) **[abs]**: Lamarckian is superior "in most cases with low learning cost". The advantage shrinks as learning cost rises. Baldwinian usually falls in between.

**Which wins when [inf, from the above]:**
- **Lamarckian wins on speed** when three things hold: the problem is static and not deceptive, learning is cheap, and the learned weights are valid in the child's world.
- **Baldwinian wins on reliability** under deception (local optima) and, in some studies, under environmental change, because it keeps genetic variance that learning can exploit.
- **The evidence on dynamic environments conflicts** (Sasaki & Tokoro vs Luo et al.).

**For our purpose the deciding argument is scientific, not performance [inf]:**
- Lamarckian inheritance makes "inherited priors help" trivially true. The child simply starts where the parent ended, so the claim we care about becomes untestable.
- Genesis made the same call for the lexicon: "copying the matrix would delete the force we are studying" (digest A §1.5).
- So keep `ebm-lamarck` as an ablation arm, with the cross-fostering control in §4.

## 4. The severed-inheritance null, defined for our setting

**The confound.** Truncation selection picks creatures that lived long. Part of a long life is luck: the world seed, early encounters, poison placement. Children of selected parents will therefore regress toward the mean.
- So "children of survivors beat their generation's average" is not evidence of inheritance. Neither is "generation 20 beats generation 1 on the selection world".
- The literature's measurement is a **parent-offspring regression**. Its slope estimates heritability (h²). The breeder's equation is R = h²·S (Genesis report 11 §3 **[read]**).
- Report 24 §4.3 **[read]** gives the reason only a severing arm can carry the word "inherited": an exogenous variable can make a trait covary with fitness with "no genetic covariance, and no evolutionary relevance" (Hajduk et al. 2020, quoted there **[2nd]**).
- Its published ABM precedent is Harper & Zietsch 2025's "Nonheritable-preferences model" **[2nd, quoted in report 24]**.
- **Mechanism note:** Genesis's first `pref-redraw` was implemented wrongly, as a redraw per decision rather than at birth (digest D). **It must live in the birth function.**

**The arms.** All share the same selection code, mutation σ, N, world seeds and number of lives. Only the birth function differs.

| Arm | Parent choice | Child genome | What it isolates |
|---|---|---|---|
| `full` | by fitness (tournament or truncation) | parent's genome + Gaussian mutation | the subject |
| `severed` | by fitness (computed and logged, then discarded) | **each locus redrawn at birth from the founder (generation-0) distribution** | everything except transmission: regression to the mean, world drift, measurement artefacts. Its trajectory must be flat. The gap "selected parents' fitness minus their severed children's fitness" *is* regression to the mean. |
| `random-parents` | uniform at random | parent's genome + mutation | drift plus mutation with selection off; the neutral baseline for gene trajectories |
| `severed-fork` (Genesis-faithful) | by fitness | at generation G/2, fork `full`. Each child locus is redrawn from **that generation's pre-selection cohort marginals** (phenotypic variance kept, parent-offspring link killed). | whether the *individual lineage* carries value beyond the population-level distribution already reached. This is report 24's exact definition: "kept phenotypic variance … additive transmission killed". |

**Note [inf].** Started from founders, "redraw from own pre-selection cohort" is the same as `severed`, because that cohort never moves. That is why the Genesis-faithful form needs the fork.

**Common garden (the replacement for cross-fostering).** These creatures have no parental care, so classic cross-fostering does not apply. Two analogues do:
1. **World cross-fostering / common garden.**
   - Freeze every k-th generation's genomes.
   - At the end, evaluate *all* frozen genomes from all arms on the **same held-out world seeds** that selection never saw.
   - This removes "the selection world got easier or harder" and selection-world overfitting.
   - It is the logic of resurrection assays against frozen ancestors (Lenski's long-term *E. coli* practice; **from memory, not re-verified this session**).
2. **Content cross-fostering** (only for `ebm-lamarck` or a distillation channel).
   - Child of genetic parent A receives the learned weights (or replay cache) of an *unrelated* survivor B.
   - The 2×2 of genome-parent × content-parent identifies both effects.
   - Genesis's own PLAN Wave I argument, quoted in report 24 §4.4 **[read]**: "'resembles my parent' and 'learned from my parent' are perfectly collinear … Severing the imprint target from genetic parentage identifies both coefficients."

**Pre-registration [inf, following report 24 §4.4]:**
- Run the parent-offspring regression on every gene and on lifespan in `full`. It is cheap and offline.
- Run `severed` as a manipulation check whose expected result is known: a flat trajectory.
- If `severed` does *not* stay flat, the evaluation is broken. Stop there.

## 5. Population genetics at laptop scale

**Drift floor.** A gene is selected rather than drifting only if it moves relative reproductive success by about **s* ≈ 1/(2Ne)** (haploid).
- Genesis measured Ne = 32.82, giving 1.523%, and found that the harmonic mean is "dominated by the bottlenecks" (digest A L-8).
- Report 11 **[read]** gives 1.25% at N=40. It warns that with always-on mutation the equilibrium variance is V* ≈ 2·Ne·Vm, large enough that unselected genes drift to the clipping bounds.

**What this means for DESIGN's current default [inf]:** N=24 with top-25% truncation leaves 6 parents per generation.
- If each parent contributes equally, Ne is on the order of the number of parents, so about 6. That makes s* about 8%. Only genes with large effects can be selected.
- Tournament selection (k=2-3) lets most individuals reproduce, so Ne should be higher at the same N.
- **Measure Ne rather than assume it.** Add one unclipped *placebo locus* (wired to nothing) and use Ne ≈ V_placebo/(2·Vm) at equilibrium.
  - The same locus is Genesis's placebo control **[2nd, digest C]** and Ackley & Littman's drift baseline **[read]**.
- Also log the fraction of each gene pinned at its bounds, per generation (report 11 **[read]**).

**Published norms:**
- **NEAT** (Stanley & Miikkulainen 2002, *Evol. Comput.* 10(2)) **[read]**:
  - population 150 (1000 for the hardest task);
  - an 80% chance a genome's weights mutate, each weight then perturbed with 90% probability or replaced with 10%;
  - add-node 0.03, add-link 0.05;
  - species champions (species >5) copied unchanged;
  - stagnation cutoff 15 generations; 25% of offspring by mutation only.
  - **Runs:** XOR over 100 runs, pole balancing over 50 runs (120 for some ablations).
- **CMA-ES** (Hansen tutorial, arXiv:1604.00772) **[2nd, search summary of the tutorial]**: default λ = 4 + ⌊3 ln n⌋ and μ = ⌊λ/2⌋. Increase λ for noisy problems. For a 6-gene genome that is λ = 9; for the 106-float θ₀ genome, λ = 17 **[inf, arithmetic]**. Our noisy-fitness setting argues for the larger end.
- **ES on plastic networks** (Najarro & Risi): σ = 0.1, population 200-500 **[read]**.
- **Minimal-ALife norm:** Izquierdo & Beer 2013 *C. elegans* klinotaxis used 20 parameters, 60 individuals, 300 generations and 100 runs. 17 of 100 runs failed **[2nd, via R2's `research/04`, which read the full text]**.
- **Ackley & Littman:** 100 independent populations per strategy **[read]**.

**How many generations × seeds:**
- Report 11's arithmetic **[read]**, with its illustrative h²=0.3 and S=0.08:
  - R ≈ 0.024 per generation;
  - signal-noise parity after about 8-9 generations, 30-40 generations for confident detection in a single run;
  - about 20 pooled seeds can surface a signal in a few generations.
- Colas, Sigaud & Oudeyer 2018 (arXiv:1806.08295) **[read, via ar5iv]**:
  - In their worked example, 5 seeds gave β = 0.51 (51% chance of missing a real effect). 10 seeds gave β = 0.19.
  - Use at least 20 samples to estimate standard deviations robustly.
  - Prefer Welch's t-test, set α below 0.05, and correct for multiple comparisons.
- Genesis's warning: "a seed is a world, not a replicate". Keep world seeds separate from evolution seeds (digest A L-12).

## 6. What the genome should contain

**Criterion:** Stephens 1991 via Genesis report 11 **[read]**:
- learning evolves under *within-generation* predictability;
- genes evolve under *between-generation* predictability;
- physics is what is true regardless of strategy.

Add Genesis L-8: few loci, added one wave at a time.

**This exposes a fact about creature v0 [inf].** The blend→effect mapping (food = A+B, poison = B+C) is fixed forever in v0, which makes it a between-generation regularity.
- A genome that can encode the policy (full θ₀) will eventually hard-wire "approach A, avoid C", and learning will be shielded (Ackley & Littman).
- That is a legitimate Baldwin experiment, but it answers a different question from "does inherited learning capacity help".
- To test that question, we also need a world where the mapping is redrawn **per life** (the v1 "seasons", moved earlier). There, only learning-related genes can help.

| Candidate | v0 verdict | Reason and precedent |
|---|---|---|
| Learning rate η_lr | **Inherit** (log-encoded) | Genesis G_LEARN; Fernando 2018 evolves hyperparameters; Najarro evolves η |
| Temperature T | **Inherit** (log-encoded) | Doya 2002: noradrenaline ↔ randomness of action [2nd, report 11]; a hyperparameter in the Fernando sense |
| Eligibility decay λ | **Inherit** | Doya: serotonin ↔ reward timescale [2nd]; a timescale only a lineage can tune |
| Initial hidden size H₀ and growth threshold | **Inherit** (see §7) | NEAT: structure is genetic and starts minimal [read] |
| Placebo locus | **Inherit** (wired to nothing) | measures drift and Ne (§5) |
| Full initial weights θ₀ (~106 floats at H₀=4) | **Not in v0** | at Ne≈6-20, 106 weakly selected loci mostly drift (L-8); Najarro found evolving initial weights added nothing [read] |
| Innate per-note valence (3 genes) | **Stage B** | Ackley & Littman: goals are cheaper to specify than implementations [read]. Two forms to compare: (i) *policy prior*, valence expanded into the initial w via the antenna symmetry (a tiny indirect encoding); (ii) *evaluator*, an evolved shaping term added to the body's lesson, r' = r + Σ_k g_k·Δ(note_k). Form (ii) is the Singh/Zheng "evolve the reward" option; Zheng 2020 predicts it transfers better if body dynamics change [abs]. |
| Drive weights w_E, w_X | **Stage C, with a guard** | Singh 2010: the best reward for a bounded agent need not be fitness [read]. But the drive is the body's physics (DESIGN law 2), and Genesis L-6 says every leak gets exploited. Fitness must stay survival. |
| Drive exponent n, setpoints | **Do not inherit** | they define what the body *is*; physics |
| Sleep length / epochs | **Stage C** | a real trade-off (sleep costs ticks, buys consolidation), so it is selectable [inf]; I found no direct precedent |
| Downscaling δ | Stage C | same reason |
| Antenna geometry | **Do not inherit in v0** | morphology changes the input statistics under every brain gene; Genesis report 12 treats body evolution as its own project [2nd, digest B]. Fix it first, evolve it later. |
| Mutation rate | **Fixed** | Genesis made it heritable [2nd], but self-adaptation needs selection signal that tiny Ne lacks [inf] |

## 7. Developmental growth vs evolutionary growth

**Three options:**
- **(a) Parent's final size.** Lamarckian structure: it copies acquired capacity and inherits the same objection as §3.
- **(b) Fixed H₀.** Pure Darwinian. Clean, but growth then never improves across generations.
- **(c) Genome-encoded H₀ plus growth rule.** Baldwinian structure.

**Precedents:**
- **NEAT [read].** Structure is inherited and complexifies only by mutation, starting minimal ("searches for the solution in the lowest-dimensional weight space possible").
  - The ablations, on double pole balancing with velocities:

    | Variant | Mean evaluations | Failure rate |
    |---|---|---|
    | Full NEAT | 3,600 | 0% |
    | No-growth (fixed topology) | 30,239 | 80% |
    | Initial-random topology | 23,033 | 5% |

  - Both growth and a minimal start matter.
- **Bongard 2011** (*PNAS*) **[abs and press]**. Robots that grow from an anguilliform to a legged body *within a life* evolved gaits for the final form faster, and the gaits were more robust. Over evolution the juvenile form was gradually lost. This is development itself being assimilated, and it is the closest precedent to (c).
- **Indirect encodings.** Stanley 2007, CPPNs (*GPEM* 8(2):131-162), and Stanley & Miikkulainen 2003, "A taxonomy for artificial embryogeny" (*Artificial Life* 9(2):93-130) **[abs/bibliographic]**. These are the path when the flat genome hits its ceiling (Genesis L-10). They are overkill for v0. The 3-gene valence map above is the smallest version of the idea.

**Recommendation [inf]: (c).**
- The genome carries H₀ (an integer), mutated by ±1 with small probability, in the spirit of NEAT's add-node at 0.03. It also carries the growth threshold.
- The child starts at its own H₀ with fresh random small weights. Nothing the parent grew is copied.
- Use asexual reproduction (mutation only), so no historical markings are needed.
- **The signature to log:** does H₀ creep up toward the typical final H of the parents' generation? (This is Bongard-style assimilation of development.) Does growth then happen earlier, or not at all?
- Compare against DESIGN's `ebm-fixed-final` arm.

---

## (a) Recommendations for creature v0 generations

**Genome, staged (L-8):**
- **Stage A:** {log η_lr, log T, λ, H₀, growth threshold} + 1 placebo locus.
- **Stage B:** + 3 valence genes. Run the policy-prior and evaluator forms as separate arms.
- **Stage C:** drive weights, sleep epochs, δ.
- Never inherit learned weights, except in the `ebm-lamarck` ablation.
- Change DESIGN §6. Its current "θ₀ plus (η_lr, T, λ)" puts about 106 loci on a population with Ne ≈ 6.

**Selection scheme [inf, from §5]:**
- N = 32-48.
- Tournament selection with k=2, plus 1-2 elites copied unchanged (as NEAT copies champions). Prefer this to top-25% truncation of 24.
- Gaussian mutation σ ≈ 0.05-0.1 in normalised gene units, on every locus. Rates are log-encoded.
- Each genome lives ≥2 lives on different world seeds per generation if the time budget allows. This cuts selection noise, which is the raw material of regression to the mean.
- Generations: G ≈ 40-50 (report 11: 30-40 for single-run detection).
- Seeds: a pilot of 10 evolution seeds per arm, then a power analysis (Colas: ≥20 samples for a stable SD), then confirmation at ≥20 seeds.
- Time one life on the laptop before committing. The budget is arms × seeds × G × N × lives.

**The two nulls:**
1. **`severed`:** each locus redrawn at birth from the founder distribution, with the same selection run and logged. Expected result: flat. It measures regression to the mean directly.
2. **`random-parents`:** inheritance on, selection off. This is the drift baseline. Add the **`severed-fork`** at G/2 for the Genesis-faithful "inherited" claim.
- Plus the learning arms after Ackley & Littman:
  - `full` (ERL);
  - no evolution (L): founders re-sampled every generation with learning on;
  - evolution with learning off (E), with η_lr forced to 0.
- Plus the Stephens 2×2: fixed blend mapping vs mapping redrawn per life.

**Metrics:**
- Common-garden lifespan of frozen genomes on held-out worlds. This is the headline.
- Time-to-competence against a bar fixed from generation 1, and asymptotic performance. The Baldwin signature is the first falling while the second stays flat.
- **Innate performance:** frozen genome run with η_lr=0. Assimilation shows as this rising.
- Per gene, per generation:
  - mean and variance vs the placebo (selected genes should show lower variance and directional change);
  - fraction at the bounds;
  - parent-offspring regression slope.
- H₀ vs the parents' final H.
- Report per-creature and per-seed denominators. Pooled events are pseudoreplication (digest C, report 24).

## (b) Questions for Ahmed

1. **Does "grows over generations" mean the brain gets bigger across generations (H₀ evolves, option c) or only within a life?** The controls differ.
2. **Should the blend→effect mapping be redrawn per life now, rather than in v1?**
   - If it stays fixed, evolution can hard-wire the answer and learning becomes optional, which is a Baldwin study.
   - If it is redrawn, only "learning to learn" can be inherited, which is the Genesis lesson.
   - My suggestion is to run both as a 2×2.
3. **Stage B: may the genome add an evolved shaping term to the body's lesson (an inherited "this smell feels good")?** Or is the body the *only* teacher with no innate valence, in which case only the policy-prior form is allowed?
4. **Asexual reproduction only for v0?** It avoids crossover alignment on variable-size brains.
5. **Is the Lamarckian arm worth its compute, given it cannot support the "inherited capacity" claim?** Or should it be replaced by the Genesis-style distillation channel: the child retrains from a capped sample of the parent's replay cache (digest A L-1)?
6. **Compute budget.** Is ~1 laptop-day per experiment acceptable, or should long sweeps go to the box?
