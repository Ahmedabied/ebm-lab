"""Export one run directory into a single run.json the browser viewer can load.

    uv run python -m creature.export runs/<label>/<seed>  [--budget-mb 5]

Reads meta.json, ticks.jsonl, events.jsonl, fields.npz and (ebm only) brain.npz, writes
runs/<label>/<seed>/run.json. Read-only with respect to everything else; draws no randomness,
changes no run file. Pure stdlib + numpy (the PNG encoder below is ~20 lines of zlib).

FIELD COLOUR CODE (fixed, identical for every run so runs can be compared by eye)
    note A -> red, note B -> green, note C -> blue
    linear world (world.blend_mode = "linear", and every run from before that field existed):
        food emits A+B -> reads YELLOW;  poison emits B+C -> reads CYAN
    xor world (world.blend_mode = "xor"):
        food emits A+B -> reads YELLOW;  poison emits A alone (RED) or B alone (GREEN)
        so in the xor world yellow = food is only readable as "red AND green together".
    The run's actual table is copied into run.json["blends"] (from creature.world.BLENDS) and the
    viewer builds its legend from it. Overlapping plumes mix additively (toward white).
    intensity = clip( log1p(v / C0) / log1p(VMAX / C0), 0, 1 ) per channel, then x255.
    C0 = 0.01, VMAX = 0.3. Measured on 20-day oracle/braitenberg runs at default config the
    field max is ~0.23-0.29 and the 99th percentile ~0.05-0.09, so VMAX=0.3 almost never clips and
    the log keeps the faint far-field gradient (~0.005) visible at ~13% intensity. This is a
    DISPLAY scale only; it is NOT what the creature senses (senses use log1p(v / sense.c0)).
    If a future config makes fields much stronger, values above VMAX saturate (clip), they are
    not rescaled per run. Change C0/VMAX here and re-export if that happens.

SIZE BUDGET
    Ticks are stored as parallel arrays (one list per column) with the run's own rounding.
    Field snapshots are 48x48 RGB PNGs, base64 data-URLs. If the total would exceed the budget
    (default 5 MB), snapshots are DOWNSAMPLED IN TIME by keeping every k-th one (k = smallest
    integer that fits); k is recorded in run.json as fields.stride and reported on stdout.
    Spatial resolution is never reduced. Note: snapshots are only taken on WAKING ticks
    (sim.py), so during a night the viewer shows the last waking snapshot.
"""
import argparse, base64, json, math, os, struct, sys, zlib
import numpy as np

C0 = 0.01
VMAX = 0.3
# Fallback ONLY for runs whose meta.json predates config.input_names. This is the creature-v0 layout
# (raw left/right antenna readings); from bb5b19d on, the 12 dims are opponent-coded
# (contrast_*, mean_*, change_*, body_E, body_X, bias), so for those older runs the labels are
# known to be approximate. run.json records which source was used ("input_names_source").
INPUT_NAMES = ["L.A", "L.B", "L.C", "R.A", "R.B", "R.C", "dA", "dB", "dC", "E", "X", "bias"]


# ---- PNG -------------------------------------------------------------------------------------
def _png_rgb(img: np.ndarray) -> bytes:
    """img (H, W, 3) uint8 -> PNG bytes. Filter type 0 per row, zlib level 9."""
    h, w, _ = img.shape
    raw = b"".join(b"\x00" + img[r].tobytes() for r in range(h))

    def chunk(tag, data):
        return struct.pack(">I", len(data)) + tag + data + struct.pack(">I", zlib.crc32(tag + data) & 0xFFFFFFFF)
    return (b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", struct.pack(">IIBBBBB", w, h, 8, 2, 0, 0, 0))
            + chunk(b"IDAT", zlib.compress(raw, 9)) + chunk(b"IEND", b""))


def field_to_rgb(f: np.ndarray) -> np.ndarray:
    """f (3, H, W) float -> (H, W, 3) uint8 under the fixed log scale above."""
    v = np.clip(np.asarray(f, dtype=np.float64), 0.0, None)
    s = np.clip(np.log1p(v / C0) / math.log1p(VMAX / C0), 0.0, 1.0)
    return np.ascontiguousarray((s * 255.0 + 0.5).astype(np.uint8).transpose(1, 2, 0))


def data_url(png: bytes) -> str:
    return "data:image/png;base64," + base64.b64encode(png).decode("ascii")


