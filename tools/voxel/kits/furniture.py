"""Parametric furniture kits. Every kit returns a small Scene built in a canonical frame:

    front (where you stand or sit to use it) = +z (south); back = z 0, against a wall at z = -1 (not included);
    x runs left -> right as seen from the back wall... i.e. west -> east.

Place with   place(scene, kit, at, facing)   (at = min corner after rotation; facing = the direction the front faces).
Wall-hung pieces (frames, banners, sconces, wall torches) need the room wall at z = -1 when stamped.

Builder craft used (vanilla, block-first; entities only as accents, see playbook §7):
  stair chairs with trapdoor arms, fence + carpet banquet tables with slab centrepieces, plank tables set with flat
  item frames, trapdoor cabinets, barrel and smoker counters, chiseled bookshelves with real books, chain + fence +
  candle chandeliers, corbel candle sconces, fence-bracket lanterns, patterned banners, carpet rugs with borders."""
import random

from .. import nbt as N
from ..scene import Scene
from .style import STYLES, Style

ROT = {"south": 0, "west": 1, "north": 2, "east": 3}


def P(state, **props):
    """Block state with properties: P(st.w("stairs"), facing="north", half="top")."""
    if not props:
        return state
    return state + "[" + ",".join(f"{k}={str(v).lower()}" for k, v in props.items()) + "]"


def _k(size, name):
    return Scene(tuple(int(v) for v in size), name)


def place(s, kit, at, facing="south", air=False):
    """Stamp `kit` into `s` with its front facing `facing`; `at` = min corner. Returns (lo, hi) inclusive."""
    k = ROT[facing]
    s.stamp(kit, tuple(int(v) for v in at), rotate=k, air=air)
    shape = kit.shape if k % 2 == 0 else (kit.shape[2], kit.shape[1], kit.shape[0])
    return tuple(at), tuple(int(a) + n - 1 for a, n in zip(at, shape))


def style(st):
    return STYLES[st] if isinstance(st, str) else st


# ------------------------------------------------------------------ entity accents
def frame_up(k, x, y, z, item, rot=0):
    """Item lying flat on the block below (an invisible frame): plates of food, books, maps on tables."""
    k.entity(N.item_frame(N.item(item), facing="up", invisible=True, rotation=rot), (x + 0.5, y + 1 / 32, z + 0.5))


def frame_wall(k, x, y, z, item, rot=0, invisible=False):
    """Framed item on the wall behind (z - 1), facing south in the canonical frame."""
    k.entity(N.item_frame(N.item(item), facing="south", invisible=invisible, rotation=rot), (x + 0.5, y + 0.5, z + 1 / 32))


# ------------------------------------------------------------------ seating
def chair(st, arms=False):
    """Stair seat, back to the north; arms = open trapdoor side panels."""
    st = style(st)
    k = _k((3 if arms else 1, 1, 1), "chair")
    x = 1 if arms else 0
    k.set(x, 0, 0, P(st.w("stairs"), facing="north"))
    if arms:
        k.set(0, 0, 0, P(st.panel, facing="west", open=True))
        k.set(2, 0, 0, P(st.panel, facing="east", open=True))
    return k


def bench(st, n=3, back=True, arms=True):
    """Pew / bench: n stair seats (or bottom slabs without a back), trapdoor ends."""
    st = style(st)
    a = 1 if arms else 0
    k = _k((n + 2 * a, 1, 1), "bench")
    for i in range(n):
        k.set(a + i, 0, 0, P(st.w("stairs"), facing="north") if back else P(st.w("slab"), type="bottom"))
    if arms:
        k.set(0, 0, 0, P(st.panel, facing="west", open=True))
        k.set(n + 1, 0, 0, P(st.panel, facing="east", open=True))
    return k


