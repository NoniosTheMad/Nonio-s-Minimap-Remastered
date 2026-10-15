"""Signed distance fields (negative = inside), evaluated at voxel centres (x + 0.5 ...). Compose with operators:

    tower = cylinder((32, 0, 32), r=6, y0=10, y1=40) - cylinder((32, 0, 32), r=4.5, y0=11, y1=41)
    rock  = (sphere((30, 8, 30), 12) | sphere((40, 5, 28), 8)).smooth(4) ... see SDF.smooth_union
    scene.fill(rock.displace(amp=2.5, scale=6), mix)

| union   & intersection   - subtraction   ~ complement
All coordinates are scene-local block coordinates (floats are fine)."""
import numpy as np

from . import noise


class SDF:
    def __init__(self, f, bbox=None):
        self.f = f          # f(x, y, z) -> distance (broadcast arrays)
        self.bbox = bbox    # optional ((x0,y0,z0),(x1,y1,z1)) conservative bounds, speeds up evaluation

    def __call__(self, x, y, z):
        return self.f(x, y, z)

    # --- CSG
    def __or__(self, o):
        return SDF(lambda x, y, z: np.minimum(self(x, y, z), o(x, y, z)), _bb_union(self.bbox, o.bbox))

    def __and__(self, o):
        return SDF(lambda x, y, z: np.maximum(self(x, y, z), o(x, y, z)), _bb_inter(self.bbox, o.bbox))

    def __sub__(self, o):
        return SDF(lambda x, y, z: np.maximum(self(x, y, z), -o(x, y, z)), self.bbox)

    def __invert__(self):
        return SDF(lambda x, y, z: -self(x, y, z))

    def smooth_union(self, o, k=3.0):
        def f(x, y, z):
            a, b = self(x, y, z), o(x, y, z)
            h = np.clip(0.5 + 0.5 * (b - a) / k, 0, 1)
            return b + (a - b) * h - k * h * (1 - h)
        return SDF(f, _bb_union(self.bbox, o.bbox, k))

    def smooth_subtract(self, o, k=3.0):
        def f(x, y, z):
            a, b = self(x, y, z), -o(x, y, z)
            h = np.clip(0.5 - 0.5 * (b - a) / k, 0, 1)
            return b + (a - b) * h + k * h * (1 - h)
        return SDF(f, self.bbox)

    # --- modifiers
    def displace(self, amp=2.0, scale=8.0, octaves=3, seed=0):
        """Add fbm noise to the surface (rocky, organic)."""
        return SDF(lambda x, y, z: self(x, y, z) + amp * noise.fbm(x, y, z, scale, octaves, seed=seed), _grow(self.bbox, amp * 1.6))

    def shell(self, thickness=1.0):
        return SDF(lambda x, y, z: np.abs(self(x, y, z)) - thickness / 2, _grow(self.bbox, thickness))

    def grow(self, r):
        return SDF(lambda x, y, z: self(x, y, z) - r, _grow(self.bbox, r))

    def translate(self, dx, dy, dz):
        bb = None if self.bbox is None else (tuple(a + d for a, d in zip(self.bbox[0], (dx, dy, dz))),
                                             tuple(a + d for a, d in zip(self.bbox[1], (dx, dy, dz))))
        return SDF(lambda x, y, z: self(x - dx, y - dy, z - dz), bb)

    def scale_y(self, s):
        return SDF(lambda x, y, z: self(x, y / s, z) * min(1, s))

    def twist(self, cx, cz, rad_per_block):
        def f(x, y, z):
            a = y * rad_per_block
            c, s = np.cos(a), np.sin(a)
            dx, dz = x - cx, z - cz
            return self(cx + c * dx - s * dz, y, cz + s * dx + c * dz)
        return SDF(f)

    def mask(self, shape, offset=(0, 0, 0)):
        """Boolean array of `shape` (the scene grid): voxel centre inside."""
        out = np.zeros(shape, bool)
        lo = [0, 0, 0]; hi = list(shape)
        if self.bbox is not None:
            for i in range(3):
                lo[i] = max(0, int(np.floor(self.bbox[0][i] - offset[i])) - 1)
                hi[i] = min(shape[i], int(np.ceil(self.bbox[1][i] - offset[i])) + 2)
                if hi[i] <= lo[i]:
                    return out
        x, y, z = np.ogrid[lo[0]:hi[0], lo[1]:hi[1], lo[2]:hi[2]]
        d = self(x + 0.5 + offset[0], y + 0.5 + offset[1], z + 0.5 + offset[2])
        out[lo[0]:hi[0], lo[1]:hi[1], lo[2]:hi[2]] = np.broadcast_to(d <= 0, (hi[0] - lo[0], hi[1] - lo[1], hi[2] - lo[2]))
        return out

    def distance(self, shape):
        x, y, z = np.ogrid[0:shape[0], 0:shape[1], 0:shape[2]]
        return np.broadcast_to(self(x + 0.5, y + 0.5, z + 0.5), shape)


def _bb_union(a, b, pad=0):
    if a is None or b is None:
        return None
    return (tuple(min(p, q) - pad for p, q in zip(a[0], b[0])), tuple(max(p, q) + pad for p, q in zip(a[1], b[1])))


