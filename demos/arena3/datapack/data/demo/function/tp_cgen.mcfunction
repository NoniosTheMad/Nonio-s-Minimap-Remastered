execute unless entity @e[type=marker,tag=nx.cgen] run return run tellraw @s {"text":"[demo] No centre generator (Rebuild map).","color":"red"}
execute at @e[type=marker,tag=nx.cgen,limit=1] run tp @s ~ ~ ~-3 facing ~ ~1 ~
