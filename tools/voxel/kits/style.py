"""Style palettes for furniture kits: one Style names the wood, stone, cloth, metal and light families a room is
built from, so the same kit reads as a peasant's cottage or a lord's solar.

    st = STYLES["keep"]
    st.w("stairs")  -> "minecraft:spruce_stairs"       st.w2("planks") -> second wood
    st.s("wall")    -> "minecraft:stone_brick_wall"     st.cloth / st.cloth2 -> dye colours
    st.lantern      -> "minecraft:lantern" | "minecraft:soul_lantern"
"""
from dataclasses import dataclass, field, replace

# wood family -> (planks, log, stripped log, wood-ish suffix)
_LOG = {"crimson": "crimson_stem", "warped": "warped_stem", "bamboo": "bamboo_block"}
_STONE = {  # family -> (block, stairs, slab, wall)
    "stone_brick": ("stone_bricks", "stone_brick_stairs", "stone_brick_slab", "stone_brick_wall"),
    "mossy_stone_brick": ("mossy_stone_bricks", "mossy_stone_brick_stairs", "mossy_stone_brick_slab", "mossy_stone_brick_wall"),
    "cobblestone": ("cobblestone", "cobblestone_stairs", "cobblestone_slab", "cobblestone_wall"),
    "brick": ("bricks", "brick_stairs", "brick_slab", "brick_wall"),
    "deepslate_brick": ("deepslate_bricks", "deepslate_brick_stairs", "deepslate_brick_slab", "deepslate_brick_wall"),
    "deepslate_tile": ("deepslate_tiles", "deepslate_tile_stairs", "deepslate_tile_slab", "deepslate_tile_wall"),
    "polished_blackstone_brick": ("polished_blackstone_bricks", "polished_blackstone_brick_stairs",
                                  "polished_blackstone_brick_slab", "polished_blackstone_brick_wall"),
    "polished_blackstone": ("polished_blackstone", "polished_blackstone_stairs", "polished_blackstone_slab",
                            "polished_blackstone_wall"),
    "tuff_brick": ("tuff_bricks", "tuff_brick_stairs", "tuff_brick_slab", "tuff_brick_wall"),
    "mud_brick": ("mud_bricks", "mud_brick_stairs", "mud_brick_slab", "mud_brick_wall"),
    "sandstone": ("cut_sandstone", "sandstone_stairs", "cut_sandstone_slab", "sandstone_wall"),
    "quartz": ("quartz_bricks", "quartz_stairs", "quartz_slab", "diorite_wall"),
    "polished_andesite": ("polished_andesite", "polished_andesite_stairs", "polished_andesite_slab", "andesite_wall"),
    "resin_brick": ("resin_bricks", "resin_brick_stairs", "resin_brick_slab", "resin_brick_wall"),
}


def _ns(b):
    return b if ":" in b else "minecraft:" + b


