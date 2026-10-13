# 01 - EBMs, Sleep, and Growing Networks: Literature Map

**Written:** 2026-10-13
**Purpose:** ground the EBM lab idea in real prior work, then turn it into a ladder of tiny experiments.

**The idea, in Ahmed's words:**
> "a small neural network made out of smaller pretrained energy based models that has one job that is to make connections, each connection makes another connection and each pattern of connection does an action, each action and connection gets cached and each small model gets retrained again at sleep for the morning and it grows over generations."

**Compute budget:** laptop CPU (numpy, PyTorch optional) plus one GPU box. Everything below is chosen to run on the laptop first.

---

## How to read the citations

- **[seen]** = I opened the paper's page or saw its abstract/listing in a search result this session (arXiv, journal, PubMed, or author page). Details like volume/pages came from those listings.
- **[secondhand]** = I only saw it described by other sources (reviews, blogs, citing papers). Treat details as unconfirmed.
- **[book]** = a classic book I did not check online. The citation is standard, but I did not open a page for it.
- I did not invent any numbers. The few numbers given are quoted from an abstract I saw, and marked.

---

## Part 1 - Energy-based model foundations

### 1.1 The core frame: LeCun et al. 2006

**Source:** LeCun, Chopra, Hadsell, Ranzato, Huang (2006), "A Tutorial on Energy-Based Learning," chapter in *Predicting Structured Data* (MIT Press). PDF: https://cs.nyu.edu/~yann/2011f-G22-2565-001/diglib/lecun-06.pdf **[seen]**

**Plain idea:** an EBM gives every configuration (input + answer) one number, the **energy**. Low energy = "these fit together." **Inference** = search for the answer with the lowest energy. **Learning** = reshape the energy surface so right answers sit lower than wrong ones. You don't need a normalised probability, which skips the hardest integral in probabilistic models.

**Why it matters for you:** your "connection" can literally be an energy. Two units/models are "connected" when their joint state has low energy. "Making a connection" = carving a new low-energy valley.

**Smallest experiment:** 2D toy. Write `E(x, y) = (y - w*x)^2` style energies by hand. Then train a tiny MLP energy `E(x, y)` on a ring-shaped 2D dataset, push data energy down and random-point energy up (with a margin). Plot the energy surface as a heatmap.

### 1.2 Hopfield networks (1982) and the "dreaming" fix

**Sources:**
- Hopfield (1982), "Neural networks and physical systems with emergent collective computational abilities," *PNAS* 79(8):2554-2558. https://pmc.ncbi.nlm.nih.gov/articles/PMC346238/ **[seen]**
- Fachechi, Agliari, Barra (2019), "Dreaming neural networks: forgetting spurious memories and reinforcing pure ones," *Neural Networks* 112:24-40. arXiv:1810.12217 **[seen]**

**Plain idea:** binary neurons, symmetric weights set by a Hebbian rule (outer products of stored patterns). The network has an energy function; each update can only lower it, so it rolls downhill into a stored memory. Give it half a pattern and it **completes** it (content-addressable memory). Weak spot: learning also creates **spurious** valleys (mixtures of memories), and capacity is limited. Fachechi et al.'s abstract puts standard Hopfield capacity at about 0.14 patterns per neuron, and reports that an offline "sleep" phase that removes spurious states can push this to the theoretical bound of 1 for symmetric networks. (Numbers quoted from their abstract.)

**Why it matters for you:** this is the **simplest possible "small EBM"**, and it already has a built-in reason to sleep. It is your atom.

**Smallest experiment:** 100 neurons, store 5-20 random ±1 patterns, corrupt 20% of bits, run updates, measure recall. Plot recall vs number of stored patterns; you will see it break. ~40 lines of numpy.

### 1.3 Modern Hopfield networks / dense associative memory

**Sources:**
- Krotov & Hopfield (2016), "Dense Associative Memory for Pattern Recognition," arXiv:1606.01164 **[seen]** (NeurIPS 2016, venue from memory, not checked)
- Ramsauer et al. (2020), "Hopfield Networks is All You Need," arXiv:2008.02217 **[seen]**
- Krotov, Hoover, Ram, Pham (2025), "Modern Methods in Associative Memory," arXiv:2507.06211, ICML 2025 tutorial with coding notebooks (tutorial.amemory.net, github bhoov/amtutorial) **[seen]**

