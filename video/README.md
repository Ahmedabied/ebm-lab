# The teaching video (lesson 01)

Ahmed's brief, the syllabus and the teaching method: `BRIEF.md`. Facts the script quotes, with sources:
`script/FACTS.md`. Referee reports on the script: `script/REFEREE-*.md`.

## Layout
- `script/NN_*.md` narration per chapter; each `## pNN | viz: …` block is one paragraph and its picture.
- `tts.py` narration audio (ElevenLabs v4 "Bella" for chapters 00–01, Kokoro `af_heart` locally for 02–09),
  cached per paragraph by text hash under `audio/NN/` with word timestamps and a `manifest.json`.
- `lib/` theme, real-data loaders (`data.py`), the voice lock (`narration.py`), widgets.
- `scenes/chNN.py` one ManimCE scene per chapter; `scenes/README.md` has the conventions.
- `data/extract_life.py` replays seed 203 bit-for-bit and dumps x, Q, weights per tick → `data/life203.npz`;
  `data/frozen_brain_test.py` re-derives the frozen / mirrored / birth-brain test on fresh seeds 500–514.
- `build.sh render|mux|concat|qc`; `provenance.py` → `out/PROVENANCE.md`.
- `out/`: `ebm-lab-lesson-01.qh.mp4`, `chapters.txt` (YouTube chapter timestamps), `thumbnail.png`, `PROVENANCE.md`, `qc/`.

## Rebuild
```
uv sync                                   # manim, numpy, kokoro, torch-cpu, soundfile, mutagen, requests
.venv/bin/python tts.py kokoro 02 03 04 05 06 07 08 09
.venv/bin/python tts.py eleven 00 01      # needs ELEVENLABS_API_KEY in .env (gitignored); free tier 10k chars/month
./build.sh render qh && ./build.sh mux qh && ./build.sh concat qh && .venv/bin/python provenance.py
```
Rendering reads `~/.TinyTeX` for `MathTex` (build.sh sets PATH). Low-quality QC: `./build.sh render ql NN && ./build.sh qc ql NN`.

## Chapter order and why
Data-flow order, with the body before the brain because the learning rule needs the body's number first:
00 cold open, 01 names, 02 maths, 03 world + senses, 04 body, 05 brain, 06 learning, 07 experiment, 08 code, 09 close.
The brief's original syllabus listed body/world after training; the referee-checked teaching method (connections per
block, the loop diagram growing one box at a time) argued for data-flow order.