def throne(st, dais=True):
    """5 wide x 4 deep: stone dais with a front step, stair seat with upside-down-stair arms, a precious backrest,
    candle posts, carpet in front. Hang banners on the wall behind (tapestry) for the full effect."""
    st = style(st)
    y0 = 1 if dais else 0
    k = _k((5, y0 + 4, 4 if dais else 3), "throne")
    if dais:
        for x in range(5):
            for z in range(3):
                k.set(x, 0, z, st.s("block"))
            k.set(x, 0, 3, P(st.s("stairs"), facing="north"))
    k.set(2, y0, 1, P(st.s("stairs"), facing="north"))
    k.set(1, y0, 1, P(st.s("stairs"), facing="west", half="top"))
    k.set(3, y0, 1, P(st.s("stairs"), facing="east", half="top"))
    for y in range(3):
        k.set(2, y0 + y, 0, st.accent)
    k.set(2, y0 + 3, 0, P(st.s("wall")))
    for x in (1, 3):
        k.set(x, y0, 0, st.s("block"))
        k.set(x, y0 + 1, 0, P(st.s("stairs"), facing="west" if x == 1 else "east", half="bottom"))
    for x in (0, 4):
        k.set(x, y0, 1, st.s("wall"))
        k.set(x, y0 + 1, 1, st.candles(3))
    if dais:
        for x in (1, 2, 3):
            k.set(x, y0, 2, st.carpet())
    return k


