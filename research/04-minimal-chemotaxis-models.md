# 04 - Minimal chemotaxis models: circuits, strategies, baselines, metrics

Research seat R2, 2026-10-13. Builds on `02-minimal-organism.md`, which was written from search snippets only.

**How to read the sourcing marks**

- **[full text]** - I read the paper's text: Europe PMC full-text XML, or the PDF for Berg & Purcell.
- **[abstract]** - I read the official abstract only (Europe PMC / PubMed record).
- **[secondhand]** - I saw the claim only in a search snippet, a review, or another paper's description. Not checked against the original.
- **[known, not fetched]** - A standard reference I am confident exists, but I did not open it this session. No numbers are taken from it.

Anything labelled "my derivation" or "suggestion" is my own reasoning, not a literature claim.

---

## Q1. Minimal neural circuits for klinotaxis in C. elegans

### Izquierdo & Lockery 2010

**Paper:** "Evolution and analysis of minimal neural circuits for klinotaxis in *Caenorhabditis elegans*", J Neurosci 30(39):12908-17, doi:10.1523/JNEUROSCI.2606-10.2010. Sourcing: [abstract] plus targeted extraction from the PMC full text (PMC3422662).

**Smallest circuit that works.** In the abstract's words, "a minimalistic neural network, comprised of an ON-OFF pair of chemosensory neurons and a pair of neck muscle motor neurons, is sufficient to generate realistic klinotaxis behavior". That is **4 neurons and no interneurons**. The paper concludes that the dynamics of klinotaxis "do not require additional processing by interneurons". In the real worm, interneurons "could be acting mainly as conduits of activity".

**Sensor encoding.** The sensory cells are not left/right spatial sensors. They are temporal-derivative cells: activation is a function of D(t) = c_N(t) - c_M(t).

- c_N is the mean concentration over the last N seconds.
- c_M is the mean over the M seconds before that.
- The ON cell takes the positive part of D.
- The OFF cell takes the negative part, sign-inverted.

Both cells read the same point, the head.

**Body and motor model.**

- The worm is a single point moving at a constant 0.022 cm/s.
- An imposed sinusoidal head-sweep oscillation has period T = 4.2 s.
- Gaussian noise with SD 0.05 is added.
- Steering comes from the neck motor neurons modulating the amplitude of the dorsal/ventral sweep.

**Fitness metric.** CI = (1/T)∫₀ᵀ (1 − h(t)/h(0)) dt.

- h(t) is the distance to the gradient peak.
- h(0) = 4.5 cm and T = 500 s.
- Negative values are clipped to 0.
- Fitness is the mean CI over 50 assays.

There were 100 evolutionary runs, and **77 evolved networks** went into the dynamical-systems analysis (the abstract says 77; the extraction tool said this subpopulation had fitness ≥ 0.75).

**What evolution found.** The abstract says emergent properties "reproduced two key experimental observations that they were not designed to fit":

1. the sinusoidal relation between turning bias and bearing;
2. the different effects of ablating the ON cell versus the OFF cell.

The mechanism is described as "remarkably parsimonious". The asymmetry needed for steering comes from shifting the motor neurons' sigmoid input-output function relative to the range of the oscillatory head-sweep input. In effect, **the phase of the head sweep gates whether a sensory change turns the worm left or right.**

**Caveat on "what hand design didn't find".** The paper does not compare against a hand-designed klinotaxis circuit. Its point of comparison is that earlier network models of worm chemotaxis "have focused almost exclusively on klinokinesis":

- Ferrée et al. 1997
- Ferrée & Lockery 1999
- Dunn et al. 2004, 2007

So the honest version is this: earlier models were mostly hand-specified or optimized for klinokinesis. Evolution found a klinotaxis mechanism built on state (phase) dependence that nobody had proposed.

### Izquierdo & Beer 2013

