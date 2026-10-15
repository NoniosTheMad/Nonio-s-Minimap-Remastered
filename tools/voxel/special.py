"""Geometry the game draws in code instead of block models: chests, banners (with patterns), heads, decorated pots
(with sherds), shulker boxes, bell bodies, plus entities (item frames + their item, paintings, armour stands + gear).

Approximations built from boxes laid out on the entity texture sheets (the standard Minecraft box UV net), good enough
to read a room at render scale. Synthetic textures are named "@..." and produced by load() for mesh.TextureArray:
  "@<texture path>#x,y,w,h"                   crop of a texture sheet (in its own pixels)
  "@banner|<base colour>|pat=col,...#x,y,w,h"  banner sheet composited with its patterns, then cropped
Canonical frame for every piece: front faces +z (south); yaw rotates about the cell centre (0 south, 90 west, 180 north,
270 east, matching Minecraft's entity yaw)."""
import functools, math

import numpy as np
from PIL import Image

from . import blockstate as bs
from .models import DVEC, EMPTY, Quads, _corners, bank

DYE = {"white": 0xF9FFFE, "orange": 0xF9801D, "magenta": 0xC74EBD, "light_blue": 0x3AB3DA, "yellow": 0xFED83D,
       "lime": 0x80C71F, "pink": 0xF38BAA, "gray": 0x474F52, "light_gray": 0x9D9D97, "cyan": 0x169C9C,
       "purple": 0x8932B8, "blue": 0x3C44AA, "brown": 0x835432, "green": 0x5E7C16, "red": 0xB02E26, "black": 0x1D1D21}
YAW = {"south": 0, "west": 90, "north": 180, "east": 270}
FACING3 = {0: "down", 1: "up", 2: "north", 3: "south", 4: "west", 5: "east"}
FACING2 = {0: "south", 1: "west", 2: "north", 3: "east"}

CHEST_TEX = {"chest": "normal", "trapped_chest": "trapped", "ender_chest": "ender", "copper_chest": "copper",
             "exposed_copper_chest": "copper_exposed", "weathered_copper_chest": "copper_weathered",
             "oxidized_copper_chest": "copper_oxidized"}
HEAD_TEX = {"skeleton": ("entity/skeleton/skeleton", 8), "wither_skeleton": ("entity/skeleton/wither_skeleton", 8),
            "zombie": ("entity/zombie/zombie", 8), "creeper": ("entity/creeper/creeper", 8),
            "piglin": ("entity/piglin/piglin", 10), "dragon": ("entity/enderdragon/dragon", 16),
            "player": ("entity/player/wide/steve", 8)}
ARMOUR_MAT = {"leather": "leather", "chainmail": "chainmail", "iron": "iron", "golden": "gold", "diamond": "diamond",
              "netherite": "netherite", "copper": "copper", "turtle": "turtle_scute"}


# ------------------------------------------------------------------ synthetic textures
def load(name):
    """PIL RGBA image (any size; TextureArray resizes) for a synthetic "@" texture name."""
    body, _, rect = name[1:].partition("#")
    if body.startswith("banner|"):
        img = _banner_sheet(body)
    else:
        img = _sheet(body)
    if img is None:
        return None
    if rect:
        x, y, w, h = [int(round(float(v))) for v in rect.split(",")]
        s = img.width / _declared_w(body)
        img = img.crop((int(x * s), int(y * s), int((x + max(w, 1)) * s), int((y + max(h, 1)) * s)))
    return img.resize((16, 16), Image.NEAREST)


def _declared_w(body):
    return 64 if body.startswith("banner|") else _sheet(body).width


@functools.lru_cache(None)
def _sheet(path):
    f = bank().root / "textures" / (path + ".png")
    if not f.exists():
        return None
    img = Image.open(f).convert("RGBA")
    if img.height > img.width * 2:  # animated strip
        img = img.crop((0, 0, img.width, img.width))
    return img


@functools.lru_cache(None)
def _banner_sheet(body):
    _, base, pats = body.split("|", 2)
    sheet = _sheet("entity/banner/base")
    out = _tinted(sheet, base)
    for p in filter(None, pats.split(",")):
        pat, _, col = p.partition("=")
        m = _sheet("entity/banner/" + pat)
        if m is not None:
            out = Image.alpha_composite(out, _tinted(m, col, keep_alpha=True))
    return out


