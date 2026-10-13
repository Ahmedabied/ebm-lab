# Genesis digest A: architecture, learning mechanics, inheritance

Source: `/home/abied/genesis-archive` (read-only). All paths below are relative to it. `genesis/` = code, `docs/` = docs.
Citations are `path:line` as of this read (2026-10-13). Note that line numbers quoted *inside* older Genesis docs can be stale. For example, `docs/research/OPEN-libido-is-not-an-organ.md:22-27` cites the chemistry at `agents.py:1722-1731`, but it now sits at `genesis/agents.py:3041-3050`.

**Legend:** **[G]** = Genesis evidence (I read it in a file). **[I]** = my inference, or a mapping onto the EBM-lab idea.

---

## 1. What Genesis actually built (mechanism by mechanism)

### 1.1 Layering and the mediation law
- **[G]** Planned as L0 physics → L1 world (fields) → L2 body → L3 nerves (two hemispheres) → L4 speech → L5 evolve → L6 observatory. The rule: "NOTHING acts on anything directly", so speech is amplitude in a sound field (`docs/GENESIS.md:28-59`).
- **[G]** The rule was broken in the code from the start, and later repaired. `_best_mate` read other agents' private `energy`/`bond` ("telepathy"). The repair is a per-tick rendered `appear` field, read only through `_perceive` with distance attenuation and Weber-proportional noise (`docs/RESEARCH-BODY.md:19-29`, `:116-120`, `:136-148`). The design keeps noise at the receiver and never in physics (`docs/RESEARCH-BODY.md:140-142`).

### 1.2 How decisions are made (the "left brain" that actually ran)
- **[G]** Decision-making is a **utility argmax over 8 acts**: forage, drink, seek_warm, rest, explore, social, court, tend (`genesis/agents.py:36-40`). The utility stack is hand-built need pressures plus a heritable per-act bias times 0.15 (`genesis/agents.py:3394-3395`). Motivation adjusts two specific rows (`:3409`, `:3415`), and boldness-scaled noise is added (`:3455-3456`). Then `act = util.argmax(axis=0)` (`:3458`).
- **[G]** Hysteresis and commitment (an anti-dithering Schmitt trigger) are applied before the argmax by `arbitrate()` (`genesis/agents.py:1010-1084`). There is a pain **reflex veto** that overwrites the argmax result with FLEE, which is deliberately not a utility column (`genesis/agents.py:41-49`, `:3077`, `:3466`). There is also a fixed, non-evolvable emergency threshold `P_CRIT = 0.90` (`genesis/agents.py:740`).
- **[G]** The header states the doctrine plainly: "the brain is a utility argmax over need pressures" (`genesis/agents.py:4-6`).

### 1.3 Chemistry ("right brain" as built)
- **[G]** The chemistry is deterministic and grounded in body state. `pressure_now = max(1-energy, 1-hydration, cold_gap/8)`. Stress is a leaky integrator of pressure and pain. Load is a slow integral of stress. Bond decays (`genesis/agents.py:3041-3050`). Load shortens lifespan: `MATURE_AGE*8*(1-0.35*load)` (`genesis/agents.py:1193-1197`). Stress raises speech sampling temperature, `tau = 0.2 + 0.9*stress` (`genesis/agents.py:5593`).
- **[G]** Motivation `m` is an EMA of obtained payoff (`genesis/agents.py:3382-3388`; design in `docs/RESEARCH-M1.md:129-131`).
- **[G]** The gloom (bistable mood) loci 33-38 were allocated but **never wired**. B3 hard-stopped on an unsourced guardrail (`docs/PLAN.md:333-340`, `:386-388`).
- **[G]** Libido started as a stateless, gene-free formula, and this was flagged as "a formula, not an organ" (`docs/research/OPEN-libido-is-not-an-organ.md:36-57`). It was later given a gene and satiety state in Wave D2 (`docs/PLAN.md:512`; `genesis/evolve.py:183-184`; `genesis/agents.py:3308`).

