# Scene conventions (read before writing a chapter scene)

One file per chapter: `scenes/chNN.py`, class `ChNN(Scene)`. Pattern: `scenes/ch00.py`.

## Voice lock
```python
n = Narration(self, "05")          # loads audio/05/manifest.json (durations + word timestamps)
d = n.say("p03")                   # waits for the previous paragraph to end, starts p03, returns its duration
n.until("p03", "softplus")         # wait until that word is spoken (first occurrence; occurrence=1 for the second)
n.remaining()                      # seconds left in the current paragraph (use for the last play's run_time)
n.end()                            # wait until the current paragraph's audio ends
n.finish()                         # at the very end: waits, writes audio/05/timeline.json (build.sh needs it)
```
Rules: every paragraph gets exactly one `n.say`. Animations inside a paragraph should fill roughly its
duration (`d`); use `n.until` so a symbol lights up on its word and `n.remaining()` for the last run_time
(`max(n.remaining() - 0.2, 0.5)`). Never call `self.wait` with a guessed number where `n.until`/`n.end` fits.
If audio for a paragraph does not exist yet, the duration is estimated (chars/16), so scenes work before TTS.

## Pictures
- `WorldView()` real fields + creature (set_tick(i) with a ValueTracker updater); `Bars(vmax=..)` three bars;
  `BodyBars()` E/X/D; `Bowl()` D against E; `Heatmap(W, col_labels=life()['input_names'])`; `LoopDiagram()`
  (`self.play(loop.lit("Brain"))`, `loop.set_done([...])`); `Landscape()` three dips + marble; `formula_F()`
  the F formula split into coloured pieces (index: 0 F(x,a) 1 = 2 b 3 w·x 4 Σ_h 5 softplus( 6 c 7 u·x 8 v 9 )).
- `pause_card(self, "question")` for a pause-and-predict beat; `title_card(self, "5", "The brain")`; `header()`, `caption()`.
- Colours: `C_X` readings, `C_W` knobs, `C_BIAS` b, `C_HID` committee, `C_SP` softplus/highlights, `C_T` dials (T, ε, γ),
  `C_E`/`C_XT` energy/toxin, `MOVE[k]` per move, `C_GOOD`/`C_BAD` lessons, `FOOD`/`POISON`.
- Text: `T("words", SZ_BODY)`; sizes SZ_TITLE 56, SZ_BIG 44, SZ_BODY 34, SZ_SMALL 26, SZ_TINY 20. Few words per screen.
- Real numbers: read them (`life()`, `run()`, `results()`, `frozen()`, `m3()`, `theta_at(i)`, `F_of(theta, x)`), never type
  them. Call `note(label, file, field, value)` for each number shown so PROVENANCE.md can list it.

## Gotchas (measured)
- An updater that changes TEXT (digits) changes the mobject family: never let it run during FadeIn/FadeOut/Transform of
  that mobject: set the value once, play the fade, then `add_updater`; `clear_updaters()` before fading out.
- `ImageMobject`: use `set_resampling_algorithm(RESAMPLING_ALGORITHMS["nearest"])` for the 48×48 fields.
- Keep everything inside the 14.2 × 8 frame; test with `./build.sh render ql NN && ./build.sh qc ql NN` and LOOK at
  `out/qc/NN/sheet.png` (frames every 10 s). Fix overlaps and anything smaller than SZ_TINY.
- Lexend is the font for all `Text`; `MathTex` renders through TinyTeX (`PATH` set by build.sh).
