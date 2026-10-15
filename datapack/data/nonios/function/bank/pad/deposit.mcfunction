# {team, Team, color, enemy}: as/at the depositor on their own pad: purse -> team bank, then the cues
# (depositor: subtitle + sounds + particles; team: chat line + chime; enemy team: actionbar + bell, like a goal scored)
scoreboard players add @s nx.coins 0
execute if score @s nx.coins matches ..0 run return 0
scoreboard players operation #amt nx.eco = @s nx.coins
scoreboard players set @s nx.coins 0
$scoreboard players add #$(team) nx.bank 0
$scoreboard players operation #$(team) nx.bank += #amt nx.eco
$scoreboard players operation #b nx.eco = #$(team) nx.bank
# depositor
title @s times 2 24 8
title @s title ""
title @s subtitle [{"text":"+","color":"gold"},{"score":{"name":"#amt","objective":"nx.eco"},"color":"gold","bold":true},{"text":"  ⇒  bank ","color":"gray"},{"score":{"name":"#b","objective":"nx.eco"},"color":"yellow"}]
playsound minecraft:block.vault.insert_item player @s ~ ~ ~ 1 1
playsound minecraft:entity.player.levelup player @s ~ ~ ~ 0.5 1.6
particle minecraft:totem_of_undying ~ ~1 ~ 0.4 0.6 0.4 0.4 30 normal @a
particle minecraft:wax_on ~ ~0.2 ~ 1 0.1 1 0 20 normal @a
# team
tag @s add nx.bk.me
$tellraw @a[team=$(team),tag=!nx.bk.me] [{"text":"🏦 ","color":"gold"},{"selector":"@s"},{"text":" banked ","color":"gray"},{"text":"+","color":"gold"},{"score":{"name":"#amt","objective":"nx.eco"},"color":"gold"},{"text":"  bank ","color":"gray"},{"score":{"name":"#b","objective":"nx.eco"},"color":"yellow"}]
$execute as @a[team=$(team),tag=!nx.bk.me] at @s run playsound minecraft:block.note_block.chime player @s ~ ~ ~ 0.8 1.4
tag @s remove nx.bk.me
# enemy team
$title @a[team=$(enemy)] actionbar [{"text":"$(Team)","color":"$(color)","bold":true},{"text":" banked ","color":"gray"},{"score":{"name":"#amt","objective":"nx.eco"},"color":"gold"}]
$execute as @a[team=$(enemy)] at @s run playsound minecraft:block.bell.use player @s ~ ~ ~ 0.8 0.7
