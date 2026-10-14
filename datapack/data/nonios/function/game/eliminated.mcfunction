# last life used up: spectator for the rest of the match
gamemode spectator @s
title @s times 10 60 20
title @s subtitle {"text":"Your Nexus is gone: no respawns. Spectating.","color":"gray"}
title @s title {"text":"ELIMINATED","color":"dark_red","bold":true}
tellraw @a [{"selector":"@s"},{"text":" is out (no Nexus, no respawn).","color":"red"}]
function nonios:game/win_check
