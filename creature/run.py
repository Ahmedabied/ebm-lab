"""CLI: python -m creature.run --policy ebm --seed 1 --label smoke --days 10

Every flag defaults to None and overrides the dataclass default ONLY when given, so a bare CLI
run has exactly the SimConfig/BrainConfig/SenseConfig/WorldConfig defaults (EXP-01's config:
T 0.3, lr 1.0, day_len 300, ...). The effective config is printed as one JSON line before the
life starts; the life's summary is the last line."""
import argparse, json, sys
from .sim import Life, SimConfig

# flag dest -> (config section or None for SimConfig, attribute name)
FIELDS = {
    "policy": (None, "policy"), "seed": (None, "seed"), "label": (None, "label"),
    "days": (None, "days"), "day_len": (None, "day_len"), "sleep": (None, "sleep"),
    "growth": (None, "growth"), "growth_every": (None, "growth_every"),
    "day_learning": (None, "day_learning"), "learner": (None, "learner"),
    "alpha_v": (None, "alpha_v"), "alpha_q": (None, "alpha_q"), "gamma": (None, "gamma"),
    "runs_dir": (None, "runs_dir"),
    "H0": ("brain", "H0"), "T": ("brain", "T"), "lr": ("brain", "lr"),
    "act_mode": ("brain", "act_mode"), "eps": ("brain", "eps"),
    "blend": ("world", "blend_mode"), "sign_features": ("sense", "sign_features"),
}


def parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="Run one creature life (defaults = dataclass defaults).")
    p.add_argument("--policy")
    p.add_argument("--seed", type=int)
    p.add_argument("--label")
    p.add_argument("--days", type=int)
    p.add_argument("--day-len", type=int)
    p.add_argument("--sleep", choices=["replay", "today", "noise", "none"])
    p.add_argument("--growth", choices=["surprise", "timer", "none"])
    p.add_argument("--growth-every", type=int)
    p.add_argument("--day-learning", action="store_true", default=None)
    p.add_argument("--learner", choices=["pg", "ac", "q"])
    p.add_argument("--alpha-v", type=float)
    p.add_argument("--alpha-q", type=float)
    p.add_argument("--gamma", type=float)
    p.add_argument("--H0", type=int)
    p.add_argument("--T", type=float)
    p.add_argument("--lr", type=float)
    p.add_argument("--blend", choices=["linear", "xor"])
    p.add_argument("--sign-features", action="store_true", default=None)
    p.add_argument("--act-mode", choices=["softmax", "egreedy"])
    p.add_argument("--eps", type=float)
    p.add_argument("--runs-dir")
    return p


def build_config(argv=None) -> SimConfig:
    a = parser().parse_args(argv)
    cfg = SimConfig()
    for dest, (section, attr) in FIELDS.items():
        v = getattr(a, dest)
        if v is None:
            continue
        setattr(getattr(cfg, section) if section else cfg, attr, v)
    return cfg


def effective_summary(life: Life) -> dict:
    c = life.cfg
    d = {"policy": c.policy, "seed": c.seed, "label": c.label, "days": c.days, "day_len": c.day_len,
         "sleep": c.sleep, "growth": c.growth, "day_learning": c.day_learning,
         "blend": c.world.blend_mode, "sign_features": c.sense.sign_features,
         "input_dim": life.senses.dim}
    if life.brain is not None:
        b = life.brain.cfg                 # effective (dim from senses; q forces egreedy)
        d.update({"learner": c.learner, "brain_dim": b.dim, "act_mode": b.act_mode, "eps": b.eps,
                  "T": b.T, "lr": b.lr, "H0": b.H0, "gamma": c.gamma, "alpha_v": c.alpha_v,
                  "alpha_q": c.alpha_q})
    return d


def main(argv=None):
    cfg = build_config(argv)
    life = Life(cfg)
    print(json.dumps({"effective_config": effective_summary(life)}), flush=True)
    s = life.run()
    print(json.dumps(s))


if __name__ == "__main__":
    main(sys.argv[1:])
