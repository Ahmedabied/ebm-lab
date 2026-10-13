# EBM lab: ground rules

Read `STATE.md` and `HANDOFF.md` first, then `IDEA.md`.

## Why this exists
Ahmed wants to learn energy-based models deeply, together, and have fun doing it. Genesis ended in burnout
and heavy token use. Keep this light: small experiments, quick feedback, teach as we go.

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
- Small steps. One experiment = one question. Run it, look at it, talk about it.
- Research phase -> design -> build. Don't build during a research phase.
- Decisions about what the experiment IS are Ahmed's. Ask; don't assume.
- Cheap first: numpy / small PyTorch on CPU or one GPU. No cloud spend without asking.
- `~/genesis-archive` is read-only. Never edit it.

## Environment notes
- Laptop: Python 3.12, numpy 1.26, no torch yet, 16 cores, 15 GB RAM, ~38 GB disk free.
  NVIDIA driver/library mismatch as of 2026-10-13 (`nvidia-smi` fails; likely needs a reboot after a driver update).
- The box (`ssh workstation`) has a GPU and is always on; use it for longer runs.
- Use `uv` for a project venv when we add dependencies.
