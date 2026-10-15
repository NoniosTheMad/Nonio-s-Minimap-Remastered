# advancement nonios:class/champion_kill: a Champion killed a player (or a demo dummy tagged nx.soul)
advancement revoke @s only nonios:class/champion_kill
execute if score @s nx.cls_champ matches ..4 run scoreboard players add @s nx.cls_champ 1
function nonios:class/champion/level
effect give @s minecraft:instant_health 1 0 true
playsound minecraft:entity.player.levelup player @a[distance=..32] ~ ~ ~ 1 0.6
particle minecraft:wax_on ~ ~1.2 ~ 0.4 0.6 0.4 0 25
title @s actionbar [{"text":"⚔ ","color":"gold"},{"score":{"name":"@s","objective":"nx.cls_champ"},"color":"yellow"}]
execute if score @s nx.cls_champ matches 3 run tellraw @a [{"selector":"@s","color":"yellow"},{"text":" ⚔ 3","color":"gold"}]
execute if score @s nx.cls_champ matches 5 run tellraw @a [{"selector":"@s","color":"yellow"},{"text":" ⚔ 5","color":"gold"}]
