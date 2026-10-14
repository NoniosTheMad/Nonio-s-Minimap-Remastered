loot spawn ~ ~1.5 ~ loot nonios:arena/surge
execute as @e[type=item,distance=..2.5,tag=!nx.flung] run function nonios:arena/event/fling
particle minecraft:happy_villager ~ ~1.5 ~ 0.4 0.6 0.4 0 20
particle minecraft:firework ~ ~1.5 ~ 0.2 0.2 0.2 0.15 15
playsound minecraft:block.amethyst_block.chime master @a ~ ~ ~ 3 1.6
scoreboard players remove @s nx.ar_ev 1
execute if score @s nx.ar_ev matches ..0 run tag @s remove nx.surge
