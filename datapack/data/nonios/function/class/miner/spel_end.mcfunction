# as the Miner: ore sense over, its markers go
scoreboard players set @s nx.cls_spel 0
scoreboard players operation #me nx.cls_tmp = @s nx.pid
execute as @e[type=marker,tag=nx.spel] if score @s nx.pid = #me nx.cls_tmp run kill @s
