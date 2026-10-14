"""Headless renderer (moderngl, offscreen OpenGL 3.3) with the game's block models + textures, sun shadows,
ambient occlusion and fog. Writes PNGs an agent can look at with its Read tool.

    views = render_views(scene, out_dir)   # -> {"iso_se": Path, ..., "top": Path, "eye_spawn_white": Path, "sheet": Path}

Views: iso_ne/iso_nw/iso_se/iso_sw (orthographic, 4 corners), top (orthographic, north up), one eye-level shot per
marker named spawn_*/cam_*/eye_* (1.62 above the marker, towards look_at / yaw / the scene centre), sightlines
(top map coloured by how many spawn/key markers see each walkable cell) and sheet (all of it on one image)."""
import math, time
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont

from . import mesh as meshmod

SKY_TOP = np.array([0.45, 0.62, 0.92]); SKY_BOT = np.array([0.80, 0.87, 0.97])
SUN = np.array([0.45, 0.80, 0.38]); SUN /= np.linalg.norm(SUN)   # from the south-east, high afternoon

VS = """#version 330
uniform mat4 mvp; uniform mat4 lightmvp;
in vec3 in_pos; in vec3 in_uvl; in vec3 in_nrm; in vec3 in_col;
out vec3 uvl; out vec3 nrm; out vec3 col; out vec4 lpos; out vec3 wpos;
void main(){ gl_Position = mvp*vec4(in_pos,1.0); uvl=in_uvl; nrm=in_nrm; col=in_col; wpos=in_pos;
  lpos = lightmvp*vec4(in_pos + in_nrm*0.04, 1.0); }"""
FS = """#version 330
uniform sampler2DArray tex; uniform sampler2DShadow shadow; uniform vec3 sun; uniform vec3 eye;
uniform vec3 fogcol; uniform float fogstart; uniform float fogend; uniform int translucent; uniform int shadows;
in vec3 uvl; in vec3 nrm; in vec3 col; in vec4 lpos; in vec3 wpos; out vec4 frag;
void main(){
  vec4 t = texture(tex, uvl);
  if (translucent==0 && t.a < 0.5) discard;
  vec3 n = normalize(nrm);
  // Minecraft-like directional face shading x soft sun
  float face = abs(n.y) > 0.5 ? (n.y > 0.0 ? 1.0 : 0.5) : (abs(n.z) > 0.5 ? 0.8 : 0.6);
  float lit = 1.0;
  if (shadows==1) {
    vec3 p = lpos.xyz/lpos.w*0.5+0.5;
    if (p.x>0.0 && p.x<1.0 && p.y>0.0 && p.y<1.0 && p.z<1.0) {
      float s = 0.0; vec2 ts = 1.0/vec2(textureSize(shadow,0));
      for (int i=-1;i<=1;i++) for (int j=-1;j<=1;j++) s += texture(shadow, vec3(p.xy+vec2(i,j)*ts, p.z-0.0015));
      lit = s/9.0;
    }
  }
  float ndl = max(dot(n, sun), 0.0);
  float light = face*(0.5 + 0.5*lit*(0.3+0.7*ndl));
  vec3 c = t.rgb*col*light;
  float d = distance(eye, wpos);
  float f = clamp((d-fogstart)/(fogend-fogstart), 0.0, 1.0);
  c = mix(c, fogcol, f*f);
  frag = vec4(c, translucent==1 ? max(t.a, 0.55) : 1.0);
}"""
SVS = """#version 330
uniform mat4 lightmvp; in vec3 in_pos; in vec3 in_uvl; out vec3 uvl;
void main(){ gl_Position = lightmvp*vec4(in_pos,1.0); uvl=in_uvl; }"""
SFS = """#version 330
uniform sampler2DArray tex; in vec3 uvl; void main(){ if (texture(tex, uvl).a < 0.5) discard; }"""


# ------------------------------------------------------------------ matrices
def look_at(eye, target, up=(0, 1, 0)):
    eye, target, up = (np.asarray(v, float) for v in (eye, target, up))
    f = target - eye; f /= np.linalg.norm(f)
    if abs(np.dot(f, up / np.linalg.norm(up))) > 0.999:
        up = np.array([0, 0, -1.0])
    s = np.cross(f, up); s /= np.linalg.norm(s)
    u = np.cross(s, f)
    m = np.eye(4)
    m[0, :3], m[1, :3], m[2, :3] = s, u, -f
    m[:3, 3] = -m[:3, :3] @ eye
    return m


def ortho(l, r, b, t, n, f):
    m = np.eye(4)
    m[0, 0] = 2 / (r - l); m[1, 1] = 2 / (t - b); m[2, 2] = -2 / (f - n)
    m[0, 3] = -(r + l) / (r - l); m[1, 3] = -(t + b) / (t - b); m[2, 3] = -(f + n) / (f - n)
    return m


