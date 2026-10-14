# The teaching video — brief (locked 2026-10-15, before Ahmed compacts)

## Ahmed's prompt, verbatim (API key redacted; it lives in `video/.env`, gitignored, chmod 600)
> ok ill take your word for it this was an amazing session im very proud of it, before the next session
> i need to learn more, make me a youtube video using this https://github.com/3b1b/manim and this
> [ELEVENLABS KEY → `video/.env`] is eleven labs key you can use eleven labs v4 with a soft girl voice to
> teach me the math, first the conecpts- namings what it means and use real life examples reflect
> complex concepts on a simplar thing in real life - teach me the math of it from the begenning and why
> does it work - teach me the math of an edm and an ebt and why does it work, teach me the experment and
> why does it work take me a step by step use examples alot it makes me understand - and in math explan
> what each number and symbol represents and why is it there and how it ties to eachother and other
> things and the code of the model itself visulaize alot moving visulaizations make things soo much
> better for me
>
> be the teacher i never could find please <3
>
> ultrathink feel free to exhaust all credits on elevn labs i dont use them also lock this prompt in your
> notes and the documentation of this session and the one before so i can compact so you can have a
> fresh ctx window

("edm" and "ebt" read as: the energy-based model, and energy-based training, i.e. the learning rules.)

## Who it is for (from memory, non-negotiable design rules)
Ahmed: dyslexia + ADHD; reads in tight word chunks with clear paragraph separation; visibility over
contrast; scannable headings and bold; warm teaching tone, bold for instructions, soft for reactions.
Therefore: **one idea per screen; few words on screen, big; the voice carries the explanation; every
symbol gets pointed at while it is named; moving pictures before equations, equations built one term at
a time with the term lighting up as it is spoken; real-life analogy first, then the math, then the code;
chapters of 4–8 minutes with a recap card; 60 fps; no wall of text, ever.** Everything shown must be
real: the creature frames, the weights, the numbers come from the lab's own `run.json` /
`results.json` / `brain.npz`, never invented (Ahmed's rule: "nothing is synthetic").

## Facts established before compaction (2026-10-15 00:33)
- **ElevenLabs:** `eleven_v4` and `eleven_v4_turbo` exist (also v3). The account is the **free tier:
  10,000 characters per month**, 0 used before the sample. A 150-character sample took 10.3 s of
  audio, so **10k characters ≈ 11 minutes of speech**. "Exhaust all credits" = ~11 minutes of voice.
  Sample (voice Jessica, v4): `video/audio/sample_jessica_v4.mp3`. Candidate soft female voices with
  ids: Jessica `cgSgspJ2msm6clMCkdW9` (playful, bright, warm), Bella `hpp4J3VqNfWAUOO0d1Us`
  (professional, bright, warm, educational), Lily `pFZP5JQG7iQjIQuC4Bku` (velvety, educational),
  Alice `Xb7hH8MSUJpSbSDYk0k2` (clear educator), Simran `TRnaQb7q41oL7sV0w6Bu` (sweet, playful).
- **Decision needed from Ahmed (ask first thing after compaction, with the sample paths):** the full
  syllabus below is ~40–60 minutes of narration (~35–55k characters). Options:
  A. Upgrade ElevenLabs for one month (Starter 30k chars ≈ $5; Creator 100k ≈ $22; his cloud-cost rule:
     ask before spending; he said he doesn't use the account).
  B. ElevenLabs v4 for ~11 minutes (the opening + the concepts chapter, the parts where warmth matters
     most) and a free local voice for the rest (Kokoro-82M, soft female voices `af_heart`/`af_bella`,
     CPU, Apache-2.0; make a 30-s sample so he can hear it). Mixed voices is a cost; say so.
  C. One ~11-minute video now (concepts + the energy formula), the rest next month when the quota resets.
  Default if he says "you decide": B, with Jessica for the voiced chapters.
- **Manim:** the linked repo is 3b1b's `manimgl`, which needs an OpenGL window (this laptop's GL goes to
  llvmpipe; see memory). We use **ManimCE 0.22** (the community fork of the same project, Cairo
  renderer, headless, same look). Installed in its own env: `~/ebm-lab/video/.venv` (`uv`). Tell Ahmed
  this swap once; it is the same lineage.
- **LaTeX** (needed for `MathTex`): no system TeX, sudo needs a password → **TinyTeX installed in
  `~/.TinyTeX` without sudo** with ManimCE's package list (install log `/tmp/tinytex-install.log`,
  `/tmp/tlmgr.log`). Verify with a one-formula render before building anything.
- Tools present: ffmpeg 6.1, sox, 16 cores, 15 GB RAM, 35 GB disk free. Renders at 1080p60 on CPU.
- No screen popups: write the mp4 to disk and give the path. YouTube upload is Ahmed's.

## Pipeline (build in this order; each step verified before the next)
1. `video/script/*.md`: the narration per chapter, written for the ear (short sentences, analogies),
   with `[[cue:name]]` markers where an animation beat starts. Count characters per chapter.
2. `video/tts.py`: per paragraph → ElevenLabs `/v1/text-to-speech/{voice}/with-timestamps`
   (`eleven_v4`, mp3_44100_128) → `audio/<chapter>/<para>.mp3` + the character alignment json
   (gives word timings for cue sync). Never re-generate a paragraph that exists (quota). Kokoro path
   for the local-voice chapters if option B.
