"""Prints the markdown tables for findings/02 from experiments/results/<prefix>_{linear,xor}/results.json.
Printing only; the only verdict-like output is the mechanical bar check the prereg fixes for P1-P5.
Arms missing from a file are skipped with a warning.
Run: .venv/bin/python experiments/report_exp02.py                      (EXP-02 data)
     .venv/bin/python experiments/report_exp02.py --results-prefix 01_main --base ebm-nosleep \\
         --gap-arms ebm,ebm-nolearn,ebm-linear,oracle --p1-arm oracle --p4-arm ebm-linear \\
         --contrasts oracle:ebm-linear,ebm-linear:ebm,ebm:ebm-nolearn   (smoke test on EXP-01 data)"""
import argparse, json, os, sys, warnings
warnings.formatwarning = lambda msg, *a, **k: f"warning: {msg}\n"   # one short line on stderr
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from stats import gap_fraction, diff, compare_gap, cross_world

R = os.path.join(os.path.dirname(os.path.abspath(__file__)), "results")
WORLDS = ("linear", "xor")
# Prereg arms-table order.
ARMS = ["random", "tabular_q", "ebm-nolearn", "ebm", "ebm-dn", "ebm-dn-sign", "ebm-dn-greedy",
        "ebm-dn-critic", "ebm-td", "ebm-all", "tabular_q_next"]   # last = exploratory (A17)
DECOMP = ["ebm-dn-sign", "ebm-dn-greedy", "ebm-dn-critic", "ebm-td", "ebm-all"]
# Prereg contrasts, as a:b meaning ΔG = G(a) - G(b): P2 (greedy > sign > critic), P5 (td >= greedy).
CONTRASTS = "ebm-dn-greedy:ebm-dn-sign,ebm-dn-sign:ebm-dn-critic,ebm-td:ebm-dn-greedy"
EXP01_EBM_CI = (806.0, 1167.0)       # EXP-01 linear `ebm` ticks_alive CI, quoted by the prereg (P3)
EXP01_FILE = os.path.join(R, "01_main_linear", "results.json")
HEADER = ("No multiple-comparisons correction. P1\u2013P5 are the only confirmatory tests, each on its own "
          "95% CI; every other contrast is exploratory.")
P1_BAR, P1_LO_BAR, P2_BAR = 0.75, 0.5, 0.4


def parse(argv=None, desc="", extra=()):
    p = argparse.ArgumentParser(description=desc)
    for flag, kw in extra: p.add_argument(flag, **kw)
    p.add_argument("--results-prefix", default="02_main")
    p.add_argument("--base", default="ebm-dn", help="gap-fraction baseline arm (G=0)")
    p.add_argument("--target", default="tabular_q", help="gap-fraction target arm (G=1)")
    p.add_argument("--n-boot", type=int, default=5000)
    p.add_argument("--gap-arms", default=",".join(DECOMP),
                   help="comma-separated arms to compute G for (default: the prereg decomposition arms)")
    p.add_argument("--p1-arm", default="ebm-all", help="P1 ceiling arm")
    p.add_argument("--p4-arm", default="ebm-dn-sign", help="P4 cross-world arm")
    p.add_argument("--contrasts", default=CONTRASTS, help="comma-separated a:b pairs for ΔG = G(a) - G(b)")
    a = p.parse_args(argv); a.gap_arms = [x for x in a.gap_arms.split(",") if x]
    a.contrasts = [tuple(x.split(":")) for x in a.contrasts.split(",") if x]
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
    out = f"{c['mean']:.{d}f} [{c['lo']:.{d}f}, {c['hi']:.{d}f}]"
    if c.get("n_nonfinite"): out += f" (n_nonfinite={c['n_nonfinite']})"
    return out


def fmt_gap(g):
    """A gap fraction, or 'undefined' when the denominator's paired CI includes 0."""
    if g is None: return "n/a"
    if not g.get("defined", True):
        return f"undefined (denominator CI includes 0; den {fmt(g['den'])})"
    return fmt(g, 2)