### 1.4 Lifetime learning: the three things that actually learn
1. **Lexicon (Roth-Erev).** Each agent holds a private matrix `lex[agent, meaning, symbol]` (`genesis/agents.py:2450`), with M=6 meanings and S=12 symbols (`:91-93`).
   - **Production:** softmax over `lex[i,m]` at stress-set temperature (`:5591-5595`). Each use adds `+0.02*G_LEARN`, "use wears a groove" (`:5604`).
   - **Comprehension:** on hearing, the agent bets on its own argmax reading and opens a 60-tick window (`:5733-5736`). If the meaning's body condition is met in the window, it reinforces `+0.15*G_LEARN` (`:5794`). On expiry it decrements by `0.02` (`:5820`).
   - **Trust:** a voice-keyed trust ledger uses the same Roth-Erev shape and the same gene (`:5815`, `:1128-1136`).
2. **Pain place-aversion.** A private coarse map, stamped by reflex events through an eligibility trace and decayed by ×0.999 each tick (`genesis/agents.py:765`, `:3095-3113`). It biases gradient moves but never blocks them (`:772`, `:3709-3721`).
3. **Salt place memory (C8).** One remembered cell per agent (`genesis/agents.py:2229-2230`). It is consulted **only** where the scent cue is undetectable, so "cue first, always" (`:3971-3993`, `:3950-3970`). It was shown to bind: "memory binds 133/135" cells (`docs/PLAN.md:435-436`).

- **[G]** **No lexicon normalisation or clip.** I found no clip or decay on `self.lex` beyond the expiry decrement (grep of `self.lex` sites: `genesis/agents.py:2450, 2868, 2954, 5591, 5604, 5635, 5717, 5733, 5794, 5820`). `eloquence()` is the clipped mean top-1 minus top-2 margin (`:2951-2956`). **[I]** So lexicon magnitudes can grow without bound, and only margins are read.
- **[G/I]** **Heard meanings never steer action.** `pending_meaning` is read only inside `_hear_and_learn` (and reset in `_spawn`). Grep finds no read in `_move_and_do` (`genesis/agents.py:2453, 2870, 5734, 5764`). The file header says "a heard symbol biases behaviour" (`:17-18`), but as far as I can find, comprehension is a passive correlational bet. It is reinforced when the body state happens to improve, not because the agent acted on it. Genesis's own docs never state this. Treat it as my finding and verify before relying on it.

### 1.5 Transmission across generations (iterated learning)
- **[G]** Founders share one proto-lexicon plus small noise (`genesis/agents.py:2740-2751`).
- **[G]** Newborns get a **zero lexicon**: "lexicon by NOTHING: the child is born languageless and must pass the bottleneck … copying the matrix would delete the force we are studying" (`genesis/evolve.py:193-196`, `:306`).
- **[G]** Infants learn from at most `BOTTLENECK = 12` witnessed (context, symbol) pairs (`genesis/agents.py:1089`). Each accepted witness adds `+0.5*G_LEARN` and spends a slot (`:5717-5718`).
- **[G]** D3 made witnessing prestige-biased. Acceptance probability rises with the speaker's `pi` (energy + eloquence), with a `PI_FLOOR = 0.05` and a 2-slot pure-random quota (`genesis/agents.py:1101`, `:1108`, `:5700-5716`).
- **[G]** Measured in v0: agreement went from 1.0 in founders, through drift, to partial re-convergence at 0.508 (`docs/GENESIS.md:86-87`). Wave B: masked agreement went 0.207 → 0.206 → 0.184 while pooled agreement rose then fell. **The two metrics disagree in direction** (`docs/PLAN.md:342-347`).

### 1.6 Genome, inheritance, mutation
- **[G]** The genome is a flat float32 vector, every locus stored raw in [0,1] and decoded to a phenotype range at the read site (`genesis/agents.py:95-110`). `G = 48` at Wave D (`genesis/agents.py:382`; `docs/PLAN.md:516`).
- **[G]** Child genome = per-locus uniform crossover (`genesis/evolve.py:258`) plus Gaussian mutation, clipped. The mutation rate is itself heritable: `rate = 0.02 + 0.10*mix[G_MUT]` (`genesis/evolve.py:302-303`).
- **[G]** The father's genome is snapshotted at conception, because slots recycle and a uid is not enough to recover genes (`genesis/evolve.py:148-155`, `:225-248`).
- **[G]** One plasticity gene, `G_LEARN`, scales the lexicon, trust and aversion learning rates (`genesis/agents.py:1129-1135`, `:3098-3108`). **[I]** This is the Baldwin hook: evolution tunes *how fast* to learn, never *what* is learned.
- **[G]** Preference genes are gathered by index array, never sliced, so later waves can append loci (`genesis/agents.py:116-128`).
- **[G]** Mate choice: `score = prefs @ cues - 0.15*d` with threshold `0.25*G_CHOOSY*(0.5+G_INVEST)` (`genesis/agents.py:5249`, `:5276-5277`). A persistent courtship "incumbency cache" exists (`genesis/agents.py:2304`, `:5278-5301`; rationale `docs/PLAN.md:357-364`).

