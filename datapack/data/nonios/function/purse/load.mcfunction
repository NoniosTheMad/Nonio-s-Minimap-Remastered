# Coin purse: mining earns coins (scoreboard "coins", shared with the shop), carrying them slows you down,
# dying hands the purse to your killer (or drops it as a coin bag). Config lives in nx.purse / nx.coinval.
scoreboard objectives add coins dummy
scoreboard objectives add nx.purse dummy
scoreboard objectives add nx.coinval dummy
scoreboard objectives add nx.bank dummy
scoreboard objectives add nx.died deathCount
scoreboard objectives add nx.pslow dummy
scoreboard objectives add nx.plast dummy

# --- config (only set when missing, so /scoreboard tweaks survive /reload) ---
# weight: speed penalty in permille = coins * w_num / w_den, capped at w_cap  (default 0.1%/coin, max 40%)
execute unless score #w_num nx.purse = #w_num nx.purse run scoreboard players set #w_num nx.purse 1
execute unless score #w_den nx.purse = #w_den nx.purse run scoreboard players set #w_den nx.purse 1
execute unless score #w_cap nx.purse = #w_cap nx.purse run scoreboard players set #w_cap nx.purse 400
# actionbar refresh period (ticks)
execute unless score #ab_every nx.purse = #ab_every nx.purse run scoreboard players set #ab_every nx.purse 40

