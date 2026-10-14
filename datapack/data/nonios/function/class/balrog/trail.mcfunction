# as/at a Balrog trail marker, each tick (from class/tick)
scoreboard players remove @s nx.cls_ttl 1
execute if score @s nx.cls_ttl matches ..0 run return run kill @s
execute if predicate nonios:class/coin run particle minecraft:large_smoke ~ ~0.2 ~ 0.2 0.1 0.2 0.01 1
execute if score @s nx.cls_ttl matches 60.. if predicate nonios:class/coin if predicate nonios:class/coin run particle minecraft:lava ~ ~0.2 ~ 0.1 0 0.1 0 1
execute if entity @s[tag=nx.bal_white] as @e[distance=..1,type=!#nonios:class/inert,team=!white,tag=!nx.cls_balrog] at @s run return run function nonios:class/balrog/curse
execute if entity @s[tag=nx.bal_black] as @e[distance=..1,type=!#nonios:class/inert,team=!black,tag=!nx.cls_balrog] at @s run return run function nonios:class/balrog/curse
execute unless entity @s[tag=nx.bal_white] unless entity @s[tag=nx.bal_black] as @e[distance=..1,type=!#nonios:class/inert,tag=!nx.cls_balrog] at @s run function nonios:class/balrog/curse
