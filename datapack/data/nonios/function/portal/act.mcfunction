# as + at a player who clicked "Open" (nx.portal_t). Re-checked here: match running, on a team, still on their own pad.
scoreboard players reset @s nx.portal_t
execute unless score #map nx.state matches 1 run return 0
execute unless score #state nx.state matches 1..2 run return 0
execute if entity @s[team=] run return 0
execute if entity @s[team=white] unless entity @e[type=marker,tag=nx.dream_pad,tag=nx.white,distance=..3] run return run title @s actionbar {"text":"Too far from the portal","color":"red"}
execute if entity @s[team=black] unless entity @e[type=marker,tag=nx.dream_pad,tag=nx.black,distance=..3] run return run title @s actionbar {"text":"Too far from the portal","color":"red"}
execute if entity @s[team=white] run return run function nonios:portal/unlock {team:"white",color:"white"}
function nonios:portal/unlock {team:"black",color:"light_purple"}
