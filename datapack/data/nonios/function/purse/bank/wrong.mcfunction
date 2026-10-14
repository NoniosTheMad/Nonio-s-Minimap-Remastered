# enemy (or teamless) player on a team's bank pad: nothing happens, rate-limited explanation
execute unless function nonios:nexus/msg_gate run return 0
scoreboard players add @s nx.msg_t 40
title @s actionbar {"text":"This is the other team's bank","color":"red"}
function nonios:hud/hold
