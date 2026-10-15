# axe put away: fury off (Rage itself stays and cools: berserker/cool)
execute unless entity @s[tag=nx.cls_rage] run return 0
tag @s remove nx.cls_rage
effect clear @s minecraft:resistance
attribute @s minecraft:attack_damage modifier remove nonios:berserk_fury
attribute @s minecraft:attack_speed modifier remove nonios:berserk_haste
scoreboard players set @s nx.cls_blvl 0
