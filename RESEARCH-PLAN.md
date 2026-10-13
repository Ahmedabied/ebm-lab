# RESEARCH PLAN — EBM lab (DRAFT v0.1, 2026-10-13, awaiting Ahmed's approval)

> **Reorder, 2026-10-13 (Ahmed):** the embodied minimal creature comes FIRST (see `DESIGN.md`,
> `research/02-minimal-organism.md`); the standard continual-learning benchmarks (tier 1 below) become a
> later validation. H1–H5 stand. Creature v0 is built; its first result is `findings/01`.

> Status: **draft**. Every choice marked ⚑ is Ahmed's to confirm or change.

## 1. The goal

**Build and test a learning system that grows its own structure and consolidates what it learned
during an offline "sleep" phase. It is made of many small energy-based models (EBMs) whose job is to form
connections. Show, with controls, whether it learns a never-ending stream of tasks better than
systems that don't grow, don't sleep, or aren't energy-based.**

The field this lives in is **continual (lifelong) learning**: learning task after task without
*catastrophic forgetting* (new learning overwriting old). That field has standard benchmarks, standard
metrics and published baselines, which is what makes a result here checkable by anyone.

**The long arc (Genesis's M2, closed properly):** once the system works on benchmarks, put it in a body
in a world and test whether it beats a hand-written baseline *"AT SURVIVING, not at looking clever"*
(`GENESIS.md:97-100`).

## 2. The thesis, as testable hypotheses

| # | Hypothesis | Falsified if… |
|---|---|---|
| **H1 Sleep** | A sleep phase with **replay + a dreaming negative phase** reduces forgetting more than replay alone, and more than no sleep. | Dreaming adds nothing over replay-only at matched compute, across ≥5 seeds. |
| **H2 Growth** | **Error/energy-directed growth** (add units/connections where the day's energy was badly fit) beats a **fixed network of the same final size** trained the same way. | The fixed same-size twin matches or beats it; or **random** growth does as well as directed growth. |
| **H3 Composition** | A network of **small composed EBMs** reuses old units for new tasks (forward transfer) better than one monolithic EBM with equal parameters. | No forward-transfer advantage over the monolith. |
| **H4 Action** | Patterns of connection read out as actions let the system **learn continually in an environment** (not just classify) without forgetting old skills. | Matches a fixed-architecture RL baseline at best. |
| **H5 Generations** | Passing **priors / learning rules** (not weights) to the next generation cuts time-to-competence. | A **severed-inheritance null** (same rules, randomly re-drawn priors) does as well. |

Each one can fail. A failed hypothesis is a result, recorded with its numbers (Genesis's rule).

## 3. What already exists (positioning, from a first search; Phase 0 does it properly)

- **Li, Du, van de Ven, Mordatch: *Energy-Based Models for Continual Learning*** (arXiv 2011.12216; CoLLAs 2022).
  EBM training interferes less with old knowledge, but they present EBMs as an *alternative* to
  growing architectures. **They don't grow.**
- **Singh et al.: *Wake-Sleep Energy Based Models for Continual Learning*** (CVPR 2024 Workshop, CLVISION).
  A wake/sleep scheme for EBMs. **Closest prior work; must be read in full and beaten or
  differentiated.** As far as we know, it has no structural growth and no modular small units.
- **Sleep-like replay for equilibrium propagation** (arXiv 2508.14081, 2025). Energy-based training and sleep, no growth.
- **Tadros et al. 2022** (Nature Comms): sleep-like replay in ANNs. **SIESTA** (arXiv 2303.10725): wake/sleep CL, not EBM.
- **Growth without EBMs:** GROWN (arXiv 2110.00908), modular growth (arXiv 2406.06262), growing neural gas, NEAT.
  **EnergyNet** (arXiv 1711.03130): energy-criterion growth, not for continual learning.

**Candidate gap (not yet confirmed):** modular *small* EBMs + energy-directed **structural growth** +
sleep with a **dreaming negative phase**, then **actions** and **generations**. The first search found
no paper combining these. Phase 0 must confirm or kill that claim before anything is called novel.

## 4. How we will measure (fixed before any result)

- **Benchmarks, tier 1 (standard continual learning):** Split-MNIST, Permuted-MNIST, Split-CIFAR-10/100,
  in the **class-incremental** and **task-free** settings (the hard ones; Li et al. use both).
- **Tier 2 (actions):** a continual-RL gridworld suite (e.g. MiniGrid tasks in sequence) ⚑.
- **Tier 3 (bodies):** a Genesis-style world, built new and small ⚑ (far horizon).
- **Metrics:** average accuracy, **backward transfer / forgetting**, **forward transfer**
  (Lopez-Paz & Ranzato 2017, GEM), all **parameter- and compute-matched**. Growth efficiency (accuracy per unit added).
- **Baselines:** fine-tune (lower bound), joint training (upper bound), EWC, experience replay, generative
  replay, **Li et al. EBM-CL**, **Singh et al. wake-sleep EBM**.
- **Ablations, every phase:** no sleep · replay-only sleep · random noise "sleep" · fixed same-size twin ·
  random growth · severed inheritance.

## 5. How we stay honest (carried from Genesis, digest D)

- **Reproduce before we compare.** Phase 0 gate: reproduce at least one published baseline number on
  our harness, within its reported spread. If we can't reproduce theirs, we can't trust ours.
- **Pre-register each experiment** in one short file: hypothesis, metric, bar, seeds. Written before the run.
- **≥5 seeds, mean ± CI**, never the best run. Report failures.
- **Every number in `findings/` carries the command and commit that re-derive it.**
- **Results are versioned, never overwritten.** Corrections are written in, not erased.
- **Denominator and empty-input checks** on every metric (Genesis's biggest error class).
- **Every cache/connection has a test proving it changes an output.** (Genesis's learned words never
  steered behaviour, verified 2026-10-13.)

## 6. Phases

| Phase | Question | Deliverable | Exit gate |
|---|---|---|---|
| **0 Foundations** | What exists, and can we reproduce it? | Systematic lit review (novelty verdict) · PyTorch harness · CL benchmark loaders + metrics · one reproduced baseline | Baseline reproduced; novelty claim confirmed or the thesis re-aimed |
| **1 The unit** | Which small EBM is stable, cheap and composable? | Hopfield / RBM / MLP-energy, trained with CD / NCE / denoising score matching, compared | One unit + training rule chosen on evidence |
| **2 Composition** | How do units combine into a network that "makes connections"? | Energy-sum vs gating vs assemblies; the connection rule | H3 tested |
| **3 Sleep** | Does dreaming-sleep beat replay and no-sleep? | Day/night loop on tier-1 benchmarks | **H1** tested vs all baselines |
| **4 Growth** | Does directed growth beat a fixed twin? | Growth rule + budget/conservation tests | **H2** tested |
| **5 Action** | Can connection patterns drive behaviour continually? | Tier-2 environment results | **H4** tested |
| **6 Generations** | Do inherited priors help? | Generational runs + severed null | **H5** tested |
| **7 Write-up** | — | arXiv preprint; target a continual-learning venue (e.g. CoLLAs) or workshop ⚑ | Every claim traceable to a command |

No dates yet; Phase 0 will tell us real speeds. ⚑

## 7. Compute

- **Laptop:** 16 cores, 15 GB RAM, no torch yet; NVIDIA driver mismatch (reboot pending).
- **Box (`ssh workstation`): RTX 5060 Ti 16 GB**, always on, no torch yet. **Disk 97% full (31 GB free)**,
  so space must be cleared before datasets/checkpoints land there ⚑.
- Tier-1 benchmarks at research scale fit one 16 GB GPU. **No cloud spend without asking.**

## 8. Risks

- **EBM training is unstable** (Langevin sampling). Mitigation: Phase 1 picks the stable training rule on evidence.
- **The gap may already be filled.** Phase 0 kills or re-aims the thesis early, cheaply.
- **Growth turns into bloat.** Mitigation: growth only on measured error, with a budget, vs a fixed twin.
- **Sleep can hurt the newest memory** (Tadros 2022). Mitigation: report old and new tasks separately.
- **Scope creep / token burn** (Genesis's pattern). Mitigation: one phase at a time, each with a gate;
  a written budget at the top of each session.

## 9. Ahmed's decisions ⚑
1. Approve or edit the goal and H1–H5.
2. Tier-2 environment choice (MiniGrid-style vs our own world).
3. Publication target: arXiv preprint only, or aim for a venue.
4. Box disk: what can be cleared for datasets.
5. Pace: sessions per week and the per-session budget.
