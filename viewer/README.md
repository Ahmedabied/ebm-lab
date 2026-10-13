# Run viewer

A read-only browser view of one creature's life. It shows only what the run logged.
It never re-runs the sim and never invents data.

## 1. Export a run

```
uv run python -m creature.export runs/<label>/<seed>
```

- Writes `runs/<label>/<seed>/run.json` (one file, everything the page needs).
- Prints the size, how many field snapshots were kept, and the `stride`.
- Budget is 5 MB by default (`--budget-mb N` to change it).
- A 20-day run at default config comes out at about 2.0-2.5 MB, so nothing gets dropped.
- If a run would go over the budget, the exporter keeps every k-th field snapshot
  (time downsampling only, never spatial). The header and the world panel then say
  "downsampled".

## 2. View it

```
cd /home/abied/ebm-lab && uv run python -m http.server 8765
```

Then open:

```
http://localhost:8765/viewer/?run=runs/smoke/1/run.json
```

- The `run=` path is **relative to the repo root** (the server root), not to `viewer/`.
- Only same-origin paths load. Full URLs (`http://...`, `//host/...`) are refused.
- With no `?run=`, the page offers a file picker for a local `run.json`.

**Keys:** `space` = play/pause, `left`/`right` = step 1 tick, `shift` + arrow = 10 ticks,
`home`/`end` = jump to the start/end.

## 3. What each panel means

### Header
- Label, seed, policy, git commit, source hash.
- The run summary: alive, days, food, poison, mean drive, first food tick, poison bites after first, H.
- Key config: sleep mode, growth, day learning, blend mode, sensor noise.
- **"full config"** expands to the whole config, the world ledger and the export info.

### World
- **Background** = the three chemical notes as colour (see the colour code below).
- **White triangle** = the creature, nose pointing along its heading.
- **Antennae**: orange = left, blue = right. The dots are exactly where `senses.py` reads the field.
- **White trail** = the last 160 ticks, fading. It is broken where the creature wraps around the torus.
- **Rings**: green = it ate this tick, pink = poison this tick, red = death.
- **Night**: the world goes dark and says "asleep".
- **Drawn with y pointing UP.** So a LEFT action turns the creature counter-clockwise on screen.
  The creature's left is your left.

### Timeline
- Scrub bar, play/pause, step buttons, speed (ticks per second).
- The badge shows the day number and DAY (awake) or NIGHT (asleep).
- The strip under the scrub bar is the whole life:
  - gold = day, dark blue = night
  - green ticks = eat, pink = poison, white = a hidden unit was added
- Click or drag the strip to seek.

### Body
- Three bars:
  - **Energy E**: out of E_max.
  - **Toxin X**: out of the highest X over the whole life (at least 0.05).
  - **Drive D**: out of the highest D over the whole life.
- Below them, **drive over the whole life**:
  - blue line = drive D
  - faint gold line = energy, on its own 0..E_max scale
  - dark bands = nights
  - green ticks at the bottom = eat, pink ticks at the top = poison
  - red line = death
- The part after the cursor is dimmed, so the line "fills in" as the life plays.
- Click or drag the plot to seek.

### Brain
- **Action energies F(x, a)** for LEFT, RIGHT and FORWARD this tick.
  - Green = lowest energy, so the most probable action.
  - `pi` = softmax(-F/T), recomputed in the page from the logged F and the config's T.
  - "chosen" marks the action actually taken. It is **sampled** from pi, so it is not always the lowest.
  - Bar axis: "this tick's range" (default) or "whole-life range". The numbers under the bars give the axis ends.
- **Hidden units H over life**: step plot, with nights shaded.
- **u matrix per night** (hidden units x 12 inputs), one small tile per night from `brain.npz`.
  - Blue = negative, orange = positive.
  - One symmetric colour scale shared by all nights. The panel says what its max |u| is.
  - Click a tile to jump to that night. The current night is outlined and drawn large.
  - Hover the large one to read single values.
  - Inputs: L.A..L.C = left antenna, R.A..R.C = right antenna, dA..dC = change of the mean,
    E/X = body, bias.
- **Per-night table**: night, day, end tick, H, plus whatever the sleep events logged
  (surprise from `sleep_start`; clip_frac, entropy, w_norm from `sleep_end`).
  - Columns a run did not log are hidden.
  - Click a row to jump to that night.

## 4. Colour code (fixed for all runs)

**Channels:** note A = red, note B = green, note C = blue.

**Linear world** (`blend_mode = "linear"`, and every run from before that field existed):
- food = A+B = **yellow**
- poison = B+C = **cyan**

**XOR world** (`blend_mode = "xor"`):
- food = A+B = **yellow**
- poison = A alone = **red**, or B alone = **green**

The legend under the world is built from the blend table that the exporter copies into `run.json`.

**Brightness** per channel = `log1p(v / 0.01) / log1p(0.3 / 0.01)`, clipped to 0..1.
- It is one fixed scale for every run, so two runs can be compared by eye.
- It is a display scale only. It is **not** what the creature senses
  (the creature senses `log1p(v / sense.c0)` plus noise).
- Values above 0.3 saturate. At default config the measured field max was about 0.23-0.29.
- Constants and reasoning: top of `creature/export.py`.

## 5. Limitations (honest list)

- **Items are not shown.** The run does not log item positions, by design.
  You see food and poison only as their smell.
- **The field during a night is stale.** Snapshots are only taken on waking ticks,
  every `snap_every` ticks (20 by default). So:
  - in the day, the field you see can be up to 19 ticks old
  - at night, it is the last waking snapshot, while the real field keeps diffusing
- **No weights before the first night.** `brain.npz` only holds end-of-night snapshots,
  so there is no heatmap before night 0.
  - A creature that dies before its first night has no `brain.npz` at all.
  - At the default config on 2026-10-13, the EBM died on day 0 for every seed tried (1-40),
    so default EBM runs show F bars but no u heatmaps.
- **Only u is drawn.** v, c, w and b are in `run.json` (`brain[i]`) but not shown.
- **Night tiles are matched to `sleep_end` events by order.** That matches how `sim.py`
  writes them today. If that ordering ever changes, the tile labels would be wrong.
- **The blend legend uses today's code.** It is read from `creature.world.BLENDS` in the
  current source at export time, not from the run's own source. If the run's `source_hash`
  differs from today's, `run.json` adds a note saying so (shown next to the legend).
- **Baselines** (random, braitenberg, oracle, tabular_q) log no F and have no brain.
  The panel says so, and still marks the chosen action.
- **Speed**: tested in headless Chrome on runs up to 9000 ticks. Very long runs make the
  first load slower, because every snapshot image is decoded up front.

## 6. How this was verified (2026-10-13)

- `node --check` on the page script.
- Headless Chrome via `~/.local/bin/cdp`, at a 1280 px wide viewport, on:
  - the smoke run
  - a 20-day braitenberg run (no F)
  - a 6-day xor-world EBM fixture with the new sleep instruments
  - an older 20-day EBM fixture
- The EBM fixtures were made with **metabolism switched off**, only so that nights and
  `brain.npz` exist to test against. They are **not results** and were deleted after testing.
- Checks on every page: no console errors, no horizontal scroll.
- A crafted `run.json` with HTML/script payloads in the label, policy, commit, actions,
  summary and blend mode rendered as plain text and ran nothing. A remote image URL in
  `fields.png` was refused.
- Screenshot: `viewer/_smoke.png` (smoke run at t=300).