def _tinted(img, colour, keep_alpha=False):
    c = DYE.get(colour, 0xFFFFFF)
    a = np.asarray(img, np.float32).copy()
    rgb = np.array([(c >> 16) & 255, (c >> 8) & 255, c & 255], np.float32) / 255
    a[..., :3] *= rgb
    if keep_alpha:  # pattern masks: white with alpha (some are greyscale with full alpha -> use luminance)
        if a[..., 3].min() == 255:
            a[..., 3] = np.asarray(img.convert("L"), np.float32)
    return Image.fromarray(a.clip(0, 255).astype(np.uint8))


def tex_crop(path, x, y, w, h):
    return f"@{path}#{x},{y},{w},{h}"


# ------------------------------------------------------------------ geometry builders (pixel units, canonical frame)
class Builder:
    def __init__(self):
        self.pos, self.uv, self.tex, self.n = [], [], [], []

    def face(self, f, t, d, tex):
        c, _ = _corners(f, t, d)
        self.pos.append(np.array(c, np.float32)); self.tex.append(tex); self.n.append(DVEC[d].copy())
        self.uv.append([(0, 0), (1, 0), (1, 1), (0, 1)])

    def box(self, f, t, sheet, u, v, dims=None, faces="NSEWUD", tex=None):
        """Box from f to t (pixels). Textures come from the box net at (u, v) with dims (w, h, d) (default: the size),
        or `tex` = {face letter: texture name} overrides."""
        w, h, d = dims or [t[i] - f[i] for i in range(3)]
        net = {"U": (u + d, v, w, d), "D": (u + d + w, v, w, d), "S": (u + d, v + d, w, h),
               "W": (u, v + d, d, h), "E": (u + d + w, v + d, d, h), "N": (u + d + w + d, v + d, w, h)}
        for L in faces:
            tx = (tex or {}).get(L) or tex_crop(sheet, *net[L])
            self.face(f, t, "DUNSWE".index(L), tx)
        return self

    def quads(self, yaw=0, scale=1 / 16, offset=(0, 0, 0), pivot=(8, 0, 8), pitch=0):
        if not self.pos:
            return EMPTY
        P = np.array(self.pos, np.float32) - np.array(pivot, np.float32)
        N = np.array(self.n, np.float32)
        if pitch:
            R = _rx(pitch); P = P @ R.T; N = N @ R.T
        if yaw:
            R = _ry(yaw); P = P @ R.T; N = N @ R.T
        P = P * scale + np.array(pivot, np.float32) / 16 + np.array(offset, np.float32)
        n = len(self.tex)
        return Quads(P, np.array(self.uv, np.float32), list(self.tex), N, N.copy(), np.full(n, -1, np.int8),
                     np.full(n, -1, np.int8), np.zeros(n, bool))


def _ry(deg):
    a = math.radians(deg); c, s = math.cos(a), math.sin(a)
    # x' = x cos - z sin ; z' = x sin + z cos  (yaw 90 turns +z (south) into -x (west))
    return np.array([[c, 0, -s], [0, 1, 0], [s, 0, c]], np.float32)


def _rx(deg):
    a = math.radians(deg); c, s = math.cos(a), math.sin(a)
    return np.array([[1, 0, 0], [0, c, -s], [0, s, c]], np.float32)


# ------------------------------------------------------------------ block entities
def kind(name):
    """Which special renderer a block name needs (None = ordinary block model)."""
    s = name.split(":")[-1].removeprefix("waxed_")
    if s in CHEST_TEX:
        return "chest"
    if s.endswith("_banner"):
        return "banner"
    if s.endswith(("_skull", "_head")) and s != "piston_head":
        return "head"
    if s == "decorated_pot":
        return "pot"
    if s.endswith("shulker_box"):
        return "shulker"
    if s == "bell":
        return "bell"
    return None


