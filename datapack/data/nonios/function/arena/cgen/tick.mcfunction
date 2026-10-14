# as + at the centre generator marker
function nonios:arena/cgen/scale
# timer; Golden Hour: x golden_speed
scoreboard players operation #cdt nx.arena = #dt nx.arena
execute if score #golden_t nx.arena matches 1.. run scoreboard players operation #cdt nx.arena *= #cg_gold nx.gen
scoreboard players operation @s nx.gen_t -= #cdt nx.arena
execute if score @s nx.gen_t matches ..0 run function nonios:arena/cgen/drop
execute as @e[type=item_display,tag=nx.cgen_core,distance=..2,limit=1] at @s run tp @s ~ ~ ~ ~18 ~
execute if score #half nx.arena matches 0 run function nonios:arena/cgen/holo
