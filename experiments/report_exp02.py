"""Prints the markdown tables for findings/02 from experiments/results/<prefix>_{linear,xor}/results.json.
Printing only; no interpretation. Arms missing from a file are skipped with a warning.
Run: uv run python experiments/report_exp02.py                      (EXP-02 data)
     uv run python experiments/report_exp02.py --results-prefix 01_main --base ebm-nosleep \\
         --gap-arms ebm,ebm-nolearn,ebm-linear,oracle   (smoke test on EXP-01 data)"""
import argparse, json, os, sys, warnings
warnings.formatwarning = lambda msg, *a, **k: f"warning: {msg}\n"   # one short line on stderr
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from stats import gap_fraction, diff

R = os.path.join(os.path.dirname(os.path.abspath(__file__)), "results")
WORLDS = ("linear", "xor")
# Prereg arms-table order.
ARMS = ["random", "tabular_q", "ebm-nolearn", "ebm", "ebm-dn", "ebm-dn-sign", "ebm-dn-greedy",
        "ebm-dn-critic", "ebm-td", "ebm-all"]
DECOMP = ["ebm-dn-sign", "ebm-dn-greedy", "ebm-dn-critic", "ebm-td", "ebm-all"]


def parse(argv=None, desc="", extra=()):
    p = argparse.ArgumentParser(description=desc)
    for flag, kw in extra: p.add_argument(flag, **kw)
    p.add_argument("--results-prefix", default="02_main")
    p.add_argument("--base", default="ebm-dn", help="gap-fraction baseline arm (G=0)")
    p.add_argument("--target", default="tabular_q", help="gap-fraction target arm (G=1)")
    p.add_argument("--n-boot", type=int, default=5000)
    p.add_argument("--gap-arms", default=",".join(DECOMP),
                   help="comma-separated arms to compute G for (default: the prereg decomposition arms)")
    a = p.parse_args(argv); a.gap_arms = [x for x in a.gap_arms.split(",") if x]
    return a


def load_worlds(prefix):
    out = {}
    for w in WORLDS:
        path = os.path.join(R, f"{prefix}_{w}", "results.json")
        if not os.path.exists(path):
            warnings.warn(f"missing {path}; world {w} skipped"); continue
        out[w] = json.load(open(path))
    return out


def present(worlds, arms, label="arm"):
    """Arms present in at least one world, in the given order; warns for each absent (arm, world)."""
    keep = []
    for a in arms:
        miss = [w for w, r in worlds.items() if a not in r["lives"]]
        for w in miss:
            warnings.warn(f"{label} {a!r} not in {worlds[w]['name']}; skipped there")
        if len(miss) < len(worlds):
            keep.append(a)
    return keep


def fmt(c, d=0):
    if c is None: return "n/a"
    return f"{c['mean']:.{d}f} [{c['lo']:.{d}f}, {c['hi']:.{d}f}]"


def gap_rows(worlds, args):
    """{world: {arm: gap dict}} for decomposition arms (and ebm, ebm-nolearn) present with base+target."""
    out = {}
    for w, r in worlds.items():
        out[w] = {}
        if args.base not in r["lives"] or args.target not in r["lives"]:
            warnings.warn(f"{r['name']}: base {args.base!r} or target {args.target!r} missing; no gap fractions")
            continue
        for a in args.gap_arms:
            if a in r["lives"]:
                out[w][a] = gap_fraction(r, a, base=args.base, target=args.target, n_boot=args.n_boot)
    return out


def main(argv=None):
    args = parse(argv, __doc__)
    worlds = load_worlds(args.results_prefix)
    if not worlds: sys.exit("no results files found")
    ws = list(worlds)
    r0 = worlds[ws[0]]
    print(f"Source: {', '.join(r['name'] + ' (commit ' + r['commit'] + ', src ' + r['source_hash'] + ', ' + str(len(r['seeds'])) + ' seeds ' + str(r['seeds'][0]) + '-' + str(r['seeds'][-1]) + ')' for r in worlds.values())}")
    print()
    arms = present(worlds, ARMS)
    print("### Ticks alive and food (mean [95% bootstrap CI], per-arm CI)\n")
    print("| arm | " + " | ".join(f"{w} ticks_alive | {w} food" for w in ws) + " |")
    print("|---|" + "---|---|" * len(ws))
    for a in arms:
        cells = []
        for w in ws:
            st = worlds[w]["stats"].get(a)
            cells += [fmt(st["ticks_alive"]) if st else "n/a", f"{st['food']['mean']:.2f}" if st else "n/a"]
        print(f"| {a} | " + " | ".join(cells) + " |")

    print(f"\n### Gap fraction G = (arm - {args.base}) / ({args.target} - {args.base}), ticks_alive, "
          f"paired bootstrap over seeds ({args.n_boot} resamples), 95% CI\n")
    gaps = gap_rows(worlds, args)
    gap_arms = [a for a in args.gap_arms if any(a in gaps[w] for w in ws)]
    for a in args.gap_arms:
        if a not in gap_arms: warnings.warn(f"decomposition arm {a!r} absent in every world; skipped")
    print("| arm | " + " | ".join(ws) + " |")
    print("|---|" + "---|" * len(ws))
    for a in gap_arms:
        print(f"| {a} | " + " | ".join(fmt(gaps[w].get(a), 2) for w in ws) + " |")

    print("\n### P3: paired difference ebm - ebm-nolearn (ticks_alive), 95% CI\n")
    print("| world | ebm - ebm-nolearn |")
    print("|---|---|")
    for w in ws:
        r = worlds[w]
        if "ebm" in r["lives"] and "ebm-nolearn" in r["lives"]:
            print(f"| {w} | {fmt(diff(r, 'ebm', 'ebm-nolearn', n_boot=args.n_boot))} |")
        else:
            warnings.warn(f"{r['name']}: ebm or ebm-nolearn missing; P3 skipped")


if __name__ == "__main__":
    main()
