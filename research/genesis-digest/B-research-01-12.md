# Genesis digest B: research reports 01-12

Source: `/home/abied/genesis-archive/docs/research/01-*.md` to `12-*.md`, each read in full (read-only).
Citations are `file:line`. All twelve are **design proposals** written against Genesis v0 code (`~/.forge/genesis`). "Genesis decided" below means what the report recommended or ruled. Whether each proposal actually shipped is outside this slice. One sign that the plans moved after they were written: report 11 proposes one canonical genome layout (G=65, `11:97-107`), but report 12 later says "Wave D leaves G=48" and puts its own genes at 48-49 (`12:73`).

The reports share three Genesis-wide rules. Each one transfers directly to the EBM lab:
- **HOUSE LAW:** an emotion is a continuous scalar and an attractor region, never a label or enum below the analysis layer (`02:282-288`, `04:3-7`, `04:282-291`).
- **Mediation law:** agents interact only through shared fields, with no direct agent-to-agent calls (`06:133-134`, `07:35`, `12:149-160`).
- **Curves, not vibes:** every mechanism comes with falsifiers stated in advance (`05:77`, `05:94`).

---

## 1. Per-report abstracts

### 01 - Pain as the primal instinct (`01-pain-instinct.md`)
**What it researched:** why pain exists, and how it is architected as a fast reflex plus slower learning.
- **Smoke-detector principle:** defend whenever `p(danger) > C_response/C_damage`. This guarantees many false alarms (Nesse 2001; 2019), and it generalizes to error-management theory (Haselton & Buss 2000) (`01:7`).
- **Loss aversion λ≈2.25** (Tversky & Kahneman 1992) is flagged **contested**. Walasek, Mullett & Stewart (2024) find 1.0-1.5 (`01:7`).
- **Pain is a priority interrupt,** not one bid among others: Eccleston & Crombez 1999, and Sloman & Croucher's 1981 "insistence" (`01:9`).
- **Stress cuts both ways:** acute stress causes analgesia (Butler & Finn 2009), while chronic load causes sensitization (Woolf 2011). The chronic side is flagged as less predictable (`01:11`).
- **Pain is not one of Panksepp's seven systems.** It sits underneath them (`01:13`).
- **Computational precedents:**
  - Man & Damasio 2019: homeostasis as the meta-goal.
  - Keramati & Gutkin 2014: homeostatic RL.
  - Seymour 2019: pain as a precision signal.
  - Mahajan, Dayan & Seymour 2025.
  - Elfwing & Seymour 2017 (MaxPain): separate reward and punishment streams.
  - Maass et al. 2026, "Evolving Afferent Architectures": sensors with gain, threshold and decay, evolved in an outer loop by CMA-ES and used by lifetime RL in an inner loop (`01:15`).

**Decided:**
- A new L2.5 INSTINCT stage. A leaky-integrator `pain` signal drives a reflex FLEE act that **bypasses argmax** (`01:19-45`).
- The reflex threshold is raised by `stress` and lowered by `load` (`01:41`).
- Roth-Erev place-aversion with eligibility traces and continuous extinction (`01:46`).
- Four genes: threshold, gain, decay and analgesia (`01:55-64`).
- Prediction: the threshold evolves toward the low end (`01:66`).

**Traps:**
- Folding pain into the utility competition (`01:88`).
- `load` never decays, so the report adds a recovery term (`01:53`, `01:90`).
- Aversions that never forget (`01:94`).
- Calling it suffering (`01:96`).

### 02 - Instinct layer and drive arbitration (`02-drive-hierarchy.md`)
**What it researched:** classical drive theory and how competing drives get arbitrated.
- **Hull (1943) and Lorenz's hydraulic model (1950) were discredited.** Lorenz's model had no feedback path. Tinbergen's (1951) hierarchy with asymmetric inhibition survived (`02:5-24`).
- **Keramati & Gutkin (2014)** define drive as a norm of setpoint deviation, `D(H)=Σ|h*−h|^(n/m)`, with reward as the drop in D. With nonlinear exponents, a large deficit suppresses the value of fixing other needs, for free (`02:26-33`).
- **Allostasis and interoception:** Sterling 2012 (regulation by prediction) and Barrett & Simmons 2015 (interoceptive prediction) (`02:33-37`).
- **Panksepp's cross-couplings are flagged contested,** per Davis & Montag 2019 (`02:39-49`).
- **Common value currency:** Padoa-Schioppa & Assad 2006 and Levy & Glimcher 2012. The anatomical claim is contested (`02:51-57`).
- **Pure winner-take-all causes "dithering"** (Tyrrell 1993). Fixes in the literature:
  - Positive feedback on the active state (Houston & Sumida 1985).
  - Opportunistic interrupts (Spier & McFarland 1997).
  - Centralized persistent selection (Redgrave, Prescott & Gurney 1999).
  (`02:57-75`)
