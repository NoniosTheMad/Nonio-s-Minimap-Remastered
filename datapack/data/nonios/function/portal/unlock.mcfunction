# as + at a player on their own pad; macro {team,color}: pay dream_cost from the purse, open the team's portal, enter
$execute if score #$(team) nx.portal matches 1 run return run function nonios:dream/try_enter
execute store result score #cost nx.portal run data get storage nonios:config dream_cost
scoreboard players add @s nx.coins 0
execute if score @s nx.coins < #cost nx.portal run return run title @s actionbar [{"text":"Not enough coins (","color":"red"},{"score":{"name":"#cost","objective":"nx.portal"},"color":"gold"},{"text":")","color":"red"}]
scoreboard players operation @s nx.coins -= #cost nx.portal
$scoreboard players set #$(team) nx.portal 1
$tellraw @a[team=$(team)] [{"selector":"@s","color":"$(color)"},{"text":" opened the Emerald Dream","color":"green"}]
$execute as @a[team=$(team)] at @s run playsound minecraft:block.end_portal.spawn master @s ~ ~ ~ 0.5 1.4
function nonios:portal/labels
function nonios:dream/try_enter
