"""Plots for EXP-01 from experiments/results/01_main_{linear,xor}/results.json.
Writes experiments/results/01_main_ticks.png and 01_main_food.png. No popups: files on disk.
Run: uv run python experiments/plot_exp01.py"""
import json, os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

R = os.path.join(os.path.dirname(os.path.abspath(__file__)), "results")
worlds = {w: json.load(open(os.path.join(R, f"01_main_{w}", "results.json"))) for w in ("linear", "xor")}
arms = list(worlds["linear"]["stats"].keys())

for metric, fname in (("ticks_alive", "01_main_ticks.png"), ("food", "01_main_food.png")):
    fig, axes = plt.subplots(1, 2, figsize=(13, 5), sharey=True)
    for ax, (w, res) in zip(axes, worlds.items()):
        st = res["stats"]
        means = [st[a][metric]["mean"] for a in arms]
        lo = [st[a][metric]["mean"] - st[a][metric]["lo"] for a in arms]
        hi = [st[a][metric]["hi"] - st[a][metric]["mean"] for a in arms]
        colors = ["#888" if not a.startswith("ebm") else ("#d9534f" if a == "ebm" else "#f0ad4e") for a in arms]
        ax.barh(range(len(arms)), means, xerr=[lo, hi], color=colors, capsize=3)
        ax.set_yticks(range(len(arms))); ax.set_yticklabels(arms)
        ax.invert_yaxis(); ax.set_title(f"{w} world  (n={len(res['seeds'])} seeds, 95% bootstrap CI)")
        ax.set_xlabel(metric); ax.grid(axis="x", alpha=0.3)
    fig.suptitle(f"EXP-01 {metric}: commit {worlds['linear']['commit']}, src {worlds['linear']['source_hash']}")
    fig.tight_layout(); fig.savefig(os.path.join(R, fname), dpi=120); print("wrote", fname)