- **Tonic vs phasic gain:** Aston-Jones & Cohen 2005 (LC-NE) and Niv et al. 2007 (tonic dopamine) (`02:77-87`).

**Decided:** a two-level frame.
- **Level 1:** stateless instinct pressures `p` in [0,1] (`02:96-114`).
- **Level 2:** slow leaky-integrator sub-drives `s` with genome coupling matrices `Wps` and `Wss` (`02:116-140`).
- **Gain and bias:** motivation acts as a *multiplicative gain* and mood as an *additive bias*, so a miserable agent still drinks (`02:142-167`).
- **Anti-dithering:** a Schmitt-trigger bonus `h` plus a commitment window, with a fixed, non-evolvable emergency override `P_CRIT=0.90` (`02:176-206`).
- **30 genes,** with clear genome-vs-physics rules (`02:208-218`).

### 03 - Motivation as an evolved sub-drive (`03-motivation.md`)
**What it researched:** vigor, wanting, and curiosity as one evolvable motivation variable.
- **Citation fix:** the seed citation is corrected to Niv, Daw, Joel & Dayan 2007 (four authors) (`03:5-12`).
- **Vigor formula:** opportunity-cost Bellman equation with optimal rate `1/τ̂=√(r̄/Kv)`. The claim that tonic dopamine equals r̄ is hedged by its own authors (`03:14-38`).
- **Wanting is separate from liking:** Berridge & Robinson 1998, Berridge 2007. SEEKING (Panksepp 1998; Alcaro et al. 2021) bundles vigor and curiosity (`03:40-52`).
- **Effort discounting:** EEfRT (Treadway et al. 2009) and the three-component apathy model (Le Heron et al. 2018) (`03:52-58`).
- **Curiosity:**
  - Learning progress `LP=⟨E(t+1)⟩−⟨E(t)⟩` (Oudeyer, Kaplan & Hafner 2007).
  - Singh, Lewis, Barto & Sorg 2010: an evolutionary search over reward functions found that the best reward is **not fitness**. It adds an inverse-recency bonus `1−1/c`, and curiosity is +0.5 when sated vs −0.01 to −0.05 when hungry (their Table I).
  - Schmidhuber 2010: compression progress.
  (`03:60-82`)
- **r̄ is learned incrementally** (Constantino & Daw 2015) (`03:93-95`).

**Decided:**
- One scalar `m`, an EMA of payoff, where payoff is the drop in summed deficits plus Δbond (`03:104-137`).
- Outputs: a penalty on rest, cheaper movement, and a curiosity bonus on explore gated by `(1−stress)` (`03:140-155`).
- Five genes, including a separate vigor output gain justified by wanting/liking separability (`03:162-177`).

**Trap:** argmax is invariant to uniform scaling, so "multiply all utilities by m" silently does nothing (`03:229-233`).

### 04 - Depression as an evolved sub-drive (`04-depression.md`)
**What it researched:** five functional theories of low mood, plus dynamical models of how mood gets trapped.
- **Disengagement** (Nesse 2000) (`04:14-21`).
- **Rank and defeat theory,** plus entrapment (Price et al. 1994; Gilbert & Allan 1998; Allen & Badcock 2003) (`04:23-32`).
- **Analytic rumination is CONTESTED** (Andrews & Thomson 2009, vs Yarkoni 2010) (`04:34-42`).
- **Sickness behavior** (Miller & Raison 2016) (`04:44-50`).
- **Learned helplessness, revised:** passivity is the default, and what gets learned is *control* (Maier & Seligman 2016) (`04:52-59`).
- **Dynamics:**
  - Critical slowing down (van de Leemput 2014). Contested by Bos & de Jonge 2014.
  - Bistable HPA toggle (Mizrachi 2023).
  - Ising symptom network with hysteresis (Cramer 2016).
  - Mood as an EMA of reward-prediction errors (Eldar et al. 2016).
  (`04:61-75`)
- **When low mood is adaptive:** a state-dependent optimum (Nettle 2009; Trimmer et al. 2013), and hysteresis from belief lag (Trimmer et al. 2015) (`04:77-88`).

