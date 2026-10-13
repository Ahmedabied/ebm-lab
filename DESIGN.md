# DESIGN — creature v0 (2026-10-13, session 02)

The smallest honest version of Ahmed's idea: a creature that is **not told what food is**, whose
**body's chemistry teaches it**, whose brain is an **energy-based model made of small units that form
connections**, that **caches its day and retrains at night**, and that **passes priors to the next
generation**. Built in numpy, runs in seconds, visualised, documented so it can scale later.

Status of each section: **[fixed]** = decided; **[default]** = a reasonable value, may change;
**[⚑]** = Ahmed's call; **[R?]** = waiting on research seat R1–R4 (`research/03–06`).

---

## 0. The laws the code must obey (tests enforce these)

1. **No label anywhere the creature can see.** The words "food" and "poison" exist only in the
   world's bookkeeping and the metrics. The creature senses chemical notes and its own body. [fixed]
2. **The body is the only teacher.** The learning signal is the change of the body's drive. [fixed]
3. **Determinism.** One `numpy.random.Generator` per run, seeded. Same seed → identical log, byte for byte.
   Logging and metrics never draw from it. [fixed]
4. **Conservation.** Every unit of mass that leaves the world is accounted for (eaten, decayed, created).
   A test closes the books each tick. (Genesis found `eat()` creating 2.8% of intake from nothing.) [fixed]
5. **Every learned thing must be shown to change an action.** A test proves that the brain's output
   depends on its weights, and that learning moves behaviour. (Genesis's heard words never steered
   behaviour.) [fixed]
6. **Every number in `findings/` carries the command and commit that re-derive it.** [fixed]
7. **Every claim has its control** (see §7). [fixed]

---

## 1. The world (`creature/physics.py`, `creature/world.py`)

- Torus grid **H×W = 48×48** [default]. Three chemical notes **A, B, C**, each a float32 field. [fixed: 3 notes]
- Physics per tick, in order: **diffuse** (4-neighbour Laplacian, coefficient α = 0.18 [default,
  stable for α ≤ 0.25]) → **decay** (keep κ = 0.95 [default]) → **emit** (sources add to fields). Physics
  takes a world and returns a world; no randomness lives in physics.
- **Sources**: `food` items emit blend **(A, B, C) = (1, 1, 0) · mass**; `poison` items emit **(0, 1, 1) · mass**.
  They share note B on purpose: blends overlap, so "B means food" is a wrong lesson the creature can
  learn and must unlearn. [fixed]
- Items have **mass**. Eating transfers mass from the item to the body (yield η = 1.0 energy per mass
  [default]). Food items regrow: when total food mass < budget, a new item spawns at a random cell
  (RNG draw, bookkept as "created"). Poison items are permanent and not consumed [default] (eating
  poison does not deplete it; the toxin enters the body).
- **Seasons** [v1, not v0]: the blend→effect mapping can be swapped on a schedule. The architecture
  must allow it (effects are a table in `world`, not constants in `body`).

## 2. The body (`creature/body.py`)

- State **h = (energy E, toxin X)**. Per tick: `E -= metabolic_cost` (0.002 [default]; moving costs
  extra 0.001 [default]); `X *= toxin_decay` (0.98 [default]); `E -= X * toxin_drain` (0.01 [default]).
- Eating food: `E += η·mass_eaten` (capped at E_max = 1.0). Eating poison: `X += mass_eaten·toxicity` (0.5 [default]).
- **Death**: E ≤ 0. (Toxin kills by draining energy, not by a second rule.) [default]
- **Drive** (Keramati & Gutkin 2014, via Genesis report 02): **D(h) = w_E·|E* − E|^n + w_X·|X* − X|^n**
  with setpoints E* = 1.0, X* = 0, exponent n = 2 [default, R1 may change], weights w_E = 1, w_X = 1 [default].
  **The drive is an energy.** The creature's whole life is lowering it.
- **The lesson** at tick t: **r_t = D(h_{t−1}) − D(h_t)**. Metabolism gives a constant negative drift
  (uninformative; removed by the baseline); eating gives spikes. Nobody tells the creature which is which.

## 3. The senses (`creature/senses.py`)

- Two antennae at ±θ_ant (45° [default]) and length ℓ = 1.5 cells [default] from the centre, bilinear
  field reads. For each note k: **left_k, right_k**. Plus **temporal change** of the mean reading
  (now − previous tick) per note. Plus body state **(E, X)**. Plus a constant 1.
  x ∈ R^(3+3+3+2+1) = R^12. [default; R2 may change the encoding]
- Readings are **log-compressed** (`log1p(c / c0)`) so a strong source does not saturate everything. [default]

## 4. The brain: an energy-based model (`creature/brain.py`)

**Why an EBM.** Acting = finding the action with the lowest energy given the sensation. Learning =
lowering energy on what the body rewarded, raising it on what the brain itself would have done. The
hidden units are the "small models"; their weights to inputs and actions are the "connections".

- Actions **a ∈ {LEFT, RIGHT, FORWARD}** [fixed for v0]. (LEFT/RIGHT turn by Δθ = 30° and move; FORWARD moves 1 cell.) [default]
- **Free energy** (conditional RBM with hidden units marginalised):
  `F(x, a) = −b_a − w_a·x − Σ_h softplus(c_h + u_h·x + v_{h,a})`
  Parameters θ = {b ∈ R^3, w ∈ R^{3×12}, c ∈ R^H, u ∈ R^{H×12}, v ∈ R^{H×3}}. H starts at **H₀ = 4** [default].
- **Policy**: `π(a|x) = softmax_a(−F(x,a)/T)`, T = 1.0 [default; R1]. Exact: only 3 actions, so no
  sampling is needed for the partition over actions.
