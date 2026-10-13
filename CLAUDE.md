# EBM lab: ground rules

Read `STATE.md` and `HANDOFF.md` first, then `IDEA.md`.

## Why this exists
A research-lab-grade project: Ahmed's real goal and plan are in `RESEARCH-PLAN.md`. He wants to learn
EBMs deeply AND produce a real, checkable result. Treat it with Genesis's seriousness. Genesis is his
favourite project and was never meant to be "fun"; do not frame this lab as a light hobby. The burnout
came from his day job, not from Genesis's rigour.

## Honesty (non-negotiable; it is why he trusts this work)
- Every number comes from running code. Each finding records the exact command that re-derives it.
- No synthetic or invented results. If something was not measured, say "not measured".
- Every effect gets a control (an OFF arm and/or a shuffled null) before it is called an effect.
- Multiple seeds, report spread, not the best run.
- Write corrections into the record; never quietly delete a wrong claim.
- Watch denominators: report rates against the right base (Genesis's "+78.9% births" was a denominator artifact).

## Working style
- Teach: explain the WHY of each EBM concept as we build it. Bold the instructions, keep it scannable
  (Ahmed has dyslexia + ADHD; short chunks, clear headings).
- One phase at a time (RESEARCH-PLAN §6), each with an exit gate. One experiment = one pre-registered question.
- Research phase -> design -> build. Don't build during a research phase.
- Decisions about what the experiment IS are Ahmed's. Ask; don't assume.
- Compute: laptop CPU + the box's RTX 5060 Ti 16 GB. No cloud spend without asking.
- `~/genesis-archive` is read-only. Never edit it.

## Environment notes
- Laptop: Python 3.12, numpy 1.26, no torch yet, 16 cores, 15 GB RAM, ~38 GB disk free.
  NVIDIA driver/library mismatch as of 2026-10-13 (`nvidia-smi` fails; likely needs a reboot after a driver update).
- The box (`ssh workstation`) has a GPU and is always on; use it for longer runs.
- Use `uv` for a project venv when we add dependencies.