**Decided:**
- A cubic bistable update, `d = gain·g(1−g)(g−θ) − exit·g`, with derived saddle-node bounds. Because the gain-to-exit ratio is a gene, **whether the trap exists at all is evolvable** (`04:127-148`).
- Three separate input channels: low vigor, defeat (unrequited courtship), and sickness (`04:114-166`).
- Act damping split into deficit acts and discretionary acts, with no `if` branch anywhere (`04:168-187`).

**M2 forward note:** gloom could raise the learning rate for *offline model-fitting*. This is flagged and should be built only if a sweep supports it (`04:198-203`).

**Trap:** an absorbing state if `load` stays unbounded (`04:273-280`).

### 05 - Renewable vs finite resource ecology (`05-resource-ecology.md`)
**What it researched:** harvesting dynamics, collapse models, and commons governance.
- **Harvesting:** Gordon/Schaefer: under open access, overharvest is the equilibrium. Free et al. 2025: collapse can come from adaptive behavior alone (`05:7`).
- **Regrowth form matters:** Sugarscape, and Perolat 2017's local regrowth (`05:9`).
- **Brander & Taylor 1998:** the regrowth rate `r` decides whether a population cycles or settles (`05:13`).
- **HANDY is contested:** Akhavan & Yorke 2019 show collapse is definitional (`05:15`). Tainter is also contested (`05:17`).
- **Commons:** Ostrom 1990's design principles. Ostrom, Walker & Gardner 1992: cheap talk alone raises cooperation (`05:23-25`).
- **Perolat et al. 2017** see naivety → tragedy → maturity. Exclusion restores sustainability but at an inequality cost (`05:27`).
- **Inequality depends on which wealth type is heritable** (Borgerhoff Mulder 2009) (`05:33`).
- **Distributions:** ideal free vs despotic (Fretwell & Lucas 1969; Fretwell 1972), and risk-sensitive foraging (Caraco) (`05:37`).

**Decided:**
- Finite, non-regrowing **salt licks** that gate gestation, chosen over minerals and shelter (`05:47-49`).
- Salt must be a *felt* utility, not only a silent precondition (`05:90`).

### 06 - Resource distribution, mating systems, social structure (`06-resources-social.md`)
**What it researched:** how ecology shapes mating systems, territory, sharing and conflict.
- **Mating systems:** Emlen & Oring 1977 (EPP), formalized as `I_s` (Shuster & Wade 2003; Crow, Wade, Arnold & Wade) (`06:8-20`).
- **Territory:** Brown 1964 (defendability). The polygyny threshold is **contested** (`06:22-36`).
- **Reproductive skew** (Vehrencamp 1983). Contested per a 2023 review (`06:38-50`).
- **Sharing:** risk-pooling vs tolerated theft vs show-off. All **contested** (`06:52-66`).
- **Contests:** Hawk-Dove, RHP, and the bourgeois convention (Maynard Smith & Price 1973; Parker 1974; Davies 1978) (`06:67-75`).
- **Bateman's founding data is discredited** (Snyder & Gowaty 2007; Gowaty et al. 2012-13), but the statistics are retained (`06:86-94`).

**Decided:**
- A territory **claim field** with slow decay (`06:109-134`).
- A contest rule that filters movement instead of adding an act (`06:136-151`).
- A `give` act gated by dyadic `known_bond` (`06:153-180`).
- **Anti-cheater rule:** a received gift raises bond much more than proximity does (`06:249-257`).

### 07 - Language as social currency (`07-language-social.md`)
**What it researched:** why language became social, and how honesty and prestige hold up.
- **Origins:** Dunbar 1996 (contested), Byrne & Whiten, Dessalles (`07:5`).
- **Image scoring** `q > c/b` (Nowak & Sigmund 1998). Gossip is trusted even alongside direct observation (Sommerfeld 2007) (`07:7`).
- **Honesty:** **Lachmann, Számadó & Bergstrom 2001:** honesty needs lies to cost the liar through verification, not costly signals. Crawford & Sobel 1982 bound cheap talk (`07:9`).
- **Prestige:** Henrich & Gil-White 2001. Smith et al. 2017 is corrected to *Nature Communications*: Agta storytellers average ~0.5 more children (`07:11`).
- **Novelty claim:** coupling communication skill to partner choice is thin in MARL (`07:13`).

**Decided:**
- Prestige-biased sampling of witnesses into the learning bottleneck (`07:19-26`).
- A `voice` timbre field plus a `trust` table that reuses the Roth-Erev pipeline (`07:28`).
- Reputation by overhearing (`07:30`).

