# as a player entering the running match on team $(team) (match start, late join, demo team switch)
tag @s remove nx.spectator
gamemode survival @s
$function nonios:game/tp_spawn with storage nonios:map $(team).spawn
# already playing this match (demo team switch): keep gear, coins and stats
execute if score @s nx.match = #match nx.state run return 0
scoreboard players operation @s nx.match = #match nx.state
clear @s
effect clear @s
effect give @s minecraft:instant_health 1 10 true
effect give @s minecraft:saturation 1 10 true
execute store result score @s nx.coins run data get storage nonios:config start_coins
scoreboard players set @s nx.plast -1
scoreboard players set @s nx.kills 0
scoreboard players set @s nx.deaths 0
scoreboard players set @s nx.mined 0
scoreboard players set @s nx.nxdmg 0
scoreboard players set @s nx.nxkill 0
scoreboard players set @s nx.mn.obsidian 0
function #nonios:kit/start