def _bb_inter(a, b):
    if a is None:
        return b
    if b is None:
        return a
    return (tuple(max(p, q) for p, q in zip(a[0], b[0])), tuple(min(p, q) for p, q in zip(a[1], b[1])))


def _grow(bb, r):
    if bb is None:
        return None
    return (tuple(v - r for v in bb[0]), tuple(v + r for v in bb[1]))


# ------------------------------------------------------------------ primitives
def sphere(c, r):
    cx, cy, cz = c
    return SDF(lambda x, y, z: np.sqrt((x - cx) ** 2 + (y - cy) ** 2 + (z - cz) ** 2) - r,
               ((cx - r, cy - r, cz - r), (cx + r, cy + r, cz + r)))


def ellipsoid(c, radii):
    cx, cy, cz = c
    rx, ry, rz = radii
    m = min(radii)
    return SDF(lambda x, y, z: (np.sqrt(((x - cx) / rx) ** 2 + ((y - cy) / ry) ** 2 + ((z - cz) / rz) ** 2) - 1) * m,
               ((cx - rx, cy - ry, cz - rz), (cx + rx, cy + ry, cz + rz)))


def box(p0, p1, round=0.0):
    """Axis-aligned box between corners p0 and p1 (block coords, p1 exclusive like slices: box((0,0,0),(4,4,4)) = 4^3)."""
    c = [(a + b) / 2 for a, b in zip(p0, p1)]
    h = [abs(b - a) / 2 - round for a, b in zip(p0, p1)]

    def f(x, y, z):
        qx, qy, qz = np.abs(x - c[0]) - h[0], np.abs(y - c[1]) - h[1], np.abs(z - c[2]) - h[2]
        out = np.sqrt(np.maximum(qx, 0) ** 2 + np.maximum(qy, 0) ** 2 + np.maximum(qz, 0) ** 2)
        return out + np.minimum(np.maximum(qx, np.maximum(qy, qz)), 0) - round
    return SDF(f, (tuple(min(a, b) for a, b in zip(p0, p1)), tuple(max(a, b) for a, b in zip(p0, p1))))


def cylinder(c, r, y0, y1, r_top=None):
    """Vertical cylinder (or cone frustum with r_top) centred on (cx, cz) from y0 to y1."""
    cx, _, cz = c
    rt = r if r_top is None else r_top

    def f(x, y, z):
        t = np.clip((y - y0) / max(1e-6, (y1 - y0)), 0, 1)
        rr = r + (rt - r) * t
        d_r = np.sqrt((x - cx) ** 2 + (z - cz) ** 2) - rr
        d_y = np.maximum(y0 - y, y - y1)
        return np.maximum(d_r, d_y)
    R = max(r, rt)
    return SDF(f, ((cx - R, y0, cz - R), (cx + R, y1, cz + R)))


def capsule(a, b, r):
    a, b = np.array(a, float), np.array(b, float)
    ba = b - a
    bb2 = float(ba @ ba)

    def f(x, y, z):
        px, py, pz = x - a[0], y - a[1], z - a[2]
        h = np.clip((px * ba[0] + py * ba[1] + pz * ba[2]) / bb2, 0, 1)
        return np.sqrt((px - ba[0] * h) ** 2 + (py - ba[1] * h) ** 2 + (pz - ba[2] * h) ** 2) - r
    lo = np.minimum(a, b) - r; hi = np.maximum(a, b) + r
    return SDF(f, (tuple(lo), tuple(hi)))


def torus(c, R, r):
    cx, cy, cz = c
    return SDF(lambda x, y, z: np.sqrt((np.sqrt((x - cx) ** 2 + (z - cz) ** 2) - R) ** 2 + (y - cy) ** 2) - r,
               ((cx - R - r, cy - r, cz - R - r), (cx + R + r, cy + r, cz + R + r)))


def half_space(axis="y", at=0.0, below=True):
    i = "xyz".index(axis)
    s = 1 if below else -1
    return SDF(lambda x, y, z: s * ((x, y, z)[i] - at))


def heightfield(h, y0=-1e9):
    """Terrain: solid where y < h[x, z] (h = 2D array over the scene's X x Z, e.g. from terrain.heightmap)."""
    h = np.asarray(h, np.float32)

    def f(x, y, z):
        xi = np.clip(np.asarray(x - 0.5).astype(int), 0, h.shape[0] - 1)
        zi = np.clip(np.asarray(z - 0.5).astype(int), 0, h.shape[1] - 1)
        return np.maximum(y - h[xi, zi], y0 - y)
    return SDF(f)


def from_mask(m):
    """Wrap a boolean grid as an SDF-ish field (-1 inside, +1 outside) so it composes with the operators."""
    m = np.asarray(m, bool)

    def f(x, y, z):
        xi, yi, zi = (np.clip(np.asarray(a - 0.5).astype(int), 0, n - 1) for a, n in zip((x, y, z), m.shape))
        return np.where(m[xi, yi, zi], -1.0, 1.0)
    return SDF(f)