**Trap:** `cold` and `care` have no confirmation path (`07:52`).

### 08 - Emergence of language structure (`08-language-structure.md`)
**What it researched:** what pressures make language structure appear.
- **Iterated learning:** the bottleneck selects for structure (Kirby 2001; Smith, Kirby & Brighton 2003; Kirby, Cornish & Smith 2008). Compressibility alone collapses into a degenerate code, so expressivity pressure is also needed (Kirby, Tamariz et al. 2015). Compositionality only appears in a narrow regime (Brighton 2002) (`08:5`).
- **Naming games:** convergence time scales as `t∝N^1.5` (Baronchelli et al. 2006). Local topology gives dialects (`08:7`).
- **MARL:**
  - Abbreviation needs a speaker cost (Chaabouni 2019).
  - Compositionality is uncorrelated with generalization but transmits better (Chaabouni 2020).
  - Resetting listeners raises topsim (Li & Bowling 2019).
  - Neural iterated learning (Ren et al. 2020).
  - A vocabulary penalty (Mordatch & Abbeel 2018).
  - Group-size effects (Raviv 2019).
  (`08:9-15`)
- **Error limit:** the seed citation is corrected to Nowak, Krakauer & Dress 1999 and Plotkin & Nowak 2000. Self-organized phonemes (Oudeyer 2005; de Boer 2000, page numbers flagged as unverified) (`08:17`).

**Decided:**
- A structured meaning space of 20, built from existing variables (`08:25`).
- Two-symbol utterances with a convex amplitude cost (`08:27`).
- A noise floor applied at hearing (`08:29`).
- The bottleneck as a sweep parameter (`08:31`).
- Factored credit assignment (`08:33-36`).
- Recursion is deliberately kept out (`08:38`).

### 09 - Sexual selection and the M1 protocol (`09-sexual-selection.md`)
**What it researched:** Fisher runaway, good-genes models, and how to measure sexual selection in a small population.
- **Runaway:** Lande 1981 and Kirkpatrick 1982. Unstable if `G_tp > G_t`. Costs collapse the line of equilibria. Rescues are biased mutation and perpetual cycling (`09:5`).
- **Finite-N cautions:** Xu 2024 (**preprint**), Reyes et al. 2025, Bailey & Moore 2013 (`09:7`).
- **Genic capture** (Rowe & Houle 1996): eloquence is condition-dependent by construction (`09:9`).
- **The Fisher/good-genes continuum is contested** (Kokko 2002 vs Kuijper 2012). Prum 2010 is flagged as advocacy (`09:11`).

**Decided:**
- **Data infrastructure:** stable `uid`s, pedigree generation, and per-event logs (`09:15-28`).
- A **pre-registered** bootstrap test with a natural/sexual split (Henshaw et al. 2018) (`09:52`).
- A three-signature runaway test (`09:54-57`).
- A preference-redraw null (`09:59`).

**Traps:**
- `I_s` is upper-bound only (`09:71`).
- Survivorship bias (`09:73`).
- The "fat, sexy, fecund" confound (`09:77`).

### 10 - ALife precedents, QD, open-endedness (`10-alife-qd.md`)
**What it researched:** what earlier ALife systems teach, how to measure open-endedness, and how evolution stalls.
- **Lessons from earlier systems:** Tierra, Avida (stepping stones needed), Polyworld (plateau), Echo, Geb, Sugarscape (`10:9-16`), and Lenia (`10:18`).
- **Lehman et al. 2020:** surprising-creativity anecdotes (`10:20`).
- **Bedau activity statistics** with a neutral shadow model: 4 classes vs the commonly cited 3 is flagged contested (`10:22-29`). ToLSim 2026 gives a mixed result (`10:31`).
- **Soros & Stanley 2014's four conditions,** secondary-sourced only. Condition 4 makes Class 4 unreachable for Genesis v0 (`10:33`).
- **Doctrine fit:** MAP-Elites is in, novelty search is off-doctrine, POET is deferred (`10:37-45`).
- **Population genetics:** mutational meltdown and N_e (`10:47`).

**Decided:**
- Bedau counters over gene bins with a "blind Cupid" shadow run (`10:51`).
- Log the QD-score (`10:53`).
- No silent archive reseeding (`10:55`).
- Swap genotype-read descriptor axes for behavioral ones (`10:57`).
- Free-energy-leak invariants: birth creates energy, rest out-earns drain, the archive can be gamed (`10:59-71`).

