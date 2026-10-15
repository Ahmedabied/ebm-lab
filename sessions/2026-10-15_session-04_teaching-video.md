# Session 04 (2026-10-15) — the teaching video, lesson 01

Ahmed: "make me the lesson ... research what I asked you last session ... give it some love". Brief:
`video/BRIEF.md` (locked the session before). Deliverable: `video/out/ebm-lab-lesson-01.qh.mp4`
with `chapters.txt`, `thumbnail.png`, `PROVENANCE.md`.

## What was built, in order
1. **Real data first.** `video/data/extract_life.py` replays seed 203 (`ebm-td`, linear) bit-for-bit
   (summary MATCH) and dumps x, Q, the weights after every tick, TD targets and fields → `life203.npz`.
   `video/data/frozen_brain_test.py` re-derives the frozen / mirrored / birth-brain test on fresh seeds
   500–514: 5250 on 15/15; mirrored 1013 (0/15); birth 1419 (2/15).
2. **A finding the lesson had to tell honestly:** in seed 203 the steering weight that grows is the
   contrast-**B** pair (positive on 100% of ticks), not the A pair (negative on days 0–1, crosses zero on
   day 3, ends small positive). `world.py` still says "B carries no information"; research/07 §2.2 has
   the correction. The lesson says so.
3. **Script** (`video/script/00–09`, ~55k chars ≈ 58 min narration) in data-flow order (names, maths,
   world+senses, body, brain, learning, experiment, code, close), every block: need → why this operation
   (alternative failing) → real-life example → the creature's real number → connections → strip-down,
   with pause-and-predict beats. `FACTS.md` = every number with its source.
4. **Two hostile referees on the script** (math honesty: 6 blockers / 11 major / 18 minor; teaching
   coherence: 20 major / 40 minor), all folded in; a re-check found one new blocker (xor stated
   backwards) and one overclaim (">99% on most seeds"), fixed; verdict then CLEAR TO RECORD. Reports:
   `video/script/REFEREE-*.md`. Blockers worth remembering: dump INDEX ≠ run TICK (350/day incl. sleep
   vs 300 waking); the weights that chose at index i are theta recorded at index i; diffusion moves
   4α of the way, not α; the 2-knob forager is 10/10 (seeds 340–349), the 5-number one 20/20.
5. **Voice.** Option B as decided: ElevenLabs v4 "Bella" for chapters 00–01 (8,766 of the 10,000 free
   characters, ~10.4 min), Kokoro-82M `af_heart` locally for 02–09 (free, word timestamps). Cloudflare
   checked read-only: Workers AI has MeloTTS and Deepgram Aura (paid partner models), no ElevenLabs
   model of its own, so it adds nothing. Per-paragraph cache keyed by text hash (`video/tts.py`).
6. **Scenes.** ManimCE 0.22, Lexend, warm dark palette; `lib/` = theme, real-data loaders, the voice
   lock (`Narration`: the scene drives the timeline, audio is placed at recorded offsets, word-level
   cues), widgets. Chapters 00/09 by the orchestrator as the pattern; 01–08 by eight forked builders in
   parallel, each rendering at 480p and inspecting its own frames; lib bugs they reported were fixed
   (Bars range/labels, BodyBars scaling, Landscape .width collision, loop arrows, stale-audio manifests).
7. **Build.** `build.sh render qh` (1080p60) → `mux` (ffmpeg adelay/amix from `timeline.json`) →
   `concat` → `chapters.txt`; `provenance.py` collects every `note()` into `out/PROVENANCE.md`.

## Lessons
- Referee the SCRIPT before spending voice: the first draft had six false spoken numbers, all from
  index/tick confusion and from quoting a result's seed count from memory.
- "No synthetic numbers" needs a replay dump: run.json alone does not keep x or the per-tick weights.
- Mixed voices (paid + local) are the cost of the free tier; the on-screen caption at chapter 02 says so.