**Plain idea:** swap the quadratic energy for a sharper one (higher-order polynomial, or exponential/log-sum-exp). Valleys become steeper and more separated, so the network stores **far more patterns than it has neurons** (Krotov & Hopfield's abstract). Ramsauer et al. show a continuous version whose one-step update is **the same maths as transformer attention** and say it can store exponentially many patterns.

**Why it matters for you:** a modern Hopfield layer is a **cache with retrieval built in**. "Each action and connection gets cached" maps directly onto "add a row to the memory matrix; retrieval is one softmax."

**Smallest experiment:** store 200 MNIST digits (or random vectors) in a 64-dim modern Hopfield memory: `new_state = X.T @ softmax(beta * X @ state)`. Compare recall against the classical net at the same size. Sweep `beta` to watch it move from "blend everything" to "snap to one memory."

### 1.4 RBMs and contrastive divergence (Hinton 2002)

**Source:** Hinton (2002), "Training Products of Experts by Minimizing Contrastive Divergence," *Neural Computation* 14(8):1771-1800. https://www.cs.utoronto.ca/~hinton/absps/nccd.pdf **[seen]**

**Plain idea:** an RBM is an EBM with a visible layer and a hidden layer, no links inside a layer. Exact maximum-likelihood training needs the gradient of the normaliser, which is intractable. **CD** approximates it: start a short Markov chain at a real data point, run 1 step, and use "data stats minus 1-step-reconstruction stats" as the update. The paper frames it as training a **product of experts**: many small models multiplied together, each vetoing what it dislikes.

**Why it matters for you:** "a network made of smaller EBMs" is very close to a **product of experts**. Energies of independent experts just **add**. This is the cleanest mathematical definition of "composing small EBMs."

**Smallest experiment:** binary RBM on 8x8 sklearn digits (bundled, no download), 64 visible / 32 hidden, CD-1 in numpy. Show reconstructions and "fantasy" samples from long Gibbs chains.

### 1.5 Deep EBMs trained with Langevin sampling (Du & Mordatch 2019) and JEM (Grathwohl 2019)

**Sources:**
- Du & Mordatch (2019), "Implicit Generation and Generalization in Energy-Based Models" (later titled "...Modeling with..."), arXiv:1903.08689, code openai/ebm_code_release **[seen]**
- Grathwohl, Wang, Jacobsen, Duvenaud, Norouzi, Swersky (2019), "Your Classifier is Secretly an Energy Based Model and You Should Treat it Like One," arXiv:1912.03263, ICLR 2020 **[seen]**

**Plain idea:** use a neural net as `E(x)`. Get "negative" samples by **Langevin dynamics**: start from noise (or a replay buffer of old samples), take gradient steps downhill on energy plus noise. Training pushes energy down on data and up on those samples. Du & Mordatch highlight **compositionality** (add energies to combine concepts) and use a **replay buffer** of past samples. JEM reinterprets an ordinary classifier's logits as energies over (x, y), so one net classifies **and** models p(x).

**Why it matters for you:** (a) the replay buffer of negative samples is literally a **cache that gets revisited**; (b) energy addition is how your small models would combine; (c) JEM shows an EBM can **also produce actions/labels**, not just recall.

**Smallest experiment:** 2D "two moons" or 8-Gaussians dataset, 3-layer MLP energy, 20-step Langevin with a replay buffer, PyTorch on CPU. Then train two EBMs on two different datasets and sample from `E1 + E2` to see composition (intersection of the two).

### 1.6 Training without sampling: score matching and NCE

**Sources:**
- Hyvärinen (2005), "Estimation of Non-Normalized Statistical Models by Score Matching," *JMLR* 6:695-709 **[seen]**
- Gutmann & Hyvärinen (2010), "Noise-contrastive estimation: A new estimation principle for unnormalized statistical models," AISTATS 2010; extended in *JMLR* 13:307-361 (2012) **[seen]**

**Plain idea:** two ways to train an energy without ever computing the normaliser. **Score matching** fits the *slope* of the log-density (the gradient field) instead of the density. **NCE** turns density learning into a classifier: "is this real data or noise I generated?" The energy sits inside that classifier.

**Why it matters for you:** sampling (Langevin/Gibbs) is the slow, flaky part of EBMs. On a laptop, NCE is often the **most stable** way to train many small EBMs. Denoising score matching is also the bridge to diffusion models.

**Smallest experiment:** same 2D dataset as 1.5, train once with NCE (noise = a wide Gaussian) and once with denoising score matching. Compare energy heatmaps and training time against the Langevin version. This is a good **control** for all later experiments: "did my fancy method beat plain NCE?"

### 1.7 Learning by local energy relaxation: equilibrium propagation, predictive coding, Forward-Forward

**Sources:**
- Scellier & Bengio (2017), "Equilibrium Propagation: Bridging the Gap between Energy-Based Models and Backpropagation," *Frontiers in Computational Neuroscience* 11:24, arXiv:1602.05179 **[seen]**
- Whittington & Bogacz (2017), "An Approximation of the Error Backpropagation Algorithm in a Predictive Coding Network with Local Hebbian Synaptic Plasticity," *Neural Computation* 29 **[secondhand]** (seen only via citing papers)
- Millidge, Seth, Buckley (2021), "Predictive Coding: a Theoretical and Experimental Review," arXiv:2107.12979 **[seen]**
- Hinton (2022), "The Forward-Forward Algorithm: Some Preliminary Investigations," arXiv:2212.13345 **[seen]**

**Plain idea:**
- **Equilibrium propagation:** let the network settle to a low-energy state (free phase), then **nudge** the output slightly toward the target and let it settle again. The difference between the two settled states gives a local weight update that approximates backprop's gradient. Same circuit for both phases.
- **Predictive coding:** each layer predicts the one below; the total squared prediction error is an energy. Inference = relax activities to reduce it; learning = local Hebbian-style weight change. Whittington & Bogacz showed (per citing papers) this approximates backprop in MLPs.
- **Forward-Forward:** no backward pass. Each layer has a "goodness" (e.g. sum of squared activities), pushed high for real data and low for negative data. Hinton's abstract explicitly calls it a preliminary study on small problems; a later write-up I saw noted reproductions found it hyperparameter-sensitive **[secondhand]**.

**Why it matters for you:** your small models need to learn **locally** (each one retrained on its own at night) without a global backprop through the whole growing graph. These three are the main families of **local, energy-based learning rules**. Forward-Forward's "goodness" is effectively a per-layer energy, so each layer *is* a small EBM.

**Smallest experiment:** Forward-Forward on sklearn 8x8 digits with 2 layers (label one-hot embedded in the input; negatives = wrong label). Compare against a same-size backprop MLP (the control). Optionally: equilibrium propagation on XOR with a 2-4-1 Hopfield-style net.

### 1.8 Energy Transformer and JEPA

**Sources:**
- Hoover, Liang, et al. (2023), "Energy Transformer," arXiv:2302.07253, NeurIPS 2023 (venue per Krotov's post and Semantic Scholar listing) **[seen]**
- LeCun (2022), "A Path Towards Autonomous Machine Intelligence," position paper on OpenReview (forum id BZ5a1r-kVsf) **[secondhand]** - I saw it referenced and summarised, not the OpenReview page itself
- Assran et al. (2023), "Self-Supervised Learning from Images with a Joint-Embedding Predictive Architecture" (I-JEPA), arXiv:2301.08243, CVPR 2023 **[seen]**

**Plain idea:** **Energy Transformer** designs a transformer block so that one forward step is a step of gradient descent on a single global energy (an associative-memory energy), so the whole network is "roll downhill." **JEPA** is LeCun's proposal for world models: don't predict raw pixels, predict the **representation** of the missing part; the energy is the mismatch in representation space. I-JEPA is the concrete image version.

**Why it matters for you:** Energy Transformer shows that "attention = settle in an energy landscape" scales up, so a modern Hopfield cache is not a toy dead end. JEPA gives the right target for "connections": predict the *embedding* of what comes next, not raw data. That keeps small models small.

**Smallest experiment:** skip implementing either at first. Read the Krotov et al. 2025 tutorial notebooks (1.3), which cover the energy view of attention, and run one of them.

### 1.9 Notable 2024-2026 EBM developments (verified to exist)

- **Energy-Based Transformers (EBTs):** Gladstone, Nanduru, Islam, Han, Ha, Chadha, Du, Ji, Li, Iqbal (2025), "Energy-Based Transformers are Scalable Learners and Thinkers," arXiv:2507.02092, also on OpenReview (id ZBj3Qp1bYg); code github.com/alexiglad/EBT **[seen]**. They train a transformer to score (context, candidate prediction) pairs and predict by **gradient descent on the candidate** until energy converges, framed as "System 2 thinking." The OpenReview abstract reports up to 35% faster pretraining scaling and up to 29% inference-time improvement vs a Transformer++ baseline (quoted from the abstract, not checked). This is the paper behind the "EBMs as System 2 thinkers" idea.
- **Modern Methods in Associative Memory** tutorial (Krotov et al. 2025, arXiv:2507.06211) **[seen]** - the best current hands-on entry point for the Hopfield side.
- **Sleep replay follow-up:** Bazhenov & Krishnan, "Not Just After One: Sleep-Inspired Replay Prevents Catastrophic Forgetting After Sequential Tasks," arXiv:2606.08447 (2026) **[seen in search results only, not opened]** - extends the Tadros et al. sleep algorithm (Part 2.5) to several tasks learned before one sleep. That is exactly your "a day of experiences, then one night" setting.

**Why it matters for you:** EBTs are the closest modern cousin of "each pattern of connection does an action": the model *thinks* by settling into a low-energy answer, and it can spend more settling steps on harder inputs.

---

## Part 2 - Sleep and offline consolidation

### 2.1 Wake-sleep (Hinton, Dayan, Frey, Neal 1995)

**Source:** "The wake-sleep algorithm for unsupervised neural networks," *Science* 268:1158-1161 (1995). https://www.cs.toronto.edu/~hinton/absps/ws.htm **[seen]**

**Plain idea:** two sets of weights. **Wake:** real data drives the bottom-up (recognition) path; train the top-down (generative) weights to reconstruct. **Sleep:** the generative path **dreams** samples from the top; train the recognition weights to recover the causes of those dreams. No teacher needed.

**Why it matters for you:** the original "learn by day, train on your own dreams at night" algorithm. It shows sleep can be a *different kind* of training, not just "more of the same data."

**Smallest experiment:** a 2-layer binary Helmholtz machine on 4x4 bars-and-stripes patterns (classic toy). Track how well dreams match the real pattern distribution.

### 2.2 Complementary learning systems (1995, updated 2016)

**Sources:**
- McClelland, McNaughton, O'Reilly (1995), "Why there are complementary learning systems in the hippocampus and neocortex," *Psychological Review* 102(3):419-457 **[seen]**
- Kumaran, Hassabis, McClelland (2016), "What Learning Systems do Intelligent Agents Need? Complementary Learning Systems Theory Updated," *Trends in Cognitive Sciences* 20(7):512-534 **[seen]**

**Plain idea:** the brain uses **two learners**. A fast one (hippocampus) stores individual episodes immediately with little overlap. A slow one (neocortex) learns shared structure gradually. The fast store **replays** episodes into the slow one, **interleaved** with old knowledge, so new learning doesn't wipe old learning. The 2016 update adds: replay can be weighted by goals, and the cortex can learn fast when new info fits existing structure. It also points to DQN's experience replay buffer as a hippocampus analogue.

**Why it matters for you:** this is **the blueprint** for your design. "Each action and connection gets cached" = hippocampus (fast store). "Each small model gets retrained at sleep" = neocortex (slow consolidation). The key lesson: **replay must be interleaved** with old material, or you get catastrophic forgetting.

**Smallest experiment:** see the learning path (step 5): fast modern-Hopfield cache + slow small EBM, compare "sleep with interleaved replay" vs "sleep on today only."

### 2.3 Hippocampal replay (Wilson & McNaughton 1994)

**Source:** Wilson & McNaughton (1994), "Reactivation of hippocampal ensemble memories during sleep," *Science* 265(5172):676-679. https://pubmed.ncbi.nlm.nih.gov/8036517/ **[seen]**

**Plain idea:** place cells that fired together while a rat explored later fired together **more often during the following sleep** than in sleep before the task. Waking experience is re-played offline.

**Why it matters for you:** the biological evidence that "cache today, replay tonight" is a real mechanism, not just a metaphor.

**Smallest experiment:** none needed by itself; it is the motivation for experiments 4-6.

### 2.4 Synaptic homeostasis (Tononi & Cirelli)

**Source:** Tononi & Cirelli (2014), "Sleep and the price of plasticity: from synaptic and cellular homeostasis to memory consolidation and integration," *Neuron* 81:12-34 **[seen via PMC listing and lab page]**

**Plain idea:** waking learning mostly **strengthens** synapses; that is costly and makes everything noisier and saturated. Sleep **downscales** connections overall, keeping the relatively strong ones and pruning weak ones, restoring signal-to-noise.

**Why it matters for you:** your system "grows connections" all day. Without a nightly **downscale + prune**, it will saturate (everything connected to everything = no information). This gives you a principled pruning rule for sleep.

**Smallest experiment:** in a growing Hebbian net, add a nightly step `W *= 0.8; W[abs(W) < threshold] = 0`. Compare recall and connection count over 30 "days" with vs without it.

### 2.5 Sleep-like replay in ANNs (Tadros et al. 2022)

**Source:** Tadros, Krishnan, Ramyaa, Bazhenov (2022), "Sleep-like unsupervised replay reduces catastrophic forgetting in artificial neural networks," *Nature Communications* 13:7742. https://www.nature.com/articles/s41467-022-34938-7 **[seen]**

**Plain idea:** after training on a new task, convert the network to a spiking-like mode, drive it with **random input**, and apply **local Hebbian** up/down weight changes ("Sleep Replay Consolidation", SRC). Old-task performance comes back. The paper reports that sleep made representations of different classes **decorrelated and sparser**, and that sleep worked both by boosting old-task connections and weakening the most recent task's. It needs no stored data, only basic input statistics. It also notes that their sleep is "likely oversimplified."

**Why it matters for you:** the closest published match to "each small model gets retrained at sleep." It shows sleep can be **unsupervised and local**, and it shows a cost: the newest task can lose a bit of performance.

**Smallest experiment:** 2-layer MLP, split-MNIST (or sklearn digits) into tasks {0,1} then {2,3}. Train task 1, train task 2, measure task-1 forgetting. Add a simplified sleep: random input, threshold activations, Hebbian increase on co-active pairs and decrease otherwise. Control: same number of "sleep" steps with random weight noise instead.

### 2.6 Dreaming as unlearning (Crick & Mitchison 1983; Hopfield, Feinstein, Palmer 1983)

**Sources:**
- Crick & Mitchison (1983), "The function of dream sleep," *Nature* 304:111-114. https://pubmed.ncbi.nlm.nih.gov/6866101/ **[seen]**
- Hopfield, Feinstein, Palmer (1983), "'Unlearning' has a stabilizing effect in collective memories," *Nature* 304:158-159, doi 10.1038/304158a0 **[seen]**

**Plain idea:** Crick & Mitchison proposed REM sleep **removes unwanted modes** by reverse learning. Hopfield et al. tested it in a Hopfield net: start from noise, let the net settle, then apply the Hebbian rule with a **negative sign** to wherever it landed. Spurious memories get weakened and real ones become easier to reach.

**Why it matters for you:** in an EBM, "dreaming" has a precise meaning: **sample from your own energy and push up on what you find**. That is the same "push up on negatives" step used in CD (1.4) and Langevin EBM training (1.5). So **sleep = the negative phase of EBM training**, run offline. This is the single most important link for your idea.

**Smallest experiment:** Hopfield net from 1.2, stored past capacity. Night: 200 dreams (random start, settle, `W -= eps * outer(s, s)`). Measure recall before/after and count spurious attractors. Sweep `eps`; too much unlearning erases real memories too (Fachechi et al. study exactly this trade-off).

### 2.7 Generative replay (Shin et al. 2017; van de Ven et al. 2020)

**Sources:**
- Shin, Lee, Kim, Kim (2017), "Continual Learning with Deep Generative Replay," arXiv:1705.08690, NeurIPS 2017 **[seen]**
- van de Ven, Siegelmann, Tolias (2020), "Brain-inspired replay for continual learning with artificial neural networks," *Nature Communications* 11, doi 10.1038/s41467-020-17866-2 **[seen]**

**Plain idea:** instead of storing old data, keep a **generator** that can produce samples like old tasks, and mix those samples into training on new tasks (Shin et al.: a "generator + solver" pair). van de Ven et al. replay **internal representations** produced by the network's own feedback connections rather than raw inputs, which scaled better.

**Why it matters for you:** an EBM **is** a generator (sample by settling). So each small EBM can produce its own replay at night, and your cache doesn't have to keep everything forever.

**Smallest experiment:** in experiment 1.5's setup, train EBM on dataset A, then B. Variant 1: train on B only. Variant 2: mix in Langevin samples from the A-trained model. Measure energy assigned to held-out A points.

### 2.8 Catastrophic forgetting and EWC (Kirkpatrick et al. 2017)

**Source:** Kirkpatrick et al. (2017), "Overcoming catastrophic forgetting in neural networks," *PNAS*, doi 10.1073/pnas.1611835114, arXiv:1612.00796 **[seen]**

**Plain idea:** after a task, estimate how important each weight was (via the Fisher information). When learning a new task, add a spring-like penalty that **slows learning on important weights** instead of freezing them.

**Why it matters for you:** EWC is the standard **non-replay baseline**. If "sleep" doesn't beat a simple EWC penalty, it isn't earning its keep. It is also cheap enough to run on a laptop.

**Smallest experiment:** the split-digits setup from 2.5, add EWC. Report it next to "no protection," "replay," and "sleep."

---

## Part 3 - Growing and self-assembling networks

### 3.1 Hebbian learning, cell assemblies, assembly calculus

**Sources:**
- Hebb (1949), *The Organization of Behavior* **[book]**
- Papadimitriou, Vempala, Mitropolsky, Collins, Maass (2020), "Brain computation by assemblies of neurons," *PNAS*, doi 10.1073/pnas.2001893117 **[seen]**

**Plain idea:** "cells that fire together wire together." Groups of neurons that repeatedly co-fire become a **cell assembly**, a unit standing for one concept. Papadimitriou et al. formalise this as the **assembly calculus**: random sparse connectivity + Hebbian plasticity + a "top-k neurons fire" rule gives operations like **project** (copy an assembly into another area), **associate**, and **merge**.

**Why it matters for you:** "each connection makes another connection" is basically **project/associate/merge**. Assemblies are your best candidate for "a pattern of connection," and the operations are defined precisely enough to code.

**Smallest experiment:** two "areas" of 1000 neurons, random 5% connectivity, top-k = 50 firing, Hebbian `W[i,j] *= (1+beta)` when j fires then i. Repeatedly project a fixed stimulus from area A into area B and measure whether the winning set in B **stabilises** (overlap across rounds). Pure numpy.

### 3.2 NEAT and HyperNEAT

**Sources:**
- Stanley & Miikkulainen (2002), "Evolving Neural Networks through Augmenting Topologies," *Evolutionary Computation* 10(2):99-127 **[secondhand]** (details from Wikipedia and the UT group page)
- Stanley, D'Ambrosio, Gauci (2009), "A Hypercube-Based Encoding for Evolving Large-Scale Neural Networks," *Artificial Life* 15(2):185-212 **[secondhand]**

**Plain idea:** evolve the **structure** of networks, not just weights. NEAT starts from **minimal** networks and adds nodes and connections by mutation. It uses historical markings to cross over different topologies and **speciation** to protect new structures until they get good. HyperNEAT evolves a small pattern-generating network that *paints* the weights of a large one, so big networks with regular structure can evolve.

**Why it matters for you:** "it grows over generations" is exactly NEAT's setting. Two lessons carry over directly: **start minimal**, and **protect new structure** for a while (new connections are bad at first and would be pruned too early).

**Smallest experiment:** use the `neat-python` package on XOR or CartPole (gymnasium). Log genome size per generation to see complexification. (I did not check the package version; verify before installing.)

### 3.3 Neural cellular automata (Mordvintsev et al. 2020)

**Source:** Mordvintsev, Randazzo, Niklasson, Levin (2020), "Growing Neural Cellular Automata," *Distill*, distill.pub/2020/growing-ca/ **[secondhand]** (metadata and architecture from search results and citing papers)

**Plain idea:** every pixel runs the **same tiny neural net**, reading only its neighbours. Trained end-to-end, the grid grows a target image from one seed cell and, when trained with damage, **regrows** it after being cut. Each cell has visible RGBA channels plus hidden channels.

**Why it matters for you:** proof that **many copies of one small local model** can build and repair a global structure. It is a strong example of "growth" coming from repeated local rules rather than a central planner.

**Smallest experiment:** the official Colab runs on CPU slowly and GPU fast. A 32x32 emoji target is a good first run on the GPU box.

### 3.4 Growing neural gas (Fritzke 1995)

**Source:** Fritzke (1995), "A Growing Neural Gas Network Learns Topologies," *Advances in NIPS 7* (NIPS 1994 proceedings), pp. 625-632 **[seen]**

**Plain idea:** start with 2 units. For each input, the nearest unit and its neighbours move toward it, and the **two nearest get connected** (Hebb-like). Edges **age** and old ones are deleted. Every N steps, **insert a new unit** where accumulated error is highest. The abstract notes no time-decaying parameters; growth continues until a performance criterion is met.

**Why it matters for you:** the cleanest, most runnable algorithm for **"make connections, grow where needed, prune what's unused."** Each node could be replaced by a small EBM, giving a "growing gas of experts."

**Smallest experiment:** GNG on 2D data (a ring plus a blob). Animate units and edges. ~80 lines of numpy. A great first "growth" demo.

### 3.5 Structural plasticity / sparse evolutionary training

**Source:** Mocanu et al. (2018), "Scalable training of artificial neural networks with adaptive sparse connectivity inspired by network science," *Nature Communications* 9:2383, arXiv:1707.04780 **[seen]**

**Plain idea:** **SET** starts with a sparse random network. After each epoch, it **removes the weakest connections** and **adds the same number of new random ones**. The topology evolves during training. The paper tests it on RBMs (EBMs), MLPs and CNNs.

**Why it matters for you:** this is the simplest working rule for **prune-and-regrow every night**. It was shown on RBMs, so it plugs directly into your small EBMs.

**Smallest experiment:** sparse RBM (10% density) on sklearn digits; after each "night," prune the smallest 20% of weights, regrow 20% at random. Control: same density, fixed random mask.

### 3.6 Networks of small models: mixture of experts, Thousand Brains, Society of Mind

**Sources:**
- Jacobs, Jordan, Nowlan, Hinton (1991), "Adaptive Mixtures of Local Experts," *Neural Computation* 3:79-87 **[seen]**
- Shazeer et al. (2017), "Outrageously Large Neural Networks: The Sparsely-Gated Mixture-of-Experts Layer," arXiv:1701.06538 **[seen]**
- Hawkins, Lewis, Klukas, Purdy, Ahmad (2019), "A Framework for Intelligence and Cortical Function Based on Grid Cells in the Neocortex," *Frontiers in Neural Circuits*, doi 10.3389/fncir.2018.00121 **[seen]**
- Minsky (1986), *The Society of Mind* **[book]**

**Plain idea:**
- **Mixture of experts:** many small networks; a **gating** net decides which expert handles each input; experts specialise automatically. Shazeer et al. made gating **sparse** (only a few experts run per input) to scale capacity.
- **Thousand Brains (Hawkins et al.):** every cortical column is a complete little model of objects with its own reference frame; columns **vote** to reach a consensus.
- **Society of Mind (Minsky):** intelligence emerges from many simple, individually mindless "agents."

**Why it matters for you:** your system **is** a society of small EBMs. Two concrete combining rules exist: **gating** (pick one expert, as in MoE) and **voting/summing energies** (products of experts, Thousand Brains-style consensus). Choose one deliberately; they behave very differently.

**Smallest experiment:** 4 small EBMs on 2D data from 4 clusters. Combine (a) by softmax gating on lowest energy (min-energy wins), (b) by summing energies. Visualise both landscapes. You will see (a) gives a union, (b) gives an intersection.

### 3.7 Open-ended / developmental learning

**Sources:**
- Wang, Lehman, Clune, Stanley (2019), "Paired Open-Ended Trailblazer (POET)," arXiv:1901.01753 **[seen]**
- Hughes et al. (2024), "Position: Open-Endedness is Essential for Artificial Superhuman Intelligence," ICML 2024, PMLR 235, arXiv:2406.04268 **[seen]**

**Plain idea:** instead of one fixed task, the system keeps generating **new challenges** and solutions; solutions that work elsewhere are transferred as stepping stones (POET). Hughes et al. define open-endedness as continuing to produce artefacts that are both **novel** and **learnable** to an observer.

**Why it matters for you:** "grows over generations" needs a reason to grow. Without new challenges, growth stalls or bloats. Hughes et al.'s "novel + learnable" gives you a **measurable** test of whether your system is actually developing.

**Smallest experiment:** a curriculum toy: the world presents patterns of increasing length/complexity only once the current ones are recalled reliably. Track how many "levels" the system reaches with and without growth.

---

## Part 4 - How the pieces could fit Ahmed's idea

> **This section is my synthesis.** Nobody has published this exact system. The mapping below is a design hypothesis, built from the sources above.

### Mapping each phrase to a mechanism

| Ahmed's phrase | Closest real mechanism | Source |
|---|---|---|
| "smaller pretrained energy based models" | small Hopfield/RBM/MLP-energy units; combine by **adding energies** | Hinton 2002 (products of experts); Du & Mordatch 2019 (composition) |
| "one job: make connections" | Hebbian links between units; assembly **project/associate/merge** | Hebb 1949; Papadimitriou et al. 2020 |
| "each connection makes another connection" | co-active assemblies spawn a new linking assembly (merge); GNG edge creation | Papadimitriou et al. 2020; Fritzke 1995 |
| "each pattern of connection does an action" | a settled low-energy state is read out as an action (energy minimisation = decision) | LeCun et al. 2006; Grathwohl 2019 (JEM); Gladstone 2025 (EBTs) |
| "each action and connection gets cached" | fast episodic store = modern Hopfield memory / replay buffer | Ramsauer 2020; McClelland et al. 1995 (CLS) |
| "retrained again at sleep for the morning" | offline consolidation: interleaved replay + dreaming (negative phase) + downscaling | CLS; Hopfield et al. 1983; Tadros 2022; Tononi & Cirelli 2014 |
| "grows over generations" | add units where error is high, prune weak links, protect new structure | Fritzke 1995; Mocanu 2018; Stanley & Miikkulainen 2002 |

### The key insight to build around

**Sleep is the negative phase.** Every EBM needs two forces: pull energy **down** on real data, push energy **up** on the model's own fantasies. Usually both happen in the same training step. Your design can split them across the day:
- **Day (wake):** see the world, cache episodes (fast store), lower energy on what was seen. Cheap, Hebbian, positive-only.
- **Night (sleep):** (1) **replay** cached episodes interleaved with old ones into the slow small EBMs (CLS); (2) **dream**: sample from each EBM's own energy and push up on what it finds, which removes spurious valleys (Hopfield 1983, wake-sleep, CD); (3) **downscale and prune** (SHY, SET); (4) **grow** a new unit where the day's error was highest (GNG).

This is honest to the literature: wake-sleep, CD and unlearning already show the two phases can be separated, at least in small systems. Whether it keeps working as the system grows is the open question your lab would actually test.

### Honest risks

- **EBM training is unstable.** Langevin-trained EBMs are known to be finicky. Start with Hopfield/RBM-style units and NCE before deep EBMs.
- **Growth without pressure becomes bloat.** NEAT and GNG both grow because of an error signal. You need a measurable error ("what failed today") to decide where to grow.
- **Sleep can hurt the newest memory.** Tadros et al. saw recent-task drops. Measure new and old memories separately.
- **"It grows" is not a result.** The result is: *the grown system does better on a fixed held-out test than a same-size network that didn't grow*.

### Suggested learning path (8 tiny experiments)

Each step reuses the previous one. All run on laptop CPU unless marked.

1. **Classical Hopfield net (numpy).**
   - **Teaches:** energy, settling, attractors, pattern completion, capacity limit.
   - **Control/null:** recall from an **untrained** (random symmetric) weight matrix; and "just return the corrupted input." Plot recall vs patterns stored.

2. **Dreaming / unlearning in that Hopfield net.**
   - **Teaches:** sleep as the negative phase; spurious attractors; over-unlearning.
   - **Control/null:** same number of night steps applying **random** weight noise of matched size; and "no night." Sweep the unlearning rate.

3. **Modern Hopfield memory as the cache.**
   - **Teaches:** exponential-capacity retrieval, the attention link, the `beta` knob.
   - **Control/null:** classical Hopfield at the same dimension and memory count; and plain nearest-neighbour lookup (a modern Hopfield cache at high `beta` should approach it, so it is the honest baseline).

4. **Tiny EBM on 2D data three ways: Langevin+replay buffer, NCE, denoising score matching (PyTorch CPU).**
   - **Teaches:** practical EBM training, why sampling is the hard part, which method is stable for your future units.
   - **Control/null:** a Gaussian mixture / kernel density estimate fitted to the same data. If your EBM can't beat KDE in 2D, something is wrong.

5. **Two-speed memory with sleep (the CLS core).** Fast modern-Hopfield cache + slow small EBM (or RBM). Days present new pattern sets; nights replay the cache into the slow model.
   - **Teaches:** consolidation, interleaving, catastrophic forgetting.
   - **Control/null:** (a) night trains on **today only** (no interleaving); (b) no sleep, train online during the day; (c) EWC penalty instead of replay. Report old-task and new-task performance separately.

6. **Composing small EBMs: products of experts vs gating.** 4 small pretrained units, combined by summed energy vs min-energy gating.
   - **Teaches:** what "a network made of smaller EBMs" means mathematically; union vs intersection.
   - **Control/null:** one monolithic EBM with the same total parameter count trained on all the data.

7. **Connections that make connections: assembly calculus + actions.** Areas of sparse random neurons with top-k firing and Hebbian links; settled assemblies map to a small set of actions in a gridworld or bandit toy; reward gates which assemblies are strengthened at night.
   - **Teaches:** assemblies as "patterns of connection," project/merge, reading actions out of settled states.
   - **Control/null:** the same architecture with **Hebbian plasticity turned off** (fixed random connections, only the readout learns); and a tabular Q-learning agent on the same toy.

8. **Growth over generations (the full loop, maybe GPU box for long runs).** Day: act and cache. Night: replay + dream + downscale/prune + add one unit where error was highest (GNG rule). Run 50-100 "days" on a curriculum that gets harder only when the current level is mastered.
   - **Teaches:** whether growth+sleep beats a fixed architecture; where it bloats or forgets.
   - **Control/null:** (a) a **fixed-size** system with the final grown size from day 1, given the same days and nights; (b) the growing system with **random** unit insertion instead of error-directed; (c) the growing system with **no sleep**. Use a fixed held-out test set and at least 3 random seeds per condition.

Optional side quests once the ladder works: Forward-Forward or equilibrium propagation as the local night-time learning rule (1.7); a GNG demo (3.4) as a warm-up before step 8; reading the EBT paper (1.9) to see the same "think by settling" idea at scale.

---

## Source list (quick reference)

**Seen this session (search listing or abstract):**
- LeCun et al. 2006 tutorial - cs.nyu.edu/~yann/2011f-G22-2565-001/diglib/lecun-06.pdf
- Hopfield 1982 - PNAS 79(8):2554, PMC346238
- Krotov & Hopfield 2016 - arXiv:1606.01164
- Ramsauer et al. 2020 - arXiv:2008.02217
- Krotov, Hoover, Ram, Pham 2025 - arXiv:2507.06211
- Hinton 2002 - Neural Computation 14(8):1771
- Du & Mordatch 2019 - arXiv:1903.08689
- Grathwohl et al. 2019 - arXiv:1912.03263
- Hyvärinen 2005 - JMLR 6:695
- Gutmann & Hyvärinen 2010 (AISTATS) / 2012 (JMLR 13:307)
- Scellier & Bengio 2017 - arXiv:1602.05179, Front. Comput. Neurosci. 11:24
- Millidge, Seth, Buckley 2021 - arXiv:2107.12979
- Hinton 2022 Forward-Forward - arXiv:2212.13345
- Hoover et al. 2023 Energy Transformer - arXiv:2302.07253
- Assran et al. 2023 I-JEPA - arXiv:2301.08243
- Gladstone et al. 2025 EBTs - arXiv:2507.02092
- Hinton, Dayan, Frey, Neal 1995 - Science 268:1158
- McClelland, McNaughton, O'Reilly 1995 - Psych. Review 102(3):419
- Kumaran, Hassabis, McClelland 2016 - TICS 20(7):512
- Wilson & McNaughton 1994 - Science 265:676
- Tononi & Cirelli 2014 - Neuron 81:12
- Tadros et al. 2022 - Nat. Commun. 13:7742
- Crick & Mitchison 1983 - Nature 304:111
- Hopfield, Feinstein, Palmer 1983 - Nature 304:158
- Fachechi, Agliari, Barra 2019 - Neural Networks 112:24, arXiv:1810.12217
- Shin et al. 2017 - arXiv:1705.08690
- van de Ven, Siegelmann, Tolias 2020 - Nat. Commun. 11, doi 10.1038/s41467-020-17866-2
- Kirkpatrick et al. 2017 - arXiv:1612.00796, PNAS
- Papadimitriou et al. 2020 - PNAS, doi 10.1073/pnas.2001893117
- Fritzke 1995 - NIPS 7, pp. 625-632
- Mocanu et al. 2018 - Nat. Commun. 9:2383
- Jacobs et al. 1991 - Neural Computation 3:79
- Shazeer et al. 2017 - arXiv:1701.06538
- Hawkins et al. 2019 - Front. Neural Circuits, doi 10.3389/fncir.2018.00121
- Wang et al. 2019 POET - arXiv:1901.01753
- Hughes et al. 2024 - arXiv:2406.04268

**Secondhand only:** Whittington & Bogacz 2017; LeCun 2022 position paper (OpenReview page not opened); Stanley & Miikkulainen 2002 and Stanley et al. 2009 (details via Wikipedia/group page); Mordvintsev et al. 2020 Distill (metadata via search/citing papers); Bazhenov & Krishnan 2026 arXiv:2606.08447 (title/abstract excerpt in search only); the Forward-Forward reproducibility remark.

**Books, not checked online:** Hebb 1949; Minsky 1986.