### 11 - Evolving the drive system (`11-evolving-drives.md`)
**What it researched:** how learning and evolution interact when the genome carries drives.
- **Ackley & Littman 1991:** evolved evaluation net plus lifetime RL. Evolution optimizes learnability.
- **Singh et al.:** for a bounded agent, the best reward is not fitness.
- **Zheng, Oh & Singh 2018/2020:** learned rewards transfer across algorithms, while policies do not. So genes should carry reward shape, never policy.
(`11:5-22`)
- **Baldwin effect:**
  - Hinton & Nowlan 1987.
  - **Fontanari & Santos 2017: H&N only showed the plastic allele was selected.**
  - Waddington assimilation.
  - Ancel 2000: learning that is too good *shields* the genotype.
  - Suzuki & Arita 2007.
  (`11:24-47`)
- **Doya 2002's neuromodulator mapping:** DA = RPE, 5-HT = timescale, NA = randomness, ACh = learning rate (the ACh term is "literature consensus," not verified) (`11:49-53`).
- **Plasticity:** Soltoggio, Stanley & Risi 2018 (`11:58-61`).
- **Stephens 1991:** learning evolves under within-generation persistence; genes evolve under between-generation persistence (`11:61-66`).
- **Kanagawa & Doya 2024:** motor reward bifurcates into a mediocre attractor (`11:75-79`).

**Decided:**
- Resolved a gene-index collision between reports 01 and 02 (`11:89-107`).
- The gene / learned / physics criterion (`11:109-123`).
- A Schmitt latch on mood for bistability (`11:125-134`).
- A three-timescale tower (`11:136-143`).
- A Baldwin signature to measure: falling time-to-competence at flat asymptotic error (`11:160-169`).
- `V*≈2·Ne·Vm` is so large that unselected genes drift to the boundaries. Selectability threshold `s*≈1/(2Ne)`≈1.25% at N=40 (`11:186-199`).

### 12 - The body as evolvable form (`12-morphology.md`)
**What it researched:** body size as an evolvable axis wired into existing physiology.
- **SOLID:**
  - Surface-to-volume scales as `M^−1/3` (geometry).
  - Kleiber's `M^0.75`.
  - Cost of transport `M^−0.32` (Taylor et al. 1982).
  - Bonduriansky 2007: 10 of 12 sexually selected traits are isometric or negative.
  - Y-model (van Noordwijk & de Jong 1986).
  (`12:22-34`)
- **CONTESTED:** the 3/4 exponent (West et al. 1997 vs Dodds et al. 2001; White & Seymour 2003; Glazier 2005), Bergmann's and Allen's rules, positive allometry, Rensch's rule, and fluctuating asymmetry (`12:36-61`).

**Decided:**
- Two genes, `G_SIZE` and `G_DIMORPH`, on the existing drain, cooling and movement lines.
- The two exponents **must differ**, or the thermal trade-off cancels silently (`12:98-126`, `12:231-238`).
- No ornament gene and no FA mechanic (`12:162-165`, `12:255-260`).
- The archive is deliberately not widened (`12:187-190`).

---

## 2. Cross-report findings that transfer to the EBM lab

Format: **Report says** (cited) / **Inference** (mine, not in the reports). A gap up front: **no report in 01-12 researches sleep, memory consolidation or offline retraining.** The nearest items are 04's offline model-fitting note and 11's Baldwin and neuromodulation material, both covered below.

**T1. A drive as a deviation norm is already an energy function.**
- *Report says:* drive `D(H)=Σ|h*−h|^(n/m)`, reward = decrease in D. Nonlinear exponents make one large deficit suppress the value of the others (`02:26-33`). Report 08 quotes GENESIS.md: "predictive coding is energy minimization" (`08:25`).
- *Inference:* this is a scalar energy over internal state that the system descends. Each small EBM's energy could be read as a homeostatic deficit. The n>m>1 coupling gives cross-module arbitration without a hand-written router. Keep each module's energy on a shared normalized scale, the [0,1] commensurability rule (`02:169-174`).

**T2. Safety signals must be able to interrupt, not just bid.**
- *Report says:* pain is a priority interrupt that bypasses argmax (`01:9`, `01:88`). Report 02 keeps a fixed, non-evolvable `P_CRIT` so that "a lineage must not evolve away its own smoke alarm" (`02:200-203`).
- *Inference:* in a growing connection network, a few hard-wired override pathways should sit outside the retrained or evolved set, or growth will prune them away.

