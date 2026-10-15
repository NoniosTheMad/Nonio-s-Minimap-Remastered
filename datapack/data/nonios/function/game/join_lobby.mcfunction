function nonios:game/lobby_player
title @s times 10 50 15
title @s subtitle {"text":"Lobby","color":"gray"}
title @s title {"text":"Nonios's Map","color":"gold","bold":true}
tellraw @s [{"text":"Lobby. ","color":"gold"},{"text":"[Choose team]","color":"green","bold":true,"click_event":{"action":"run_command","command":"/trigger nx.team set 1"}}]
