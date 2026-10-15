# as the Angel: let go of its ally
scoreboard players set @s nx.cls_alk 0
scoreboard players operation #me nx.cls_tmp = @s nx.pid
execute as @e[tag=nx.ang_t] if score @s nx.cls_atg = #me nx.cls_tmp run function nonios:class/angel/release
