scoreboard players add #solo nx.cls_lvl 1
execute if score #solo nx.cls_lvl matches 4.. run scoreboard players set #solo nx.cls_lvl 1
scoreboard players operation #white nx.cls_lvl = #solo nx.cls_lvl
scoreboard players operation #black nx.cls_lvl = #solo nx.cls_lvl
execute store result storage demo:tmp m.l int 1 run scoreboard players get #solo nx.cls_lvl
function demo:level_say with storage demo:tmp m
execute if score @s nx.cls_basic matches 1.. unless function nonios:class/gen/is_shop run function demo:reapply_basic
