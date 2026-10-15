"""NBT for block entities and entities: SNBT in, binary out, plus builders for the 26.3 formats.

Everything is an nbtlib Compound internally; authors pass SNBT strings, Compounds or the builders below:

    s.set(x, y, z, "chest[facing=south]", nbt=chest([item("apple", 3), item("bread", 2, slot=4)]))
    s.set(x, y, z, "oak_wall_sign[facing=north]", nbt=sign(["The", "Rusty", "Anchor"], color="white", glow=True))
    s.set(x, y, z, "red_wall_banner[facing=south]", nbt=banner([("stripe_top", "black"), ("border", "yellow")]))
    s.entity("item_frame", (x + .5, y + .5, z + .97), item_frame(item("iron_sword"), facing="north"))

Formats verified on a 26.3 server (data get after setblock/summon, 2026-10-15):
  chest/barrel   Items:[{Slot:0b,id,count}]          sign  front_text/back_text:{messages:[4 x text], color, has_glowing_text}, is_waxed
  banner         patterns:[{pattern:"minecraft:x", color:"red"}]        skull  profile:{name:"..."} (or properties)
  decorated_pot  sherds:{back,left,right,front: {id}}  (a record, NOT a list), item:{id,count}
  lectern        Book:{id,count,components}, Page     item frame  Facing (3D byte), block_pos:[I;x,y,z], Item, Fixed, Invisible
  painting       facing (2D byte: 0 S, 1 W, 2 N, 3 E), block_pos, variant         armour stand  equipment:{head,chest,legs,feet,mainhand,offhand}
Heterogeneous lists (["a", {text:"b"}]) can't be written by nbtlib: use all strings or all compounds."""
import io, json, struct

import nbtlib
from nbtlib import (Byte, Compound, Double, Float, Int, IntArray, List, String, parse_nbt, serialize_tag)

# block name (no namespace) -> block entity id, for blocks that carry one
_BE_SUFFIX = [("_wall_hanging_sign", "hanging_sign"), ("_hanging_sign", "hanging_sign"), ("_wall_sign", "sign"),
              ("_sign", "sign"), ("_wall_banner", "banner"), ("_banner", "banner"), ("_bed", "bed"),
              ("_shulker_box", "shulker_box"), ("_skull", "skull"), ("_head", "skull"), ("_wall_skull", "skull"),
              ("_wall_head", "skull"), ("_copper_chest", "chest"), ("copper_golem_statue", "copper_golem_statue")]
_BE_EXACT = {"chest": "chest", "trapped_chest": "trapped_chest", "ender_chest": "ender_chest", "copper_chest": "chest",
             "barrel": "barrel", "furnace": "furnace", "blast_furnace": "blast_furnace", "smoker": "smoker",
             "shulker_box": "shulker_box", "decorated_pot": "decorated_pot", "lectern": "lectern", "campfire": "campfire",
             "soul_campfire": "campfire", "brewing_stand": "brewing_stand", "chiseled_bookshelf": "chiseled_bookshelf",
             "dispenser": "dispenser", "dropper": "dropper", "hopper": "hopper", "jukebox": "jukebox", "bell": "bell",
             "beehive": "beehive", "bee_nest": "beehive", "enchanting_table": "enchanting_table", "beacon": "beacon",
             "conduit": "conduit", "crafter": "crafter", "vault": "vault", "trial_spawner": "trial_spawner",
             "spawner": "mob_spawner", "creaking_heart": "creaking_heart", "shelf": "shelf"}


def be_id(block_name):
    """Block entity id for a block ('minecraft:oak_wall_sign' -> 'minecraft:sign'), or None if it has none."""
    n = block_name.split(":")[-1]
    if n in _BE_EXACT:
        return "minecraft:" + _BE_EXACT[n]
    if n.endswith("_shelf"):
        return "minecraft:shelf"
    for suf, i in _BE_SUFFIX:
        if n.endswith(suf):
            return "minecraft:" + i
    return None


