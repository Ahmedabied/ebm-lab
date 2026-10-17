# EBM lab

A playground for learning energy-based models deeply, by building Ahmed's idea: a growing network of
small energy-based models whose job is to make connections, that caches what it did during the day and
retrains during sleep, generation after generation. See `IDEA.md`.

Started 2026-10-13. Separate from Genesis: `~/genesis-archive` is a read-only research library we draw
knowledge from. No Genesis code is carried over.

## Layout

| Path | What |
|---|---|
| `IDEA.md` | the idea, verbatim, and its parts |
| `RESEARCH-PLAN.md` | the goal, hypotheses H1–H5, phases (v0.1; the creature-first reorder is in session 02's journal) |
| `DESIGN.md` + `DESIGN-AMENDMENTS.md` | creature v0's spec, and every change to it with its reason |
| `creature/` | the code: physics, world, body, senses, brain (EBM), baselines, sim, run, export |
| `tests/` | the laws (`uv run pytest`) |
| `experiments/` | harness, calibration, pilots, pre-registrations, `results/` (json + png) |
| `viewer/` | the run viewer (see its README) |
| `runs/` | exported lives to watch |
| `weights/` | the trained brains (final weights of seed 203, both worlds) + `try_it.py` to drop one into a new world |
| `CLAUDE.md` | ground rules for any agent working here |
| `STATE.md` | where the lab is right now (updated every session) |
| `HANDOFF.md` | what the next session does first |
| `research/genesis-digest/` | what Genesis learned, distilled and cited (A-E + `00-SYNTHESIS.md`) |
| `research/` | research seats R1–R4 (`03`–`06`), the proof-of-possibility note `07` with its scripts |
| `experiments/` | one folder per experiment, each with its own question, code, and results |
| `decisions/` | numbered decision records |
| `findings/` | durable results, each with the command that re-derives it (`01` negative, `02` the first positive learning result) |
| `sessions/` | one journal per session |