### 1.7 The QD archive
- **[G]** MAP-Elites with 4 axes × 5 bins: social act share, bold act share, eloquence, load. Elite score = offspring **recruited** to maturity, with a tiny age tie-break (`genesis/evolve.py:361-402`). It is offered every adult once per season (`genesis/run.py:2266-2268`).
- **[G]** **Output only.** I found no read of `arch.bins` that feeds back into the population. `run.py` writes it to a sidecar (`genesis/run.py:3162-3170`). Elite-seeded restarts were allowed only "as a separate, labeled arm" (`docs/RESEARCH-M1.md:419-420`).

### 1.8 Sleep, consolidation, replay
- **[G]** **None exists.** Grep for sleep, replay, consolidat, dream and predict over `agents.py`, `evolve.py`, `world.py`, `physics.py` and `run.py` finds only comments ("byte-identical replay" means deterministic re-run). The nearest analogues:
  - rest-gated `load` recovery (`docs/PLAN.md:159-167`)
  - aversion decay (`genesis/agents.py:765`)
  - one-cell salt memory (§1.4)
- **[G]** The theory doc names "Memory: feeling tags what survives consolidation" as a **missing piece** (`docs/research/THEORY-right-brain-2026-08-13.md:85`).

### 1.9 Testing and determinism discipline (built and enforced)
- **[G]** Five execution laws (`docs/PLAN.md:23-44`):
  - **L1:** the rng stream is the experiment. Any change in draw count or order re-rolls the universe, and instrumentation must use zero draws.
  - **L2:** re-baseline after every behaviour change.
  - **L3:** archives never cross waves.
  - **L4:** no unwired genes.
  - **L5:** instrument, then calibrate, then conclude.
- **[G]** Tests stood at 483 passing / 0 failing at the `wave-D` tag (`docs/PLAN.md:507-508`). Behaviour-neutral changes are proven by byte-identical event logs (`docs/PLAN.md:197-199`; `genesis/evolve.py:109-114`).

---

## 2. Planned but never built

- **[G]** **M2, the energy-based predictive left brain.** "Replace act-argmax with a small energy-based predictive model per agent (genome-seeded weights, lifetime learning by prediction-error descent; the Baldwin effect gets to operate). Keep the argmax as the fallback organ … it must beat [it] AT SURVIVING" (`docs/GENESIS.md:97-100`; framing at `:38-42`). **Never built.** No energy or prediction code exists in `genesis/` (grep above), and decisions remain the argmax (§1.2).
- **[G]** Attraction-as-chemistry was explicitly deferred "to M2, where mate-directed wanting becomes a special case of the predictive machinery" (`docs/RESEARCH-BODY.md:479-485`).
- **[G]** M3 (Panksepp drive modules as coupled ODEs), M4 (Rust port, scale) and M5 (socket to the house) were all unbuilt (`docs/GENESIS.md:101-111`). The general evolvable coupling matrix (`Wps`, `Wss`) was deferred to M3 (`docs/RESEARCH-M1.md:173-178`).
- **[G]** **Wave E**, speech structure: factored meanings, length-2 utterances, amplitude cost, hearing noise, and the bottleneck as a sweep axis {6, 12, 24} (`docs/RESEARCH-M1.md:282-307`). It was "NOT this week" and never opened (`docs/PLAN.md:713-714`; `docs/START-HERE.md:42-44`). **So the bottleneck's headline payoff, compositionality, was never tested.** `docs/GENESIS.md:115-117` itself says compositionality needs "M2's predictive states".
- **[G]** Waves F-I (size, mark, self/rhp, learned preference) were never built (`docs/PLAN.md:586-648`). Gloom was never wired (§1.3). `give`/sharing was struck (`docs/PLAN.md:530-534`).
- **[G]** CVT-MAP-Elites was recommended as the long-term archive fix and not adopted (`docs/RESEARCH-BODY.md:548-551`). A generative body-plan genotype was named as "a real later option at M2+" (`docs/RESEARCH-BODY.md:791-797`).
- **[G]** The right-brain theory (emotion as a read-out of energy settling, actor-critic) is **theory only**, with six named missing pieces (`docs/research/THEORY-right-brain-2026-08-13.md:23-86`).

