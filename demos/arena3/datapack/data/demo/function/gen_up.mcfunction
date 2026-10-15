# free upgrade of the nearest generator; at Lv 3 back to Lv 1
execute unless entity @e[type=marker,tag=nx.gen] run return run tellraw @s {"text":"[demo] No generator (Rebuild map).","color":"red"}
execute as @e[type=marker,tag=nx.gen,sort=nearest,limit=1] at @s store success score #ok nx.gen run function nonios:generator/upgrade
execute if score #ok nx.gen matches 0 as @e[type=marker,tag=nx.gen,sort=nearest,limit=1] at @s run function nonios:generator/set_level {lvl:1}
execute as @e[type=marker,tag=nx.gen,sort=nearest,limit=1] run tellraw @a[tag=nx.admin] [{"text":"[demo] Nearest generator: Lv ","color":"yellow"},{"score":{"name":"@s","objective":"nx.gen_lvl"},"color":"white"}]