def block_quads(state, be=None):
    """Quads (block units, cell-local) for a special block, using its block entity data when present."""
    name, props = bs.parse(state)
    k = kind(name)
    fn = {"chest": _chest, "banner": _banner, "head": _head, "pot": _pot, "shulker": _shulker, "bell": _bell}.get(k)
    try:
        return fn(name.split(":")[-1].removeprefix("waxed_"), props, _plain(be)) if fn else EMPTY
    except Exception as e:  # never let a decoration break a render
        print(f"[voxel] special {state}: {e}")
        return EMPTY


def _plain(t):
    if t is None:
        return {}
    from .nbt import norm
    v = norm(t)
    return v if isinstance(v, dict) else {}


def _chest(s, props, be):
    yaw = YAW.get(props.get("facing", "north"), 180)
    typ = props.get("type", "single")
    base = "entity/chest/" + CHEST_TEX[s]
    b = Builder()
    if typ == "single":
        b.box((1, 0, 1), (15, 10, 15), base, 0, 19)
        b.box((1, 9, 1), (15, 14, 15), base, 0, 0)
        b.box((7, 7, 15), (9, 11, 16), base, 0, 0, dims=(2, 4, 1))
    else:
        # LEFT: partner is clockwise of facing (for a south-facing chest: west, -x) -> this half spans x 0..15
        sheet = base + ("_left" if typ == "left" else "_right")
        x0, x1 = (0, 15) if typ == "left" else (1, 16)
        b.box((x0, 0, 1), (x1, 10, 15), sheet, 0, 19)
        b.box((x0, 9, 1), (x1, 14, 15), sheet, 0, 0)
        lx = (0, 1) if typ == "left" else (15, 16)
        b.box((lx[0], 7, 15), (lx[1], 11, 16), sheet, 0, 0, dims=(1, 4, 1))
    return b.quads(yaw)


def _banner(s, props, be):
    """Model pixels as in BannerRenderer, drawn at its 2/3 scale: standing pole ~1.75 blocks, flag ~0.83 x 1.67."""
    colour = s.replace("_wall_banner", "").replace("_banner", "")
    pats = ",".join(f"{str(p.get('pattern', '')).split(':')[-1]}={p.get('color', 'white')}"
                    for p in be.get("patterns", []) if isinstance(p, dict))
    key = f"banner|{colour}|{pats}"
    top, bot = f"@{key}#1,1,20,20", f"@{key}#1,21,20,20"
    side = f"@{key}#0,1,1,40"
    wood = "entity/banner/banner_base"
    b = Builder()
    if "wall_banner" in s:
        yaw = YAW.get(props.get("facing", "south"), 0)
        pivot = (8, 16, 0)
        b.box((-2, 14, 0), (18, 16, 2), wood, 0, 42, dims=(20, 2, 2))
        y0, z0 = -25, 2
    else:
        yaw = int(props.get("rotation", "0") or 0) * 22.5
        pivot = (8, 0, 8)
        b.box((7, 0, 7), (9, 42, 9), wood, 44, 0, dims=(2, 42, 2))
        b.box((-2, 42, 7), (18, 44, 9), wood, 0, 42, dims=(20, 2, 2))
        y0, z0 = 2, 9
    for (ya, yb), tx in (((y0 + 20, y0 + 40), top), ((y0, y0 + 20), bot)):
        b.face((-2, ya, z0), (18, yb, z0 + 1), 3, tx)   # front
        b.face((-2, ya, z0), (18, yb, z0 + 1), 2, tx)   # back (mirrored, close enough)
        b.face((-2, ya, z0), (18, yb, z0 + 1), 4, side)
        b.face((-2, ya, z0), (18, yb, z0 + 1), 5, side)
    return b.quads(yaw, scale=1 / 24, pivot=pivot)