@dataclass(frozen=True)
class Style:
    name: str
    wood: str = "spruce"           # main joinery
    wood2: str = "dark_oak"        # accents, legs, trims
    stone: str = "stone_brick"     # hearths, altars, plinths
    cloth: str = "red"             # beds, carpets, banners
    cloth2: str = "black"          # patterns / borders
    cloth3: str = "yellow"         # highlights (borders, trims)
    metal: str = "iron"            # iron | gold | copper
    soul: bool = False             # soul lanterns / soul campfires
    candle: str = ""               # candle colour ("" = plain)
    accent: str = "chiseled_stone_bricks"   # precious block (thrones, altars)
    plants: tuple = ("potted_fern", "potted_red_tulip", "potted_azalea_bush")
    food: tuple = ("bread", "cooked_chicken", "apple", "baked_potato", "cooked_beef")
    extra: dict = field(default_factory=dict)

    # wood helpers
    def w(self, part, wood=None):
        wd = wood or self.wood
        if part == "log":
            return _ns(_LOG.get(wd, wd + "_log"))
        if part == "stripped":
            return _ns("stripped_" + _LOG.get(wd, wd + "_log")) if wd != "bamboo" else _ns("stripped_bamboo_block")
        if part == "wood":
            if wd in ("crimson", "warped"):
                return _ns(f"{wd}_hyphae")
            return _ns(f"{wd}_wood") if wd != "bamboo" else _ns("bamboo_block")
        if part == "wall_sign":
            return _ns(f"{wd}_wall_sign")
        return _ns(f"{wd}_{part}")

    def w2(self, part):
        return self.w(part, self.wood2)

    def s(self, part):
        b, st, sl, wl = _STONE[self.stone]
        return _ns({"block": b, "stairs": st, "slab": sl, "wall": wl}[part])

    @property
    def lantern(self):
        return _ns("soul_lantern" if self.soul else "lantern")

    @property
    def torch(self):
        return _ns("soul_torch" if self.soul else "torch"), _ns("soul_wall_torch" if self.soul else "wall_torch")

    @property
    def campfire(self):
        return _ns("soul_campfire" if self.soul else "campfire")

    def candles(self, n=3, lit=True):
        c = (self.candle + "_candle") if self.candle else "candle"
        return _ns(f"{c}[candles={max(1, min(4, n))},lit={'true' if lit else 'false'}]")

    @property
    def chain(self):
        return _ns("waxed_copper_chain" if self.metal == "copper" else "iron_chain")

    @property
    def panel(self):
        """Trapdoor for cabinet doors and armrests: the main wood if its trapdoor is solid, else spruce."""
        return self.w("trapdoor") if self.wood in ("spruce", "birch", "dark_oak", "pale_oak") else _ns("spruce_trapdoor")

    @property
    def metal_block(self):
        return _ns({"gold": "gold_block", "copper": "waxed_cut_copper", "iron": "iron_block"}[self.metal])

    @property
    def bars(self):
        return _ns("waxed_copper_bars" if self.metal == "copper" else "iron_bars")

    def carpet(self, colour=None):
        return _ns(f"{colour or self.cloth}_carpet")

    def wool(self, colour=None):
        return _ns(f"{colour or self.cloth}_wool")

    def bed(self, colour=None):
        return _ns(f"{colour or self.cloth}_bed")

    def banner(self, colour=None, wall=True):
        return _ns(f"{colour or self.cloth}_{'wall_' if wall else ''}banner")

    def but(self, **kw):
        return replace(self, **kw)


STYLES = {
    # the castle's working rooms: spruce joinery on stone, red & black heraldry
    "keep": Style("keep", wood="spruce", wood2="dark_oak", stone="stone_brick", cloth="red", cloth2="black",
                  cloth3="yellow"),
    # lord's apartments: dark oak, blackstone, purple & gold, gilt metal
    "noble": Style("noble", wood="dark_oak", wood2="spruce", stone="polished_blackstone_brick", cloth="purple",
                   cloth2="yellow", cloth3="black", metal="gold", candle="", accent="gold_block",
                   plants=("potted_flowering_azalea_bush", "potted_allium", "potted_white_tulip"),
                   food=("golden_apple", "cooked_chicken", "bread", "pumpkin_pie", "glow_berries")),
    # peasants, servants, cottages: oak & birch, cobble, earthy greens
    "cottage": Style("cottage", wood="oak", wood2="spruce", stone="cobblestone", cloth="green", cloth2="brown",
                     cloth3="white", plants=("potted_dandelion", "potted_oxeye_daisy", "potted_fern"),
                     food=("bread", "apple", "carrot", "baked_potato", "beetroot_soup")),
    # chapel: pale birch & quartz, white & blue, candles everywhere
    "chapel": Style("chapel", wood="birch", wood2="dark_oak", stone="quartz", cloth="white", cloth2="blue",
                    cloth3="light_blue", metal="gold", candle="white", accent="chiseled_quartz_block",
                    plants=("potted_lily_of_the_valley", "potted_white_tulip", "potted_azure_bluet")),
    # the alchemist / mage: dark oak & crimson, deepslate, purple & cyan, soul light
    "arcane": Style("arcane", wood="dark_oak", wood2="crimson", stone="deepslate_tile", cloth="purple",
                    cloth2="cyan", cloth3="magenta", metal="copper", soul=True, candle="purple",
                    accent="amethyst_block", plants=("potted_crimson_fungus", "potted_warped_roots", "potted_red_mushroom"),
                    food=("glass_bottle", "potion", "honey_bottle", "spider_eye", "fermented_spider_eye")),
}
