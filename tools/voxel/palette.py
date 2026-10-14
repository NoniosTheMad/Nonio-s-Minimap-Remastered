"""Block specs: what to put in each voxel of a fill. A spec is one of
  "minecraft:stone"                    a block state string
  None                                 keep whatever is there
  Mix({...: weight})                   weighted random (per position, deterministic)
  Gradient(by, [(upto, spec), ...])    pick by a field (height, depth, exposure, noise...) with optional jitter
  Noise([(upto, spec), ...], scale)    pick by fbm noise (clumpy patches)
  callable(ctx) -> spec array          anything else (ctx = FillContext)
Specs nest: Gradient stops and Mix items can themselves be Mixes/Gradients."""
import numpy as np

from . import noise


class FillContext:
    """Positions being filled (1D arrays xs, ys, zs) + lazily computed fields over them."""

    def __init__(self, scene, xs, ys, zs, mask):
        self.scene, self.xs, self.ys, self.zs, self.mask = scene, xs, ys, zs, mask
        self._cache = {}
        self._grids = {}  # full-grid fields, shared with subsets

    def subset(self, sel):
        c = FillContext(self.scene, self.xs[sel], self.ys[sel], self.zs[sel], self.mask)
        c._grids = self._grids
        for k, v in self._cache.items():
            c._cache[k] = v[sel]
        return c

    def field(self, by):
        if callable(by):
            return np.asarray(by(self), np.float32)
        if by in self._cache:
            return self._cache[by]
        s = self.scene
        if by == "x":
            v = self.xs.astype(np.float32)
        elif by == "y":
            v = self.ys.astype(np.float32)
        elif by == "z":
            v = self.zs.astype(np.float32)
        elif by == "height":  # 0 at the bottom of this fill, 1 at its top
            lo, hi = self.ys.min(), self.ys.max()
            v = ((self.ys - lo) / max(1, hi - lo)).astype(np.float32)
        elif by in ("depth", "exposure", "up"):
            if by not in self._grids:
                solid = s.solid() | self.mask
                if by == "depth":  # blocks of solid above this one (0 = sky-exposed top surface), counting this fill
                    g = depth_from_top(solid)
                elif by == "exposure":  # 3D distance to the nearest air (1 = surface block)
                    from scipy.ndimage import distance_transform_edt
                    g = distance_transform_edt(np.pad(solid, 1, constant_values=False))[1:-1, 1:-1, 1:-1]
                else:  # 1 if the block above is air (top faces)
                    above = np.zeros_like(solid)
                    above[:, :-1] = solid[:, 1:]
                    g = ~above
                self._grids[by] = g
            v = self._grids[by][self.xs, self.ys, self.zs].astype(np.float32)
        else:
            raise ValueError(f"unknown field {by!r}")
        self._cache[by] = v
        return v


def depth_from_top(solid):
    """depth[x,y,z] = number of solid voxels directly above (0 for the top surface); air = -1."""
    X, Y, Z = solid.shape
    d = np.full(solid.shape, -1, np.int32)
    run = np.full((X, Z), -1, np.int32)
    for y in range(Y - 1, -1, -1):
        run = np.where(solid[:, y], run + 1, -1)
        d[:, y] = run
    return d


class Mix:
    def __init__(self, items, seed=0):
        if isinstance(items, dict):
            items = list(items.items())
        self.specs = [s for s, _ in items]
        w = np.array([float(w) for _, w in items])
        self.cum = np.cumsum(w / w.sum())
        self.seed = seed

    def resolve(self, ctx):
        r = noise.hash01(ctx.xs, ctx.ys, ctx.zs, seed=self.seed + 7919)
        k = np.minimum(np.searchsorted(self.cum, r, side="right"), len(self.specs) - 1)
        return _dispatch(ctx, k, self.specs)


class Gradient:
    """by: 'y' | 'height' | 'depth' | 'exposure' | 'up' | 'x' | 'z' | callable(ctx)->array.
    stops: [(upto, spec), ...] ascending; spec applies while value < upto; the last applies above.
    jitter: amount added to the value (+-), dithered per block (jitter_scale=0) or clumpy fbm (jitter_scale>0)."""

    def __init__(self, by, stops, jitter=0.0, jitter_scale=0.0, seed=0):
        self.by, self.stops, self.jitter, self.js, self.seed = by, stops, jitter, jitter_scale, seed

    def resolve(self, ctx):
        v = ctx.field(self.by)
        if self.jitter:
            if self.js:
                n = noise.fbm(ctx.xs, ctx.ys, ctx.zs, self.js, 2, seed=self.seed + 31)
            else:
                n = noise.hash01(ctx.xs, ctx.ys, ctx.zs, seed=self.seed + 31) * 2 - 1
            v = v + self.jitter * n
        ups = np.array([u for u, _ in self.stops[:-1]] + [np.inf], np.float32)
        k = np.minimum(np.searchsorted(ups, v, side="right"), len(self.stops) - 1)
        return _dispatch(ctx, k, [s for _, s in self.stops])


class Noise:
    """Patches: fbm noise in [-1, 1] picks a stop. Noise([(-0.2, moss), (1, stone)], scale=6)."""

    def __init__(self, stops, scale=8.0, octaves=2, seed=0):
        self.stops, self.scale, self.oct, self.seed = stops, scale, octaves, seed

    def resolve(self, ctx):
        g = Gradient(lambda c: noise.fbm(c.xs, c.ys, c.zs, self.scale, self.oct, seed=self.seed), self.stops)
        return g.resolve(ctx)


def _dispatch(ctx, k, specs):
    out = np.zeros(len(ctx.xs), np.int32)
    for i, spec in enumerate(specs):
        sel = k == i
        if sel.any():
            out[sel] = resolve(spec, ctx.subset(sel))
    return out


KEEP = -1


def resolve(spec, ctx):
    """Palette ids for every position in ctx (-1 = keep)."""
    n = len(ctx.xs)
    if spec is None:
        return np.full(n, KEEP, np.int32)
    if isinstance(spec, str):
        return np.full(n, ctx.scene.id(spec), np.int32)
    if hasattr(spec, "resolve"):
        return spec.resolve(ctx)
    if callable(spec):
        r = spec(ctx)
        if isinstance(r, str) or r is None or hasattr(r, "resolve"):
            return resolve(r, ctx)
        r = np.asarray(r)
        if r.dtype.kind in "US":
            ids = {s: ctx.scene.id(s) for s in np.unique(r)}
            return np.vectorize(ids.get, otypes=[np.int32])(r)
        return r.astype(np.int32)
    raise TypeError(f"bad block spec {spec!r}")
