# The charged scythe was used (0.5 s wind-up, 8 s cooldown): release the souls. 2 + 2 per soul magic damage + wither
# within 6 blocks; teammates are spared. Released souls that kill count as Reaper kills, so a good burst refills itself.
execute unless score @s nx.cls_souls matches 1.. run return run function nonios:class/reaper/no_souls
scoreboard players operation #dmg nx.cls_tmp = @s nx.cls_souls
scoreboard players operation #dmg nx.cls_tmp += @s nx.cls_souls
scoreboard players add #dmg nx.cls_tmp 2
execute store result storage nonios:class tmp.dmg int 1 run scoreboard players get #dmg nx.cls_tmp
tag @s add nx.cls_me
execute if entity @s[team=white] run tag @e[type=player,team=white] add nx.cls_ally
execute if entity @s[team=black] run tag @e[type=player,team=black] add nx.cls_ally
scoreboard players set @s nx.cls_souls 0
function nonios:class/reaper/burst with storage nonios:class tmp
tag @e[tag=nx.cls_ally] remove nx.cls_ally
tag @s remove nx.cls_me
particle minecraft:sculk_soul ~ ~1 ~ 3 1 3 0.05 120
particle minecraft:sonic_boom ~ ~1 ~ 0 0 0 0 1
playsound minecraft:entity.warden.sonic_boom player @a ~ ~ ~ 1.2 1.3
title @s actionbar [{"text":"☠ souls released: ","color":"dark_purple"},{"score":{"name":"#dmg","objective":"nx.cls_tmp"},"color":"light_purple"},{"text":" damage","color":"dark_purple"}]
