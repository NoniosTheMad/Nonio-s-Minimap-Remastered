"""Room zones: named, empty interior volumes for the zone decorators (s.meta["zones"]).

Each zone: name, type (the rooms.furnish kind it is meant for, or a free type), box = the interior AIR volume, inclusive
(x0, y0, z0, x1, y1, z1), the same convention as tools/voxel/kits/rooms.furnish; floor = top cell of the floor (feet
floor + 1); shape (box / cylinder / ellipsoid / cave) + its parameters; mood; must-have features; doors (feet cells).
Nothing is furnished here. docs/builds/orrery-zones.md is the human-readable list."""
import math

from .common import C, FLOOR, LAKE_Y

TOWER_NAMES = {30: ("Dome Tower", "observatory"), 150: ("Bell Tower", "chapel"), 190: ("West Watch", "armoury"),
               230: ("Armillary Tower", "lab"), 270: ("Needle Tower", "library"), 310: ("North Watch", "armoury"),
               350: ("East Watch", "bedroom")}


def _cyl(name, typ, c, r, y0, y1, mood, features, doors=(), floor=None):
    x, z = c
    return dict(name=name, type=typ, shape="cylinder", c=[round(x, 1), round(z, 1)], r=round(float(r), 1),
                box=[int(math.floor(x - r)), int(y0), int(math.floor(z - r)), int(math.ceil(x + r)) - 1, int(y1),
                     int(math.ceil(z + r)) - 1],
                floor=int(floor if floor is not None else y0 - 1), mood=mood, features=list(features), doors=list(doors))


def _box(name, typ, box, mood, features, doors=(), floor=None):
    return dict(name=name, type=typ, shape="box", box=[int(v) for v in box], floor=int(floor if floor is not None else box[1] - 1),
                mood=mood, features=list(features), doors=list(doors))


