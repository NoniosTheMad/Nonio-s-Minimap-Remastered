# as a player in the active exit: out at their team's gate (no team, or no gate of theirs: the first gate)
data modify storage nonios:arena go set from entity @e[type=marker,tag=nx.agate,limit=1] data.out
execute if entity @s[team=white] if entity @e[type=marker,tag=nx.agate,tag=nx.white] run data modify storage nonios:arena go set from entity @e[type=marker,tag=nx.agate,tag=nx.white,limit=1] data.out
execute if entity @s[team=black] if entity @e[type=marker,tag=nx.agate,tag=nx.black] run data modify storage nonios:arena go set from entity @e[type=marker,tag=nx.agate,tag=nx.black,limit=1] data.out
function nonios:arena/gate/go with storage nonios:arena go
execute at @s run playsound minecraft:entity.enderman.teleport player @s ~ ~ ~ 0.8 1
scoreboard players add #g_out nx.arena 1
