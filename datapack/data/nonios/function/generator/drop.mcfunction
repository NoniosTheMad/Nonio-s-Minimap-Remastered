# as + at a generator marker whose timer ran out
# Too many item stacks lying here: hold the drop until someone picks them up (keeps item piles bounded).
execute store result score #items nx.gen if entity @e[type=item,distance=..2]
execute if score #items nx.gen >= #item_cap nx.gen run tag @s add nx.gen_full
execute if score #items nx.gen >= #item_cap nx.gen run return run scoreboard players set @s nx.gen_t 0
tag @s remove nx.gen_full
scoreboard players set #left nx.gen 1
execute if entity @s[tag=nx.gen.white] run scoreboard players operation #left nx.gen = #r_white nx.gen
execute if entity @s[tag=nx.gen.black] run scoreboard players operation #left nx.gen = #r_black nx.gen
function nonios:generator/rolls with entity @s data
scoreboard players operation @s nx.gen_pot < @s nx.gen_cap
particle minecraft:end_rod ~ ~0.9 ~ 0.15 0.15 0.15 0.03 6
playsound minecraft:block.amethyst_block.chime block @a[distance=..16] ~ ~ ~ 0.7 1.3
scoreboard players operation @s nx.gen_t += @s nx.gen_iv
# sped-up time can owe more than one drop
execute if score @s nx.gen_t matches ..0 run function nonios:generator/drop