def zones(ctx):
    from . import spire
    from .castle import WALK
    from .island import GROTTO, GROTTO_FLOOR, GROTTO_R, SHAFT_R
    Z = []
    # ---- the Spire
    r = lambda y: float(spire.radius(y)) - spire.WALL_T - 0.5
    Z.append(_cyl("Orrery Hall", "hall", C, r(FLOOR + 1), spire.HALL[0], spire.HALL[1], "solemn, cold light from the lancets, the heart glowing up through the oculus",
                  ["oculus over the Root Shaft (keep clear, r 7)", "star-map floor inlay", "11 lancets", "south door", "turret door (NNW)",
                   "orrery model / central instrument around the oculus rim"], doors=["south door (104, 109, 117)", "turret door"]))
    Z.append(_cyl("Star Archive", "library", C, r(spire.ARCHIVE[0]), spire.ARCHIVE[0], spire.ARCHIVE[1], "hushed, dusty, star charts and catalogues",
                  ["tall shelves against the curved wall", "mezzanine possible (18 tall)", "door from the stair turret"], doors=["turret door at feet 131"]))
    Z.append(_cyl("Gallery Room", "hall", C, r(spire.GALLERY_Y + 1), spire.GALLERY_Y + 1, spire.SHAFT_DECK[0] - 2, "bright, wind, the rings sweeping past the doors",
                  ["4 doors to the gallery deck (r 21.5, wraps the turret)", "turret arrival", "stair up to the Gear Room (keep the helix clear)"]))
    Z.append(_cyl("Gear Room", "lab", C, r(spire.GEAR_Y + 1), spire.GEAR_Y + 1, spire.LENS_Y - 2, "mechanical, copper and oil, the axles turning under the grate floor",
                  ["copper grate floor over the shaft deck (axles + central gear drum visible below)", "helix stair on the wall"]))
    Z.append(_cyl("Lens Room", "lab", C, r(spire.LENS_Y + 1), spire.LENS_Y + 1, spire.LANTERN_Y - 2, "focused, purple light, the lens grinder's workshop",
                  ["doors to the upper deck (r 12.5)", "helix stair to the Lantern"]))
    Z.append(_cyl("Lantern", "chapel", C, 6.4, spire.LANTERN_Y + 1, spire.LANTERN_Y + 13, "open sky, the Focus floating overhead",
                  ["open cage (8 posts, bars rail)", "the Focus (amethyst octahedron, glowstone core) overhead: keep clear"]))
    # ---- castle wings
    W = ctx.get("wings", {})
    if "library" in W:
        Z.append(_box("Library", "library", W["library"]["box"], "warm, wood and candlelight, purple lancet light",
                      ["5 lancets per long side", "door to the court (east)", "inner door to the West Watch (north end)"],
                      doors=[str(W["library"]["door"])]))
    if "chart_room" in W:
        Z.append(_box("Chart Room", "lab", W["chart_room"]["box"], "bright, maps and brass, a table under the lancets",
                      ["door to the court (west)", "instrument terrace on the flat roof"], doors=[str(W["chart_room"]["door"])]))
    if "service" in W:
        x0, y0, z0, x1, y1, z1 = W["service"]["box"]
        fy = ctx.get("service_floor", FLOOR + 7)
        Z.append(_box("Kitchen", "kitchen", (x0, y0, z0, x1, fy - 1, z1), "smoky, hearth light, busy",
                      ["door to the court (south)", "stair up to the Quarters (north wall, keep clear)", "door to the Needle Tower (north)"],
                      doors=[str(W["service"]["door"])]))
        Z.append(_box("Quarters", "bedroom", (x0, fy + 1, z0, x1, y1, z1), "quiet, low, wooden floor, the court below the windows",
                      ["stair hole with balustrade (north)", "windows to the court"]))
    gr = ctx.get("gate_room")
    if gr:
        Z.append(_box("Gate Room", "armoury", gr, "martial, the rose window glowing over the gate",
                      ["rose window (south)", "two wall-walk doors (east/west)", "murder slots over the passage possible"]))
    # ---- towers
    for t in ctx.get("towers", []):
        x, z = t["c"]
        a = int(round(math.degrees(math.atan2(z - C[1], x - C[0])) % 360))
        nm, typ = TOWER_NAMES.get(a, (f"Tower {a}", "armoury"))
        Z.append(_cyl(nm + " (ground)", typ, (x, z), t["room"], FLOOR + 1, WALK - 1, "narrow, slit light", ["court door", "ladder to the upper room (outer wall)", "slit windows"]))
        Z.append(_cyl(nm + " (upper)", typ, (x, z), t["room"], WALK + 1, t["top"] - 2, "lookout, wind at the slits", ["wall-walk doors", "ladder hole", "slit windows"]))
    # ---- inside the island (Route B)
    Z.append(dict(name="Root Grotto", type="cave", shape="ellipsoid", c=list(GROTTO), r=list(GROTTO_R),
                  box=[int(GROTTO[0] - GROTTO_R[0]), GROTTO_FLOOR + 1, int(GROTTO[2] - GROTTO_R[2]), int(GROTTO[0] + GROTTO_R[0]) - 1,
                       int(GROTTO[1] + GROTTO_R[1]) - 1, int(GROTTO[2] + GROTTO_R[2]) - 1], floor=GROTTO_FLOOR,
                  mood="crystalline, purple glow, the heart column humming", features=["flat floor ring round the Throat (open below: lethal fall)",
                  "amethyst heart column", "Root Helix arrives from below, Shaft Helix leaves upward"], doors=[]))
    Z.append(_cyl("Root Shaft", "cave", C, SHAFT_R, GROTTO_FLOOR + 1, FLOOR, "vertical, ribbed, the heart glowing at the core",
                  ["Shaft Helix (keep clear)", "open core: the deliberate fall"]))
    for k, f in enumerate(ctx.get("foundations", [])):
        x, y0, z = f["c"]
        Z.append(dict(name=f"Torn Cellar {k + 1}", type="cellar", shape="half-room", c=[round(x, 1), round(z, 1)], a=f["a"],
                      box=[int(x - f["w"] / 2 - 1), int(y0), int(z - f["w"] / 2 - 1), int(x + f["w"] / 2 + 1), int(y0 + f["h"] - 1), int(z + f["w"] / 2 + 1)],
                      floor=int(y0 - 1), mood="ruin, open to the sky on the outer side, wind", features=["barrel vault", "broken floor at the rim (fall risk)"], doors=[]))
    # ---- crater
    Z.append(dict(name="Root Geode", type="cave", shape="sphere", c=[C[0], LAKE_Y + 6, C[1]], r=8.3,
                  box=[int(C[0] - 8), LAKE_Y + 2, int(C[1] - 8), int(C[0] + 8), LAKE_Y + 14, int(C[1] + 8)], floor=LAKE_Y + 1,
                  mood="sacred, amethyst everywhere, the conduit shards rising through the broken roof",
                  features=["south mouth onto the causeway", "Root Helix (keep clear)", "oculus in the roof"], doors=[]))
    for k, (c, R, a) in enumerate(ctx.get("lesser_geodes", [])):
        ri = R - 3.2
        Z.append(dict(name=f"Geode Grotto {k + 1}", type="cave", shape="sphere", c=[round(v, 1) for v in c], r=round(ri, 1), a=a,
                      box=[int(c[0] - ri), int(c[1] - ri), int(c[2] - ri), int(c[0] + ri), int(c[1] + ri), int(c[2] + ri)],
                      floor=None, mood="small, glittering, a hiding place", features=["mouth onto the crater shore"], doors=[]))
    return Z


def build(s, ctx):
    s.meta["zones"] = zones(ctx)
