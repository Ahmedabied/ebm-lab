"""CLI: uv run python -m creature.run --policy ebm --seed 1 --label smoke --days 10"""
import argparse, json
from .sim import Life, SimConfig


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--policy", default="ebm")
    p.add_argument("--seed", type=int, default=0)
    p.add_argument("--label", default="smoke")
    p.add_argument("--days", type=int, default=20)
    p.add_argument("--day-len", type=int, default=400)
    p.add_argument("--sleep", default="replay", choices=["replay", "today", "noise", "none"])
    p.add_argument("--growth", default="surprise", choices=["surprise", "timer", "none"])
    p.add_argument("--day-learning", action="store_true")
    p.add_argument("--H0", type=int, default=4)
    p.add_argument("--T", type=float, default=1.0)
    p.add_argument("--lr", type=float, default=0.05)
    p.add_argument("--blend", default="linear", choices=["linear", "xor"])
    p.add_argument("--sign-features", action="store_true")
    p.add_argument("--act-mode", default="softmax", choices=["softmax", "egreedy"])
    p.add_argument("--eps", type=float, default=0.1)
    p.add_argument("--runs-dir", default="runs")
    a = p.parse_args()
    cfg = SimConfig(seed=a.seed, label=a.label, policy=a.policy, days=a.days, day_len=a.day_len,
                    sleep=a.sleep, growth=a.growth, day_learning=a.day_learning,
                    runs_dir=a.runs_dir)
    cfg.brain.H0 = a.H0; cfg.brain.T = a.T; cfg.brain.lr = a.lr
    cfg.world.blend_mode = a.blend
    cfg.sense.sign_features = a.sign_features
    cfg.brain.act_mode = a.act_mode; cfg.brain.eps = a.eps
    s = Life(cfg).run()
    print(json.dumps(s))


if __name__ == "__main__":
    main()
