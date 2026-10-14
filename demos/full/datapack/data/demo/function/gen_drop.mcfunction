# my nearest generator drops now (ignores the phase gate)
execute unless entity @e[type=marker,tag=nx.gen] run return run tellraw @s {"text":"[demo] No generator.","color":"red"}
execute as @e[type=marker,tag=nx.gen,sort=nearest,limit=1] at @s run function nonios:generator/drop
execute as @e[type=marker,tag=nx.gen,sort=nearest,limit=1] at @s run function nonios:generator/holo
tellraw @s {"text":"[demo] Nearest generator dropped.","color":"yellow"}