---

## 3. Lessons that transfer to the EBM lab

The new idea in brief: small pretrained EBMs whose one job is making connections; connections beget connections; patterns of connections are actions; actions and connections are cached; each model retrains at "sleep"; the system grows over generations.

### L-1. Inherit the capacity to learn, not the learned content (bottleneck)
- **[G]** The child gets genes, including the learning rate `G_LEARN` and the mutation rate `G_MUT`, but a zero lexicon. It re-learns from ≤12 witnessed samples (`genesis/evolve.py:193-196`, `:302`; `genesis/agents.py:1089`). The rationale is Kirby's: "Copying would delete the force we're studying" (`docs/GENESIS.md:66`).
- **[G] caveat:** Genesis never showed the bottleneck *producing* structure. Wave E never ran (§2), and agreement metrics disagree in direction (`docs/PLAN.md:342-347`).
- **[I] mapping:**
  - "Each small model gets retrained at sleep" plus "grows over generations" maps onto **teacher → student distillation through a capped replay sample**.
  - The next generation's EBMs should not inherit parent weights wholesale. They should be retrained from a bounded sample of the parent's cached connection→action episodes.
  - The cap size is the experimental knob, and Genesis's planned {6, 12, 24} sweep is a ready template.
  - Inherit hyperparameters (learning rate, plasticity, maybe architecture priors) as genes.

### L-2. Credit assignment as a delayed, windowed bet (Roth-Erev)
- **[G]** A connection (heard symbol → meaning) is a pending bet with a 60-tick window: +0.15·G_LEARN on confirmation, −0.02 on expiry (`genesis/agents.py:5733-5820`).
- **[G]** The audits found **unreachable confirmation paths**. Two of five meanings could never be confirmed, so they could only be punished (`docs/RESEARCH-M1.md:323-327`). The male mate-call confirmation was satisfiable only by females (`docs/PLAN.md:175-180`).
- **[I] mapping:**
  - Every new connection in the EBM lab can carry an eligibility window and resolve as confirm or decay.
  - **Write a test that every connection type has a reachable confirmation path.** Otherwise the cache will be silently biased against whole classes of connection.

### L-3. "Learned but never steers" is invisible from outside
- **[G]** A Genesis test makes this point directly: "a memory that is written and cleared but never STEERS is indistinguishable … from a memory that was never wired". The fix is a binding counter that must be nonzero (`genesis/tests.py:9575-9580`; L5 at `docs/PLAN.md:42-44`).
- **[G/I]** My reading is that the lexicon's comprehension side has exactly this property (§1.4).
- **[I] mapping:**
  - A cached connection-pattern must be *read by action selection*, or it is decoration.
  - For every cache, log "times this cache entry decided an action".

### L-4. Scale invariance of argmax/argmin
- **[G]** "argmax is invariant to a positive rescale of the WHOLE vector, so any modulation that touches every row equally is a silent no-op" (`genesis/agents.py:3398-3400`; `docs/RESEARCH-M1.md:139-140`).
- **[I] mapping:**
  - An EBM picks `argmin E`. Adding a constant to every candidate's energy changes nothing.
  - Modulators such as mood or "feeling" must act non-uniformly: per candidate, per connection type, or on temperature.

### L-5. Anti-dithering, and the free-resampling exploit
- **[G]** Without an incumbency bonus, choice dithers. The switch-rate knee was measured: switch rate 46.92 → 25.23 → 20.43 → 15.65 across h, while responsiveness rose (`docs/PLAN.md:326`).
- **[G]** Repeated noisy re-reads average out by the CLT. That reconstructs perfect information unless the first impression is cached (`docs/RESEARCH-BODY.md:727-729`).
- **[I] mapping:** "Each connection makes another connection" is an iterative settle loop. It needs commitment (incumbency) or it will oscillate. Repeated re-querying of a stochastic EBM can quietly defeat any intended noise or uncertainty.