**T3. Hysteresis, commitment and bistability are needed against dithering.**
- *Report says:* pure per-tick winner-take-all dithers (Tyrrell 1993). The fix is an incumbent bonus plus a minimum commitment window, swept jointly against an occupancy histogram, because too much stickiness starves rare acts (`02:176-206`, `02:252-280`). A cubic bistable update can make "whether a basin exists" evolvable (`04:136-148`).
- *Inference:* if "each pattern of connection does an action," the pattern-to-action selection needs the same incumbent bonus and commitment window. Otherwise competing patterns flicker. Track a per-pattern occupancy histogram to catch starved patterns.

**T4. Use gain and bias, never a uniform scale.**
- *Report says:* argmax is invariant to uniform scaling (`03:229-233`). Motivation works as multiplicative gain on drive signals, mood as an additive per-act bias, so survival acts are never zeroed out (`02:142-167`).
- *Inference:* a global "arousal" multiplier on all module energies does nothing to an argmin decision. Modulators have to act unevenly, or through temperature, or after selection.

**T5. Evolve the reward or evaluator, not the policy.**
- *Report says:* Ackley & Littman 1991 found evolution selects learnability (`11:5-10`). Zheng, Oh & Singh found learned rewards transfer across learning algorithms where policies do not (`11:16-22`). Singh et al. 2010 found the best reward for a bounded agent is not fitness and includes a novelty term (`03:66-78`).
- *Inference:* this fits a design where pretrained EBMs are evaluators and generations evolve which energies and couplings exist, rather than evolving fixed connection behavior.

**T6. Decide per parameter what is genetic, what is learned, and what is physics.**
- *Report says:* the Stephens 1991 criterion. Learn what persists *within* a generation, encode as genes what persists *between* generations, and fix as physics what is true regardless of strategy. Pain shows this works per parameter: recognizing danger is learned, the reflex threshold is genetic (`11:61-66`, `11:109-123`).
- *Inference:* use the same split for the lab. Connection-making is learned during "waking." Module hyperparameters such as gains and time constants pass across generations. Energy normalization is fixed.

**T7. The Baldwin effect and its two failure modes.**
- *Report says:* the Baldwin signature is time-to-competence falling while asymptotic error stays flat (`11:160-169`). Shielding (Ancel 2000) means learning that is too good hides the genotype, so nothing is ever assimilated, and only gene variance reveals it (`11:38-43`, `11:224-228`). H&N 1987's evidence was overread (Fontanari & Santos 2017) (`11:24-32`).
- *Inference:* "retrain at sleep, grow over generations" is a learning-evolution stack. To show generations add anything, log time-to-competence after "birth" and the variance of inherited parameters. If sleep retraining fully compensates every generation, evolution will be invisible.

**T8. Offline reallocation: the only sleep-adjacent proposal.**
- *Report says:* M2 forward note: `lr = lr_base·(1+k·gloom)`, i.e. suppressed action cycles spent on offline model-fitting. Explicitly conditional, not load-bearing, built on contested rumination theory (`04:198-203`). Separately, Doya's ACh is the learning-rate modulator, and GENESIS.md's "stress sets learning rates" was intent, not code (`11:49-57`).
- *Inference:* a weak precedent for gating the strength of sleep retraining on internal state, for example retraining harder after high prediction error. Not evidence that it helps. Test it against a matched ablation, as report 04 requires.

**T9. Language as connection-making, and the bottleneck as the anti-overfitting force.**
- *Report says:* a transmission bottleneck selects for compressible, compositional structure. Compressibility alone collapses into one-symbol-for-everything, so expressivity pressure is required (`08:5`). A loose bottleneck lets idiosyncratic holistic codes survive, while a naive learner each generation is "definitionally anti-encryption" (`08:60`). Resetting listeners raises structure (`08:11`). Abbreviation needs an explicit cost (`08:10`).
- *Inference:* if connection patterns are cached and passed to the next generation, passing them through a small sample (a bottleneck) instead of copying the whole cache should favor reusable, compositional connection motifs. A per-connection cost (convex, like `08:27`) stops runaway connection growth. The metrics transfer directly: topographic similarity, effective symbol count, a permutation-null onset test (`08:42-46`).

**T10. Credit assignment over compound patterns.**
- *Report says:* when one outcome rewards a multi-part utterance, split the payoff 1/L so total reinforcement does not depend on length. Do not split motor self-entrenchment (`08:33-36`).
- *Inference:* when "each connection makes another connection," a reward for the final action should be split across the chain, or long chains get over-reinforced just for being long.

