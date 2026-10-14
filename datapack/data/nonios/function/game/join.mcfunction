# as a player who joined (first time or reconnect)
tag @s add nx.seen
scoreboard players reset @s nx.left
execute if score #state nx.state matches 0 run return run function nonios:game/join_lobby
execute if score #state nx.state matches 3 run return run function nonios:game/lobby_player
# match running: same match + still on a team = carry on where they were
execute if score @s nx.match = #match nx.state if entity @s[team=!] run return 0
# newcomer: watch as a spectator until they pick a team
team leave @s
function nonios:game/spectate
tellraw @s [{"text":"A match is running. ","color":"gold"},{"text":"[Join a team]","color":"green","bold":true,"click_event":{"action":"run_command","command":"/trigger nx.team set 1"}}]
