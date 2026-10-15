# axe put away: fury off
execute unless entity @s[tag=nx.cls_rage] run return 0
tag @s remove nx.cls_rage
effect clear @s minecraft:resistance
effect clear @s minecraft:strength
scoreboard players set @s nx.cls_blvl 0
