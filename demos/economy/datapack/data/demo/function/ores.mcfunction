# a 2-high ore wall 3 blocks east of you (one column per yield: stone, coal, copper, iron, gold, redstone, lapis, diamond,
# emerald, emerald block) + pickaxes: plain, Fortune I / II / III, Silk Touch. Buttons again = fresh wall.
execute align xyz run fill ~3 ~ ~-5 ~3 ~1 ~4 minecraft:stone
execute align xyz run fill ~3 ~ ~-4 ~3 ~1 ~-4 minecraft:coal_ore
execute align xyz run fill ~3 ~ ~-3 ~3 ~1 ~-3 minecraft:copper_ore
execute align xyz run fill ~3 ~ ~-2 ~3 ~1 ~-2 minecraft:iron_ore
execute align xyz run fill ~3 ~ ~-1 ~3 ~1 ~-1 minecraft:gold_ore
execute align xyz run fill ~3 ~ ~ ~3 ~1 ~ minecraft:redstone_ore
execute align xyz run fill ~3 ~ ~1 ~3 ~1 ~1 minecraft:lapis_ore
execute align xyz run fill ~3 ~ ~2 ~3 ~1 ~2 minecraft:diamond_ore
execute align xyz run fill ~3 ~ ~3 ~3 ~1 ~3 minecraft:emerald_ore
execute align xyz run fill ~3 ~ ~4 ~3 ~1 ~4 minecraft:deepslate
execute align xyz run fill ~2 ~ ~-5 ~2 ~1 ~4 minecraft:air
execute align xyz run fill ~2 ~-1 ~-5 ~2 ~-1 ~4 minecraft:smooth_stone keep
clear @s *[minecraft:custom_data={demo_pick:1b}]
give @s minecraft:diamond_pickaxe[custom_data={demo_pick:1b},item_name={text:"Pickaxe (no Fortune)"}]
give @s minecraft:diamond_pickaxe[custom_data={demo_pick:1b},enchantments={"minecraft:fortune":1},item_name={text:"Fortune I (+40%)"}]
give @s minecraft:diamond_pickaxe[custom_data={demo_pick:1b},enchantments={"minecraft:fortune":2},item_name={text:"Fortune II (+80%)"}]
give @s minecraft:diamond_pickaxe[custom_data={demo_pick:1b},enchantments={"minecraft:fortune":3},item_name={text:"Fortune III (+120%)"}]
give @s minecraft:diamond_pickaxe[custom_data={demo_pick:1b},enchantments={"minecraft:silk_touch":1},item_name={text:"Silk Touch (place-back test)"}]
tellraw @s {"text":"[demo] Ore wall 3 blocks east (north to south: stone, coal 0.1, copper 0.2, iron 0.5, gold 1, redstone 2, lapis 4, diamond 3, emerald 5, deepslate). 5 pickaxes.","color":"yellow"}