def _head(s, props, be):
    mob = s.replace("_wall_skull", "").replace("_wall_head", "").replace("_skull", "").replace("_head", "")
    sheet, w = HEAD_TEX.get(mob, HEAD_TEX["player"])
    b = Builder()
    wall = "_wall_" in s
    yaw = YAW.get(props.get("facing", "south"), 0) if wall else int(props.get("rotation", "0") or 0) * 22.5
    if mob == "dragon":
        f, t, net = ((0, 0, 0), (16, 16, 16), (112, 30)) if not wall else ((0, 0, 0), (16, 16, 16), (112, 30))
        b.box(f, t, sheet, *net, dims=(16, 16, 16))
        return b.quads(yaw)
    x0 = 8 - w / 2
    y0, z0 = (4, 0) if wall else (0, 4)
    b.box((x0, y0, z0), (x0 + w, y0 + 8, z0 + 8), sheet, 0, 0, dims=(w, 8, 8))
    if mob == "player":
        e = 0.5
        b.box((x0 - e, y0 - e, z0 - e), (x0 + w + e, y0 + 8 + e, z0 + 8 + e), sheet, 32, 0, dims=(8, 8, 8))
    return b.quads(yaw)


def _pot(s, props, be):
    yaw = YAW.get(props.get("facing", "north"), 180)
    sherds = be.get("sherds", {}) if isinstance(be.get("sherds"), dict) else {}

    def side(which):
        sid = str(sherds.get(which, {}).get("id", "") if isinstance(sherds.get(which), dict) else sherds.get(which, ""))
        sid = sid.split(":")[-1]
        p = f"entity/decorated_pot/{sid.replace('_pottery_sherd', '_pottery_pattern')}" if sid.endswith("_sherd") else \
            "entity/decorated_pot/decorated_pot_side"
        if _sheet(p) is None:
            p = "entity/decorated_pot/decorated_pot_side"
        return tex_crop(p, 1, 0, 14, 16)

    base = "entity/decorated_pot/decorated_pot_base"
    b = Builder()
    # canonical front +z; the pot's left (facing +z) is +x
    b.box((1, 0, 1), (15, 16, 15), base, 0, 13, dims=(14, 16, 14),
          tex={"S": side("front"), "N": side("back"), "E": side("left"), "W": side("right"),
               "U": tex_crop(base, 0, 13, 14, 14), "D": tex_crop(base, 14, 13, 14, 14)})
    b.box((5, 16, 5), (11, 17, 11), base, 0, 0, dims=(6, 1, 6))
    b.box((4, 17, 4), (12, 20, 12), base, 0, 0, dims=(8, 3, 8))
    return b.quads(yaw)


def _shulker(s, props, be):
    colour = s.replace("_shulker_box", "").replace("shulker_box", "")
    sheet = "entity/shulker/shulker" + (f"_{colour}" if colour else "")
    b = Builder()
    b.box((0, 4, 0), (16, 16, 16), sheet, 0, 0, dims=(16, 12, 16))
    b.box((0.02, 0, 0.02), (15.98, 8, 15.98), sheet, 0, 28, dims=(16, 8, 16), faces="NSEWD")
    f = props.get("facing", "up")
    pitch, yaw = {"up": (0, 0), "down": (180, 0), "north": (-90, 0), "south": (90, 0), "west": (90, 90),
                  "east": (90, 270)}.get(f, (0, 0))
    return b.quads(yaw, pivot=(8, 8, 8), pitch=pitch)


def _bell(s, props, be):
    b = Builder()
    sheet = "entity/bell/bell_body"
    att = props.get("attachment", "floor")
    dy = -2 if att == "ceiling" else 0
    b.box((5, 6 + dy, 5), (11, 13 + dy, 11), sheet, 0, 0, dims=(6, 7, 6))
    b.box((4, 4 + dy, 4), (12, 6 + dy, 12), sheet, 0, 13, dims=(8, 2, 8))
    return b.quads(YAW.get(props.get("facing", "north"), 180))


# ------------------------------------------------------------------ entities
def entity_quads(e):
    """(Quads in block units relative to the scene origin, cell for tinting) for one scene entity, or None."""
    from .nbt import norm
    t = norm(e["nbt"])
    eid = str(t.get("id", "")).split(":")[-1]
    pos = np.array(e["pos"], np.float32)
    try:
        if eid in ("item_frame", "glow_item_frame"):
            return _frame(eid, t, pos)
        if eid == "painting":
            return _painting(t, pos)
        if eid == "armor_stand":
            return _stand(t, pos)
    except Exception as ex:
        print(f"[voxel] entity {eid}: {ex}")
    return None


