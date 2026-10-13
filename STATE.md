# STATE — EBM lab

Updated 2026-10-13, end of session 02. Commit: see `git log` (everything below is committed).

## Where we are
- **Creature v0 is built, tested, visualised and measured.** 23 law tests pass (`uv run pytest`).
  One life runs in ~0.1 s. Code: `creature/` (physics, world, body, senses, brain, baselines, sim, run, export).
- **The first pre-registered experiment (EXP-01) is done and its main prediction FAILED:** within-life
  EBM learning did not beat no learning (973 vs 1224 ticks, linear world, 20 fresh seeds). The pilot's
  2178 on tuning seeds did not replicate. Full write-up: `findings/01_exp01_within_life_learning.md`.
  Plots: `experiments/results/01_main_{ticks,food}.png`.
- **Viewer works:** `viewer/index.html` (vanilla JS, verified headless). Exported lives to watch:
  `runs/exp01-linear/100-{ebm,braitenberg,oracle,tabular_q}/run.json`, `runs/exp01-xor/100/run.json`.
  Serve: `cd ~/ebm-lab && uv run python -m http.server 8765` → `http://localhost:8765/viewer/?run=runs/exp01-linear/100-ebm/run.json`.
- **Research seats R1–R4 filed** (`research/03`–`06`), each ending with v0 recommendations and
  questions for Ahmed. Adopted amendments: `DESIGN-AMENDMENTS.md` A1–A13; the not-yet-implemented
  recommendations are listed at its foot.

## The design in one breath
3 diffusing chemical notes; items emit blends (`linear`: food A+B / poison B+C; `xor`: food = A+B
together, poison = A or B alone); a body with energy, toxin and a homeostatic DRIVE (an energy); the only
lesson is the drive's change; a conditional-RBM free-energy brain over (contrast, mean, change, body) × 3
actions; π = softmax(−F/T); contrastive policy-gradient learning; day = act + cache; night = importance-
corrected replay + downscaling + (placeholder) growth; baselines random / braitenberg / tabular_q / oracle.

## Verified by Claude this session (from execution)
- All numbers in `findings/01` and `decisions/0001` come from `experiments/results/*/results.json`.
- Zero-weight EBM lives as long as a random walker (loop is fair): `01b_diag_uniform`.
- Finite-difference gradient check of the learning rule passes to 1e-6.

## Known limitations of v0 (do not over-read)
- No seasons, no generations, no critic, no generative dreaming, placeholder growth rule.
- Items never shown in the viewer (by design); field snapshots only on waking ticks.
- Hyperparameters T/lr/clip were chosen on seeds 0–7; those seeds are burned for all future experiments.

## Environment
- Laptop venv via `uv` (numpy 2.5, pytest, matplotlib). No torch, none needed yet. GPU not needed.
- Box: RTX 5060 Ti 16 GB, disk 97% full. Not used.
- Token note: session 02 used ~10 Opus/Fable agent runs (research ×4, viewer ×1) + heavy main-thread work.
