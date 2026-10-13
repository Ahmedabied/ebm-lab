# Session 01 — setup (2026-10-13, laptop)

**What we did:** set up the lab and built the knowledge base. No experiments.

- Found Ahmed's original prompts in the box session (`~/.forge/genesis`, `386e4166`); copied verbatim to `IDEA.md`.
- Five subagents digested the Genesis archive (A–E); one ran a web literature search (01).
- Claude verified the most surprising claim in person: Genesis's heard words never steered behaviour.
- Wrote `00-SYNTHESIS.md`, `STATE.md`, `HANDOFF.md`, `CLAUDE.md`.

**What surprised us:** Genesis planned an EBM brain (M2) from day one and never built it, so this lab
is its unfinished milestone. And the cleanest bridge to Ahmed's idea: **sleep = the negative phase** of
EBM training.

**Cost note:** 6 subagents (~1.4M subagent tokens total). Heavy for a setup day; later sessions should
be leaner.

**Next:** Ahmed picks the path (see HANDOFF).

## Later the same session: correction and the real plan
Ahmed: "genises was never menat to be fun my job sucks my soul out im soo proud of gnises its my favourite
ever project, but i need a real goal and a real plan with it, it is not a small project i belive its a
research lab grade". Claude had framed the lab as light and fun, which was wrong. Fixed in CLAUDE.md, 00-SYNTHESIS §4
and digest E (retraction note). Wrote `RESEARCH-PLAN.md` v0.1: continual learning framing, H1–H5 with
falsifiers, prior-work positioning (Li et al.; Singh et al. wake-sleep EBMs), phases 0–7 with gates.

---
# Session 02 (same day, laptop, Fable 5.1) — creature v0 built, measured, written up

**Ahmed's instruction:** "re review this and research some more with opus5 agents ... lets build it now ...
but lets build it right truly right and once its built and visualized document everything".
Earlier the same day he reframed the whole thing: start with a minimal organism (amoeba finding food), and
"the creature doesn't spawn knowing what food is, its body and the chemistry teach it".

**Built:** `creature/` (physics → world → body → senses → EBM brain → baselines → life loop → CLI → export),
23 law tests incl. a finite-difference gradient check, `DESIGN.md`, 13 recorded amendments, the experiment
harness, calibration (`decisions/0001`), 5 pilots, the pre-registered EXP-01, the viewer (Opus agent,
headless-verified), plots, `findings/01`.

**Research:** 4 Opus seats (R1 energy policies + homeostatic RL; R2 minimal chemotaxis; R3 sleep + growth;
R4 generations). Each caught something real: off-policy replay needs correction (R1), note B carried no
information in the linear world (R2), "sleep" claims need matched updates (R3), a 106-float genome is far too
big for Ne≈6 (R4).

**Result:** EXP-01's primary prediction failed. Within-life EBM learning from the body's lessons did not beat
no learning in one lifespan; the tuned pilot did not replicate on fresh seeds. The weights move in the right
direction but too weakly; making the policy decisive makes it confidently wrong. Baselines: Braitenberg 4072,
oracle 3616, tabular Q 3212, random 1303, EBM 973 ticks (linear). In the xor world Braitenberg eats poison and
halves its lifespan, as predicted.

**What surprised us:** how many of the day's bugs were *physics or scale*, not learning: the brain cost more
than the body; a turning bias loops; raw sensor differences were too small to act on. Every one of them was
found by a number that looked wrong, never by reading code.

**Token cost:** heavy (≈ 10 agent runs ≈ 1.6M agent tokens + a long main thread). Next sessions: one lever,
one pre-registered experiment, no new research seats unless a question needs one.
