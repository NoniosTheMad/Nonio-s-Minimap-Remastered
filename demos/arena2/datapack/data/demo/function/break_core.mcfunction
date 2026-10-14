# empty the core as if mined (no drop); during battle it regrows within half a second
execute unless entity @e[type=marker,tag=nx.acore] run return run tellraw @s {"text":"[demo] No core (Rebuild map).","color":"red"}
execute at @e[type=marker,tag=nx.acore,limit=1] run setblock ~ ~ ~ minecraft:air
execute unless score #on nx.arena matches 1 run return run tellraw @s {"text":"[demo] Core emptied. The arena is paused (not battle): it stays empty until the battle.","color":"yellow"}
tellraw @s {"text":"[demo] Core emptied: watch it regrow.","color":"yellow"}
