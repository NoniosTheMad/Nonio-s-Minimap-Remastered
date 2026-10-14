# as a player who died and has respawned (from nonios:death). Spawnpoint = team spawn, so they are already home.
execute unless score #state nx.state matches 1..2 run return 0
execute if entity @s[team=] run return 0
scoreboard players add @s nx.deaths 1
execute if entity @s[team=white] if score #white nx.last matches 1 run return run function nonios:game/eliminated
execute if entity @s[team=black] if score #black nx.last matches 1 run return run function nonios:game/eliminated
# respawn kit hook (classes plug in here): function tag #nonios:kit/respawn
function #nonios:kit/respawn
