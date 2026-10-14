# Recursive: build the node at tmp.nodes[0] (defaults from config, then the node's own fields), then the rest.
execute unless data storage nonios:arena tmp.nodes[0] run return 0
data modify storage nonios:arena n set value {r:2,h:3}
data modify storage nonios:arena n.loot set from storage nonios:arena config.loot
data modify storage nonios:arena n.every set from storage nonios:arena config.payout_every
data modify storage nonios:arena n.coins set from storage nonios:arena config.coins
data modify storage nonios:arena n.ind set from storage nonios:arena config.indicator_dy
data modify storage nonios:arena n merge from storage nonios:arena tmp.nodes[0]
# zone box: x0 = x - r, z0 = z - r, dx = dz = 2r, dy = h - 1 (selector boxes span d + 1 blocks); hologram at y + h
execute store result score #x nx.arena run data get storage nonios:arena n.x
execute store result score #z nx.arena run data get storage nonios:arena n.z
execute store result score #r nx.arena run data get storage nonios:arena n.r
execute store result score #h nx.arena run data get storage nonios:arena n.h
scoreboard players operation #x nx.arena -= #r nx.arena
scoreboard players operation #z nx.arena -= #r nx.arena
execute store result storage nonios:arena n.x0 int 1 run scoreboard players get #x nx.arena
execute store result storage nonios:arena n.z0 int 1 run scoreboard players get #z nx.arena
execute store result storage nonios:arena n.hy int 1 run scoreboard players get #h nx.arena
scoreboard players operation #r nx.arena += #r nx.arena
execute store result storage nonios:arena n.dx int 1 run scoreboard players get #r nx.arena
scoreboard players remove #h nx.arena 1
execute store result storage nonios:arena n.dy int 1 run scoreboard players get #h nx.arena
function nonios:arena/node/spawn with storage nonios:arena n
data remove storage nonios:arena tmp.nodes[0]
function nonios:arena/node/setup_next
