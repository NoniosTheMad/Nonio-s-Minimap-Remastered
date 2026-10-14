# as + at the centre generator whose timer ran out: #crolls rolls of its level's table (coins -> pot, items drop).
# Too many item stacks lying here: hold the drop until someone collects.
execute store result score #items nx.arena if entity @e[type=item,distance=..2.5]
execute if score #items nx.arena >= #cg_icap nx.gen run return run scoreboard players set @s nx.gen_t 0
scoreboard players operation #left nx.arena = #crolls nx.arena
execute store result storage nonios:arena cg.lvl int 1 run scoreboard players get @s nx.gen_lvl
function nonios:arena/cgen/roll_m with storage nonios:arena cg
scoreboard players operation @s nx.gen_pot < @s nx.gen_cap
particle minecraft:end_rod ~ ~0.9 ~ 0.2 0.2 0.2 0.03 8
playsound minecraft:block.amethyst_block.chime block @a[distance=..24] ~ ~ ~ 0.9 1.1
scoreboard players operation @s nx.gen_t += #cg_iv nx.gen
execute if score @s nx.gen_t matches ..0 run function nonios:arena/cgen/drop
