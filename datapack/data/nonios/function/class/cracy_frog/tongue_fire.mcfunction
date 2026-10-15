# Shoot the tongue: a marker that flies 1.5 blocks/tick where the frog looked (12 blocks max, 8 ticks). Visible and dodgeable.
function nonios:dream/pid
scoreboard players operation #me nx.cls_tmp = @s nx.pid
execute as @e[type=marker,tag=nx.frog_tongue] if score @s nx.pid = #me nx.cls_tmp run kill @s
tag @s add nx.cls_me
execute anchored eyes positioned ^ ^ ^0.4 run summon minecraft:marker ~ ~ ~ {Tags:["nx.frog_tongue","nx.new"]}
execute as @e[type=marker,tag=nx.new] at @s rotated as @e[tag=nx.cls_me,limit=1] run tp @s ~ ~ ~ ~ ~
scoreboard players operation @e[type=marker,tag=nx.new] nx.pid = #me nx.cls_tmp
tag @e[type=marker,tag=nx.new] remove nx.new
tag @s remove nx.cls_me
scoreboard players set @s nx.cls_tng 8
playsound minecraft:entity.frog.tongue player @a ~ ~ ~ 2 0.8
