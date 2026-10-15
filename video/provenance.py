"""Collect every chapter's provenance.json (written by Narration.finish from lib.data.note calls) into
out/PROVENANCE.md, with the fixed source list the script was written from."""
import json, glob, os
HERE = os.path.dirname(os.path.abspath(__file__))
rows = []
for f in sorted(glob.glob(os.path.join(HERE, "audio", "*", "provenance.json"))):
    ch = os.path.basename(os.path.dirname(f))
    for r in json.load(open(f)):
        rows.append((ch, r["label"], r["file"], r["field"], r["value"]))
out = ["# Provenance of every number shown in the lesson", "",
       "Every number on screen is read by the scene code from a lab file; nothing is typed in. Sources:", "",
       "- `runs/exp02-linear/203-ebm-td/run.json` (seed 203, arm ebm-td, commit 112e957): nightly weights, per-tick F, events, summary.",
       "- `video/data/life203.npz`: a bit-for-bit replay of that life (`video/data/extract_life.py`), adding the sensation x, Q, the weights after every tick, the TD targets and the fields.",
       "- `experiments/results/02_main_linear/results.json` and `02_main_report.md` (EXP-02, seeds 200–219); `experiments/results/01_main_linear/results.json` (EXP-01, seeds 100–119).",
       "- `video/data/frozen_brain_test.json` (`video/data/frozen_brain_test.py`, fresh seeds 500–514): the frozen / mirrored / birth-brain test re-derived for the lesson.",
       "- `research/07-proof-of-possibility/m3_bias.json` (proof seeds 300–319): the night-by-night turning bias.",
       "- `findings/01`, `findings/02`, `research/07`, `DESIGN-AMENDMENTS.md`, `decisions/0002`: every claim about what the experiments showed, with the referees' corrections applied.",
       "- The script's fact sheet with each number and its source: `video/script/FACTS.md`; referee reports: `video/script/REFEREE-*.md`.", "",
       "## Numbers shown, per chapter", "", "| chapter | what | file | field | value |", "|---|---|---|---|---|"]
for ch, l, f, fi, v in rows:
    out.append(f"| {ch} | {l} | `{f}` | {fi} | {v} |")
os.makedirs(os.path.join(HERE, "out"), exist_ok=True)
open(os.path.join(HERE, "out", "PROVENANCE.md"), "w").write("\n".join(out) + "\n")
print("wrote out/PROVENANCE.md with", len(rows), "rows")