def ns(x):
    return x if ":" in x else "minecraft:" + x


def to_tag(v) -> Compound:
    """SNBT string / Compound / dict-of-tags -> Compound."""
    if v is None:
        return None
    if isinstance(v, Compound):
        return v
    if isinstance(v, str):
        t = parse_nbt(v)
        if not isinstance(t, Compound):
            raise ValueError(f"not a compound: {v[:60]}")
        return t
    if isinstance(v, dict):
        return parse_nbt(snbt_from_py(v))
    raise TypeError(f"nbt: {type(v)}")


def snbt(t) -> str:
    return serialize_tag(t, compact=True)


def snbt_from_py(v):
    """Python -> SNBT with light typing: bool -> byte, int -> int, float -> double, str -> string.
    Use explicit SNBT (e.g. '3b') through the Raw wrapper for anything else."""
    if isinstance(v, Raw):
        return v.s
    if isinstance(v, bool):
        return "1b" if v else "0b"
    if isinstance(v, int):
        return str(v)
    if isinstance(v, float):
        return repr(v) + "d"
    if isinstance(v, str):
        return json.dumps(v)
    if isinstance(v, (list, tuple)):
        return "[" + ",".join(snbt_from_py(x) for x in v) + "]"
    if isinstance(v, dict):
        return "{" + ",".join(f"{_key(k)}:{snbt_from_py(x)}" for k, x in v.items()) + "}"
    if isinstance(v, nbtlib.tag.Base):
        return snbt(v)
    raise TypeError(type(v))


def _key(k):
    return k if all(c.isalnum() or c in "_.+-" for c in k) else json.dumps(k)


class Raw:
    """A literal SNBT fragment inside snbt_from_py ('3b', '[I;1,2,3]')."""

    def __init__(self, s):
        self.s = s


# ------------------------------------------------------------------ binary
def named_bytes(name, tag) -> bytes:
    b = io.BytesIO()
    tag.write(b, byteorder="big")
    nb = name.encode("utf-8")
    return bytes([tag.tag_id]) + struct.pack(">H", len(nb)) + nb + b.getvalue()


# ------------------------------------------------------------------ comparison
def unwrap(t):
    """26.x heterogeneous lists come back as [{"": x}, ...]; unwrap those."""
    if isinstance(t, Compound) and len(t) == 1 and "" in t:
        return unwrap(t[""])
    return t


def norm(t):
    """Plain python value for comparisons (numbers lose their width: 1b == 1 == 1.0)."""
    t = unwrap(t)
    if isinstance(t, Compound):
        d = {str(k): norm(v) for k, v in t.items()}
        if list(d) == ["text"] and isinstance(d["text"], str):
            return d["text"]  # plain text component {text:"x"} is stored as "x"
        return d
    if isinstance(t, (List, list)) or isinstance(t, nbtlib.tag.Array):
        return [norm(x) for x in t]
    if isinstance(t, String):
        return str(t)
    if isinstance(t, (int, float)):
        return float(t)
    return t


IGNORE_KEYS = {"x", "y", "z", "keepPacked", "components", "UUID", "Pos", "Motion", "Air", "fall_distance", "OnGround",
               "PortalCooldown", "Fire", "Brain", "attributes", "HurtTime", "DeathTime", "AbsorptionAmount", "FallFlying",
               "Health", "current_impulse_context_reset_grace_time", "block_pos", "TileX", "TileY", "TileZ"}