- **Learning rule** (contrastive, body-taught). For a cached step (x, a, R) where R is the eligibility-weighted,
  baseline-subtracted lesson (see §5):
  `Δθ = η_lr · R · [ −∂F(x,a)/∂θ + Σ_{a'} π(a'|x) · ∂F(x,a')/∂θ ]`
  The first term lowers the energy of what was done (positive phase). The second raises the energy of
  what the brain itself prefers (negative phase: the brain's own "fantasy" is pushed up). This is the
  policy gradient for a Boltzmann policy [R1 confirms]. η_lr = 0.05 [default].
- **Growth** [v0 includes it as a switch]: after a night, if the mean |R| over the day's cache stayed
  above a threshold (the brain is still being surprised), add one hidden unit with small random weights.
  Budget: each hidden unit costs `unit_cost` energy per tick (0.0002 [default]) so bloat is paid for. [R3 may change the rule]

## 5. Day and night (`creature/sim.py`)

- A **day** = `day_len` ticks (400 [default]). The creature acts and **caches** every (x, a, r).
- **Credit**: the lesson for step t is `R_t = Σ_{k≥0} λ^k r_{t+k} − baseline`, λ = 0.9 [default; R1],
  baseline = running mean of the same quantity. (A steering decision gets credit for the meal that
  follows it.)
- **Day learning** [⚑ default: OFF]: optionally apply the rule online with a small rate.
- **Night (sleep)** = `sleep_epochs` passes (3 [default]) over the cache in shuffled mini-batches, with
  the same rule; plus **downscaling**: θ *= (1 − δ), δ = 0.01 [default; R3]. Interleaving: the cache
  keeps the last `cache_days` days (3 [default]) so old lessons are replayed with new ones.
- Sleeping costs ticks during which the body still metabolises (`sleep_len` = 50 ticks [default]).
- **Life** = repeat until death or `max_days`.

## 6. Generations (`creature/evolve.py`) [v0: minimal]

- Population N = 24 [default], each creature lives alone in its own world (same world seed per
  generation across creatures for a fair comparison [default]).
- **Genome** = the initial brain weights θ₀ **plus** (η_lr, T, λ) [default; R4 decides what is inherited].
  **Learned weights are NOT inherited** (Darwinian / Baldwin). Ablation: Lamarckian ON.
- Fitness = days survived, tie-break by mean drive [default]. Truncation selection (top 25%), Gaussian
  mutation σ = 0.05 [default]. Generations G = 20 [default].
- **Severed-inheritance null**: children get θ₀ re-drawn at random with the same statistics. If that
  does as well, "inheritance helps" is false.

## 7. Baselines and controls (`creature/baselines.py`, `experiments/`)

| Name | What | Role |
|---|---|---|
| `random` | uniform action each tick | floor |
| `braitenberg` | hand-wired: turn toward the stronger side of note A, away from note C | "steering is easy" baseline |
| `braitenberg-learned-sign` | same wiring, but the sign per note is learned from the body (one scalar per note) | the smallest learner |
| `tabular-q` | Q-learning on a discretised sensation with the same lesson signal | standard RL baseline |
| `oracle` | sees item positions; greedy nearest food, avoids poison radius | upper bound (not "optimal", say so) |
| `ebm` | §4 brain | the subject |
| `ebm-nosleep` | §4 with online learning only, matched number of updates | tests sleep |
| `ebm-sleep-today-only` | cache holds only today | tests interleaving |
| `ebm-sleep-noise` | night applies random weight noise of matched norm | tests that it is the content, not the perturbation |
| `ebm-fixed-final` | no growth, H = the grown system's final H from day 1 | tests growth |
| `ebm-random-growth` | growth on a timer, not on surprise | tests the growth rule |
| `ebm-lamarck` | inherits learned weights | tests inheritance mode |
| `ebm-severed` | θ₀ re-drawn each generation | tests inheritance at all |

**Metrics** (pre-registered per experiment; R2 may add chemotaxis index): lifespan (ticks),
mean drive over life (allostatic load), food mass eaten, poison mass eaten, time-to-first-food,
fraction of ticks within 3 cells of food, "poison approaches after first poisoning" (did it learn?).
**Seeds ≥ 10 per arm**, mean ± 95% CI (bootstrap). Report every arm, including the losers.

## 8. Logging (`creature/log.py`) and the viewer (`viewer/`)

- One run → one directory `runs/<label>/<seed>/` with `meta.json` (all parameters, commit, source hash),
  `ticks.jsonl` (per tick: t, day, phase, x, y, heading, action, E, X, D, r, F_left/right/forward),
  `events.jsonl` (eat, poison, sleep-start/end, grow, death), `fields.npz` (every `snap_every` ticks,
  the three fields, downsampled), `brain.npz` (weights at each night).
- Viewer: a single HTML file that loads a run and animates: fields as RGB (A→red, B→green, C→blue, so
  food is yellow and poison is cyan), the creature with heading and trail, body bars, the three action
  energies live, day/night, hidden-unit count, drive curve. Served with `python -m http.server`.

## 9. What v0 does NOT do (so nobody over-reads it)

- No seasons (meaning never flips) → v0 cannot test continual-learning savings. v1.
- No generative dreaming (sampling sensations from the model) → the negative phase is over actions only.
- One creature per world → no social anything.
- Growth is a crude surprise-trigger → the growth *rule* is a placeholder until R3.

## 10. Open [⚑] for Ahmed
1. Day learning ON or OFF by default (OFF makes sleep the only learning, the cleanest test).
2. Grid size / day length if runs feel too slow or too fast to watch.
3. Which baseline table rows to run first.
