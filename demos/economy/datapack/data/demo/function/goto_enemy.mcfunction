# teleport next to the other team's bank vault (it should refuse you)
execute if entity @s[team=] run return run tellraw @s {"text":"[demo] Join a team first (Start match does it for you).","color":"red"}
execute if entity @s[team=white] run return run function demo:tp_bank with storage nonios:map black.bank
function demo:tp_bank with storage nonios:map white.bank
