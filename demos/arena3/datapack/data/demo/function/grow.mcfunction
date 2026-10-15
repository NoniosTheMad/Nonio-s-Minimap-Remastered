execute unless entity @e[type=marker,tag=nx.gen] run return run tellraw @s {"text":"[demo] No generator (Rebuild map).","color":"red"}
execute as @e[type=marker,tag=nx.gen,sort=nearest,limit=1] at @s run function nonios:generator/grow
tellraw @s {"text":"[demo] Nearest generator: new block.","color":"yellow"}
