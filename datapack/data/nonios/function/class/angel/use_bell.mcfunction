# Sanctuary Bell rung (45 s cooldown, the horn puts it on): the Angel and every ally within 8 blocks are blessed
# (angel/bless), and a golden ring runs out over the ground (angel/wave)
tag @s add nx.cls_me
function nonios:class/angel/allies
tag @s add nx.cls_ally
execute as @e[tag=nx.cls_ally,distance=..8] at @s run function nonios:class/angel/bless
tag @e[tag=nx.cls_ally] remove nx.cls_ally
tag @s remove nx.cls_me
summon minecraft:marker ~ ~ ~ {Tags:["nx.ang_wave","nx.ang_new"]}
scoreboard players operation @e[type=marker,tag=nx.ang_new] nx.pid = @s nx.pid
scoreboard players set @e[type=marker,tag=nx.ang_new] nx.cls_aw 0
tag @e[type=marker,tag=nx.ang_new] remove nx.ang_new
playsound minecraft:block.beacon.power_select player @a ~ ~ ~ 1.5 1.4
