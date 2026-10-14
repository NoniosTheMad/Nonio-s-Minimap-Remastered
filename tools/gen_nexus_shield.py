# Usage: python tools/gen_nexus_shield.py resourcepack/assets/nonios/textures/block
# Generates animated forcefield-style shell textures (grayscale, tinted in-game via dyed_color).
# Based on vanilla textures/misc/forcefield.png: diagonal stripes, period 8 px (here 2x -> 32 px tile, period 16).
# Damage stages (cumulative): nexus_shield (>75%), _crack1 (<=75%), _crack2 (<=50%), _crack3 (<=25%).
# Cracks are bold (white core + black outline) so they stay readable from 10-20 blocks.
import math, random, json, sys
from PIL import Image
from pathlib import Path
out = Path(sys.argv[1]); out.mkdir(parents=True, exist_ok=True)
S, FR = 32, 8                     # 32x32 per frame, 8 frames (shift 2 px/frame = one full period)
prof = [(201,171),(174,156),(179,126),(153,60),(0,0),(0,0),(0,0),(0,0)]
prof = [p for p in prof for _ in (0,1)]
BASE_A = 34                       # faint fill so the shell reads as a volume

def star(seed, cx, cy, rays, length):
    """impact star: jagged rays from (cx,cy); returns core pixel set (1 px; outline adds the dark border)"""
    rnd = random.Random(seed); core = set()
    for i in range(rays):
        ang = 2 * math.pi * i / rays + rnd.uniform(-0.4, 0.4)
        x, y = float(cx), float(cy); n = rnd.randint(length // 2, length)
        for _ in range(n):
            ang += rnd.uniform(-0.35, 0.35)
            x += math.cos(ang); y += math.sin(ang)
            core.add((int(round(x)) % S, int(round(y)) % S))
    return core

def holes(seed, n):
    rnd = random.Random(seed); px = set()
    for _ in range(n):
        cx, cy, r = rnd.randrange(S), rnd.randrange(S), rnd.randint(3, 5)
        for x in range(cx-r, cx+r+1):
            for y in range(cy-r, cy+r+1):
                if (x-cx)**2 + (y-cy)**2 <= r*r: px.add((x % S, y % S))
    return px

def outline(core):
    o = set()
    for (x, y) in core:
        for dx in (-1,0,1):
            for dy in (-1,0,1):
                p = ((x+dx) % S, (y+dy) % S)
                if p not in core: o.add(p)
    return o

def make(name, core=frozenset(), hole_px=frozenset(), base_a=BASE_A):
    edge = outline(core)
    im = Image.new("RGBA", (S, S * FR))
    for f in range(FR):
        shimmer = 1.0 + 0.08 * (1 if f % 4 < 2 else -1)
        for y in range(S):
            for x in range(S):
                L, A = prof[(x + y + 2 * f) % 16]
                a = max(A, base_a); l = 255 if A == 0 else min(255, int((L + 60) * shimmer))
                if x in (0, S-1) or y in (0, S-1): a, l = max(a, 150), 255   # glowing edges
                if (x, y) in hole_px: a, l = 0, 0
                if (x, y) in edge: a, l = 190, 0                            # dark crack outline
                if (x, y) in core: a, l = 255, 255                          # bright crack core
                im.putpixel((x, y + f * S), (l, l, l, min(255, int(a))))
    im.save(out / f"{name}.png")
    (out / f"{name}.png.mcmeta").write_text(json.dumps({"animation": {"frametime": 2, "interpolate": True}}, indent=1))

c1 = star(1, 11, 12, 5, 12)
c2 = c1 | star(2, 23, 22, 6, 13) | star(3, 25, 6, 4, 9)
c3 = c2 | star(4, 6, 26, 5, 10) | star(5, 17, 4, 4, 8)
h3 = holes(9, 4) - c3
for old in ("nexus_shield_cracked", "nexus_shield_critical"):
    for ext in (".png", ".png.mcmeta"):
        (out / (old + ext)).unlink(missing_ok=True)
make("nexus_shield")
make("nexus_shield_crack1", c1)
make("nexus_shield_crack2", c2, base_a=44)
make("nexus_shield_crack3", c3, h3, base_a=54)
print("ok")
