# STATE — EBM lab

Updated 2026-10-13, session 01.

## Where we are
- **Phase: research done, design not started.** No experiment code exists yet.
- Lab created at `~/ebm-lab` (git, branch `main`).
- Knowledge base written:
  - `research/genesis-digest/00-SYNTHESIS.md`: the one-page version. **Start here.**
  - `research/genesis-digest/A–E`: architecture, reports 01–12, reports 13–24, methodology, process (all cited).
  - `research/01-ebm-sleep-growth-literature.md`: EBM / sleep / growth literature, 36 sources checked,
    6 secondhand and flagged, an 8-step learning ladder.

## Verified this session (by Claude, from source)
- Genesis's heard-symbol reading never enters action choice (`agents.py:5733-5839`; no read of
  `pending_meaning` outside `_hear_and_learn`).
- The 8-step ladder and the denominator corrections, read directly in the digests at their cited lines.

## Not verified
- Each digest's other individual citations were written by subagents and spot-checked only.

## Environment
- Laptop: Python 3.12, numpy 1.26, **no torch**; 16 cores, 15 GB RAM, ~38 GB free disk.
- **`nvidia-smi` fails: driver/library version mismatch** (likely needs a reboot after a driver update).
- Box (`ssh workstation`) available for longer runs.

## Open decisions (Ahmed's)
See HANDOFF.md.
