scoreboard players set @s nx.cls_fuel 0
execute if score @s nx.cls_fly matches 1.. run ride @s dismount
execute if score @s nx.cls_fly matches 1.. run function nonios:class/cracy_frog/unmount
scoreboard players set @s nx.cls_fly 0
scoreboard players set @s nx.cls_tng 0
scoreboard players set @s nx.cls_leap 0
scoreboard players operation #me nx.cls_tmp = @s nx.pid
execute as @e[type=marker,tag=nx.frog_tongue] if score @s nx.pid = #me nx.cls_tmp run kill @s