**T11. Roth-Erev, eligibility traces and continuous extinction as a cache rule.**
- *Report says:* eligibility trace (`*=0.85`), reinforcement on event, continuous decay (`*=0.999`). Bias, never a hard block, so stale associations fade (`01:46`, `01:94`).
- *Inference:* a cached connection or action store needs decay, or early accidents become permanent taboos. This is relevant to "each action and connection gets cached."

**T12. Quality-diversity and open-endedness measurement.**
- *Report says:*
  - MAP-Elites coverage and QD-score (`10:53`).
  - Behavioral descriptors, not genotype descriptors, or bins credit traits never expressed (Pugh, Soros & Stanley) (`10:57`).
  - Bedau activity with a neutral shadow model to separate adaptive from neutral novelty (`10:22-31`, `10:51`).
  - Class 4 requires unbounded representation (Soros & Stanley condition 4). A fixed-width genome caps D(t) (`10:33`).
  - Novelty search is off-doctrine because it decouples from viability (`10:43`).
  - Avida needs stepping-stone rewards (`10:12`).
- *Inference:* a network that literally grows (new modules, new connections) could meet condition 4 where Genesis v0 could not. Bin by behavior, for example which action patterns a network actually uses, and run a shadow model with random connection formation as the baseline.

**T13. Stalls, Goodhart and free-energy leaks.**
- *Report says:*
  - Polyworld plateaued under static carrying capacity, and depletion keeps reopening optima (`10:13`, `10:90`).
  - Lehman et al. 2020's reward-hacking anecdotes (`10:20`, `11:68-74`).
  - Genesis's own leaks found in code: birth created energy, resting out-earned drain, the archive was gameable (`10:66-68`).
  - Kanagawa & Doya 2024's mediocre bifurcated attractor (`11:75-79`).
- *Inference:* any "energy" budget for connection growth needs conservation invariants as tests from day one. Any score that also drives reproduction will be gamed.

**T14. Small-population drift swamps weak selection.**
- *Report says:* `V*≈2·Ne·Vm`. Genes below `s*≈1/(2Ne)` random-walk to the boundaries. Log the fraction of genes pinned at 0 or 1. Add genes in gated groups, because of Hill-Robertson interference (`11:186-199`, `11:240-247`). Treat the seed as the unit of replication (`10:79`). Survivorship bias (`09:73`).
- *Inference:* with a small population of networks, most evolvable hyperparameters will drift. Add them a few at a time, each with a falsifier.

**T15. Morphology and growth: trade-offs need different exponents.**
- *Report says:* two scalings with different exponents produce a real trade-off with no hand-coded rule. The same exponent cancels silently (`12:105-107`, `12:231-238`). Mass starts at the population-mean calibration so only variance is new (`12:77-81`).
- *Inference:* if network size or depth "grows," let its benefit and its cost scale with different exponents (for example capacity vs metabolic or compute cost), or growth becomes either free or useless. Start growth parameters centered so generation 0 matches the untuned baseline.

**T16. Homeostasis needs recovery terms.**
- *Report says:* `load` only ever increases, which causes uniform early death and absorbing states. Every report that touches it adds a recovery term or a guardrail (`01:53`, `04:273-280`).
- *Inference:* every accumulator in the lab, such as a connection cache, a fatigue variable or "sleep pressure," needs a discharge path. This is the obvious role for a sleep phase.

**T17. Verification beats signal cost for honesty.**
- *Report says:* honesty holds when lies cost the liar through verification (Lachmann et al. 2001) (`07:9`). Trust is updated by the same confirm/expire pipeline as meaning (`07:28`).
- *Inference:* if modules "propose" connections to one another, confirming them against outcomes, not taxing every proposal, is the cheaper way to keep proposals reliable.

---

## 3. Literature worth following up (as cited in these reports)

**Energy, homeostasis, drives**
- Keramati & Gutkin 2014, *eLife* 3:e04811 (`02:295`).
- Sterling 2012 (`02:296`).
- Barrett & Simmons 2015 (`02:297`).
- Man & Damasio 2019 (`01:121`).
- Seymour 2019 (`01:123`).
- Mahajan, Dayan & Seymour 2025 (`01:124`).
- Bach 2009, PSI (`02:312`).
- Avila-García & Cañamero 2004 (`02:308`).

