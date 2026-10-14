# Usage: python tools/gen_nexus_shield.py resourcepack/assets/nonios/textures/block
# Generates animated forcefield-style shell textures (grayscale, tinted in-game via dyed_color).
# Based on vanilla textures/misc/forcefield.png: diagonal stripes, period 8 px (here 2x -> 32 px tile, period 16).
import random, json, sys
from PIL import Image
from pathlib import Path
out = Path(sys.argv[1]); out.mkdir(parents=True, exist_ok=True)
S, FR = 32, 8                     # 32x32 per frame, 8 frames (shift 2 px/frame = one full period)
# vanilla stripe profile (L, A) for 8 steps; doubled to 16
prof = [(201,171),(174,156),(179,126),(153,60),(0,0),(0,0),(0,0),(0,0)]
prof = [p for p in prof for _ in (0,1)]
BASE_A = 34                       # faint fill so the shell reads as a volume
def cracks(seed, n, length):
    rnd = random.Random(seed); px = set()
    for _ in range(n):
        x, y = rnd.randrange(S), rnd.randrange(S); dx, dy = rnd.choice([(1,0),(0,1),(-1,0),(0,-1),(1,1),(-1,1)])
        for _ in range(length):
            px.add((x % S, y % S))
            if rnd.random() < 0.35: dx, dy = rnd.choice([(1,0),(0,1),(-1,0),(0,-1),(1,1),(1,-1),(-1,1),(-1,-1)])
            x += dx; y += dy
            if rnd.random() < 0.08:  # branch
                bx, by = x, y
                for _ in range(length // 3):
                    px.add((bx % S, by % S)); bx += rnd.choice([-1,0,1]); by += rnd.choice([-1,0,1])
    return px
def holes(seed, n):
    rnd = random.Random(seed); px = set()
    for _ in range(n):
        cx, cy, r = rnd.randrange(S), rnd.randrange(S), rnd.randint(2, 4)
        for x in range(cx-r, cx+r+1):
            for y in range(cy-r, cy+r+1):
                if (x-cx)**2 + (y-cy)**2 <= r*r: px.add((x % S, y % S))
    return px
def make(name, crack_px=frozenset(), hole_px=frozenset()):
    im = Image.new("RGBA", (S, S * FR))
    for f in range(FR):
        shimmer = 1.0 + 0.08 * (1 if f % 4 < 2 else -1)
        for y in range(S):
            for x in range(S):
                L, A = prof[(x + y + 2 * f) % 16]
                a = max(A, BASE_A); l = 255 if A == 0 else min(255, int((L + 60) * shimmer))
                if x in (0, S-1) or y in (0, S-1): a, l = max(a, 150), 255   # glowing edges
                if (x, y) in hole_px: a = A // 4
                if (x, y) in crack_px: a, l = 235, 255
                im.putpixel((x, y + f * S), (l, l, l, min(255, int(a))))
    im.save(out / f"{name}.png")
    (out / f"{name}.png.mcmeta").write_text(json.dumps({"animation": {"frametime": 2, "interpolate": True}}, indent=1))
make("nexus_shield")
make("nexus_shield_cracked", cracks(7, 3, 14))
make("nexus_shield_critical", cracks(7, 3, 14) | cracks(11, 4, 18), holes(5, 4))
print("ok")
