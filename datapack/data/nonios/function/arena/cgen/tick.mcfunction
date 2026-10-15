# as + at the centre generator marker, every arena loop (10 ticks)
function nonios:arena/cgen/scale
scoreboard players operation @s nx.gen_t -= #dt nx.arena
execute if score @s nx.gen_t matches ..0 run function nonios:arena/cgen/drop
# the core spins and bobs; green glints rise from it (gold ones too in Golden Hour)
execute as @e[type=item_display,tag=nx.cgen_core,distance=..3,limit=1] at @s run tp @s ~ ~ ~ ~24 ~
particle minecraft:happy_villager ~ ~1.1 ~ 0.35 0.45 0.35 0 2
particle minecraft:composter ~ ~0.2 ~ 0.6 0.05 0.6 0 3
execute if score #golden_t nx.arena matches 1.. run particle minecraft:wax_on ~ ~1.2 ~ 0.5 0.5 0.5 0.5 4
