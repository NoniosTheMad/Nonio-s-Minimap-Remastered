# free Emerald Dream unlock for my team (no coins)
execute if entity @s[team=] run return run tellraw @s {"text":"[demo] Join a team first.","color":"red"}
execute if entity @s[team=white] run scoreboard players set #white nx.portal 1
execute if entity @s[team=black] run scoreboard players set #black nx.portal 1
function nonios:portal/labels
tellraw @s {"text":"[demo] Your team's Dream portal is open (free).","color":"yellow"}