3. `video/scenes/*.py` (ManimCE): one Scene per chapter; each animation beat's run_time is set from the
   paragraph's audio duration and the cue timestamps, so picture and voice stay locked.
   Data loaders read `../runs/exp02-linear/203-ebm-td/run.json` (fields, creature, antennae, F per
   tick), `../experiments/results/02_main_*/results.json` (the bars), `brain.npz` is not committed:
   regenerate with the command in `findings/02` or use the per-night `brain` arrays inside `run.json`.
4. `video/build.sh`: render each scene at 1080p60 (`-qh --fps 60`), mux audio with ffmpeg, concat
   chapters, write `out/ebm-lab-lesson-01.mp4`, a `chapters.txt` (YouTube chapter timestamps), a
   thumbnail PNG, and `out/README.md` with every source number's provenance.
5. Headless QC: extract 1 frame per 10 s, look at them (Read), check text size, overlap, legibility;
   listen-check by transcribing one chapter (whisper if present) against the script.

## Syllabus (the chapters; each = analogy → picture → math → code → recap)
0. **Cold open (1 min):** a real life replaying (seed 203, the learner): fields in colour, antennae,
   the three energies as bars; "by the end you will know what every number here means".
1. **The names (concepts).** Energy (a landscape; a ball rolls to the valley); model (a machine with
   knobs); energy-based model (a machine that scores every option with a height, and prefers low);
   temperature (how much the table shakes); weight (a knob); vector (a list of readings);
   dot product (how much two lists agree); gradient (which way is downhill); learning rate (step size);
   lesson/reward (the body's "better or worse" number); drive (how far from comfortable: hunger as a
   bowl); value (how good is this spot, counting the future); policy (the habit of choosing).
2. **Math from the beginning.** Lists and weighted sums (the 12 senses × the 12 knobs); exponent and
   why e; softmax (turning heights into odds; the Boltzmann rule; what T does, animate the three bars
   melting as T rises); log (why: big ranges, products into sums; decibels, the antenna's log1p);
   slope and gradient (one knob, then many; the ball on a hill); expectation (an average over chances).
3. **The EBM, symbol by symbol.** F(x,a) = −b_a − w_a·x − Σ_h softplus(c_h + u_h·x + v_{h,a}).
   Point at every symbol: x (the 12 senses), a (which of the 3 moves), b (the move's baseline mood),
   w (the move's preference knobs for each sense), h (a committee of small detectors), c (a detector's
   threshold), u (what it listens to), v (what it says about each move), softplus (a soft "count it if
   positive": animate ReLU → softplus), Σ (the committee votes add up). Why "free" energy: show the
   two states of one hidden unit, sum them, watch log(1 + e^z) appear. Then π = softmax(−F/T).
4. **Energy-based training (why it works).** The contrastive rule: lower the energy of what the body
   liked (positive phase), raise the energy of what the brain would have done anyway (negative phase);
   show what happens with only the positive phase (everything sinks; the praise-without-comparison
   analogy); show it equals the policy gradient. Then the rule that actually worked: Q = −F, the
   Bellman promise "now = this tick's lesson + γ × the best next", the moving target, ε-greedy
   (mostly the best, sometimes a try), γ as "how much tomorrow counts". Use the day-trip-planning
   analogy for γ. Why it works: consistency pulls every estimate toward the truth (animate a chain).
5. **The body as the only teacher.** D = (1−E)² + X²: a bowl; E and X as the ball's position; r = D
   before − D after as how far it rolled toward the bottom; why squared; why metabolism makes every
   quiet tick slightly bad; death at E = 0. Food raises E, poison raises X then drains E.
6. **The world and the senses.** Diffusion (heat on a plate; the 4-neighbour rule; α ≤ ¼ or it
   explodes, animate); decay; food = A+B, poison = B+C, the creature never sees the labels; two
   antennae; contrast (L−R)/(|L|+|R|+ε) (why normalise: the same turn signal near and far); log1p
   (ears, decibels).
7. **The experiment, step by step.** EXP-01: it did not learn (the bars); why (the nightly step 8–16×
   the weights, animate the policy lurching between corners); the swarm and the two hostile referees
   (what a referee caught, with the bandit counterexample as a picture); EXP-02's arms as characters;
   the result bars (real numbers); **the weights themselves changing night by night** (animate the
   w heatmap from the real brain, the "turn toward A" weight crossing zero); the frozen-brain test;
   what the referees would not let us say; the pivot (brain cells: learn, connect, function, die, born).
8. **The code.** `creature/brain.py`: `F`, `policy`, `act`, `grad_negF`, `learn_q`; `creature/sim.py`:
   `q_targets`, `_online_q`; `creature/body.py`: `drive`, `tick`. Each line beside its formula with
   the symbol and the variable name highlighted together (w ↔ `th["w"]`, softplus ↔ `np.logaddexp`,
   Σ_h ↔ `.sum(axis=1)`, γ ↔ `gamma`, ε ↔ `eps`).
9. **Close.** What is proved, what is not, the five open doors, "next session we pick one".

## Verification rules for this build
Every number spoken or shown is read from a lab file by the scene code (no retyping). A one-page
`out/PROVENANCE.md` lists each: file, field, value. The script is checked against `findings/02`,
`research/07` and `DESIGN.md` before recording (the referees' corrections apply to the lesson too:
no "gravity well", no "beats tabular Q", no "3 numbers"). One hostile-referee pass on the script for
mathematical honesty before any audio is spent.
