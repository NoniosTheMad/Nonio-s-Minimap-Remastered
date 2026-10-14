"""shaderlab: run the pack's post effects offline on a test scene and film them.

    python tools/shaderlab/lab.py --fx cosmic --time night --frames 24 --out out/cosmic
    python tools/shaderlab/lab.py --fx angel --fx-file my_angel.json ...   (any post_effect JSON)

The scene (scene.frag) is a ray-marched Minecraft-like voxel world that writes colour with the demo
overlay's low-bit markers and a reversed-Z depth, so the real post_effect JSONs and .fsh files run
unchanged: std140 uniform blocks are rewritten to plain uniforms, includes resolved from the pack and
the vanilla client jar, targets are RGBA8 like the game, `bilinear` inputs get GL_LINEAR.
Outputs: <out>.gif (animation), <out>_sheet.png (contact sheet), <out>_NN.png (with --pngs).
"""
import argparse, json, math, os, re, zipfile
from pathlib import Path

import moderngl
import numpy as np
from PIL import Image

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
PACK = ROOT / "resourcepack" / "assets"
OVERLAY = ROOT / "demos" / "shaders" / "resourcepack" / "assets"
JAR = Path(r"C:\Users\danir\curseforge\minecraft\Install\versions\26.3\26.3.jar")
VANILLA = HERE / ".vanilla"  # extracted shaders (gitignored)

VS = """#version 330
out vec2 texCoord;
void main() {
    vec2 uv = vec2((gl_VertexID << 1) & 2, gl_VertexID & 2);
    gl_Position = vec4(uv * 2.0 - 1.0, 0.0, 1.0);
    texCoord = uv;
}
"""


def vanilla():
    if not (VANILLA / "assets").exists():
        with zipfile.ZipFile(JAR) as z:
            for n in z.namelist():
                if n.startswith("assets/minecraft/shaders/") or n.startswith("assets/minecraft/post_effect/"):
                    z.extract(n, VANILLA)
    return VANILLA / "assets"


def resolve(ns_path, kind):
    """kind: 'shaders' file id like nonios:post/x (.fsh) or include id minecraft:x.glsl"""
    ns, p = ns_path.split(":")
    for base in (PACK, OVERLAY, vanilla()):
        f = base / ns / kind / p
        if f.exists():
            return f
    raise FileNotFoundError(ns_path)


def preprocess(src, seen=None):
    seen = seen if seen is not None else set()
    out = []
    for line in src.splitlines():
        m = re.match(r"\s*#include\s*<([^>]+)>", line)
        if m:
            inc = m.group(1)
            if inc not in seen:
                seen.add(inc)
                f = resolve(inc, "shaders/include")
                out.append(preprocess(f.read_text(), seen))
            continue
        if line.startswith("#extension"):
            line = line.replace("require", "enable")
        out.append(line)
    s = "\n".join(out)
    s = re.sub(r"//[^\n]*", "", s)

    def block(m):
        body = m.group(2)
        decls = [d.strip() for d in body.split(";") if d.strip()]
        return "\n".join("uniform %s;" % d for d in decls)

    s = re.sub(r"layout\s*\(\s*std140\s*\)\s*uniform\s+(\w+)\s*\{(.*?)\}\s*;", block, s, flags=re.S)
    s = s.replace("gl_VertexIndex", "gl_VertexID")
    # version must stay first
    lines = s.splitlines()
    ver = [l for l in lines if l.startswith("#version")]
    rest = [l for l in lines if not l.startswith("#version")]
    return "\n".join(ver[:1] + ["#extension GL_ARB_separate_shader_objects : enable"] + rest)


class Lab:
    def __init__(self, w, h):
        self.w, self.h = w, h
        self.ctx = moderngl.create_standalone_context(require=330)
        self.vao_cache = {}
        self.progs = {}
        self.scene = self.ctx.program(vertex_shader=VS, fragment_shader=preprocess((HERE / "scene.frag").read_text()))
        self.main = self.ctx.texture((w, h), 4)
        self.depth = self.ctx.texture((w, h), 1, dtype="f4")
        self.scene_fbo = self.ctx.framebuffer([self.main, self.depth])
        self.targets = {}

    def vao(self, prog):
        k = id(prog)
        if k not in self.vao_cache:
            self.vao_cache[k] = self.ctx.vertex_array(prog, [])
        return self.vao_cache[k]

    def set(self, prog, name, v):
        if name in prog:
            u = prog[name]
            if isinstance(v, (list, tuple)):
                v = tuple(v)[: u.dimension] if u.dimension > 1 else v[0]
            elif u.dimension > 1:
                v = (v,) * u.dimension
            u.value = v

    def render_scene(self, cam, rot, daytime, t, fov=70.0, rd=160.0):
        p = self.scene
        self.set(p, "Res", (self.w, self.h))
        self.set(p, "CamPos", cam)
        self.set(p, "CamRot", rot)
        self.set(p, "TanHalfFov", math.tan(math.radians(fov / 2)))
        self.set(p, "DayTime", daytime)
        self.set(p, "Time", t)
        self.set(p, "Near", 0.05)
        self.set(p, "RenderDist", rd)
        self.scene_fbo.use()
        self.vao(p).render(moderngl.TRIANGLES, vertices=3)

    def prog(self, fsh_id):
        if fsh_id not in self.progs:
            src = preprocess(resolve(fsh_id, "shaders").read_text() if False else
                             resolve(fsh_id.split(":")[0] + ":" + fsh_id.split(":")[1] + ".fsh", "shaders").read_text())
            self.progs[fsh_id] = self.ctx.program(vertex_shader=VS, fragment_shader=src)
        return self.progs[fsh_id]

    def target(self, name):
        if name == "minecraft:main":
            return self.main
        if name not in self.targets:
            self.targets[name] = self.ctx.texture((self.w, self.h), 4)
        return self.targets[name]

    def run_effect(self, effect, game_time):
        """effect: post_effect dict. Runs every pass; result ends in self.main."""
        for p in effect["passes"]:
            prog = self.prog(p["fragment_shader"])
            unit = 0
            for inp in p.get("inputs", []):
                if inp.get("use_depth_buffer"):
                    tex = self.depth
                else:
                    tex = self.target(inp["target"])
                f = moderngl.LINEAR if inp.get("bilinear") else moderngl.NEAREST
                tex.filter = (f, f)
                tex.repeat_x = tex.repeat_y = False
                tex.use(unit)
                self.set(prog, inp["sampler_name"] + "Sampler", unit)
                unit += 1
            self.set(prog, "OutSize", (self.w, self.h))
            self.set(prog, "InSize", (self.w, self.h))
            self.set(prog, "ScreenSize", (self.w, self.h))
            self.set(prog, "GameTime", game_time)
            self.set(prog, "MenuBlurRadius", 0)
            for blk in p.get("uniforms", {}).values():
                for u in blk:
                    self.set(prog, u["name"], u["value"])
            out = self.target(p["output"])
            # the game never reads and writes the same target in one pass; copy main if needed
            fbo = self.ctx.framebuffer([out])
            fbo.use()
            self.vao(prog).render(moderngl.TRIANGLES, vertices=3)
            fbo.release()

    def read_main(self):
        a = np.frombuffer(self.main.read(), dtype=np.uint8).reshape(self.h, self.w, 4)
        return Image.fromarray(a[::-1, :, :3].copy())