**Paper:** "Connecting a connectome to behavior: an ensemble of neuroanatomical models of *C. elegans* klinotaxis", PLoS Comput Biol 9(2):e1002890, doi:10.1371/journal.pcbi.1002890. Sourcing: [full text] (https://pmc.ncbi.nlm.nih.gov/articles/PMC3567170/).

**Finding the circuit.** The authors searched the connectome from the chemosensory neurons to 10 head/neck motor neuron classes.

- The unconstrained ASE→SMB network contained 88.41% of all neurons.
- Restricting to paths of length 3 cut it to 23 neurons (7.61%) and 276 synapses/gap junctions.
- Keeping only connections with ≥ 2 contacts left two interneuron classes, **AIY and AIZ**.

The result is the "minimal klinotaxis network": ASE (ON = ASEL, OFF = ASER) → AIY → AIZ → SMB (dorsal/ventral, left/right). "Any further simplification breaks the fully-connected criterion." Notably, AIY and AIZ were already known experimentally to matter, and they came out of the pruning without being chosen.

**Model details.**

- Sensors use the same ON/OFF derivative operator, with N and M evolved in [0.1, 4.2] s.
- Interneurons are passive isopotential nodes with tonic, sigmoidal chemical synapses and non-rectifying gap junctions.
- The body is a point at 0.022 cm/s with an imposed 4.2 s sine oscillation.
- Pirouettes are random reorientations at 0.033 Hz, switched off during analysis.
- The gradient is conical during evolution, with steepness randomized in [−0.38, −0.01]. Cones avoid the Gaussian problem where steepness is tied to distance. Tests were then run in Gaussian gradients.
- 20 parameters, 60 individuals, 300 generations, 100 runs.

**Results.**

- 17 of 100 runs failed (CI < 0.5).
- 27 reached CI ≥ 0.75. Over a longer assay these averaged CI 0.87.
- Conical vs Gaussian CI: 0.875 vs 0.871.
- Reliability was 100%, where reliability is the proportion that reach within 0.1 cm of the peak.

**What evolution found.**

1. **An ensemble, not one answer.** Several different mechanisms fit the same anatomy. The authors frame evolution as "a kind of semi-automated hypothesis generator".
2. **Unconstrained left/right asymmetry.** In the best network, AIYL responds to small changes either way, while AIYR, because of a strong negative bias, responds only to large increases. Their ranges are complementary.
3. **Shared operating principles across the ensemble.**
   - ON activation reduces path curvature and OFF activation increases it.
   - When one motor neuron is sensitive, the other is not.
   - Turning changes last about one head sweep.

A follow-up information-flow analysis of the same ensemble exists: Izquierdo, Williams & Beer 2015, PLoS ONE, doi:10.1371/journal.pone.0140397 [secondhand: title and abstract seen only].

**Lesson for us.** The worm's minimal circuit does not compare left and right. It compares now with a moment ago at one point, and **turns time into space by sweeping its head**. That bears directly on Q3.

---

## Q2. Learning in worm chemotaxis

### Hironaka & Sumi 2025

**Paper:** "A neural network model that generates salt concentration memory-dependent chemotaxis in *C. elegans*", eLife 14:RP104456, version of record 28 Aug 2025, doi:10.7554/eLife.104456. Sourcing: [full text, including the assessment, public reviews and author response] (https://pmc.ncbi.nlm.nih.gov/articles/PMC12393885/).

**The proposed "plasticity".** The authors start from earlier experimental work on the ASER→AIB synapse in klinokinesis [secondhand, via this paper: Sato et al. 2021; Hiroki et al. 2022]:

- ASER's **basal glutamate release** rises transiently when current salt is below the cultivation salt, and falls when current salt is above it.
- AIB carries an excitatory glutamate receptor (GLR-1) and an inhibitory one (AVR-14) with different sensitivities.
- So the sign of the ASER→AIB synapse flips depending on the gap between the remembered and the current concentration.

They hypothesize that the same holds for ASER→AIY in klinotaxis. They reused the Izquierdo & Beer network, added an experimental constraint that AIY→AIZ is inhibitory, and evolved parameters for CI. Replacing the inhibitory ASER→AIY connection with an excitatory one reversed the salt preference.

**This is not a learning rule.** Reviewer 1: "the ASER-to-AIY connection is predefined as inhibitory or excitatory in separate models". In plain terms, there are two hand-set parameter regimes and no dynamics that compute the switch from experience. The authors answer that they also swept the weight gradually from inhibitory to excitatory (their Figs S4-S5).

**What critics say.**

- **Original eLife assessment** (quoted in the author response): the work rests on "an established model", but "the model's lack of integration of newer experimental findings, its reliance on predefined synaptic states, and oversimplified sensory dynamics" make it "incomplete".
- **Final assessment:** "valuable" and "solid".
- **Reviewer 1:** ablation studies indicate "AIY is not critical for chemotaxis", and other interneurons have overlapping roles, which "challenge the centrality of AIY". ASER's complex, context-dependent responses are not modelled. The oscillator is imposed from outside, so conclusions about gap junctions should be read cautiously.
  - Authors' reply: experimental CI mixes klinokinesis with klinotaxis, so AIY's role in klinotaxis may be hidden.
- **Reviewer 2:** "key assumptions" lack biological validation. CI is only an endpoint metric. Trajectories from the constrained model converge visibly faster even though CI shows no significant difference.

**Lesson for us.** The biological story is a **slowly updated set point**: remembered concentration, with a sign given by current minus memory, that flips the valence of one fast sensory pathway. That is a cheap, one-scalar-per-note inductive bias. It suggests the baseline in Q4: a learned sign per note. Reviewer 2's point about CI also argues for **pre-registering a trajectory metric next to any endpoint metric**.

### Pierce-Shimomura, Morse & Lockery 1999: klinokinesis

**Paper:** "The fundamental role of pirouettes in *Caenorhabditis elegans* chemotaxis", J Neurosci 19(21):9557-69, doi:10.1523/JNEUROSCI.19-21-09557.1999. Sourcing: [abstract].

- Worm tracks split into runs and pirouettes.
- Pirouette onset correlates with dC/dt, not with absolute C. Pirouettes are most likely when heading down the gradient and least likely when heading up.
- After a pirouette, the mean heading is up the gradient.
- A stochastic point model using only this correlation produced chemotaxis in both radial and planar gradients.

Iino & Yoshida 2009, J Neurosci, doi:10.1523/JNEUROSCI.3633-08.2009 [abstract], added the weathervane (klinotaxis) mechanism. Their simulation found that "both mechanisms need to act in parallel for efficient chemotaxis". ASE and AIZ are essential for both, and salt-conditioned animals reverse both.

**Takeaway.** Two strategies sit side by side even in the worm:

- **klinokinesis** - when to turn, driven by dC/dt;
- **klinotaxis** - which way to steer.

Our creature's three actions can express both. Turning in place amounts to a reorientation, and asymmetric turning is steering.

---

## Q3. The bacterial strategy, and spatial versus temporal comparison

**Segall, Block & Berg 1986.** "Temporal comparisons in bacterial chemotaxis", PNAS 83:8987-91, doi:10.1073/pnas.83.23.8987. Sourcing: [abstract].

- Wild-type *E. coli* "make short-term temporal comparisons extending 4 sec into the past". The last ~1 s is weighted positively, the previous ~3 s negatively, "and the cells respond to the difference".
- cheRcheB methylation mutants do not make these comparisons.
- cheZ mutants weight back "at least 40 sec".
- The gain is huge: "the change in occupancy of one receptor molecule produces a significant response".

**Run-and-tumble as a 1-bit strategy.**

- Typical runs are ~1 s and tumbles ~0.1 s; speed is ~14-20 µm/s [secondhand, via search summaries of Berg & Brown and Berg's texts]. I did not open *Random Walks in Biology* (Berg, Princeton UP) [known, not fetched].
- The output is one bit per moment: keep running or tumble.
- The memory is a bipolar filter. This is exactly the D(t) operator in the worm model, with N ≈ 1 s and M ≈ 3 s.
- So **the same "now minus recent past" kernel shows up in bacterium and worm models**.

**Berg & Purcell 1977.** "Physics of chemoreception", Biophys J 20:193-219. Sourcing: [full text, PDF]. The usual story is that bacteria are too small for spatial sensing. The paper is more nuanced:

1. From experiments, *E. coli* makes temporal comparisons over about 1 s, and "for E. coli, even 5 s would be prohibitive".
2. They then ask whether front-versus-back comparison could work, and find T > 1.7 s for the Dahlquist experiment: "a mechanism involving spatial comparisons remains feasible."
3. "But there is a much more serious problem: motion of the cell will generate an apparent spatial gradient". The moving cell sees an apparent gradient of decay length D/3v, which in that experiment is "600 times steeper than the real gradient!"
4. "The spatial mechanism is much more effective if the cell is large", as with *Dictyostelium*.

**Supporting results.**

- Mora & Wingreen 2010 (arXiv:1002.3907) [full text skimmed via ar5iv] contrast large eukaryotes (*Dictyostelium*, yeast), which sense spatially across their length, with small bacteria, which sense ramps over time.
- Endres & Wingreen 2008, PNAS, doi:10.1073/pnas.0804688105 [abstract], derive physical limits for direct gradient sensing and find *Dictyostelium* operates near them.
- In *Drosophila* larvae, a single functional olfactory neuron is enough for chemotaxis, and **bilateral input improves accuracy through higher signal-to-noise**. Source: Louis, Huber, Benton, Sakmar & Vosshall 2008, Nat Neurosci 11:187-199, doi:10.1038/nn2031 [abstract].
- Larvae also mix both modes. Negative gradients integrated during runs set when to turn; positive gradients sensed during head casts set which way. Source: Gomez-Marin, Stephens & Louis 2011, Nat Commun 2:441, doi:10.1038/ncomms1455 [abstract]. The authors call this intermediate between *E. coli*'s biased random walk and stereo-olfaction.

**Should both channels be offered? Yes, but in a specific way (suggestion).**

- **Spatial channel.** Give the brain raw L and R readings per note. The L−R difference is a free spatial cue.
- **Temporal channel.** Do *not* give the brain a pre-computed dC/dt. If the brain has any recurrent state or a short input history, it can build the temporal comparison itself. Building it is a small, measurable piece of learning.
- **Ablation probes.** Run a one-antenna condition (both antennae read the same point, or one is masked) and a no-memory condition. These show which channel the learned policy actually uses. That mirrors the Louis 2008 unilateral/bilateral experiment.

**Which is more honest for a creature our size? (my derivation)**

Take a steady-state diffusing-and-decaying field from a point source on a grid. Far from the source it falls roughly as exp(−r/λ), with λ = √(D/k): diffusion over decay. Then:

- Fractional left-right difference across antenna spacing s: ΔC/C ≈ s/λ.
- Fractional change from one forward step of length ℓ: ≈ ℓ·cosθ/λ.

If s ≈ ℓ ≈ 1 cell, **spatial and temporal signals are about the same size**. Without sensor noise, both are perfectly reliable, so the task is trivial and nothing has to be learned about direction.

Berg & Purcell's framing says the honest choice is set by **noise relative to the gradient over the sensing baseline**, plus motion artifacts. So:

1. Add multiplicative or Poisson-like sensor noise.
2. Choose λ so that s/λ is near the noise level at mid-range distances.

Then neither cue is free. Temporal integration over several steps, or averaging the two antennae, becomes worth learning. A grid creature with body-length antenna spacing is closer to a worm or larva (a few mm) than to a bacterium. Spatial comparison is "honest" if, and only if, the noise is there.

---

## Q4. Braitenberg vehicles as a hand-wired baseline

**Source.** Braitenberg, *Vehicles: Experiments in Synthetic Psychology*, MIT Press 1984 [known, not fetched]. The wiring below is as described by Wikipedia and course notes [secondhand]: https://en.wikipedia.org/wiki/Braitenberg_vehicle. The 3b description in particular comes from lecture slides.

| Vehicle | Wiring | Sign | Behaviour |
|---|---|---|---|
| 2a "fear" | uncrossed (L sensor→L motor) | excitatory | turns away from the source, speeds up near it |
| 2b "aggression" | crossed (L→R motor) | excitatory | turns toward the source, accelerates into it |
| 3a "love" | uncrossed | inhibitory | turns toward the source, slows and comes to rest facing it |
| 3b "explorer" | crossed | inhibitory | turns away from the strongest point, slows near sources; drifts off to other sources |

**Mapping to turn-left / turn-right / forward (suggestion).** Our creature has a discrete action set instead of differential drive. Let d = s_L − s_R for one note:

```
APPROACH (2b/3a analogue):  if d > +τ: turn LEFT;  if d < −τ: turn RIGHT;  else FORWARD
AVOID    (2a/3b analogue):  if d > +τ: turn RIGHT; if d < −τ: turn LEFT;  else FORWARD
```

- Crossed-excitatory and uncrossed-inhibitory both give "turn toward"; the sign only changes speed. With a fixed forward step there is no speed channel, so **2b and 3a collapse into one approach rule, and 2a and 3b into one avoid rule.**
- If you want 3a's "come to rest", add a fourth no-op action, or tie the forward probability to −(s_L + s_R).
- Use a softmax over (d·w) instead of the hard threshold τ, so the baseline is stochastic. This avoids limit cycles where a creature sits exactly between two sources.

**Baseline ladder (suggestion).**

- **B0 Random.** Uniform over the 3 actions.
- **B1 Hand-wired Braitenberg with oracle signs.** Approach A, avoid C, ignore B. This is "the designer knows the answer", and it is the ceiling for a reactive sensor-only policy with no memory.
- **B2 Braitenberg with learned per-note sign.** The policy is a weighted sum over notes, Σᵢ wᵢ·(L_i − R_i), followed by turn left, turn right or forward. Each weight wᵢ is learned from body changes, for example a delta rule: Δwᵢ ∝ (Δenergy − Δtoxin) × recent mean(L_i + R_i). The input is what the creature smelled just before eating.
  - This is the computational skeleton of the worm's ASER→AIY sign-switch story from Q2, with only 3 numbers to learn.
  - **An EBM brain that cannot beat B2 is not yet demonstrating anything beyond valence learning.**
- **B3 B2 plus a klinokinesis term.** Turn probability rises when the valence-weighted sum (s_L + s_R) falls over the last k steps. This is Pierce-Shimomura's rule with a learned valence.

---

## Q5. Metrics from the chemotaxis literature

**Precise definitions.**

1. **Population (endpoint) chemotaxis index.** CI = (N_attractant − N_control)/(N_total, or N_attractant + N_control). Range −1 to +1.
   - Source: the standard worm plate assay [secondhand: vendor and protocol pages, e.g. JoVE https://www.jove.com/t/50069, and a 2022 microPublication, PMC9136590, which gives the ±1 range]. These usually cite Bargmann, Hartwieg & Horvitz 1993 (Cell).
   - I could **not** verify the exact formula in a primary paper.
   - Our version per creature: CI_food/poison = (t_near_food − t_near_poison)/(t_near_food + t_near_poison).
2. **Izquierdo time-averaged distance CI.** CI = (1/T)∫₀ᵀ (1 − h(t)/h(0)) dt, clipped at 0. [full text, PMC3567170]
   - It needs one target and a fixed start distance. It is awkward with many food items on a torus.
3. **Reliability, or reach probability.** The fraction of trials that come within radius r of the target before time T. Izquierdo & Beer use r = 0.1 cm.
4. **Time to target.** First-passage time to within r. **Censor at T** and report survival curves or medians rather than a mean, because a mean over censored data is biased.
5. **Path efficiency, or straightness index.** Shortest distance from start to target divided by the length of the path actually walked, giving a value in (0, 1].
   - Benhamou 2004 (J Theor Biol 229:209-220) [secondhand: description only] says straightness is reliable for directed, goal-oriented paths but not for random-search paths.
   - On our torus, use toroidal shortest distance. Better still, divide **oracle steps (turns included) by agent steps**, since turning costs steps.
6. **Fraction of time within radius.** (1/T)·Σₜ 𝟙[min distance to any food < r]. A matching poison-side version gives exposure.

**Pre-register for v0 (suggestion).**

- **Primary: normalized foraging score.**
  - Raw score = (food eaten − poison eaten) per 1000 steps, or net energy gain per 1000 steps.
  - Normalized: S = (agent − B0 random)/(oracle − B0 random).
  - It is a rate, works with many items and respawning, and has two fixed anchors.
- **Secondary 1: time-to-first-food.** Median with censoring.
- **Secondary 2: poison exposure.** Fraction of steps within r of poison.
- **Secondary 3: path efficiency on isolated single-target trials.** One food, no poison, a fixed start distance, Izquierdo-style. This makes the creature comparable to the chemotaxis literature and separates steering skill from valence learning.
- **Learning curve.** S over time, including the number of steps to reach S = 0.5. This is the actual research quantity.

---

## Q6. The oracle forager: a fair upper bound

**Simple, defensible oracle (suggestion).**

1. **Planning state.** Treat (x, y, heading) as the state. Turns cost one step, so plain Euclidean or BFS distance on (x, y) underestimates the cost.
2. **Cost map.** Run multi-source BFS or Dijkstra over (x, y, heading) on the torus from all current food cells. Edge cost is 1 per action, plus a large penalty for entering any cell where the toxin gain would exceed what eating the target food is worth.
3. **Policy.** Take the first action of the cheapest path. Replan every step, so respawns and eaten items are handled automatically.

This is greedy nearest-food with poison-aware costs. It is cheap: grid size × 4 headings per replan.

**Value iteration** is clean only when the world is static. With items that get eaten, the true state includes which items remain, so the state space explodes. A value iteration on (x, y, heading) against a *fixed* reward map is just the BFS above with discounting. Sutton & Barto, *Reinforcement Learning* (2nd ed., 2018) [known, not fetched] is the standard reference.

**Pitfalls in calling it "optimal".**

1. **Greedy nearest-first is not optimal for multi-item collection.** Choosing the best order of visits is a TSP / orienteering-type problem, and orienteering is known to be NP-hard (Golden, Levy & Vohra 1987) [known, not fetched]. Call it a "strong omniscient heuristic", not an upper bound in the strict sense. Report it as "oracle-greedy".
2. **It is omniscient; the creature is partially observable.** The gap between creature and oracle mixes two things: what is unlearnable from smell alone, and what the creature failed to learn.
   - **Add an intermediate "sensor-limited oracle"**: the B1 hand-wired policy that knows the true valences but sees only the antennae. Then:
     - gap(oracle, B1) is the cost of partial observability;
     - gap(B1, creature) is the cost of not knowing valences or of poor steering.
   - A Bayes-optimal searcher from odour alone is possible in principle (e.g. infotaxis: Vergassola, Villermaux & Shraiman 2007, Nature [known, not fetched]), but it is expensive. Not needed for v0.
3. **Body dynamics.** If eating restores energy with a delay, if toxin decays, or if energy runs out, then "maximize food rate" and "maximize survival" differ. Fix one objective for the oracle that matches the primary metric.
4. **Respawn and stochasticity.** With random respawn, the oracle is optimal only in expectation. Compare on **matched seeds**: the same world RNG streams for oracle, baselines and creature.
5. **Over-tuned penalties.** If the poison penalty in the oracle is tuned until it looks good, it stops being a fixed anchor. Set it once from the body equations and freeze it before running any creature.

---

## Q7. Sensory ecology: is "3 notes, food = A+B, poison = B+C" a good minimal blend design?

**Is there a standard?** I found **no standard minimal attractant/repellent blend paradigm** for chemotaxis models. Searches for larval chemotaxis to binary attractive/aversive mixtures did not turn one up.

**What the *Drosophila* larva literature offers instead.**

- **Single-OSN sufficiency** (Louis et al. 2008 [abstract]; Fishilevich et al. 2005, Curr Biol [secondhand]).
  - Fishilevich et al. also report a combinatorial effect: one OSN that could not drive chemotaxis alone enhanced it when paired with another [secondhand: EPFL record summary].
- **OSNs act as differentiators.** Schulze et al. 2015, eLife 4:e06694, doi:10.7554/eLife.06694 [abstract] find OSNs "act as differentiators that transiently normalize stimulus intensity". High OSN activity suppresses turning; low activity facilitates it. That is the same temporal-derivative encoding again, now at the periphery.

**Lessons on discriminability from the mixture and conditioning literature.**

1. **Elemental versus configural.** Whether a mixture is perceived as its parts or as a new "odour object" depends on the components *and their ratios*. Source: Thomas-Danguin et al. 2014, Front Psychol, doi:10.3389/fpsyg.2014.00504 [abstract]. Specific ratio results in mice and humans are [secondhand, search snippets].
2. **Shared elements raise generalization.** Pearce 1994, Psych Rev, doi:10.1037/0033-295x.101.4.587 [abstract] is the classic configural model of how similarity, including shared elements, affects discrimination learning. The standard test of truly configural learning is **negative patterning**: A+, B+, AB− [known paradigm; the specific insect studies were not fetched].

**Critique of the current design (my analysis).**

- Food = A+B and poison = B+C is **linearly separable on the unique notes alone**. A means food, C means poison, and B carries no identity information.
- A linear sign-learner (B2 above) solves it fully by learning w_A > 0, w_C < 0, w_B ≈ 0. **The blend does not force any configural computation.**
- That is fine for v0, because it tests valence learning plus steering. But do not claim it tests blend discrimination.
- What B *does* do: it is a **shared, ambiguous cue**. Its field is the sum of the food and poison fields. Early learners will chase B, and the speed at which w_B decays to near zero is a nice measurable signal of credit assignment.

**Spatial superposition.** Fields from nearby sources add. Near a food item next to a poison item the creature reads A + 2B + C. The concentration ratio A/C is a more robust identity feature than absolute A, because absolute values also code distance.

**Upgrades if blends should matter later (suggestion).**

- **(i) Ratio-coded.** Food = A:B at 2:1 and poison = A:B at 1:2. Only the ratio tells them apart, which is hard because the ratio changes with superposition.
- **(ii) Negative patterning.** A-only items are food, B-only items are food, A+B items are poison. This requires a nonlinear or configural unit, a clean test for "does the EBM build features?".
- **(iii) Valence reversal mid-life.** Swap which note means food. This is the C. elegans salt-memory analogue and the continual-learning test that note 02 calls the real research.

---

## (a) Recommendations for creature v0

**Sensor encoding**

- Raw per-note readings from the L and R antennae: 6 numbers, plus multiplicative sensor noise. Start at about 5-10% SD and tune so that s/λ ≈ noise at mid-range.
- Log-compress the readings: input = log(c + ε). This gives Weber-like ratio sensitivity, so the L−R difference approximates the fractional gradient. (Design choice, not a literature claim.)
- No pre-computed dC/dt. Give the brain a short input history (k = 3-5 steps) or recurrent state, and let temporal comparison be learned.
- Provide body state (energy, toxin) as an input, and keep it separate as the teaching signal.

**Body / motor**

- Actions: turn left 90° (or 45°), turn right, forward 1 cell. Antennae at forward-left and forward-right of the head, spacing s = 1 cell.
- Eating is automatic on entering a cell.
- Metabolic cost per step. Toxin decays slowly.
- Death or reset at energy 0 or toxin above a threshold. Separate "lives" so learning carries across deaths. This must be stated explicitly.

**World**

- Torus about 48×48 to 64×64.
- Per-note diffusion with decay giving λ ≈ 4-8 cells. Concrete D and k values are to be chosen in simulation.
- About 8 food and 8 poison items, respawning at random positions on consumption.
- Fixed world RNG seeds shared across all agents.
- Fields at steady state: either recompute them on respawn or run a few diffusion substeps per tick.

**Baselines (all on matched seeds)**

- B0 random
- B1 hand-wired Braitenberg with true signs (sensor-limited oracle)
- B2 Braitenberg with learned per-note sign (3-parameter delta rule)
- B3 B2 plus klinokinesis
- Oracle-greedy: (x, y, heading)-BFS with a poison-aware cost, replanning every step

**Metrics to pre-register**

- **Primary:** normalized foraging score S = (agent − B0)/(oracle − B0), with net energy gain per 1000 steps after a fixed learning budget.
- **Secondary:** learning curve of S; median time-to-first-food (censored); poison exposure fraction; path efficiency on single-target trials; final learned weight on the shared note B (expected ≈ 0).
- **Ablations:** one antenna; no history/memory.

**Claim discipline.** With A+B / B+C, claim "valence learning and steering", not "blend discrimination". If the EBM matches B2 but does not exceed it, report that honestly.

---

## (b) Questions for Ahmed

1. **Purpose of note B.** Is it meant to be a distractor, or should the blend demand configural discrimination? If the latter, pick a ratio-coded or negative-patterning design now, because A+B / B+C does not demand it.
2. **Valence over time.** Does valence stay fixed for a whole life, or should it reverse mid-life? Reversal is the continual-learning test and the salt-memory analogue.
3. **Sensor noise.** OK to add it? Without it, two antennae make steering trivial and the oracle-B1 gap collapses.
4. **Own heading.** Is the creature told its heading or position, or only the antennae and body? Telling it anything spatial weakens the honesty of the "only teacher is the body" rule.
5. **Death and learning.** Is death a reset of the world only (learning persists), or a reset of the brain too? This changes what "learning curve" means.
6. **Turn size and stopping.** 90° or 45° turns? Should there be a "stay" action, which Braitenberg 3a "comes to rest" needs?
7. **Primary metric.** Net energy rate (foraging) or survival time? The oracle must optimize the same thing, so this needs a single answer before anything is pre-registered.
8. **Compute budget per run.** Steps per lifetime and number of seeds. This sets whether the learning-curve metric is affordable at, say, 10 seeds × 3 baselines.