def _item_tex(item_id):
    """Texture for an item stack's sprite: item/<id>, else the block's own texture, else its model's first texture."""
    s = item_id.split(":")[-1]
    s = {"crossbow": "crossbow_standby", "clock": "clock_00", "compass": "compass_16", "recovery_compass": "recovery_compass_16",
         "potion": "potion", "splash_potion": "splash_potion", "filled_map": "filled_map"}.get(s, s)
    root = bank().root / "textures"
    for p in ("item/" + s, "block/" + s, "block/" + s + "_front", "block/" + s + "_side"):
        if (root / (p + ".png")).exists():
            return p
    m = bank().model("block/" + s)
    if m["textures"]:
        return bank()._tex(m["textures"], next(iter(m["textures"].values())))
    return "item/barrier"


def _frame(eid, t, pos):
    face = FACING3.get(int(t.get("Facing", 3)), "south")
    item = t.get("Item") or {}
    mid = str(item.get("id", "")).split(":")[-1]
    model = "minecraft:block/" + eid + ("_map" if mid == "filled_map" else "")
    rot = {"north": (0, 0), "east": (0, 90), "south": (0, 180), "west": (0, 270), "up": (270, 0), "down": (90, 0)}[face]
    q = bank().bake_model(model, rot[0], rot[1]) if not t.get("Invisible") else EMPTY
    d = {"north": (0, 0, -1), "south": (0, 0, 1), "west": (-1, 0, 0), "east": (1, 0, 0), "up": (0, 1, 0), "down": (0, -1, 0)}[face]
    cell = np.floor(pos + 0.25 * np.array(d, np.float32))
    parts = [_shift(q, cell)]
    if mid and mid != "filled_map":
        b = Builder()
        b.face((4, 4, 14.4), (12, 12, 14.6), 2, _item_tex(mid))  # item sprite facing north in the frame-north model space
        yaw = {"north": 0, "east": 90, "south": 180, "west": 270}.get(face, 0)
        pitch = {"up": 90, "down": -90}.get(face, 0)
        parts.append(b.quads(yaw, pivot=(8, 8, 8), pitch=pitch, offset=cell))
    return Quads.concat(parts), tuple(int(v) for v in cell)


def _shift(q, off):
    if not len(q):
        return q
    return Quads(q.pos + np.asarray(off, np.float32), q.uv, list(q.tex), q.normal, q.shade, np.full(len(q), -1, np.int8),
                 q.tint, np.zeros(len(q), bool))