def load_effect(name_or_file):
    f = Path(name_or_file)
    if not f.exists():
        f = PACK / "nonios" / "post_effect" / (name_or_file + ".json")
    return json.loads(f.read_text())


TIMES = {"noon": 0.0, "dusk": 0.23, "night": 0.5, "dawn": 0.77}

SHOTS = {
    # name: (start cam, end cam, yaw, pitch)  - a slow dolly over the trees
    "walk": ((4.5, 80.0, -30.0), (4.5, 80.5, -14.0), (0.35, 0.39), (-0.12, -0.10)),
    "high": ((0.5, 150.0, -40.0), (6.5, 150.0, -36.0), (0.30, 0.34), (-0.35, -0.33)),
    "moon": ((0.5, 120.0, -40.0), (2.5, 120.0, -38.0), (-1.88, -1.84), (0.08, 0.10)),
    "sun": ((-40.5, 70.0, -10.5), (-38.5, 70.3, -10.0), (1.26, 1.33), (0.20, 0.19)),
    "treemoon": ((10.5, 71.0, -22.0), (11.5, 71.0, -21.0), (-1.95, -1.80), (0.42, 0.45)),
    "trees": ((9.5, 76.0, -24.0), (11.5, 76.0, -20.0), (0.10, 0.16), (0.05, 0.08)),
}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--fx", action="append", default=[], help="post effect id or json file (stack in order)")
    ap.add_argument("--time", default="noon")
    ap.add_argument("--shot", default="walk")
    ap.add_argument("--frames", type=int, default=16)
    ap.add_argument("--secs", type=float, default=4.0)
    ap.add_argument("--size", default="640x360")
    ap.add_argument("--t0", type=float, default=0.0, help="game seconds offset")
    ap.add_argument("--rd", type=float, default=160.0, help="render distance (blocks)")
    ap.add_argument("--out", required=True)
    ap.add_argument("--pngs", action="store_true")
    ap.add_argument("--gif-scale", type=float, default=1.0)
    a = ap.parse_args()
    w, h = map(int, a.size.split("x"))
    lab = Lab(w, h)
    effects = [load_effect(x) for x in a.fx]
    c0, c1, yaw, pitch = SHOTS[a.shot]
    frames = []
    for i in range(a.frames):
        k = i / max(a.frames - 1, 1)
        sec = a.t0 + k * a.secs
        cam = tuple(c0[j] + (c1[j] - c0[j]) * k for j in range(3))
        rot = (yaw[0] + (yaw[1] - yaw[0]) * k, pitch[0] + (pitch[1] - pitch[0]) * k)
        lab.render_scene(cam, rot, TIMES.get(a.time, 0.0) if a.time in TIMES else float(a.time), sec, rd=a.rd)
        gt = (sec * 20.0 / 24000.0) % 1.0
        for e in effects:
            lab.run_effect(e, gt)
        frames.append(lab.read_main())
    out = Path(a.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    if a.pngs:
        for i, f in enumerate(frames):
            f.save(f"{out}_{i:02d}.png")
    g = [f.resize((int(w * a.gif_scale), int(h * a.gif_scale)), Image.LANCZOS) if a.gif_scale != 1 else f for f in frames]
    g[0].save(f"{out}.gif", save_all=True, append_images=g[1:], duration=int(1000 * a.secs / max(a.frames, 1)), loop=0)
    # contact sheet: up to 6 frames, 3 per row
    pick = [frames[int(i * (len(frames) - 1) / 5)] for i in range(6)] if len(frames) >= 6 else frames
    cols = 3 if len(pick) > 1 else 1
    rows = (len(pick) + cols - 1) // cols
    sheet = Image.new("RGB", (w * cols, h * rows))
    for i, f in enumerate(pick):
        sheet.paste(f, ((i % cols) * w, (i // cols) * h))
    sheet.save(f"{out}_sheet.png")
    print("wrote", f"{out}.gif", f"{out}_sheet.png")


if __name__ == "__main__":
    main()
