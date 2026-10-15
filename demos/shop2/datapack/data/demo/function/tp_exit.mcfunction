# into the active exit (open in battle: it sends you back to your gate at once)
execute unless entity @e[type=marker,tag=nx.aslot_on] run return run tellraw @s {"text":"[demo] No active slot (Rebuild map).","color":"red"}
execute at @e[type=marker,tag=nx.aslot_on,limit=1] run tp @s ~ ~ ~
