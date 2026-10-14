# #nonios:dream/on_exit (as the player, before the way back is read). The saved spot is void once the match is over,
# another one started or the player changed team: forget it, so portal/fallback sends them to their team spawn (or the lobby).
# Also: no pad prompt if they land back on the frame (until they step off).
execute unless score #map nx.state matches 1 run return 0
tag @s add nx.on_pad
scoreboard players set #ok nx.portal 1
execute unless score #state nx.state matches 1..3 run scoreboard players set #ok nx.portal 0
execute unless score @s nx.dmatch = #match nx.state run scoreboard players set #ok nx.portal 0
execute if entity @s[team=] run scoreboard players set #ok nx.portal 0
execute if entity @s[team=white] unless score @s nx.dteam matches 1 run scoreboard players set #ok nx.portal 0
execute if entity @s[team=black] unless score @s nx.dteam matches 2 run scoreboard players set #ok nx.portal 0
execute if score #ok nx.portal matches 1 run return 0
function nonios:dream/pid
execute store result storage nonios:dream tmp.id int 1 run scoreboard players get @s nx.pid
function nonios:dream/exit/forget with storage nonios:dream tmp