def perspective(fovy, aspect, n, f):
    t = 1 / math.tan(math.radians(fovy) / 2)
    m = np.zeros((4, 4))
    m[0, 0] = t / aspect; m[1, 1] = t; m[2, 2] = (f + n) / (n - f); m[2, 3] = 2 * f * n / (n - f); m[3, 2] = -1
    return m


def _fit_ortho(view, pts, aspect, margin=1.06):
    p = (view @ np.c_[pts, np.ones(len(pts))].T).T[:, :3]
    lo, hi = p.min(0), p.max(0)
    cx, cy = (lo[:2] + hi[:2]) / 2
    w, h = (hi[0] - lo[0]) * margin, (hi[1] - lo[1]) * margin
    if w / h < aspect:
        w = h * aspect
    else:
        h = w / aspect
    return ortho(cx - w / 2, cx + w / 2, cy - h / 2, cy + h / 2, -hi[2] - 10, -lo[2] + 10)


class Camera:
    def __init__(self, name, eye, target, kind="persp", fov=70.0, elev=None):
        self.name, self.eye, self.target, self.kind, self.fov = name, np.asarray(eye, float), np.asarray(target, float), kind, fov


# ------------------------------------------------------------------ renderer
class Renderer:
    def __init__(self, width=1280, height=800, ssaa=2):
        import moderngl
        self.ctx = moderngl.create_standalone_context()
        self.w, self.h, self.ss = width, height, ssaa
        self.prog = self.ctx.program(vertex_shader=VS, fragment_shader=FS)
        self.sprog = self.ctx.program(vertex_shader=SVS, fragment_shader=SFS)
        W, H = width * ssaa, height * ssaa
        self.fbo = self.ctx.framebuffer(self.ctx.renderbuffer((W, H), 4), self.ctx.depth_renderbuffer((W, H)))
        self.sres = 4096
        self.sdepth = self.ctx.depth_texture((self.sres, self.sres))
        self.sdepth.compare_func = "<="
        self.sdepth.filter = (self.ctx.LINEAR, self.ctx.LINEAR)
        self.sfbo = self.ctx.framebuffer(depth_attachment=self.sdepth)

    def load(self, m):
        import moderngl
        ctx = self.ctx
        arr = m.tex.array()
        self.texarr = ctx.texture_array((16, 16, len(arr)), 4, arr.tobytes())
        self.texarr.build_mipmaps(0, 4)
        self.texarr.filter = (moderngl.NEAREST_MIPMAP_LINEAR, moderngl.NEAREST)
        self.texarr.anisotropy = 8.0
        data = np.concatenate([m.pos, m.uvl, m.nrm, m.col], 1).astype("f4")
        self.vbo = ctx.buffer(data.tobytes())
        fmt = (self.vbo, "3f 3f 3f 3f", "in_pos", "in_uvl", "in_nrm", "in_col")
        self.vao = self.tvao = None
        if len(m.idx):
            self.vao = ctx.vertex_array(self.prog, [fmt], ctx.buffer(m.idx.astype("u4").tobytes()))
            self.svao = ctx.vertex_array(self.sprog, [(self.vbo, "3f 3f 24x", "in_pos", "in_uvl")], ctx.buffer(m.idx.astype("u4").tobytes()))
        if len(m.tidx):
            self.tvao = ctx.vertex_array(self.prog, [fmt], ctx.buffer(m.tidx.astype("u4").tobytes()))
        lo, hi = m.pos.min(0), m.pos.max(0)
        self.lo, self.hi = lo, hi
        step = max(1, len(m.pos) // 200000)
        self.fitpts = m.pos[::step].astype(float)  # ortho views fit the actual geometry, not its bounding box
        self.centre = (lo + hi) / 2
        self.radius = float(np.linalg.norm(hi - lo) / 2) + 1
        # sun shadow map
        c = self.centre
        lv = look_at(c + SUN * self.radius * 2, c)
        corners = np.array([[x, y, z] for x in (lo[0], hi[0]) for y in (lo[1], hi[1]) for z in (lo[2], hi[2])])
        self.lightmvp = _fit_ortho(lv, corners, 1.0, 1.02) @ lv
        if self.vao is not None:
            self.sfbo.use(); self.sfbo.clear(depth=1.0)
            ctx.enable(moderngl.DEPTH_TEST); ctx.disable(moderngl.CULL_FACE)
            self.texarr.use(0)
            self.sprog["lightmvp"].write(self.lightmvp.T.astype("f4").tobytes())
            self.sprog["tex"].value = 0
            self.svao.render()

    def render(self, cam, path=None, shadows=True):
        import moderngl
        ctx = self.ctx
        W, H = self.w * self.ss, self.h * self.ss
        aspect = W / H
        view = look_at(cam.eye, cam.target, (0, 1, 0) if cam.kind != "top" else (0, 0, -1))
        corners = np.array([[x, y, z] for x in (self.lo[0], self.hi[0]) for y in (self.lo[1], self.hi[1]) for z in (self.lo[2], self.hi[2])])
        if cam.kind == "persp":
            proj = perspective(cam.fov, aspect, 0.1, self.radius * 6)
            fog = (self.radius * 1.4, self.radius * 4)
        else:
            proj = _fit_ortho(view, self.fitpts, aspect)
            fog = (1e6, 2e6)
        mvp = proj @ view
        self.fbo.use()
        ctx.viewport = (0, 0, W, H)
        ctx.clear(*SKY_BOT, 1.0)
        # sky gradient: draw by clearing then a fullscreen quad would need another program; cheap trick: bands
        ctx.enable(moderngl.DEPTH_TEST); ctx.disable(moderngl.CULL_FACE)
        p = self.prog
        p["mvp"].write(mvp.T.astype("f4").tobytes())
        p["lightmvp"].write(self.lightmvp.T.astype("f4").tobytes())
        p["sun"].value = tuple(SUN)
        p["eye"].value = tuple(cam.eye)
        p["fogcol"].value = tuple(SKY_BOT)
        p["fogstart"].value, p["fogend"].value = fog
        p["shadows"].value = 1 if shadows else 0
        self.texarr.use(0); self.sdepth.use(1)
        p["tex"].value = 0; p["shadow"].value = 1
        if self.vao is not None:
            p["translucent"].value = 0
            self.vao.render()
        if self.tvao is not None:
            ctx.enable(moderngl.BLEND); ctx.blend_func = moderngl.SRC_ALPHA, moderngl.ONE_MINUS_SRC_ALPHA
            ctx.depth_mask = False
            p["translucent"].value = 1
            self.tvao.render()
            ctx.depth_mask = True; ctx.disable(moderngl.BLEND)
        raw = np.frombuffer(self.fbo.read(components=3), np.uint8).reshape(H, W, 3)[::-1]
        img = Image.fromarray(_sky(raw, cam.kind))
        if self.ss > 1:
            img = img.resize((self.w, self.h), Image.LANCZOS)
        if path:
            img.save(path)
        return img


def _sky(raw, kind):
    """Replace the flat clear colour with a vertical gradient (perspective views only)."""
    if kind != "persp":
        return raw
    H = raw.shape[0]
    clear = np.all(raw == (SKY_BOT * 255).round().astype(np.uint8), axis=2)
    t = np.linspace(0, 1, H)[:, None, None]
    grad = ((SKY_TOP * (1 - t) + SKY_BOT * t) * 255).astype(np.uint8)
    out = raw.copy()
    out[clear] = np.broadcast_to(grad, raw.shape)[clear]
    return out


# ------------------------------------------------------------------ view set
def default_cameras(scene, origin=(0, 0, 0)):
    b = scene.bounds()
    if b is None:
        return []
    lo = np.array(b[0], float) + origin; hi = np.array(b[1], float) + 1 + origin
    c = (lo + hi) / 2
    r = np.linalg.norm(hi - lo)
    cams = []
    for name, dx, dz in (("iso_se", 1, 1), ("iso_sw", -1, 1), ("iso_nw", -1, -1), ("iso_ne", 1, -1)):
        d = np.array([dx, 1.15, dz], float); d /= np.linalg.norm(d)
        cams.append(Camera(name, c + d * r * 2, c, "ortho"))
    cams.append(Camera("top", c + np.array([0, r * 2, 0]), c, "top"))
    eyes = {k: v for k, v in scene.markers.items() if k.startswith(("spawn", "cam", "eye", "key"))}
    for k, mk in eyes.items():
        if k.startswith("key"):
            continue
        e = np.array(mk["pos"], float) + origin + np.array([0, 1.62, 0])
        if mk.get("look_at"):
            t = np.array(mk["look_at"], float) + origin
        elif mk.get("yaw") is not None:
            y = math.radians(mk["yaw"])
            t = e + np.array([-math.sin(y), 0, math.cos(y)]) * 10
        else:
            t = c
        cams.append(Camera("eye_" + k, e, t, "persp", fov=mk.get("fov", 75)))
    if not any(cm.kind == "persp" for cm in cams):  # no markers: a ground-level look from the south edge
        surf = scene.surface()
        X, _, Z = scene.shape
        x = X // 2
        col = surf[x, Z - 1]
        e = np.array([x + 0.5, max(col, 0) + 1 + 1.62, Z + 6.0]) + origin
        cams.append(Camera("eye_south", e, c, "persp"))
    return cams


def sightline_map(scene, scale=4):
    """Top-down map: walkable cells (solid with 2 air above) coloured by how many eye markers (spawn_*, key_*) see them."""
    keys = {k: v for k, v in scene.markers.items() if k.startswith(("spawn", "key"))}
    solid = scene.solid()
    X, Y, Z = scene.shape
    surf = scene.surface()
    if not keys:
        return None
    walk = np.zeros((X, Z), bool)
    xs, zs = np.nonzero(surf >= 0)
    ys = surf[xs, zs]
    ok = ys + 2 < Y
    walk[xs[ok], zs[ok]] = True
    seen = np.zeros((X, Z), np.int32)
    tx, tz = np.nonzero(walk)
    ty = surf[tx, tz] + 1 + 1.2  # body height above the cell
    targets = np.stack([tx + 0.5, ty, tz + 0.5], 1)
    for mk in keys.values():
        e = np.array(mk["pos"], float) + [0, 1.62, 0]
        vis = np.ones(len(targets), bool)
        d = targets - e
        dist = np.linalg.norm(d, axis=1)
        steps = int(dist.max() * 2) + 1
        for t in np.linspace(0.02, 0.97, steps):
            p = e + d * t
            ix = np.clip(p[:, 0].astype(int), 0, X - 1); iy = np.clip(p[:, 1].astype(int), 0, Y - 1); iz = np.clip(p[:, 2].astype(int), 0, Z - 1)
            vis &= ~solid[ix, iy, iz] | (np.abs(p[:, 0] - targets[:, 0]) + np.abs(p[:, 2] - targets[:, 2]) < 0.8)
        seen[tx[vis], tz[vis]] += 1
    # base: height shading
    h = np.where(surf >= 0, surf, 0).astype(float)
    shade = 0.35 + 0.65 * (h - h.min()) / max(1, h.max() - h.min())
    base = np.stack([shade] * 3, -1) * 200
    pal = np.array([[60, 60, 200], [80, 200, 80], [240, 200, 40], [240, 110, 30], [230, 40, 40]], float)
    col = pal[np.clip(seen, 0, 4)]
    img = np.where(walk[..., None], base * 0.45 + col * 0.55, 30).astype(np.uint8)
    im = Image.fromarray(img.transpose(1, 0, 2)).resize((X * scale, Z * scale), Image.NEAREST)  # rows = z (north up)
    dr = ImageDraw.Draw(im)
    for k, mk in keys.items():
        x, _, z = mk["pos"]
        dr.ellipse([x * scale - 5, z * scale - 5, x * scale + 5, z * scale + 5], fill=(255, 255, 255), outline=(0, 0, 0))
        dr.text((x * scale + 7, z * scale - 6), k, fill=(255, 255, 255))
    dr.text((4, 4), "seen by: blue 0  green 1  yellow 2  orange 3  red 4+   (N up)", fill=(255, 255, 255))
    return im


def contact_sheet(images, path, cols=3, w=640, h=400):
    items = list(images.items())
    rows = (len(items) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * w, rows * (h + 18)), (20, 20, 24))
    dr = ImageDraw.Draw(sheet)
    for i, (name, im) in enumerate(items):
        k = min(w / im.width, h / im.height)
        t = im.resize((max(1, int(im.width * k)), max(1, int(im.height * k))), Image.LANCZOS)
        x, y = (i % cols) * w, (i // cols) * (h + 18)
        sheet.paste(t, (x + (w - t.width) // 2, y + 18 + (h - t.height) // 2))
        dr.text((x + 4, y + 3), name, fill=(230, 230, 230))
    sheet.save(path)
    return path


def render_views(scene, out, width=1280, height=800, only=None, shadows=True, extra_cams=(), vtint=None, sightlines=True):
    t0 = time.time()
    out = Path(out); out.mkdir(parents=True, exist_ok=True)
    m = meshmod.build(scene, vtint=vtint)
    t1 = time.time()
    r = Renderer(width, height)
    r.load(m)
    res, imgs = {}, {}
    for cam in list(default_cameras(scene)) + list(extra_cams):
        if only and not any(cam.name.startswith(o) for o in only):
            continue
        p = out / f"{cam.name}.png"
        imgs[cam.name] = r.render(cam, p, shadows)
        res[cam.name] = p
    if sightlines and (not only or "sightlines" in only):
        sl = sightline_map(scene)
        if sl is not None:
            p = out / "sightlines.png"; sl.save(p); res["sightlines"] = p; imgs["sightlines"] = sl
    if len(imgs) > 1:
        res["sheet"] = contact_sheet(imgs, out / "sheet.png")
    print(f"[voxel] mesh {m.quads} quads, {len(m.tex.layers)} textures in {t1 - t0:.1f}s; rendered {len(imgs)} views in {time.time() - t1:.1f}s -> {out}")
    return res