def ceiling(r):
    """Ticks of a life that survives every day: days * (day_len + sleep_len). sleep_len comes from the
    stored effective config; results files older than that field fall back to the SimConfig default."""
    cfgs = r.get("configs") or {}
    if cfgs:
        sl = {c["sleep_len"] for c in cfgs.values()}
        if len(sl) != 1: warnings.warn(f"{r['name']}: arms differ in sleep_len {sl}; using max")
        sleep_len = max(sl)
    else:
        sys.path.insert(0, os.path.dirname(os.path.dirname(R)))   # repo root
        from creature.sim import SimConfig
        sleep_len = SimConfig().sleep_len
        warnings.warn(f"{r['name']}: no stored configs; sleep_len={sleep_len} from the current SimConfig default")
    return r["days"] * (r["day_len"] + sleep_len)


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


def has(r, *arms):
    return all(a in r["lives"] for a in arms)


def main(argv=None):
    args = parse(argv, __doc__)
    worlds = load_worlds(args.results_prefix)
    if not worlds: sys.exit("no results files found")
    ws = list(worlds)
    print(HEADER)
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

    ceil = {w: ceiling(r) for w, r in worlds.items()}
    print(f"\n### Lives censored at the {worlds[ws[0]]['days']}-day ceiling (ticks_alive == "
          + ", ".join(f"{w} {c}" for w, c in ceil.items()) + "), out of n seeds\n")
    print("| arm | " + " | ".join(ws) + " |")
    print("|---|" + "---|" * len(ws))
    for a in arms:
        cells = []
        for w, r in worlds.items():
            L = r["lives"].get(a)
            cells.append(f"{sum(l['ticks_alive'] >= ceil[w] for l in L)}/{len(L)}" if L else "n/a")
        print(f"| {a} | " + " | ".join(cells) + " |")

    print(f"\n### Gap fraction G = (arm - {args.base}) / ({args.target} - {args.base}), ticks_alive, "
          f"paired bootstrap over seeds ({args.n_boot} resamples), 95% CI\n")
    gaps = gap_rows(worlds, args)
    gap_arms = [a for a in args.gap_arms if any(a in gaps[w] for w in ws)]
    for a in args.gap_arms:
        if a not in gap_arms: warnings.warn(f"decomposition arm {a!r} absent in every world; skipped")
    for w in ws:
        g0 = next(iter(gaps[w].values()), None)
        if g0: print(f"Denominator {args.target} - {args.base} ({w}): {fmt(g0['den'])}" + ("" if g0["defined"] else "  -> CI includes 0, every G in this world is undefined"))
    print()
    print("| arm | " + " | ".join(ws) + " |")
    print("|---|" + "---|" * len(ws))
    for a in gap_arms:
        print(f"| {a} | " + " | ".join(fmt_gap(gaps[w].get(a)) for w in ws) + " |")

    # ---- exploratory: G against the textbook Q target, and paired differences (referee, session 03) --
    if all("tabular_q_next" in r["lives"] for r in worlds.values()):
        a2 = argparse.Namespace(**{**vars(args), "target": "tabular_q_next"})
        gaps2 = gap_rows(worlds, a2)
        print(f"\n### Exploratory: G against the textbook target tabular_q_next (addendum item 10)\n")
        for w in ws:
            g0 = next(iter(gaps2[w].values()), None)
            if g0: print(f"Denominator tabular_q_next - {args.base} ({w}): {fmt(g0['den'])}")
        print("\n| arm | " + " | ".join(ws) + " |")
        print("|---|" + "---|" * len(ws))
        for a in gap_arms:
            print(f"| {a} | " + " | ".join(fmt_gap(gaps2[w].get(a)) for w in ws) + " |")
    print("\n### Paired differences in ticks_alive (arm_a - arm_b, paired bootstrap; the honest companion to G near the ceiling)\n")
    pairs = [("ebm-td", "tabular_q"), ("ebm-td", "tabular_q_next"), ("ebm-all", "ebm-td"),
             ("ebm-dn-sign", "ebm-dn"), ("ebm-dn-critic", "ebm-dn-greedy"), ("tabular_q_next", "tabular_q")]
    print("| a - b | " + " | ".join(ws) + " |")
    print("|---|" + "---|" * len(ws))
    for a, b in pairs:
        cells = [fmt(diff(worlds[w], a, b, "ticks_alive", n_boot=args.n_boot)) if has(worlds[w], a, b) else "n/a" for w in ws]
        print(f"| {a} - {b} | " + " | ".join(cells) + " |")

    # ---- confirmatory tests (linear world unless stated) --------------------------------------------
    print("\n## Confirmatory tests P1-P5 (prereg; linear world unless stated)\n")
    lin = worlds.get("linear")
    kw = dict(base=args.base, target=args.target, n_boot=args.n_boot)

    print(f"**P1 (ceiling)**: bar G({args.p1_arm}) >= {P1_BAR} with CI lower bound > {P1_LO_BAR}")
    if lin and has(lin, args.base, args.target, args.p1_arm):
        g = gap_fraction(lin, args.p1_arm, **kw)
        if g["defined"]:
            print(f"  G = {fmt(g, 2)};  point >= {P1_BAR}: {'yes' if g['mean'] >= P1_BAR else 'no'};  "
                  f"lo > {P1_LO_BAR}: {'yes' if g['lo'] > P1_LO_BAR else 'no'}")
        else:
            print(f"  G = {fmt_gap(g)}")
    else: warnings.warn("P1 skipped (linear world or arms missing)")

    print(f"\n**P2 / P5 (ΔG = G(a) - G(b), paired; frac = share of replicates with G(a) > G(b))**")
    if lin and has(lin, args.base, args.target):
        for a, b in args.contrasts:
            if not has(lin, a, b): warnings.warn(f"contrast {a}:{b} skipped (arm missing)"); continue
            c = compare_gap(lin, a, b, **kw)
            print(f"  G({a}) - G({b}) = {fmt(c, 3)};  frac_a_gt_b = {c['frac_a_gt_b']:.3f};  "
                  f"CI excludes 0: {'yes' if c['lo'] > 0 or c['hi'] < 0 else 'no'}")
        ga = "ebm-dn-greedy"
        if has(lin, ga):
            g = gap_fraction(lin, ga, **kw)
            print(f"  P2 bar G({ga}) > {P2_BAR}: G = {fmt_gap(g)}")
    else: warnings.warn("P2/P5 skipped (linear world or base/target missing)")

    print(f"\n**P3 (replication)**: `ebm` inside EXP-01's CI [{EXP01_EBM_CI[0]:.0f}, {EXP01_EBM_CI[1]:.0f}] "
          "and ebm - ebm-nolearn CI includes 0")
    if os.path.exists(EXP01_FILE):
        e1 = json.load(open(EXP01_FILE))["stats"]["ebm"]["ticks_alive"]
        e1_ci = (e1["lo"], e1["hi"])
        print(f"  EXP-01 (01_main_linear) ebm: {fmt(e1)}")
    else:
        e1_ci = EXP01_EBM_CI; warnings.warn(f"missing {EXP01_FILE}; using the prereg's quoted CI")
    if lin and has(lin, "ebm"):
        m = lin["stats"]["ebm"]["ticks_alive"]
        inside = e1_ci[0] <= m["mean"] <= e1_ci[1]
        print(f"  this run ({lin['name']}) ebm mean = {m['mean']:.1f} (own CI [{m['lo']:.0f}, {m['hi']:.0f}]);  "
              f"inside EXP-01 CI [{e1_ci[0]:.0f}, {e1_ci[1]:.0f}]: {'in' if inside else 'OUT'}")
    for w in ws:
        r = worlds[w]
        if has(r, "ebm", "ebm-nolearn"):
            d = diff(r, "ebm", "ebm-nolearn", n_boot=args.n_boot)
            print(f"  {w}: ebm - ebm-nolearn = {fmt(d)};  CI includes 0: {'yes' if d['lo'] <= 0 <= d['hi'] else 'no'}")
        else:
            warnings.warn(f"{r['name']}: ebm or ebm-nolearn missing; P3 diff skipped")

    print(f"\n**P4 (xor)**: G_xor({args.p4_arm}) < G_linear({args.p4_arm}); ΔG = G_linear - G_xor, joined by seed")
    if "linear" in worlds and "xor" in worlds and all(has(worlds[w], args.base, args.target, args.p4_arm) for w in ("linear", "xor")):
        c = cross_world(worlds["linear"], worlds["xor"], args.p4_arm, **kw)
        dl = {w: gap_fraction(worlds[w], args.p4_arm, **kw)["defined"] for w in ("linear", "xor")}
        print(f"  G_linear = {c['G_linear']:.3f}, G_xor = {c['G_xor']:.3f};  ΔG = {fmt(c, 3)};  "
              f"CI > 0: {'yes' if c['lo'] > 0 else 'no'};  denominators defined: linear {dl['linear']}, xor {dl['xor']}")
    else: warnings.warn("P4 skipped (a world or arm missing)")


if __name__ == "__main__":
    main()
