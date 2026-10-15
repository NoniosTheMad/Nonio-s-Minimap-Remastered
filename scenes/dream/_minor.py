"""Shared ground kit for the minor Dream sites (17 x 17 ground sites)."""
import numpy as np

from scenes.dream._dream import ROCK, SOIL, skirt
from tools.voxel.palette import Mix, Noise

FLOWERS = ["wildflowers[flower_amount=3,facing=north]", "wildflowers[flower_amount=4,facing=east]",
           "pink_petals[flower_amount=2,facing=south]", "pink_petals[flower_amount=4,facing=west]",
           "short_grass", "short_grass", "short_grass", "fern", "lily_of_the_valley", "azure_bluet", "allium",
           "moss_carpet", "moss_carpet"]


def disc(s, a, r=8.2, seed=0):
    """Irregular turf disc at y = a-1 (ground the site sits on) + a tapering skirt below. Returns the 2D footprint."""
    W, _, D = s.shape
    cx, cz = (W - 1) / 2, (D - 1) / 2
    gx, gz = np.meshgrid(np.arange(W), np.arange(D), indexing="ij")
    rng = np.random.default_rng(seed)
    ang = np.arctan2(gz - cz, gx - cx)
    wob = 1 + 0.07 * np.sin(3 * ang + rng.uniform(0, 6)) + 0.05 * np.sin(7 * ang + rng.uniform(0, 6))
    fp = np.hypot(gx - cx, gz - cz) < r * wob
    m = np.zeros(s.shape, bool)
    m[:, a - 1, :] = fp
    s.fill(m, Noise([(-0.35, "moss_block"), (0.45, "grass_block"), (1, Mix({"grass_block": 3, "rooted_dirt": 1}))],
                    scale=4, seed=seed))
    skirt(s, fp, a, depth=8, seed=seed)
    return fp


def scatter(s, a, fp, chance=0.35, seed=0, keep_clear=None):
    """Flowers / grass / moss carpet on free turf cells (y = a) of the footprint."""
    rng = np.random.default_rng(seed)
    W, _, D = s.shape
    for x in range(W):
        for z in range(D):
            if not fp[x, z] or s.idx[x, a, z] != 0 or rng.random() > chance:
                continue
            if keep_clear is not None and keep_clear[x, z]:
                continue
            g = s.get(x, a - 1, z)
            if "grass_block" not in g and "moss_block" not in g:
                continue
            s.set(x, a, z, FLOWERS[rng.integers(len(FLOWERS))])
