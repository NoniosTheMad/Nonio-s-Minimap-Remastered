# next to the core, looking at it
execute unless entity @e[type=marker,tag=nx.acore] run return run tellraw @s {"text":"[demo] No core (Rebuild map).","color":"red"}
execute at @e[type=marker,tag=nx.acore,limit=1] run tp @s ~2 ~-1.5 ~ facing ~ ~ ~
