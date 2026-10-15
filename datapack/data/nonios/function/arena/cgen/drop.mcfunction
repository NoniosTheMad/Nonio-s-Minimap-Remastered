# as + at the centre generator whose timer ran out: spit #crolls emeralds (x golden_mult in Golden Hour) onto the floor.
# Already item_cap emeralds lying within 4 blocks: hold it until someone grabs some.
scoreboard players set #items nx.arena 0
execute as @e[type=item,distance=..4] if items entity @s contents minecraft:emerald run function nonios:arena/cgen/count
execute if score #items nx.arena >= #cg_icap nx.gen run return run scoreboard players set @s nx.gen_t 0
scoreboard players operation #left nx.arena = #crolls nx.arena
execute if score #golden_t nx.arena matches 1.. run scoreboard players operation #left nx.arena *= #golden_mult nx.arena
scoreboard players operation #room nx.arena = #cg_icap nx.gen
scoreboard players operation #room nx.arena -= #items nx.arena
scoreboard players operation #left nx.arena < #room nx.arena
function nonios:arena/cgen/spit
particle minecraft:happy_villager ~ ~1.2 ~ 0.3 0.3 0.3 0 10
playsound minecraft:block.amethyst_block.chime block @a[distance=..24] ~ ~ ~ 0.9 1.4
playsound minecraft:entity.item.pickup block @a[distance=..16] ~ ~1 ~ 0.5 0.6
scoreboard players operation @s nx.gen_t += #cg_iv nx.gen
execute if score @s nx.gen_t matches ..0 run scoreboard players operation @s nx.gen_t = #cg_iv nx.gen
