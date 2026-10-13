# 02 — The minimal organism: how the simplest creatures find food

Session 01, 2026-10-13. Ahmed's proposal: start much smaller than a complex creature, with an amoeba that
must (1) tell whether a signal is food or not food, and (2) steer its body toward the food.
Sources were found by web search this session; the summaries come from abstracts, captions and review text, **not full papers**.

## Four real organisms, four ways to solve it

| Organism | Nervous system | How it finds direction | Source |
|---|---|---|---|
| **Dictyostelium (amoeba)** | **none**; chemistry inside one cell (GPCR receptors, PI3K signalling) | **Spatial**: compares the front and back of its body at once; keeps the best-aimed pseudopod rather than making new ones | Nature Cell Biology ncb1536; Frontiers 2021 review; arXiv 2503.04716 |
| **E. coli (bacterium)** | **none** | **Temporal**: "run and tumble"; compares now vs ~4 s ago (recent 1 s weighted +, prior 3 s −); receptor methylation gives a slower memory of tens of seconds | Segall, Block & Berg PNAS 1986 (Caltech resolver); J. Bacteriol 2014 (PMC4272591); arXiv 2504.15385 |
| **C. elegans (worm)** | **302 neurons, fully mapped** | Klinotaxis (gradual turning); minimal model circuit ASE (sensor) → AIY / AIZ (interneurons) → SMB (neck motor). Flipping ASER→AIY from inhibitory to excitatory flips salt preference based on memory. **AIY's centrality is contested by reviewers.** | eLife 104456 (2025) + its reviews |
| **Braitenberg vehicle (thought experiment)** | 2 sensors, 2 motors, 2–4 wires | Crossed vs uncrossed, excitatory vs inhibitory wires give approach / avoid behaviours | Braitenberg, *Vehicles*, MIT Press 1984 |

## What this means for the lab (Claude's reading)

1. **A real amoeba has no neurons.** Its "network" is chemistry. If we want a *neural* minimal organism,
   the honest real-world reference is **C. elegans**: a mapped, tiny, real circuit that learns.
2. **Direction can be found two ways:** comparing two sensors at once (spatial) or comparing now vs a
   moment ago (temporal, which needs **memory**). The temporal way is where learning naturally enters.
3. **Steering alone is too easy to be the research.** Two hand-wired Braitenberg wires already climb a
   gradient. That becomes the **baseline to beat**, not the result.
4. **"Food or not food" is the real research part.** If some signals are food and some are poison, and their
   meaning **changes over time**, the creature must learn, remember and not forget. That is **continual
   learning in a body**. Sleep (H1) and growth (H2) can then be tested at tiny scale, against an
   optimal forager we can compute exactly.