# ------------------------------------------------------------------ tables
def table(st, w=4, d=1, kind="plank", seats="chairs", head=False, setting=True, seed=0):
    """Table along x (w long, d deep) with seats on both long sides.
    kind: "plank" (top slabs, set with flat frames, candles, pots) | "cloth" (fence + carpet banquet table with a slab
    centrepiece every third cell). seats: "chairs" (every other cell) | "benches" (continuous) | None."""
    st = style(st)
    rng = random.Random(seed)
    hx = 1 if head else 0
    cz = 1 if seats else 0
    W, D = w + 2 * hx, d + 2 * cz
    k = _k((W, 2, D), "table")
    centre = set()
    for i in range(w):
        for j in range(d):
            x, z = hx + i, cz + j
            if kind == "cloth" and not (w >= 3 and i % 3 == 1):
                k.set(x, 0, z, st.w2("fence"))
                k.set(x, 1, z, st.carpet(st.cloth3 if i in (0, w - 1) else st.cloth))
            else:
                k.set(x, 0, z, P(st.w2("slab"), type="top"))
                centre.add((x, z))
    if seats:
        for i in range(w):
            if seats == "chairs" and w > 3 and i % 2:
                continue
            k.set(hx + i, 0, 0, P(st.w("stairs"), facing="north"))
            k.set(hx + i, 0, D - 1, P(st.w("stairs"), facing="south"))
    if head:
        k.set(0, 0, cz + d // 2, P(st.w("stairs"), facing="west"))
        k.set(W - 1, 0, cz + d // 2, P(st.w("stairs"), facing="east"))
    if setting:
        cells = sorted(centre)
        for n, (x, z) in enumerate(cells):
            r = rng.random()
            mid = kind == "cloth" or (n % 4 == 2)
            if mid:
                k.set(x, 1, z, rng.choice([st.lantern, st.candles(3), st.candles(2), rng.choice(st.plants),
                                           "minecraft:decorated_pot"]) if kind == "cloth" or r < 0.6 else st.candles(3))
            elif r < 0.55:
                frame_up(k, x, 1, z, rng.choice(st.food), rot=rng.randrange(8))
            elif r < 0.7:
                k.set(x, 1, z, st.candles(rng.randint(1, 3)))
            elif r < 0.8:
                k.set(x, 1, z, rng.choice(st.plants))
    return k


def desk(st, seed=0):
    """Writing desk: 2-long slab top with a chair, candles, a book lying open and a lectern-side lantern."""
    st = style(st)
    k = _k((2, 2, 2), "desk")
    for x in (0, 1):
        k.set(x, 0, 0, P(st.w2("slab"), type="top"))
    k.set(0, 0, 1, P(st.w("stairs"), facing="south"))
    k.set(1, 1, 0, st.candles(2))
    frame_up(k, 0, 1, 0, random.Random(seed).choice(["writable_book", "book", "map", "paper"]))
    return k


# ------------------------------------------------------------------ sleeping
def bed(st, double=False, canopy=False, nightstand=True, foot_chest=True, colour=None, seed=0):
    """Headboard against the back wall. nightstand: barrel + candle/plant column on the left (and right if double);
    canopy: dark posts at the head corners with a trapdoor tester above; foot_chest: chest at the foot."""
    st = style(st)
    rng = random.Random(seed)
    bw = 2 if double else 1
    ns_l = 1 if nightstand else 0
    ns_r = 1 if (nightstand and double) else 0
    post = 1 if canopy else 0
    W = ns_l + post + bw + post + ns_r
    D = 2 + (1 if foot_chest else 0)
    k = _k((W, 3 if canopy else 2, D), "bed")
    b0 = ns_l + post
    for i in range(bw):
        k.set(b0 + i, 0, 0, P(st.bed(colour), facing="north", part="head"))
        k.set(b0 + i, 0, 1, P(st.bed(colour), facing="north", part="foot"))
    if canopy:
        for x in (b0 - 1, b0 + bw):
            for y in range(3):
                k.set(x, y, 0, st.w2("fence"))
        for x in range(b0, b0 + bw):
            k.set(x, 2, 0, P(st.w2("trapdoor"), half="top"))
            k.set(x, 2, 1, P(st.w2("trapdoor"), half="top", facing="south", open=True))
    for x in ([0] if ns_l else []) + ([W - 1] if ns_r else []):
        k.set(x, 0, 0, P("minecraft:barrel", facing="up"), nbt=N.barrel([N.item("candle", 4), N.item("paper", 6)]))
        k.set(x, 1, 0, rng.choice([st.candles(2), st.candles(1), rng.choice(st.plants), st.lantern]))
    if foot_chest:
        stuff = N.chest([N.item(st.wool().split(":")[-1], 3), N.item("book", 1), N.item("bread", 2)])
        if double:
            k.set(b0, 0, 2, P("minecraft:chest", facing="south", type="right"), nbt=stuff)
            k.set(b0 + 1, 0, 2, P("minecraft:chest", facing="south", type="left"), nbt=N.chest([]))
        else:
            k.set(b0, 0, 2, P("minecraft:chest", facing="south"), nbt=stuff)
    return k


# ------------------------------------------------------------------ storage
def bookshelf(st, w=3, h=3, chiseled=0.35, cornice=True, pilasters=True, seed=0):
    """Wall of shelves: log pilasters, bookshelves mixed with partly filled chiseled bookshelves, stair cornice."""
    st = style(st)
    rng = random.Random(seed)
    k = _k((w, h, 2 if cornice else 1), "bookshelf")
    books = ["book", "book", "book", "enchanted_book", "writable_book"]
    for x in range(w):
        for y in range(h):
            if pilasters and w > 2 and x in (0, w - 1):
                k.set(x, y, 0, P(st.w2("log"), axis="y"))
            elif rng.random() < chiseled:
                slots = [rng.random() < 0.6 for _ in range(6)]
                props = {f"slot_{i}_occupied": v for i, v in enumerate(slots)}
                items = [N.item(rng.choice(books), slot=i) for i, v in enumerate(slots) if v]
                k.set(x, y, 0, P("minecraft:chiseled_bookshelf", facing="south", **props), nbt=N.container(items))
            else:
                k.set(x, y, 0, "minecraft:bookshelf")
        if cornice:
            k.set(x, h - 1, 1, P(st.w("stairs"), facing="north", half="top"))
    return k


def wardrobe(st, w=2):
    """Plank body, open-trapdoor doors, stair cornice: 2 deep, 3 tall."""
    st = style(st)
    k = _k((w, 3, 2), "wardrobe")
    for x in range(w):
        for y in range(3):
            k.set(x, y, 0, st.w("planks"))
        k.set(x, 0, 1, P(st.panel, facing="south", open=True))
        k.set(x, 1, 1, P(st.panel, facing="south", open=True))
        k.set(x, 2, 1, P(st.w("stairs"), facing="north", half="top"))
    return k


def shelf(st, w=3, seed=0):
    """Wall shelf at head height: top-half trapdoors... as a slab ledge with pots, candles and a book."""
    st = style(st)
    rng = random.Random(seed)
    k = _k((w, 3, 1), "shelf")
    for x in range(w):
        k.set(x, 1, 0, P(st.w("slab"), type="top"))
        k.set(x, 2, 0, rng.choice([rng.choice(st.plants), st.candles(rng.randint(1, 3)), rng.choice(st.plants),
                                   "minecraft:flower_pot"]))
    return k


# ------------------------------------------------------------------ hearth, kitchen, workshop
def hearth(st, w=5, h=5):
    """Fireplace: stone jambs, brick firebox with a campfire, lintel, mantel shelf (upside-down stairs) with candles
    and pots, sloped hood, chimney to the ceiling (h = room height)."""
    st = style(st)
    w = max(5, w | 1)
    c = w // 2
    k = _k((w, h, 3), "hearth")
    stone, brick = st.s("block"), "minecraft:bricks"
    for y in (0, 1):
        for z in (0, 1):
            k.set(c - 2, y, z, stone); k.set(c + 2, y, z, stone)
        for x in (c - 1, c, c + 1):
            k.set(x, y, 0, brick)
    k.set(c, 0, 1, P(st.campfire, facing="south", lit=True))
    for x in range(c - 2, c + 3):
        for z in (0, 1):
            k.set(x, 2, z, stone)
        k.set(x, 2, 2, P(st.s("stairs"), facing="north", half="top"))
    for z in (0, 1):
        k.set(c - 2, 3, z, P(st.s("stairs"), facing="east"))
        k.set(c + 2, 3, z, P(st.s("stairs"), facing="west"))
        for x in (c - 1, c, c + 1):
            k.set(x, 3, z, stone if z == 0 else P(st.s("stairs"), facing="north"))
    for y in range(4, h):
        for x in (c - 1, c, c + 1):
            k.set(x, y, 0, stone)
    k.set(c - 2, 3, 2, st.candles(3)); k.set(c + 2, 3, 2, st.candles(2))
    k.set(c - 1, 3, 2, "minecraft:decorated_pot"); k.set(c + 1, 3, 2, st.plants[0])
    if w >= 7:  # firewood stacks
        for x in (0, w - 1):
            for y in (0, 1):
                k.set(x, y, 0, P(st.w("log"), axis="z"))
    return k


def counter(st, w=4, seed=0):
    """Kitchen counter: barrels (cabinet fronts), smoker, furnace, crafting table; produce on top; tools framed above."""
    st = style(st)
    rng = random.Random(seed)
    k = _k((w, 3, 1), "counter")
    cyc = [P("minecraft:barrel", facing="south"), P("minecraft:smoker", facing="south"),
           P("minecraft:barrel", facing="south"), "minecraft:crafting_table", P("minecraft:furnace", facing="south")]
    off = rng.randrange(len(cyc))
    for x in range(w):
        b = cyc[(x + off) % len(cyc)]
        k.set(x, 0, 0, b, nbt=N.barrel([N.item(rng.choice(["wheat", "potato", "carrot", "beetroot"]), 16)])
              if "barrel" in b else None)
        top = rng.random()
        if top < 0.35:
            frame_up(k, x, 1, 0, rng.choice(st.food + ("bowl", "egg", "sugar")), rot=rng.randrange(8))
        elif top < 0.75:
            k.set(x, 1, 0, st.candles(rng.randint(1, 2)))
        elif top < 0.85:
            k.set(x, 1, 0, rng.choice(st.plants))
    return k


def cauldron(st):
    k = _k((1, 1, 1), "cauldron")
    k.set(0, 0, 0, "minecraft:water_cauldron[level=3]")
    return k


def workbench(st, seed=0):
    """Smithy corner: anvil, grindstone, smithing table, barrel of ingots."""
    st = style(st)
    k = _k((4, 2, 1), "workbench")
    k.set(0, 0, 0, "minecraft:smithing_table")
    k.set(1, 0, 0, "minecraft:anvil[facing=east]")
    k.set(2, 0, 0, "minecraft:grindstone[face=floor,facing=south]")
    k.set(3, 0, 0, P("minecraft:barrel", facing="up"), nbt=N.barrel([N.item("iron_ingot", 12), N.item("coal", 20)]))
    k.set(3, 1, 0, st.lantern)
    return k


def alchemy(st, w=4, seed=0):
    """Alchemist's bench: chiseled bookshelf, water cauldron, a stone worktop, barrel; brewing stands with potions,
    amethyst, candles, a skull and potted fungi on top; ingredients framed on the wall."""
    st = style(st)
    rng = random.Random(seed)
    k = _k((w, 3, 1), "alchemy")
    base = ["shelf", "cauldron", "top", "barrel"]
    for x in range(w):
        b = base[x % len(base)]
        if b == "shelf":
            items = [N.item(rng.choice(["book", "enchanted_book"]), slot=i) for i in range(0, 6, 2)]
            k.set(x, 0, 0, P("minecraft:chiseled_bookshelf", facing="south", slot_0_occupied=True,
                             slot_2_occupied=True, slot_4_occupied=True), nbt=N.container(items))
        elif b == "cauldron":
            k.set(x, 0, 0, "minecraft:water_cauldron[level=3]")
            continue
        elif b == "barrel":
            k.set(x, 0, 0, P("minecraft:barrel", facing="up"), nbt=N.barrel([N.item("glass_bottle", 8), N.item("nether_wart", 12)]))
        else:
            k.set(x, 0, 0, st.s("block"))
        if b == "top" or (b != "cauldron" and x == w - 1):
            pots = [N.item("potion", slot=i, potion_contents={"potion": rng.choice(
                ["minecraft:healing", "minecraft:swiftness", "minecraft:night_vision", "minecraft:fire_resistance"])})
                    for i in range(2)]
            k.set(x, 1, 0, "minecraft:brewing_stand[has_bottle_0=true,has_bottle_1=true,has_bottle_2=false]",
                  nbt=N.container(pots))
        else:
            k.set(x, 1, 0, rng.choice([st.candles(rng.randint(2, 4)), "minecraft:amethyst_cluster[facing=up]",
                                       "minecraft:skeleton_skull[rotation=%d]" % rng.randrange(16), st.plants[0]]))
        if x % 2 == 0:
            frame_wall(k, x, 2, 0, rng.choice(["glass_bottle", "blaze_rod", "ender_eye", "spider_eye", "glowstone_dust"]))
    return k


# ------------------------------------------------------------------ chapel
def altar(st, w=5, centre="book"):
    """Gradin (upside-down stairs) with candles against the wall, altar table (precious block between upside-down stair
    ends) in front, candlesticks at the ends, a carpet kneeler."""
    st = style(st)
    w = max(5, w | 1)
    c = w // 2
    k = _k((w, 3, 3), "altar")
    for x in range(1, w - 1):
        k.set(x, 0, 0, P(st.s("stairs"), facing="north", half="top"))
        k.set(x, 1, 0, st.candles(4 if x == c else (3 if (x - c) % 2 else 1)))
    for x in (0, w - 1):
        k.set(x, 0, 0, st.s("wall")); k.set(x, 1, 0, st.s("wall")); k.set(x, 2, 0, st.candles(3))
    k.set(c, 0, 1, st.accent)
    k.set(c - 1, 0, 1, P(st.s("stairs"), facing="west", half="top"))
    k.set(c + 1, 0, 1, P(st.s("stairs"), facing="east", half="top"))
    k.set(c - 1, 1, 1, st.candles(3)); k.set(c + 1, 1, 1, st.candles(3))
    if centre:
        frame_up(k, c, 1, 1, {"book": "enchanted_book"}.get(centre, centre))
    for x in range(w):
        k.set(x, 0, 2, st.carpet(st.cloth2))
    return k


# ------------------------------------------------------------------ lights
def chandelier(st, r=1, drop=1, kind="candle"):
    """Hangs from the ceiling (the kit's top row touches it): chain, a fence ring (plus-shape for r=1, ring + arms for
    r=2), candles on the posts or lanterns hanging under the arms. Height = drop + 3."""
    st = style(st)
    S = 2 * r + 1
    H = drop + 3
    k = _k((S, H, S), "chandelier")
    c = r
    ring = {(c, c)}
    for d in range(1, r + 1):
        ring |= {(c + d, c), (c - d, c), (c, c + d), (c, c - d)}
    if r >= 2:
        ring |= {(x, z) for x in range(S) for z in range(S) if max(abs(x - c), abs(z - c)) == r}
    for x, z in ring:
        k.set(x, 1, z, st.w2("fence"))
    for y in range(2, H):
        k.set(c, y, c, P(st.chain, axis="y"))
    tips = [(c + r, c), (c - r, c), (c, c + r), (c, c - r)]
    if r >= 2:
        tips += [(c + r, c + r), (c - r, c - r), (c + r, c - r), (c - r, c + r)]
    for x, z in tips:
        if kind == "candle":
            k.set(x, 2, z, st.candles(3 if (x == c or z == c) else 2))
        else:
            k.set(x, 0, z, P(st.lantern, hanging=True))
    if kind == "candle" and r >= 2:
        k.set(c, 0, c, P(st.lantern, hanging=True))
    return k


def hanging_lantern(st, drop=2):
    """Lantern on a chain: height = drop + 1 (top touches the ceiling)."""
    st = style(st)
    k = _k((1, drop + 1, 1), "hanging_lantern")
    k.set(0, 0, 0, P(st.lantern, hanging=True))
    for y in range(1, drop + 1):
        k.set(0, y, 0, P(st.chain, axis="y"))
    return k


def sconce(st, kind="bracket"):
    """Wall light (wall at z = -1). bracket: fence arm with a hanging lantern below (2 tall);
    candle: upside-down stair corbel with candles (2 tall); torch: a wall torch (1 tall)."""
    st = style(st)
    if kind == "torch":
        k = _k((1, 1, 1), "sconce")
        k.set(0, 0, 0, P(st.torch[1], facing="south"))
        return k
    k = _k((1, 2, 1), "sconce")
    if kind == "bracket":
        k.set(0, 1, 0, st.w2("fence"))
        k.set(0, 0, 0, P(st.lantern, hanging=True))
    else:
        k.set(0, 0, 0, P(st.s("stairs"), facing="north", half="top"))
        k.set(0, 1, 0, st.candles(3))
    return k


# ------------------------------------------------------------------ armoury
WEAPONS = ["iron_sword", "iron_axe", "bow", "crossbow", "iron_spear", "mace", "stone_sword", "iron_sword"]


def weapon_rack(st, w=3, seed=0):
    """Framed weapons on the wall at two heights (swords at 45 degrees), barrels of arrows at the ends."""
    st = style(st)
    rng = random.Random(seed)
    k = _k((w, 3, 1), "weapon_rack")
    for x in range(w):
        for y in (1, 2):
            it = rng.choice(WEAPONS)
            frame_wall(k, x, y, 0, it, rot=1 if "sword" in it or "spear" in it else 0)
    for x in (0, w - 1):
        k.set(x, 0, 0, P("minecraft:barrel", facing="up"), nbt=N.barrel([N.item("arrow", 64)]))
    return k


GEAR = {"iron": "iron", "chain": "chainmail", "gold": "golden", "leather": "leather", "diamond": "diamond",
        "copper": "copper", "netherite": "netherite"}


def armour(st, gear="iron", weapon="iron_sword"):
    """Armour stand (an entity: use a few, as accents) in full gear, facing south."""
    g = GEAR.get(gear, gear)
    st = style(st)
    k = _k((1, 2, 1), "armour")
    k.set(0, 0, 0, st.extra.get("plate", "minecraft:stone_pressure_plate"))   # plinth (keeps the spot taken)
    k.entity(N.armor_stand(head=f"{g}_helmet", chest=f"{g}_chestplate", legs=f"{g}_leggings", feet=f"{g}_boots",
                           mainhand=weapon, yaw=0), (0.5, 1 / 16, 0.5))
    return k


# ------------------------------------------------------------------ textiles
def banner_designs(st):
    c1, c2, c3 = st.cloth, st.cloth2, st.cloth3
    return [
        [("stripe_center", c3), ("border", c2)],
        [("rhombus", c2), ("circle", c3), ("border", c2)],
        [("triangles_bottom", c2), ("circle", c3)],
        [("cross", c3), ("border", c2)],
        [("triangle_bottom", c2), ("flower", c3)],
    ]


def tapestry(st, n=1, design=0, gap=0):
    """Patterned wall banners (they hang down over the block below: place 2 above the floor); n banners, `gap` apart."""
    st = style(st)
    ds = banner_designs(st)
    k = _k((n + (n - 1) * gap, 1, 1), "tapestry")
    for i in range(n):
        k.set(i * (gap + 1), 0, 0, P(st.banner(), facing="south"), nbt=N.banner(ds[(design + i) % len(ds)]))
    return k


def rug(st, w, d, pattern="border", colours=None):
    """Carpet rug: border | diamond | checker | stripes | runner. colours = (field, border, motif)."""
    st = style(st)
    f, b, m = colours or (st.cloth, st.cloth2, st.cloth3)
    k = _k((w, 1, d), "rug")
    cx, cz = (w - 1) / 2, (d - 1) / 2
    for x in range(w):
        for z in range(d):
            edge = min(x, z, w - 1 - x, d - 1 - z)
            if pattern == "border":
                c = b if edge == 0 else (m if edge == 1 and min(w, d) >= 5 else f)
                if edge >= 2 and abs(x - cx) + abs(z - cz) <= 1:
                    c = m
            elif pattern == "diamond":
                c = b if edge == 0 else (m if int(abs(x - cx) + abs(z - cz)) % 3 == 0 else f)
            elif pattern == "checker":
                c = b if edge == 0 else (f if (x + z) % 2 else m)
            elif pattern == "stripes":
                c = b if edge == 0 else (m if z % 3 == 1 else f)
            else:  # runner: long axis x, coloured edges
                c = b if z in (0, d - 1) else (m if x % 4 == 0 else f)
            k.set(x, 0, z, st.carpet(c))
    return k


# ------------------------------------------------------------------ clutter
def clutter(st, kind="barrels", seed=0):
    """Small prop clusters for corners and wall gaps (1-2 wide, 1 deep):
    barrels | crates | sacks | pots | plants | candles | firewood | hay | books."""
    st = style(st)
    rng = random.Random(seed)
    if kind == "barrels":
        k = _k((2, 2, 1), "barrels")
        k.set(0, 0, 0, P("minecraft:barrel", facing="up"), nbt=N.barrel([N.item("apple", rng.randint(4, 32))]))
        k.set(1, 0, 0, P("minecraft:barrel", facing=rng.choice(["south", "east"])))
        if rng.random() < 0.6:
            k.set(0, 1, 0, P("minecraft:barrel", facing="up"))
        else:
            k.set(0, 1, 0, st.candles(2))
        return k
    if kind == "crates":
        k = _k((2, 2, 1), "crates")
        k.set(0, 0, 0, "minecraft:composter[level=0]"); k.set(1, 0, 0, P("minecraft:barrel", facing="south"))
        if rng.random() < 0.5:
            k.set(0, 1, 0, "minecraft:composter[level=0]")
        return k
    if kind == "sacks":
        k = _k((2, 2, 1), "sacks")
        k.set(0, 0, 0, "minecraft:white_wool"); k.set(1, 0, 0, "minecraft:light_gray_wool")
        k.set(0, 1, 0, "minecraft:brown_carpet")
        return k
    if kind == "pots":
        k = _k((2, 1, 1), "pots")
        k.set(0, 0, 0, "minecraft:decorated_pot[facing=south]")
        if rng.random() < 0.7:
            k.set(1, 0, 0, "minecraft:decorated_pot[facing=east]")
        return k
    if kind == "plants":
        k = _k((1, 2, 1), "plants")
        k.set(0, 0, 0, P(st.w2("slab"), type="top")); k.set(0, 1, 0, rng.choice(st.plants))
        return k
    if kind == "candles":
        k = _k((1, 2, 1), "candles")
        k.set(0, 0, 0, P(st.s("wall"))); k.set(0, 1, 0, st.candles(rng.randint(2, 4)))
        return k
    if kind == "firewood":
        k = _k((2, 2, 1), "firewood")
        for x in (0, 1):
            k.set(x, 0, 0, P(st.w("log"), axis="z"))
        k.set(0, 1, 0, P(st.w("log"), axis="z"))
        return k
    if kind == "hay":
        k = _k((2, 2, 1), "hay")
        k.set(0, 0, 0, "minecraft:hay_block[axis=x]"); k.set(1, 0, 0, "minecraft:hay_block[axis=x]")
        k.set(0, 1, 0, "minecraft:hay_block[axis=z]")
        return k
    if kind == "books":
        k = _k((1, 2, 1), "books")
        k.set(0, 0, 0, P("minecraft:lectern", facing="south", has_book=True),
              nbt=N.lectern(N.book("Chronicle", "Archivist", ["Year of the long winter.", "The east tower fell."])))
        return k
    raise ValueError(kind)


def lectern(st, title="Chronicle", pages=("",)):
    k = _k((1, 1, 1), "lectern")
    k.set(0, 0, 0, P("minecraft:lectern", facing="south", has_book=True), nbt=N.lectern(N.book(title, "Archivist", list(pages))))
    return k


# ------------------------------------------------------------------ catalogue (for galleries and room helpers)
def catalogue(st, seed=0):
    """[(label, kit)] of every kit in representative sizes."""
    st = style(st)
    return [
        ("chair", chair(st)), ("armchair", chair(st, arms=True)), ("bench", bench(st, 3)), ("throne", throne(st)),
        ("table", table(st, 4, 1, seed=seed)), ("feast table", table(st, 6, 2, kind="cloth", seats="benches", head=True, seed=seed)),
        ("desk", desk(st, seed)), ("bed", bed(st, seed=seed)), ("double canopy bed", bed(st, double=True, canopy=True, seed=seed)),
        ("bookshelf", bookshelf(st, 4, 3, seed=seed)), ("wardrobe", wardrobe(st)), ("shelf", shelf(st, 3, seed)),
        ("hearth", hearth(st, 5, 5)), ("counter", counter(st, 4, seed)), ("cauldron", cauldron(st)),
        ("workbench", workbench(st)), ("alchemy bench", alchemy(st, 4, seed)), ("altar", altar(st, 5)),
        ("chandelier", chandelier(st, 1, 1)), ("great chandelier", chandelier(st, 2, 1)),
        ("lantern chandelier", chandelier(st, 1, 1, kind="lantern")), ("hanging lantern", hanging_lantern(st, 2)),
        ("bracket sconce", sconce(st, "bracket")), ("candle sconce", sconce(st, "candle")), ("torch", sconce(st, "torch")),
        ("weapon rack", weapon_rack(st, 3, seed)), ("armour", armour(st)), ("tapestry", tapestry(st, 3, gap=1)),
        ("rug border", rug(st, 5, 4, "border")), ("rug diamond", rug(st, 5, 5, "diamond")), ("runner", rug(st, 6, 3, "runner")),
        ("barrels", clutter(st, "barrels", seed)), ("crates", clutter(st, "crates", seed)), ("sacks", clutter(st, "sacks")),
        ("pots", clutter(st, "pots", seed)), ("plants", clutter(st, "plants", seed)), ("candles", clutter(st, "candles", seed)),
        ("firewood", clutter(st, "firewood")), ("hay", clutter(st, "hay")), ("lectern", clutter(st, "books")),
    ]