# ---- readers ---------------------------------------------------------------------------------
def read_jsonl(path):
    if not os.path.exists(path):
        return []
    with open(path) as fh:
        return [json.loads(line) for line in fh if line.strip()]


def ticks_to_columns(ticks):
    """List of tick dicts -> dict of parallel arrays. F is split into F0/F1/F2 (None where absent)."""
    cols = {k: [] for k in ("t", "day", "sleep", "y", "x", "h", "a", "E", "X", "D", "r", "H")}
    F = [[], [], []]
    anyF = False
    for d in ticks:
        cols["t"].append(d["t"]); cols["day"].append(d["day"])
        cols["sleep"].append(1 if d.get("phase") == "sleep" else 0)
        for k in ("y", "x", "h", "a", "E", "X", "D", "r", "H"):
            cols[k].append(d.get(k))
        f = d.get("F")
        if f is not None:
            anyF = True
            for i in range(3):
                F[i].append(f[i])
        else:
            for i in range(3):
                F[i].append(None)
    cols["F"] = F if anyF else None
    return cols


# per-night instruments, copied as-is (None stays None) when the event carries them; absent before
END_KEYS = ("clip_frac", "entropy", "w_norm", "td_abs", "td_abs_day")   # sleep_end (td_*: ac/q only)
START_KEYS = ("surprise", "wake_entropy")                              # sleep_start
INSTR_KEYS = START_KEYS + END_KEYS


def read_brain(path, events):
    """brain.npz -> list of per-night dicts {night, t, day, H, u, ...every other param key...,
    + the instruments in END_KEYS / START_KEYS}. The i-th snapshot is taken just before the i-th
    sleep_end event (sim.py), so that event supplies its time, day and END_KEYS; the i-th
    sleep_start supplies START_KEYS. Keys an event did not log are simply left out."""
    if not os.path.exists(path):
        return None
    z = np.load(path)
    by_i = {}
    for k in z.files:
        name, i = k.rsplit("_", 1)
        by_i.setdefault(int(i), {})[name] = k
    ends = [e for e in events if e["kind"] == "sleep_end"]
    starts = [e for e in events if e["kind"] == "sleep_start"]
    out = []
    for i in sorted(by_i):
        e = ends[i] if i < len(ends) else {"t": None, "day": None}
        d = {"night": i, "t": e["t"], "day": e["day"]}
        for name, key in by_i[i].items():
            d[name] = np.round(z[key], 4).tolist()
        d["H"] = int(np.asarray(z[by_i[i]["u"]]).shape[0]) if "u" in by_i[i] else None
        if i < len(starts):
            for k in START_KEYS:
                if k in starts[i]:
                    d[k] = starts[i][k]
        for k in END_KEYS:
            if k in e:
                d[k] = e[k]
        out.append(d)
    return out


def blend_table(cfg: dict) -> dict:
    """Which chemical blend is food and which is poison in this run's world, for the legend.
    Taken from creature.world.BLENDS of the CURRENT source tree, keyed by the run's
    world.blend_mode (runs from before blend_mode existed are 'linear', the only world then).
    If the run's source_hash differs from today's source, the table could in principle differ;
    the note field says so."""
    mode = cfg.get("world", {}).get("blend_mode", "linear")
    try:
        from .world import BLENDS, FOOD, POISON
        from .sim import source_hash
        if mode not in BLENDS:  # noqa
            return {"mode": mode, "table": None, "note": "unknown blend_mode"}
        tab = {"food": [np.asarray(v).tolist() for v in BLENDS[mode][FOOD]],
               "poison": [np.asarray(v).tolist() for v in BLENDS[mode][POISON]]}
        note = None
        if source_hash() != cfg.get("_source_hash_of_run"):
            note = "blend table read from current source"
        return {"mode": mode, "table": tab, "note": note}
    except Exception as ex:   # never fail an export over the legend
        return {"mode": mode, "table": None, "note": f"could not read BLENDS: {ex}"}


def input_names(meta: dict, brain) -> tuple[list[str] | None, str]:
    """(names, source). Names come from meta.json's config.input_names (written by sim.py from
    Senses.names()). Older runs lack it: fall back to the legacy 12 only if the brain is 12 wide
    (or there is no brain); otherwise None (the viewer then labels columns x0, x1, ...)."""
    names = meta.get("config", {}).get("input_names")
    if names:
        return list(names), "meta"
    width = len(brain[0]["u"][0]) if brain and brain[0].get("u") else None
    if width in (None, len(INPUT_NAMES)):
        return list(INPUT_NAMES), "fallback-legacy-12"
    return None, "absent"