### L-6. Every growth process finds free energy
- **[G]** Exploits found in the source:
  - birth manufactured +0.07 energy (`docs/RESEARCH-M1.md:313-316`)
  - rest out-earned existence for low-metabolism genomes (`docs/RESEARCH-M1.md:317-319`)
  - the archive was Goodhart-gameable by neglect (`docs/RESEARCH-M1.md:320-322`)
  - `eat()` manufactured 2.8% of biomass intake, *below* seed-to-seed variance, so screens would never have flagged it (`docs/PLAN.md:68-72`)
- **[I] mapping:**
  - Self-reinforcing connection growth is a classic runaway.
  - Budget connections like energy: conservation asserts, an explicit cost per connection, bounded weights. Genesis's `lex` had no clip (§1.4).
  - Score cached patterns on *downstream* outcome (recruitment), not on immediate count (fecundity).

### L-7. What goes in the prior vs what is learned
- **[G]** The criterion: **gene** = an ancestral fact only a lineage can discover, where a wrong first guess is fatal. **Learned** = what the current world can teach within a life. **Physics** = true regardless of strategy (`docs/RESEARCH-M1.md:182-188`). It is grounded in Stephens 1991: within-generation regularity favours learning, between-generation regularity favours genes.
- **[I] mapping:** this is a principled split for the EBM lab:
  - "pretrained" = genes
  - "day learning plus sleep retraining" = learned
  - fixed architecture/energy form = physics

### L-8. Selectability limits on heritable knobs
- **[G]** A gene must shift relative reproductive success by ≳1/(2N_e) to be selected rather than drift (`docs/RESEARCH-M1.md:404-407`). Measured aggregate N_e was 32.82, giving a floor of 1.523% (`docs/PLAN.md:249-252`). Census peaks did not raise N_e, because "the harmonic mean … is dominated by the bottlenecks" (`docs/PLAN.md:254-257`).
- **[G]** Rules followed: no unwired genes (L4), and staged rollout, because "41 new genes at once at N≈40 is how you manufacture drift artifacts" (`docs/RESEARCH-M1.md:204-206`).
- **[I] mapping:** with a small population of EBM-networks, only a handful of heritable hyperparameters can actually be selected. Add them one wave at a time.

### L-9. Determinism as a scientific instrument
- **[G]** L1-L3 (`docs/PLAN.md:25-38`). Byte-identical event logs prove that instrumentation changed nothing (`docs/PLAN.md:197-199`). Every pre-fix run is "void as a control" (`docs/PLAN.md:28-29`).
- **[I] mapping:**
  - Seed all sleep retraining: data order, init, dropout.
  - Keep logging off the RNG stream.
  - Version the "genome" or architecture and refuse to compare caches or archives across versions.

### L-10. The flat-genome ceiling and growth
- **[G]** "a 24→58-float direct genome absorbs *scalar dials* … It cannot grow a body *plan*". Sims, Framsticks and CPPN-NEAT exist because their authors hit this wall (`docs/RESEARCH-BODY.md:791-798`). Bedau Class 4 is "structurally unreachable with a fixed-width genome" (`docs/RESEARCH-M1.md:476-477`).
- **[I] mapping:** "grows over generations" in the EBM lab *requires* a variable-size, graph-like genotype (NEAT-style add-node and add-edge), not a fixed vector. Genesis is the negative example here.

### L-11. The QD archive as the output
- **[G]** Descriptors must read **behaviour**, not genotype, because genotype axes "fill bins trivially" (`docs/PLAN.md:63-66`, `:108-113`).
- **[G]** Don't widen axes: going from 625 to 3,125 bins reads as a fake coverage crash (`docs/RESEARCH-BODY.md:536-541`). "Never add an axis to 'capture' new behaviour" (`:553-554`).
- **[I] mapping:** an archive of connection-pattern repertoires binned by behaviour, using CVT bins from day one, is a natural "diversity across generations" output.

### L-12. The variance you measure must be the right one
- **[G]** "A seed is a world, not a replicate". Habitable worlds kept 8/10 founder draws alive and uninhabitable ones 0/10 (`docs/RESEARCH-BODY.md:85-95`, `:582-589`).
- **[G]** A 15-cell canary was blind to an 89% → 64% drop that 75 cells revealed (`docs/PLAN.md:565-566`).
- **[I] mapping:** separate task or environment seeds from model seeds, and size evaluation blocks before trusting "no regression".

### L-13. A mechanism can move an internal statistic without moving outcomes
- **[G]** "Prestige moves the CUE and not the FITNESS". The eloquence cue share went to 0.3006 vs 0.1761, while the fitness gradient did not follow (`docs/PLAN.md:555-559`).
- **[I] mapping:** more or denser connections, or sharper cached patterns, are not performance. Pre-register the outcome metric.

