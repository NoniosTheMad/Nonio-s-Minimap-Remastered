# onto my team's gate pad (open in battle: it sends you in at once)
execute unless entity @e[type=marker,tag=nx.agate] run return run tellraw @s {"text":"[demo] No gates (Rebuild map).","color":"red"}
execute if entity @s[team=black] at @e[type=marker,tag=nx.agate,tag=nx.black,limit=1] run return run tp @s ~ ~ ~
execute at @e[type=marker,tag=nx.agate,tag=nx.white,limit=1] run tp @s ~ ~ ~
