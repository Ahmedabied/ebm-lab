# Trained weights

The brains that seed 203's creature ended its 15-day life with in EXP-02 (arm `ebm-td`, the energy-based
brain trained as a value function). One per world.

| file | world | hidden units | its own life |
|---|---|---|---|
| `ebm-td_linear_seed203_final.npz` | linear | 5 | all 15 days, 13.35 food |
| `ebm-td_xor_seed203_final.npz` | xor | 8 | all 15 days, 9.9 food |

Each `.npz` holds the five parameter arrays of `creature/brain.py` (`b`, `w`, `c`, `u`, `v`); the `.json` next
to it has the brain config, the 12 input names and the life's summary. Load them with
`Brain(cfg, rng, theta=dict(np.load(path)))`.

## Try it

```
uv sync
uv run python weights/try_it.py                        # linear world, seed 9000, brain frozen
uv run python weights/try_it.py --world xor --seed 9001
uv run python weights/try_it.py --learn                # keep learning from these weights
```

It prints the life's summary and writes a `run.json` you can watch in the browser viewer (the command
is printed at the end).

## How good are they (20 fresh worlds, seeds 9000–9019, 15 days, ceiling 5250 ticks)

| | mean ticks alive | lived all 15 days |
|---|---|---|
| linear, frozen | 3299 | 10 / 20 |
| linear, keeps learning | 5250 | 20 / 20 |
| xor, frozen | 2174 | 4 / 20 |
| xor, keeps learning | 3491 | 9 / 20 |

Read this honestly: the final brain alone is not a reliable forager in a new world; the same brain that
keeps learning is, in the linear world. What the creature learned is a good starting point, not a
finished policy. These seeds are a demo, not part of the lab's record (see `findings/02` for that).

Regenerate the files: `uv run python weights/export_weights.py` (re-lives both lives and checks
they match the recorded ones before saving).
