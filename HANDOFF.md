# HANDOFF — next session

## First (10 minutes)
1. Read `STATE.md`, then `findings/01_exp01_within_life_learning.md` (the negative result and what it points to).
2. Run `uv run pytest -q` (expect 23 passed) and `uv run python -m creature.run --policy ebm --seed 100 --days 5`.
3. If Ahmed hasn't watched a life yet: serve the viewer (STATE.md) and watch `100-ebm` vs `100-braitenberg`.

## Ahmed's decisions pending (ask, don't assume)
From `findings/01` §"What it points to": which lever first?
  (1) critic / actor-critic + entropy bonus (R1), (2) generations with inherited learning-rule genes and
  innate valences (R4), (3) a protected childhood, (4) an `ebm-signfeatures` arm to test whether Q wins
  on its hand-built features.
Also open from the research seats (each file's "Questions for Ahmed"): should valence flip mid-life
(seasons) now; is sensor noise OK; should the brain grow within life or across generations; is the
per-unit cost physics or a gene; dreams now or v0.1.

## Then (whichever lever he picks), the protocol
- Pre-register in `experiments/EXP-02-prereg.md` BEFORE running: arms, seeds (>= 20; never 0-7 or 100-119
  for tuning), primary metric, predictions.
- Tune only on a declared pilot with its own seeds; burn them.
- Write `findings/02` with the command, the commit, the table, the CIs, every arm.

## Not yet implemented but adopted in principle (DESIGN-AMENDMENTS.md foot)
R3 growth rule (candidate units vs permutation null), fast+slow weights, generative dreaming (v0.1),
R4 genome (log lr, log T, lambda, H0, growth threshold, placebo gene) with `severed` and `random-parents`
nulls and common-garden tests, R2 `braitenberg-learned-sign` baseline and sensor-limited oracle.

## Traps found this session (do not re-learn them)
- Tuning-seed results do not replicate (pilot 2178 -> main 973). Always fresh seeds.
- The brain's unit cost can silently exceed the body's metabolism (A8).
- A near-uniform start matters: any turning bias traps an untrained creature in loops (A7).
- The eligibility trace must be reset when the brain grows (A12).
- A saturated softmax (T small, confident) has zero policy gradient and cannot unlearn.
- Test worlds: the default food budget puts 12 items in a 16x16 test world; set `food_budget` explicitly.
- `git add -A` sweeps in whatever a concurrent agent is writing (viewer fixtures got committed once).