def subset(want, got, path=""):
    """True if every key/value in `want` is present and equal in `got` (got may hold extra defaults).
    Returns (ok, first mismatch path)."""
    if isinstance(want, dict):
        if not isinstance(got, dict):
            return False, path
        for k, v in want.items():
            if k in IGNORE_KEYS:
                continue
            if k not in got:
                if _is_default(v):
                    continue
                return False, f"{path}.{k}"
            if k == "Rotation" and isinstance(v, list) and isinstance(got[k], list) and v and got[k]:
                yaw_ok = abs(((v[0] - got[k][0]) + 180) % 360 - 180) < 1e-2  # yaw is unwrapped (-540 == 180)
                if not yaw_ok:
                    return False, f"{path}.{k}[0]"
                continue
            ok, p = subset(v, got[k], f"{path}.{k}")
            if not ok:
                return False, p
        return True, ""
    if isinstance(want, list):
        if not isinstance(got, list) or len(want) != len(got):
            return False, path
        for i, (a, b) in enumerate(zip(want, got)):
            ok, p = subset(a, b, f"{path}[{i}]")
            if not ok:
                return False, p
        return True, ""
    if isinstance(want, float) and isinstance(got, float):
        return abs(want - got) < 1e-3, path
    return want == got, path


def _is_default(v):
    return v in (0.0, "", [], {}) or v is False


# ------------------------------------------------------------------ builders (return Compounds)
def item(id, count=1, slot=None, components=None, **comp):
    """Item stack. components: dict of SNBT fragments keyed by component id, e.g. {"custom_name": "'Old key'"}
    (values are SNBT strings), or keyword args (python values)."""
    d = {"id": ns(id), "count": int(count)}
    if slot is not None:
        d["Slot"] = Raw(f"{int(slot)}b")
    cs = dict(components or {})
    for k, v in comp.items():
        cs[k] = v
    if cs:
        d["components"] = Raw("{" + ",".join(f"{json.dumps(ns(k))}:{v if isinstance(v, str) else snbt_from_py(v)}"
                                             for k, v in cs.items()) + "}")
    return to_tag(d)


def container(items, lock=None, loot_table=None):
    """Chest / barrel / shulker contents. items: list of item() Compounds (Slot set automatically if missing).
    lock: an item predicate SNBT ('{items:"minecraft:tripwire_hook"}') = can't be opened without it (decor chests)."""
    out = []
    used = {int(i["Slot"]) for i in items if "Slot" in i}
    free = (s for s in range(27) if s not in used)
    for it in items:
        it = Compound(it)
        if "Slot" not in it:
            it["Slot"] = Byte(next(free))
        out.append(it)
    d = Compound({"Items": List[Compound](out)})
    if lock:
        d["lock"] = to_tag(lock)
    if loot_table:
        d["LootTable"] = String(ns(loot_table))
    return d


chest = barrel = container


def _text(line):
    if isinstance(line, dict):
        return to_tag(line)
    return Compound({"text": String(str(line))})


def sign(front=(), back=(), color="black", glow=False, waxed=True):
    """Sign text (up to 4 lines a side). waxed=True: players can't edit it."""
    def side(lines):
        lines = list(lines)[:4] + [""] * (4 - min(4, len(list(lines))))
        return Compound({"messages": List[Compound]([_text(l) for l in lines]), "color": String(color),
                         "has_glowing_text": Byte(1 if glow else 0)})
    return Compound({"front_text": side(front), "back_text": side(back), "is_waxed": Byte(1 if waxed else 0)})


def banner(patterns):
    """patterns: [(pattern, colour), ...] bottom layer first, e.g. [("stripe_top", "black"), ("border", "yellow")]."""
    return Compound({"patterns": List[Compound]([Compound({"pattern": String(ns(p)), "color": String(c)}) for p, c in patterns])})


def head(name=None, texture=None):
    """Player head: by player name (needs the profile to be looked up by the server/client) or a base64 skin texture."""
    if texture:
        return to_tag({"profile": {"properties": [{"name": "textures", "value": texture}]}})
    return to_tag({"profile": {"name": name or "MHF_Steve"}})


def pot(front=None, back=None, left=None, right=None, item_in=None):
    """Decorated pot: sherd item ids per side (None = plain brick)."""
    sh = {k: {"id": ns(v)} for k, v in (("front", front), ("back", back), ("left", left), ("right", right)) if v}
    d = {}
    if sh:
        d["sherds"] = sh
    t = to_tag(d)
    if item_in is not None:
        t["item"] = item_in
    return t


