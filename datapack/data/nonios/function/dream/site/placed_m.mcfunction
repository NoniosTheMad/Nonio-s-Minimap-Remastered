$tag @s add nx.dream_t_$(tier)
# the beam must reach the sky: punch a 1x1 shaft through any island above the beacon
$execute as @e[type=marker,tag=nx.dream_beam,distance=..$(r)] at @s run fill ~ ~2 ~ ~ 255 ~ minecraft:air
$execute as @e[type=marker,tag=nx.dream_vseed,distance=..$(r)] at @s run function nonios:dream/vein/seed
$execute if score #dbg nx.dream matches 1 run tellraw @a[tag=nx.dream_dbg] [{"text":"site $(name) ($(tier)) at ","color":"gray"},{"storage":"nonios:dream","nbt":"site.x"},{"text":" "},{"storage":"nonios:dream","nbt":"site.z"}]
$execute if data storage nonios:dream site.placed{tier:"nightmare"} run function nonios:dream/nightmare/placed {r:$(r)}
