# advancement nonios:game/dummy_killed (a player killed a test dummy): counts as a kill, may end the match
advancement revoke @s only nonios:game/dummy_killed
scoreboard players add @s nx.kills 1
# kill reward (victim profile: #dummy nx.streak / nx.tier)
execute if score #state nx.state matches 1..2 run function nonios:economy/kill/dummy
function nonios:game/win_check
