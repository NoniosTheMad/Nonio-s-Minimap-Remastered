# #nonios:dream/gate (as the player): in the match, only a team that opened its portal may enter, and only in prep/battle
execute unless score #map nx.state matches 1 run return 0
execute unless score #state nx.state matches 1..2 run return run scoreboard players set #deny nx.dream 1
execute if entity @s[team=white] if score #white nx.portal matches 1 run return 0
execute if entity @s[team=black] if score #black nx.portal matches 1 run return 0
scoreboard players set #deny nx.dream 1