def book(title, author, pages):
    """Written book item (pages: list of plain strings)."""
    return item("written_book", 1, components={
        "written_book_content": "{" + f"title:{{raw:{json.dumps(title)}}},author:{json.dumps(author)},pages:["
        + ",".join("{raw:" + json.dumps(p) + "}" for p in pages) + "]}"})


def lectern(book_item=None, page=0):
    if book_item is None:
        book_item = item("writable_book")
    return Compound({"Book": book_item, "Page": Int(page)})


# ------------------------------------------------------------------ entities
FACING3 = {"down": 0, "up": 1, "north": 2, "south": 3, "west": 4, "east": 5}
FACING2 = {"south": 0, "west": 1, "north": 2, "east": 3}


def item_frame(it=None, facing="south", fixed=True, invisible=False, glow=False, rotation=0, invulnerable=True):
    """Item frame hanging on the wall BEHIND it: facing = the direction it looks (out of the wall)."""
    d = Compound({"id": String("minecraft:glow_item_frame" if glow else "minecraft:item_frame"),
                  "Facing": Byte(FACING3[facing]), "Fixed": Byte(1 if fixed else 0), "Invisible": Byte(1 if invisible else 0),
                  "ItemRotation": Byte(rotation % 8), "Invulnerable": Byte(1 if invulnerable else 0)})
    if it is not None:
        d["Item"] = it
    return d


def painting(variant, facing="south", invulnerable=True):
    return Compound({"id": String("minecraft:painting"), "variant": String(ns(variant)), "facing": Byte(FACING2[facing]),
                     "Invulnerable": Byte(1 if invulnerable else 0)})


def armor_stand(head=None, chest=None, legs=None, feet=None, mainhand=None, offhand=None, yaw=0.0, arms=True,
                small=False, base=True, pose=None, locked=True, invulnerable=True):
    """Armour stand with gear (item() Compounds or item ids). locked: players can't take or swap the gear."""
    eq = {}
    for k, v in (("head", head), ("chest", chest), ("legs", legs), ("feet", feet), ("mainhand", mainhand), ("offhand", offhand)):
        if v is not None:
            eq[k] = item(v) if isinstance(v, str) else v
    d = Compound({"id": String("minecraft:armor_stand"), "ShowArms": Byte(1 if arms else 0), "Small": Byte(1 if small else 0),
                  "NoBasePlate": Byte(0 if base else 1), "Rotation": List[Float]([Float(yaw), Float(0)]),
                  "Invulnerable": Byte(1 if invulnerable else 0)})
    if eq:
        d["equipment"] = Compound(eq)
    if locked:
        d["DisabledSlots"] = Int(4144959)   # every slot: no taking, no putting, no swapping
    if pose:
        d["Pose"] = to_tag(pose)
    return d


_CW = {"north": "east", "east": "south", "south": "west", "west": "north"}
_F3 = {v: k for k, v in FACING3.items()}
_F2 = {v: k for k, v in FACING2.items()}


def transform_entity(t, k, mirror=False):
    """Entity nbt through an optional east<->west mirror, then k quarter turns clockwise (seen from above)."""
    t = Compound(t)
    def turn(d):
        if mirror:
            d = {"east": "west", "west": "east"}.get(d, d)
        for _ in range(k % 4):
            d = _CW.get(d, d)
        return d
    if "Facing" in t:
        t["Facing"] = Byte(FACING3[turn(_F3[int(t["Facing"])])])
    if "facing" in t and str(t["id"]).endswith("painting"):
        t["facing"] = Byte(FACING2[turn(_F2[int(t["facing"])])])
    if "Rotation" in t:
        yaw = float(t["Rotation"][0])
        if mirror:
            yaw = -yaw
        t["Rotation"] = List[Float]([Float((yaw + 90 * k) % 360), Float(t["Rotation"][1])])
    return t
