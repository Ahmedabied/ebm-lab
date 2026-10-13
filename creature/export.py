"""Export one run directory into a single run.json the browser viewer can load.

    uv run python -m creature.export runs/<label>/<seed>  [--budget-mb 5]

Reads meta.json, ticks.jsonl, events.jsonl, fields.npz and (ebm only) brain.npz, writes
runs/<label>/<seed>/run.json. Read-only with respect to everything else; draws no randomness,
changes no run file. Pure stdlib + numpy (the PNG encoder below is ~20 lines of zlib).

FIELD COLOUR CODE (fixed, identical for every run so runs can be compared by eye)
    note A -> red, note B -> green, note C -> blue
    food emits A+B   -> reads YELLOW
    poison emits B+C -> reads CYAN
    a cell that holds both blends reads toward WHITE
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


def read_brain(path, events):
    """brain.npz -> list of per-night dicts {t, day, H, u, v, c}. The i-th snapshot is taken just
    before the i-th sleep_end event (sim.py), so that event supplies its time and day."""
    if not os.path.exists(path):
        return None
    z = np.load(path)
    idx = sorted({int(k.rsplit("_", 1)[1]) for k in z.files})
    ends = [e for e in events if e["kind"] == "sleep_end"]
    out = []
    for i in idx:
        e = ends[i] if i < len(ends) else {"t": None, "day": None}
        u = z[f"u_{i}"]
        out.append({"night": i, "t": e["t"], "day": e["day"], "H": int(u.shape[0]),
                    "u": np.round(u, 4).tolist(),
                    "v": np.round(z[f"v_{i}"], 4).tolist(),
                    "c": np.round(z[f"c_{i}"], 4).tolist(),
                    "w": np.round(z[f"w_{i}"], 4).tolist(),
                    "b": np.round(z[f"b_{i}"], 4).tolist()})
    return out


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

    doc = {"format": "ebm-lab-run/1", "run_dir": run_dir, "meta": meta, "events": events,
           "ticks": cols, "brain": brain, "input_names": INPUT_NAMES,
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
                      "has_F": cols["F"] is not None}))
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
