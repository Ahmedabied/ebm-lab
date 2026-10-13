"""L0 — physics: laws on fields. No objects, no names, no randomness.

Every function takes arrays and returns arrays. The creature never reads this file's names.
Chemistry here is three numbers per cell that spread and fade; that is the whole model of "smell".
"""
import numpy as np


def diffuse(f: np.ndarray, alpha: float) -> np.ndarray:
    """4-neighbour diffusion on a torus. Conserves the field's total mass exactly (up to float
    rounding). Stable for alpha <= 0.25 (explicit scheme, 4 neighbours)."""
    assert 0.0 <= alpha <= 0.25, "explicit diffusion is unstable above 0.25"
    lap = (np.roll(f, 1, axis=-1) + np.roll(f, -1, axis=-1)
           + np.roll(f, 1, axis=-2) + np.roll(f, -1, axis=-2) - 4.0 * f)
    return f + alpha * lap


def decay(f: np.ndarray, keep: float) -> np.ndarray:
    """Multiplicative fade. Removes (1-keep) of the mass; the caller books it."""
    assert 0.0 <= keep <= 1.0
    return f * keep


def bilinear(f: np.ndarray, y: float, x: float) -> np.ndarray:
    """Read field(s) f[..., H, W] at a continuous point (y, x) on the torus, bilinearly.
    Returns shape f.shape[:-2]."""
    H, W = f.shape[-2], f.shape[-1]
    y = y % H
    x = x % W
    y0 = int(np.floor(y)); x0 = int(np.floor(x))
    fy = y - y0;           fx = x - x0
    y1 = (y0 + 1) % H;     x1 = (x0 + 1) % W
    return ((1 - fy) * (1 - fx) * f[..., y0, x0] + (1 - fy) * fx * f[..., y0, x1]
            + fy * (1 - fx) * f[..., y1, x0] + fy * fx * f[..., y1, x1])