**Evolving evaluators, rewards, plasticity (closest to "small pretrained models retrained, growing over generations")**
- Ackley & Littman 1991 (`11:258`).
- Singh, Lewis, Barto & Sorg 2010 (`03:274`).
- Zheng, Oh & Singh 2018/2020 (`11:260`).
- Soltoggio, Stanley & Risi 2018, "Born to Learn" (`11:267`).
- Doya 2002 (`11:266`).
- Stephens 1991 (`11:268`).
- Hinton & Nowlan 1987, and Fontanari & Santos 2017 (`11:261-262`).
- Ancel 2000 (`11:264`).
- Suzuki & Arita 2007 (`11:265`).
- Kanagawa & Doya 2024, arXiv:2406.15016 (`11:270`).
- Maass, Janzen, Saxena & Mukherjee 2026, arXiv:2602.04807 (`01:127`).

**Intrinsic motivation and curiosity**
- Oudeyer, Kaplan & Hafner 2007 (`03:273`).
- Schmidhuber 2010 (`03:275`).
- Constantino & Daw 2015 (`03:277`).
- Eldar, Rutledge, Dolan & Niv 2016 (`04:315`).

**Connection-making and structure emergence**
- Kirby et al. 2008, 2015 (`08:64-65`).
- Brighton 2002 (`08:67`).
- Smith, Kirby & Brighton 2003 (`08:66`).
- Ren et al. 2020, ICLR (`08:76`).
- Li & Bowling 2019 (`08:75`).
- Chaabouni et al. 2019, 2020 (`08:73-74`).
- Mordatch & Abbeel 2018 (`08:77`).
- Baronchelli et al. 2006 (`08:69`).
- Lazaridou & Baroni 2020 survey (`08:72`).
- Nowak, Plotkin & Jansen 2000 (`08:81`).

**Bistability and dynamics**
- Mizrachi et al. 2023 (`04:313`).
- Cramer et al. 2016 (`04:314`).
- Scheffer et al. 2009/2012 (`04:312`).
- Houston & Sumida 1985 (`02:303`).
- Redgrave, Prescott & Gurney 1999 (`02:306`).

**QD and open-endedness**
- Mouret & Clune 2015 (`10:127`).
- Vassiliades et al. 2017, CVT-MAP-Elites (`10:128`).
- Pugh, Soros & Stanley 2016 (`10:129`).
- Cully et al. 2015 (`10:130`).
- Brant & Stanley 2017/2020 (`10:126`).
- Wang et al. 2019, POET (`10:125`).
- Standish 2000 (`10:119`).
- Taylor, Bedau, Channon et al., arXiv:1909.04430 (`10:122`).
- Adams et al., arXiv:1607.01750 (`10:121`).
- ToLSim, arXiv:2603.01701 (`10:120`).
- Lehman, Clune, Misevic et al. 2020 (`10:117`).
- Lenia, Chan 2018/2023 (`10:113`).

**Sleep and consolidation:** none cited anywhere in reports 01-12. A separate search is needed.

---

## 4. Retractions, corrections and uncertainty flags carried by these reports

**Citation corrections**
- Niv et al. 2007 has four authors, not three (`03:5-12`).
- Smith et al. 2017 is in *Nature Communications*, not *Nature Human Behaviour* (`07:11`).
- The error-limit derivation is Nowak, Krakauer & Dress 1999 and Plotkin & Nowak 2000, not Nowak & Krakauer 1999 (`08:17`).

**Overread or discredited evidence**
- Hinton & Nowlan's Baldwin result was overread (`11:27-32`).
- Bateman 1948's data is discredited (`06:86-94`).
- HANDY's collapse is definitional (`05:15`).

**Flagged contested**
- Loss-aversion magnitude (`01:7`).
- Panksepp cross-couplings and the attractor framing (`02:39-49`).
- Dunbar (`07:5`).
- Analytic rumination (`04:34-42`).
- The metabolic exponent and Bergmann's rule (`12:36-48`).
- Penn & Számadó on Grafen (`09:9`).
- Prum is advocacy (`09:11`).

**Unpublished, unverified or secondary-only sources**
- Xu 2024 and Cruzan 2022 are not peer-reviewed (`09:7`).
- Soros & Stanley 2014 is secondary-sourced only (`10:33`).
- Bedau 1998 was reconstructed from secondary sources (`10:118`).
- ALIEN was not verified (`10:18`).
- de Boer's page numbers are unverified (`08:17`).
- Several sources were read via abstract or were paywalled: Seymour, Mahajan, Miller & Raison, Huys, Ancel (`01:129`, `04:295-299`, `11:264`).
