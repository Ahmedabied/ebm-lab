"""EXP-01b DIAGNOSTIC — is the EBM life loop fair? A brain with ALL-ZERO weights is exactly a
uniform policy, so it must live as long as the random policy (in distribution). If it doesn't,
there is a bug in the brain arm's loop, not in learning. 16 seeds.
Run: uv run python experiments/01b_diag_uniform.py
"""
from harness import run_arms, table
arms = {
    "random":        {"policy": "random"},
    "ebm-zero":      {"policy": "ebm", "sleep": "none", "growth": "none", "brain.init_scale": 0.0,
                      "sense.noise": 0.0, "brain.H0": 4},
    "ebm-zero-H0":   {"policy": "ebm", "sleep": "none", "growth": "none", "brain.init_scale": 0.0,
                      "sense.noise": 0.0, "brain.H0": 0},
}
res = run_arms("01b_diag_uniform", arms, seeds=range(16), days=15)
print(table(res))