def effective(meta: dict) -> dict:
    """The brain settings the life actually ran with (meta.json stores the EFFECTIVE brain config
    under config.brain since 9dd8c14; older runs store the requested one)."""
    c = meta.get("config", {}); b = c.get("brain") or {}
    is_ebm = c.get("policy") == "ebm"
    return {"brain_dim": b.get("dim") if is_ebm else None,
            "act_mode": b.get("act_mode", "softmax") if is_ebm else None,
            "learner": c.get("learner", "pg") if is_ebm else None,
            "T": b.get("T") if is_ebm else None}


# ---- main ------------------------------------------------------------------------------------
def export(run_dir: str, budget_mb: float = 5.0) -> dict:
    meta = json.load(open(os.path.join(run_dir, "meta.json")))
    ticks = read_jsonl(os.path.join(run_dir, "ticks.jsonl"))
    events = read_jsonl(os.path.join(run_dir, "events.jsonl"))
    cols = ticks_to_columns(ticks)
    brain = read_brain(os.path.join(run_dir, "brain.npz"), events)

    fpath = os.path.join(run_dir, "fields.npz")
    snap_t, urls = [], []
    if os.path.exists(fpath):
        z = np.load(fpath)
        snap_t = [int(t) for t in z["t"]]
        fields = z["fields"]
        urls = [data_url(_png_rgb(field_to_rgb(fields[i]))) for i in range(len(snap_t))]

    names, names_src = input_names(meta, brain)
    eff = effective(meta)
    meta = {**meta, **eff, "input_names_source": names_src}
    if brain and names is not None and len(brain[0].get("u", [[]])[0]) != len(names):
        print(f"warning: u is {len(brain[0]['u'][0])} wide but there are {len(names)} input names",
              file=sys.stderr)
    doc = {"format": "ebm-lab-run/1", "run_dir": run_dir, "meta": meta, "events": events,
           "ticks": cols, "brain": brain, "input_names": names, "input_names_source": names_src,
           "blends": blend_table({**meta["config"], "_source_hash_of_run": meta.get("source_hash")}),
           "sense": meta["config"].get("sense", {}),
           "world": {"H": meta["config"]["world"]["H"], "W": meta["config"]["world"]["W"]},
           "fields": {"scale": {"C0": C0, "VMAX": VMAX, "rule": "log1p(v/C0)/log1p(VMAX/C0), clipped"},
                      "channels": {"A": "red", "B": "green", "C": "blue"},
                      "snap_every": meta["config"].get("snap_every"),
                      "n_original": len(snap_t), "stride": 1, "t": snap_t, "png": urls}}

    budget = budget_mb * 1024 * 1024
    base = len(json.dumps({**doc, "fields": {**doc["fields"], "t": [], "png": []}}, separators=(",", ":")))
    img_bytes = sum(len(u) + 3 for u in urls) + 8 * len(snap_t)
    stride = 1
    if urls and base + img_bytes > budget:
        room = max(budget - base, 1)
        stride = max(1, math.ceil(img_bytes / room))
    if stride > 1:
        doc["fields"]["stride"] = stride
        doc["fields"]["t"] = snap_t[::stride]
        doc["fields"]["png"] = urls[::stride]

    out = os.path.join(run_dir, "run.json")
    with open(out, "w") as fh:
        json.dump(doc, fh, separators=(",", ":"))
    size = os.path.getsize(out)
    print(json.dumps({"wrote": out, "bytes": size, "MB": round(size / 1048576, 2), "ticks": len(ticks),
                      "events": len(events), "snapshots_kept": len(doc["fields"]["t"]),
                      "snapshots_original": len(snap_t), "stride": stride,
                      "brain_nights": 0 if brain is None else len(brain),
                      "has_F": cols["F"] is not None, "n_inputs": None if names is None else len(names),
                      "input_names_source": names_src, **eff}))
    if size > budget:
        print(f"warning: run.json is {size/1048576:.2f} MB, over the {budget_mb} MB budget "
              "(tick arrays alone exceed it)", file=sys.stderr)
    return doc


def main():
    p = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    p.add_argument("run_dir", help="runs/<label>/<seed>")
    p.add_argument("--budget-mb", type=float, default=5.0)
    a = p.parse_args()
    export(a.run_dir.rstrip("/"), a.budget_mb)


if __name__ == "__main__":
    main()