# --- coins per mined block (fake player #<block> in nx.coinval; 0 = worthless) ---
# Placing one of these blocks costs its value back, so silk-touch place/mine loops earn nothing.
scoreboard objectives add nx.mn.stone minecraft.mined:minecraft.stone
scoreboard objectives add nx.pl.stone minecraft.used:minecraft.stone
execute unless score #stone nx.coinval = #stone nx.coinval run scoreboard players set #stone nx.coinval 1
scoreboard objectives add nx.mn.deepslate minecraft.mined:minecraft.deepslate
scoreboard objectives add nx.pl.deepslate minecraft.used:minecraft.deepslate
execute unless score #deepslate nx.coinval = #deepslate nx.coinval run scoreboard players set #deepslate nx.coinval 1
scoreboard objectives add nx.mn.coal_ore minecraft.mined:minecraft.coal_ore
scoreboard objectives add nx.pl.coal_ore minecraft.used:minecraft.coal_ore
execute unless score #coal_ore nx.coinval = #coal_ore nx.coinval run scoreboard players set #coal_ore nx.coinval 3
scoreboard objectives add nx.mn.deepslate_coal_ore minecraft.mined:minecraft.deepslate_coal_ore
scoreboard objectives add nx.pl.deepslate_coal_ore minecraft.used:minecraft.deepslate_coal_ore
execute unless score #deepslate_coal_ore nx.coinval = #deepslate_coal_ore nx.coinval run scoreboard players set #deepslate_coal_ore nx.coinval 3
scoreboard objectives add nx.mn.copper_ore minecraft.mined:minecraft.copper_ore
scoreboard objectives add nx.pl.copper_ore minecraft.used:minecraft.copper_ore
execute unless score #copper_ore nx.coinval = #copper_ore nx.coinval run scoreboard players set #copper_ore nx.coinval 3
scoreboard objectives add nx.mn.deepslate_copper_ore minecraft.mined:minecraft.deepslate_copper_ore
scoreboard objectives add nx.pl.deepslate_copper_ore minecraft.used:minecraft.deepslate_copper_ore
execute unless score #deepslate_copper_ore nx.coinval = #deepslate_copper_ore nx.coinval run scoreboard players set #deepslate_copper_ore nx.coinval 3
scoreboard objectives add nx.mn.iron_ore minecraft.mined:minecraft.iron_ore
scoreboard objectives add nx.pl.iron_ore minecraft.used:minecraft.iron_ore
execute unless score #iron_ore nx.coinval = #iron_ore nx.coinval run scoreboard players set #iron_ore nx.coinval 5
scoreboard objectives add nx.mn.deepslate_iron_ore minecraft.mined:minecraft.deepslate_iron_ore
scoreboard objectives add nx.pl.deepslate_iron_ore minecraft.used:minecraft.deepslate_iron_ore
execute unless score #deepslate_iron_ore nx.coinval = #deepslate_iron_ore nx.coinval run scoreboard players set #deepslate_iron_ore nx.coinval 5
scoreboard objectives add nx.mn.redstone_ore minecraft.mined:minecraft.redstone_ore
scoreboard objectives add nx.pl.redstone_ore minecraft.used:minecraft.redstone_ore
execute unless score #redstone_ore nx.coinval = #redstone_ore nx.coinval run scoreboard players set #redstone_ore nx.coinval 5
scoreboard objectives add nx.mn.deepslate_redstone_ore minecraft.mined:minecraft.deepslate_redstone_ore
scoreboard objectives add nx.pl.deepslate_redstone_ore minecraft.used:minecraft.deepslate_redstone_ore
execute unless score #deepslate_redstone_ore nx.coinval = #deepslate_redstone_ore nx.coinval run scoreboard players set #deepslate_redstone_ore nx.coinval 5
scoreboard objectives add nx.mn.lapis_ore minecraft.mined:minecraft.lapis_ore
scoreboard objectives add nx.pl.lapis_ore minecraft.used:minecraft.lapis_ore
execute unless score #lapis_ore nx.coinval = #lapis_ore nx.coinval run scoreboard players set #lapis_ore nx.coinval 6
scoreboard objectives add nx.mn.deepslate_lapis_ore minecraft.mined:minecraft.deepslate_lapis_ore
scoreboard objectives add nx.pl.deepslate_lapis_ore minecraft.used:minecraft.deepslate_lapis_ore
execute unless score #deepslate_lapis_ore nx.coinval = #deepslate_lapis_ore nx.coinval run scoreboard players set #deepslate_lapis_ore nx.coinval 6
scoreboard objectives add nx.mn.gold_ore minecraft.mined:minecraft.gold_ore
scoreboard objectives add nx.pl.gold_ore minecraft.used:minecraft.gold_ore
execute unless score #gold_ore nx.coinval = #gold_ore nx.coinval run scoreboard players set #gold_ore nx.coinval 8
scoreboard objectives add nx.mn.deepslate_gold_ore minecraft.mined:minecraft.deepslate_gold_ore
scoreboard objectives add nx.pl.deepslate_gold_ore minecraft.used:minecraft.deepslate_gold_ore
execute unless score #deepslate_gold_ore nx.coinval = #deepslate_gold_ore nx.coinval run scoreboard players set #deepslate_gold_ore nx.coinval 8
scoreboard objectives add nx.mn.nether_gold_ore minecraft.mined:minecraft.nether_gold_ore
scoreboard objectives add nx.pl.nether_gold_ore minecraft.used:minecraft.nether_gold_ore
execute unless score #nether_gold_ore nx.coinval = #nether_gold_ore nx.coinval run scoreboard players set #nether_gold_ore nx.coinval 4
scoreboard objectives add nx.mn.diamond_ore minecraft.mined:minecraft.diamond_ore
scoreboard objectives add nx.pl.diamond_ore minecraft.used:minecraft.diamond_ore
execute unless score #diamond_ore nx.coinval = #diamond_ore nx.coinval run scoreboard players set #diamond_ore nx.coinval 20
scoreboard objectives add nx.mn.deepslate_diamond_ore minecraft.mined:minecraft.deepslate_diamond_ore
scoreboard objectives add nx.pl.deepslate_diamond_ore minecraft.used:minecraft.deepslate_diamond_ore
execute unless score #deepslate_diamond_ore nx.coinval = #deepslate_diamond_ore nx.coinval run scoreboard players set #deepslate_diamond_ore nx.coinval 20
scoreboard objectives add nx.mn.emerald_ore minecraft.mined:minecraft.emerald_ore
scoreboard objectives add nx.pl.emerald_ore minecraft.used:minecraft.emerald_ore
execute unless score #emerald_ore nx.coinval = #emerald_ore nx.coinval run scoreboard players set #emerald_ore nx.coinval 25
scoreboard objectives add nx.mn.deepslate_emerald_ore minecraft.mined:minecraft.deepslate_emerald_ore
scoreboard objectives add nx.pl.deepslate_emerald_ore minecraft.used:minecraft.deepslate_emerald_ore
execute unless score #deepslate_emerald_ore nx.coinval = #deepslate_emerald_ore nx.coinval run scoreboard players set #deepslate_emerald_ore nx.coinval 25

scoreboard players set #10 nx.purse 10