### L-14. Feeling as a read-out of how an EBM settled (theory, unbuilt)
- **[G]** The theory doc: "a feeling is NOT a predictor". It is a read-out of the settling geometry:
  - valence = sign of ΔE
  - arousal = gradient magnitude
  - surprise = distance from the prior
  - hurt = residual `E(x,y*)`

  It co-trains actor-critic style (`docs/research/THEORY-right-brain-2026-08-13.md:23-50`). It also names "feeling tags what survives consolidation" (`:85`). Status: never implemented.
- **[I] mapping:** this is the most direct precursor to the EBM lab. The residual energy or ΔE at settle time is a cheap, label-free signal for **which day-episodes enter the sleep replay buffer** (prioritised replay by residual).

### L-15. Parallelise across population, not time
- **[G]** "your loop must parallelise across *something* (population/space/environments) or it loses" (`docs/research/THEORY-right-brain-2026-08-13.md:52-64`).
- **[G]** Measured: Genesis's cost was per-agent Python loops, about 0.79 ms of a 1.2 ms tick, not physics (`docs/PLAN.md:689-692`). Vectorised reads were 12-18× faster (`docs/RESEARCH-BODY.md:160-165`).
- **[I] mapping:** recurrent settle loops are fine if many networks settle in one batched call. Avoid per-node Python loops.

### L-16. Audit for "formula pretending to be an organ"
- **[G]** Libido was a stateless, gene-free expression. It was invisible in review because the neighbouring drives were real dynamical variables (`docs/research/OPEN-libido-is-not-an-organ.md:36-57`). This was later fixed in D2 (§1.3).
- **[I] mapping:** for each "small EBM", check that it has state, heritable variation and real inputs. Otherwise selection and sleep retraining have nothing to act on.

---

## 4. Open questions for the EBM lab

1. **What is the confirmation signal for a connection?** Genesis had grounded body-state confirmations (`genesis/agents.py:5764-5793`). What is the EBM lab's equivalent of "food followed within 60 ticks", and does every connection type have a reachable one (L-2)?
2. **Inheritance channel.** Copy weights, distill through a capped replay sample (Kirby-style), or inherit only hyperparameters? Genesis chose the bottleneck but never measured its structural payoff (§2, Wave E).
3. **Sleep replay selection.** Uniform replay, recency, or residual-energy-prioritised (L-14)? Genesis has no data here. Its own theory lists consolidation as missing.
4. **What bounds connection growth?** Cost per connection, weight clipping, pruning at sleep? Genesis's analogue (`lex`) was unbounded (§1.4), and every free-energy leak got exploited (L-6).
5. **How are actions read off connection patterns, and is the readout an argmin with commitment (L-4, L-5)?** Without an incumbency term, expect dithering.
6. **Genotype for growth.** A fixed vector cannot grow topology (L-10). Which variable-size encoding, and how do crossover and mutation act on it?
7. **Population size vs heritable knobs.** With N_e in the tens, how many heritable parameters can actually be selected (L-8)?
8. **What is the EBM lab's "M2 baseline"?** Genesis demanded that the EBM beat the hand-built argmax *at surviving* (`docs/GENESIS.md:99-100`). What simple non-EBM baseline must the connection-maker beat, on what pre-registered metric (L-13)?
9. **Determinism of sleep.** Can retraining be made byte-reproducible per seed, so behaviour-neutral changes are provable (L-9)?
10. **Descriptors for a QD archive of connection repertoires.** Which behaviour-read axes, using CVT from the start (L-11)?

---

### Flags carried from the source
- The Wave B, C and D tags sit on **amended gates** (scope cuts, not passes) (`docs/PLAN.md:366-397`, `:441-500`, `:530-551`).
- "births +78.9%" was **corrected** to +0.5% per adult-season (`docs/PLAN.md:389-394`).
- The salt-gate scarcity claim was **retired** (`docs/PLAN.md:470-472`).
- The Wave D eloquence-fitness bridge (item 1) **failed** (`docs/PLAN.md:524-527`).
- The `pref-redraw` null is owed before the word "inherited" may be used (`docs/PLAN.md:577-580`).
- The finding that heard meanings never steer action is mine (§1.4) and is not stated in Genesis docs.
