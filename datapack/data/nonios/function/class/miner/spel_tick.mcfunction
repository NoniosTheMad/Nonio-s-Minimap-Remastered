# as/at a Miner with ore sense left (nx.cls_spel ticks): every 3rd tick redraw the dots
scoreboard players remove @s nx.cls_spel 1
execute if score @s nx.cls_spel matches ..0 run return run function nonios:class/miner/spel_end
scoreboard players operation #s nx.cls_tmp = @s nx.cls_spel
scoreboard players operation #s nx.cls_tmp %= #3 nx.cls_tmp
execute unless score #s nx.cls_tmp matches 0 run return 0
tag @s add nx.spel_me
scoreboard players operation #me nx.cls_tmp = @s nx.pid
execute as @e[type=marker,tag=nx.spel] if score @s nx.pid = #me nx.cls_tmp at @s run function nonios:class/miner/spel_dot
tag @s remove nx.spel_me
