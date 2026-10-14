# Usage: python tools/gen_nexus_shield.py resourcepack/assets/nonios/textures/block
# Generates animated forcefield-style shell textures (grayscale, tinted in-game via dyed_color).
# Based on vanilla textures/misc/forcefield.png: diagonal stripes, period 8 px (here 2x -> 32 px tile, period 16).
# Damage stages: nexus_shield (>75%), _crack1 (<=75%), _crack2 (<=50%), _crack3 (<=25%).
# Cracks = vanilla block-breaking overlay destroy_stage_2/5/8 (read from the client jar), scaled 2x nearest onto the
# 32 px grid (same texel size as the stripes, crisp at distance), drawn dark so players read them as "this is breaking".
import io, json, sys, zipfile
from PIL import Image
from pathlib import Path
JAR = r"C:\Users\danir\curseforge\minecraft\Install\versions\26.3\26.3.jar"
out = Path(sys.argv[1]); out.mkdir(parents=True, exist_ok=True)
S, FR = 32, 8                     # 32x32 per frame, 8 frames (shift 2 px/frame = one full period)
prof = [(201,171),(174,156),(179,126),(153,60),(0,0),(0,0),(0,0),(0,0)]
prof = [p for p in prof for _ in (0,1)]
BASE_A = 34                       # faint fill so the shell reads as a volume

def destroy(stage):
    """{(x,y): 'line'|'shade'} from destroy_stage_N: 61 = crack line, 155 = crack edge, rest transparent."""
    with zipfile.ZipFile(JAR) as z:
        im = Image.open(io.BytesIO(z.read(f"assets/minecraft/textures/block/destroy_stage_{stage}.png"))).convert("RGBA")
    px = {}
    for y in range(16):
        for x in range(16):
            r, g, b, a = im.getpixel((x, y))
            kind = None if a < 128 else "line" if r < 100 else "shade" if r < 200 else None
            if kind:
                for dx in (0, 1):
                    for dy in (0, 1): px[(2*x + dx, 2*y + dy)] = kind
    return px

def make(name, cracks=None, base_a=BASE_A):
    cracks = cracks or {}
    im = Image.new("RGBA", (S, S * FR))
    for f in range(FR):
        shimmer = 1.0 + 0.08 * (1 if f % 4 < 2 else -1)
        for y in range(S):
            for x in range(S):
                L, A = prof[(x + y + 2 * f) % 16]
                a = max(A, base_a); l = 255 if A == 0 else min(255, int((L + 60) * shimmer))
                if x in (0, S-1) or y in (0, S-1): a, l = max(a, 150), 255   # glowing edges
                k = cracks.get((x, y))
                if k == "line": a, l = 235, 18                              # crack line (dark)
                elif k == "shade": a, l = max(a, 150), 95                   # crack edge
                im.putpixel((x, y + f * S), (l, l, l, min(255, int(a))))
    im.save(out / f"{name}.png")
    (out / f"{name}.png.mcmeta").write_text(json.dumps({"animation": {"frametime": 2, "interpolate": True}}, indent=1))

make("nexus_shield")
make("nexus_shield_crack1", destroy(2))
make("nexus_shield_crack2", destroy(5), base_a=40)
make("nexus_shield_crack3", destroy(8), base_a=46)
print("ok")
