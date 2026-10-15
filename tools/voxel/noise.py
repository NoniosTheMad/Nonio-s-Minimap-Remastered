"""Vectorised, deterministic noise. All functions take broadcastable numpy arrays of coordinates (block units).

perlin(x, y, z)       improved Perlin, ~[-1, 1]
fbm(x, y, z, ...)     fractal sum of perlin, ~[-1, 1]
ridged(x, y, z, ...)  1 - |fbm|-style ridges, [0, 1]
hash01(x, y, z)       per-integer-position white noise in [0, 1) (stable: depends on the position only)
"""
import functools

import numpy as np

_G = np.array([[1, 1, 0], [-1, 1, 0], [1, -1, 0], [-1, -1, 0], [1, 0, 1], [-1, 0, 1], [1, 0, -1], [-1, 0, -1],
               [0, 1, 1], [0, -1, 1], [0, 1, -1], [0, -1, -1], [1, 1, 0], [0, -1, 1], [-1, 1, 0], [0, -1, -1]],
              np.float32)


@functools.lru_cache(64)
def _perm(seed):
    p = np.random.default_rng(seed).permutation(256).astype(np.int32)
    return np.concatenate([p, p])


def _fade(t):
    return t * t * t * (t * (t * 6 - 15) + 10)


def perlin(x, y, z=0.0, seed=0):
    x, y, z = (np.asarray(a, np.float32) for a in (x, y, z))
    x, y, z = np.broadcast_arrays(x, y, z)
    p = _perm(seed)
    xi, yi, zi = (np.floor(a).astype(np.int32) for a in (x, y, z))
    xf, yf, zf = x - xi, y - yi, z - zi
    xi &= 255; yi &= 255; zi &= 255
    u, v, w = _fade(xf), _fade(yf), _fade(zf)

    def g(h, dx, dy, dz):
        gv = _G[h & 15]
        return gv[..., 0] * dx + gv[..., 1] * dy + gv[..., 2] * dz

    a = p[xi] + yi; aa = p[a] + zi; ab = p[a + 1] + zi
    b = p[xi + 1] + yi; ba = p[b] + zi; bb = p[b + 1] + zi
    l = lambda t, a_, b_: a_ + t * (b_ - a_)
    x1 = l(u, g(p[aa], xf, yf, zf), g(p[ba], xf - 1, yf, zf))
    x2 = l(u, g(p[ab], xf, yf - 1, zf), g(p[bb], xf - 1, yf - 1, zf))
    x3 = l(u, g(p[aa + 1], xf, yf, zf - 1), g(p[ba + 1], xf - 1, yf, zf - 1))
    x4 = l(u, g(p[ab + 1], xf, yf - 1, zf - 1), g(p[bb + 1], xf - 1, yf - 1, zf - 1))
    return l(w, l(v, x1, x2), l(v, x3, x4))


def fbm(x, y, z=0.0, scale=16.0, octaves=4, lacunarity=2.0, gain=0.5, seed=0):
    """Fractal noise. `scale` = feature size in blocks of the first octave."""
    x, y, z = (np.asarray(a, np.float32) / scale for a in (x, y, z))
    total, amp, norm = 0.0, 1.0, 0.0
    for o in range(octaves):
        f = lacunarity ** o
        total = total + amp * perlin(x * f, y * f, z * f, seed + 1013 * o)
        norm += amp
        amp *= gain
    return total / norm * 1.6  # perlin rarely exceeds +-0.7: stretch to ~[-1, 1]


def ridged(x, y, z=0.0, scale=16.0, octaves=4, seed=0):
    return np.clip(1.0 - np.abs(fbm(x, y, z, scale, octaves, seed=seed)), 0, 1)


def hash01(x, y, z=0, seed=0):
    x, y, z = (np.asarray(a).astype(np.int64) for a in (x, y, z))
    h = (x * 73856093) ^ (y * 19349663) ^ (z * 83492791) ^ (seed * 2654435761)
    h = h & 0xFFFFFFFF
    h = (h ^ (h >> 16)) * 0x45D9F3B & 0xFFFFFFFF
    h = (h ^ (h >> 16)) * 0x45D9F3B & 0xFFFFFFFF
    h = h ^ (h >> 16)
    return (h & 0xFFFFFF).astype(np.float32) / float(1 << 24)
