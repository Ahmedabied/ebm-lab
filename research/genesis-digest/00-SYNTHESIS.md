# 00 — What we bring into the EBM lab

One page. The long versions, with `file:line` citations, are A–E in this folder and
`research/01-ebm-sleep-growth-literature.md`. Written 2026-10-13 (session 01).

## 1. Genesis never built the thing we're about to build

- **The energy-based brain was Genesis's milestone M2** (`GENESIS.md:38-42, 97-100`). It was
  never implemented. The brain that ran was a hand-built argmax over 8 actions (digest A §1).
- **There was no sleep, replay or consolidation anywhere** in Genesis (digest A §1).
- **The archive has no sleep literature** (digest B). That came from the new web search (lit §2).

So the lab is new ground, and it is Genesis's unfinished M2. M2's own test still holds:
*an EBM must beat a simple baseline "AT SURVIVING, not at looking clever"*.

## 2. Lessons from Genesis that shape the design

| Lesson | Evidence | What it means for us |
|---|---|---|
| **A learned thing that never steers behaviour looks identical to one that was never wired** | Verified this session: Genesis's heard-word reading (`pending_meaning`) is never read by action choice, though the file header says it is (`agents.py:17` vs `:5733-5839`) | Every cache / connection must have a **test proving it changes an action**. |
| **Inherit the ability to learn, not the learned content** | Children got genes + an empty lexicon, relearned from ≤12 utterances (A §4) | "Grows over generations" should pass on learning rules / small priors, not copy weights wholesale. |
| **A fixed-length genome cannot grow structure** | reports 10, 19 (B, C) | Growth needs a *generating rule*. Fits "each connection makes another connection". |
| **Growth finds every free-energy leak** | `world.eat()` was creating 2.8% of intake from nothing (archive README) | Write conservation / budget tests before letting anything grow. |
| **Two-speed forgetting, asymmetric updates** | report 22: "is it paying" fades fast, "does it exist" slowly; extinction is new learning, not erasure (C) | Sleep should weaken failed connections toward a floor, never delete outright. |
| **Winner-take-all flickers** | reports 02, 23, 24 (B, C) | Patterns → actions need stickiness / a commitment window; losers back off, they don't lose ability. |
| **Evolve the evaluator, not the policy** | Ackley & Littman 1991; Singh et al. 2010 (report 11, B) | Generations could evolve the *energy functions*, while sleep tunes behaviour. |
| **Small populations drift** | Genesis measured an effective population of ~33 (A) | Evolve few knobs at a time, with nulls. |

## 3. How Genesis kept its numbers honest (digest D)

- **Every number has the command that re-derives it.** No command = not a result.
- **Controls in the same run:** ON / OFF / SHUFFLE arms on matched seeds.
- **Write the prediction before the run.** If it fails, the failure is recorded, not re-scored.
- **Watch denominators.** The biggest error class. "+78.9% births" was really **+0.5%** per
  adult-season (`BENCHMARKS.md:418`). A cumulative counter summed over rows inflated deaths
  **~10×** (`:1051`).
- **Check what a metric does on empty input.** An all-zero row "agreed" with itself and inflated
  language agreement.
- **Same seed → identical output; measuring must not change the run.**

## 4. What made Genesis stop being fun (digest E, interpretation labelled there)

It went from **a creature you could watch** to **an audit trail you had to read**. Runs were
unattended at night, journals grew to 1,000 lines, and small changes forced every corpus to be re-run.
Ahmed's late inputs were mostly about *stopping*.

**So for the lab:**
1. **Live and together.** Predict, run, look. Runs take seconds, not hours.
2. **A picture every experiment:** energy landscape, recall plot, animation.
3. **One question per session** that teaches one EBM idea. A one-line prediction, not a gate document.
4. **Do the core math in the main conversation.** Agents read papers; they don't do the learning for us.
5. **Light bookkeeping:** STATE + a short journal. Keep the honesty rules, drop the ceremony.
6. **Fun check at every close:** "did you learn something and enjoy it?"

## 5. The bridge: sleep is the negative phase (lit §4, synthesis)

Every EBM needs two forces:
- **pull energy DOWN** on real data
- **push energy UP** on the model's own fantasies

Ahmed's design splits them across a day:
- **Day:** act, cache episodes, lower energy on what happened.
- **Night:** replay the cache mixed with old memories, **dream** and push up on false valleys
  (Hopfield, Feinstein & Palmer 1983; wake-sleep 1995), prune weak links, grow where the day's error was highest.

That is a known split in small systems. Whether it still works **as the network grows** is the
real question this lab can answer.

## 6. The proposed ladder (lit §4; each step has a control)

1. Classical Hopfield net: energy, attractors, capacity
2. Dreaming / unlearning: sleep as the negative phase
3. Modern Hopfield memory: the cache
4. A tiny EBM trained three ways (Langevin, NCE, score matching)
5. Two-speed memory with sleep (complementary learning systems)
6. Combining small EBMs: adding energies vs gating
7. Assemblies: connections that make connections, patterns that pick actions
8. The full loop: day / night / growth over generations, vs a fixed-size twin and a no-sleep twin
