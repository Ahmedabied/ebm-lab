# HANDOFF — next session

## First
1. Read `STATE.md`, `IDEA.md`, `research/genesis-digest/00-SYNTHESIS.md`.
2. Get Ahmed's answers to the open questions below. Don't build before he picks.

## Open questions for Ahmed
1. **Path:** climb the 8-step ladder (Hopfield first, learn each piece), or build a crude toy of the
   full idea early and use the ladder to fix its parts?
2. **The world:** what do the "actions" act on? (a gridworld, a bandit, a pattern task, something of his)
3. **How to watch it:** Jupyter notebook, or a small local HTML page that redraws after each run?
4. **Pace / budget:** how much per session? (Genesis lesson: set it at the top of the session.)

## Suggested first experiment (if he picks the ladder)
**Step 1: classical Hopfield net in numpy.** Store patterns, corrupt them, watch the energy fall as it
settles. Plot recall vs number of stored patterns (capacity ~0.14N). Control: untrained random
symmetric weights, plus "return the corrupted input". Runs in seconds, no torch needed.
