# Start a match from the lobby (admin dialog / demo). Messages go to @s (the admin) when there is one.
execute unless score #state nx.state matches 0 run return run tellraw @s {"text":"A match is already running (Stop it first).","color":"red"}
execute unless score #map nx.state matches 1 run return run tellraw @s {"text":"No map yet: Rebuild map first.","color":"red"}
function nonios:team/balance
execute unless entity @a[team=!] run return run tellraw @s {"text":"Nobody is on a team.","color":"red"}
execute if score #dirty nx.state matches 1 run function nonios:map/build
scoreboard players set #dirty nx.state 1
scoreboard players add #match nx.state 1
function nonios:game/apply_config
# per-match resets
scoreboard players set #white nx.last 0
scoreboard players set #black nx.last 0
scoreboard players set #white nx.bank 0
scoreboard players set #black nx.bank 0
function nonios:economy/match_start
kill @e[type=item,tag=nx.coinbag]
kill @e[type=husk,tag=nx.dummy]
function nonios:nexus/spawn with storage nonios:map white.nexus
function nonios:nexus/spawn with storage nonios:map black.nexus
function nonios:map/walls/up
execute as @a[team=white] run function nonios:game/enter {team:"white"}
execute as @a[team=black] run function nonios:game/enter {team:"black"}
execute as @a[team=] run function nonios:game/spectate
# phase: preparation
scoreboard players set #state nx.state 1
execute store result score #timer nx.state run data get storage nonios:config prep_time 20
execute store result bossbar nonios:phase max run data get storage nonios:config prep_time
bossbar set nonios:phase color yellow
bossbar set nonios:phase visible true
title @a times 10 60 20
title @a subtitle {"text":"Mine, build, buy. The walls drop when the timer ends.","color":"gray"}
title @a title {"text":"PREPARATION","color":"yellow","bold":true}
execute as @a at @s run playsound minecraft:block.beacon.activate master @s ~ ~ ~ 1 1
tellraw @a [{"text":"Match #","color":"gold"},{"score":{"name":"#match","objective":"nx.state"},"color":"gold"},{"text":" started. Shop: the villager at your base. Bank: the vault on the gold pad (right-click). Coins: mine ores.","color":"gold"}]
execute if score #timer nx.state matches ..0 run return run function nonios:game/battle/start
function nonios:game/prep/second