@functools.lru_cache(None)
def _painting_size(variant):
    img = _sheet("painting/" + variant)
    if img is None:
        return 1, 1
    return max(1, img.width // 16), max(1, img.height // 16)


def _painting(t, pos):
    v = str(t.get("variant", "kebab")).split(":")[-1]
    w, h = _painting_size(v)
    face = FACING2.get(int(t.get("facing", 0)), "south")
    b = Builder()
    sheet = "painting/" + v
    img = _sheet(sheet)
    ppb = img.width / w if img is not None else 16
    for i in range(w):
        for j in range(h):
            x0, y0 = -8 * w + 16 * i, 8 * h - 16 * (j + 1)
            tx = tex_crop(sheet, i * ppb, j * ppb, ppb, ppb) if img is not None else "painting/back"
            b.face((x0, y0, -0.5), (x0 + 16, y0 + 16, 0.5), 3, tx)
    b.box((-8 * w, -8 * h, -0.5), (8 * w, 8 * h, 0.4), "painting/back", 0, 0, faces="N",
          tex={"N": "painting/back"})
    q = b.quads(YAW[face], pivot=(0, 0, 0), offset=pos)
    return q, tuple(int(c) for c in np.floor(pos - 0.2 * DVEC[{"south": 3, "west": 4, "north": 2, "east": 5}[face]]))


def _armour_mat(item_id):
    s = item_id.split(":")[-1]
    for k, v in ARMOUR_MAT.items():
        if s.startswith(k + "_"):
            return v
    return None


def _stand(t, pos):
    sheet = "entity/armorstand/armorstand"
    rot = t.get("Rotation") or [0, 0]
    yaw = float(rot[0]) if rot else 0
    small = bool(t.get("Small"))
    eq = t.get("equipment") or {}
    b = Builder()
    if not t.get("Invisible"):
        if not t.get("NoBasePlate"):
            b.box((-6, 0, -6), (6, 1, 6), sheet, 0, 32, dims=(12, 1, 12))
        b.box((-3, 1, -1), (-1, 12, 1), sheet, 8, 0, dims=(2, 11, 2))     # right leg (-x when facing +z)
        b.box((1, 1, -1), (3, 12, 1), sheet, 40, 16, dims=(2, 11, 2))     # left leg
        b.box((-4, 12, -1), (4, 14, 1), sheet, 0, 48, dims=(8, 2, 2))     # hip
        b.box((-3, 14, -1), (-1, 21, 1), sheet, 16, 0, dims=(2, 7, 2))
        b.box((1, 14, -1), (3, 21, 1), sheet, 48, 16, dims=(2, 7, 2))
        b.box((-6, 21, -1.5), (6, 24, 1.5), sheet, 0, 26, dims=(12, 3, 3))  # shoulders
        b.box((-1, 24, -1), (1, 31, 1), sheet, 0, 0, dims=(2, 7, 2))      # neck
        if t.get("ShowArms"):
            b.box((-8, 12, -1), (-6, 24, 1), sheet, 24, 0, dims=(2, 12, 2))
            b.box((6, 12, -1), (8, 24, 1), sheet, 32, 16, dims=(2, 12, 2))

    def it(slot):
        v = eq.get(slot)
        return str(v.get("id", "")) if isinstance(v, dict) else ""

    head = it("head").split(":")[-1]
    if head:
        mat = _armour_mat(head)
        if mat:
            b.box((-5, 23, -5), (5, 33, 5), f"entity/equipment/humanoid/{mat}", 0, 0, dims=(8, 8, 8))
        elif kind(head):
            mob = head.replace("_skull", "").replace("_head", "")
            sh, w = HEAD_TEX.get(mob, HEAD_TEX["player"])
            b.box((-4, 24, -4), (4, 32, 4), sh, 0, 0, dims=(w, 8, 8))
        else:
            b.box((-4, 24, -4), (4, 32, 4), "", 0, 0, tex={k: _item_tex(head) for k in "NSEWUD"})
    mat = _armour_mat(it("chest"))
    if mat:
        tx = f"entity/equipment/humanoid/{mat}"
        b.box((-5, 11, -3), (5, 25, 3), tx, 16, 16, dims=(8, 12, 4))
        b.box((-9, 11, -3), (-5, 25, 3), tx, 40, 16, dims=(4, 12, 4))
        b.box((5, 11, -3), (9, 25, 3), tx, 40, 16, dims=(4, 12, 4))
    mat = _armour_mat(it("legs"))
    if mat:
        tx = f"entity/equipment/humanoid_leggings/{mat}"
        b.box((-4.5, 11.5, -2.5), (4.5, 14, 2.5), tx, 16, 16, dims=(8, 12, 4), faces="NSEW")
        b.box((-4.5, -0.5, -2.5), (0, 12.5, 2.5), tx, 0, 16, dims=(4, 12, 4))
        b.box((0, -0.5, -2.5), (4.5, 12.5, 2.5), tx, 0, 16, dims=(4, 12, 4))
    mat = _armour_mat(it("feet"))
    if mat:
        tx = f"entity/equipment/humanoid/{mat}"
        b.box((-5, -1, -3), (0, 13, 3), tx, 0, 16, dims=(4, 12, 4))
        b.box((0, -1, -3), (5, 13, 3), tx, 0, 16, dims=(4, 12, 4))
    for slot, x in (("mainhand", -7), ("offhand", 7)):
        s = it(slot).split(":")[-1]
        if s:
            b.face((x, 4, -8), (x, 20, 8), 4, _item_tex(s))
            b.face((x, 4, -8), (x, 20, 8), 5, _item_tex(s))
    q = b.quads(yaw, scale=(1 / 32 if small else 1 / 16), pivot=(0, 0, 0), offset=pos)
    return q, tuple(int(c) for c in np.floor(pos + np.array([0, 0.1, 0], np.float32)))
