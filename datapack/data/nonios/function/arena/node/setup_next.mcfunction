# Recursive: build the node at tmp.nodes[0] (defaults from config, then the node's own fields), then the rest.
execute unless data storage nonios:arena tmp.nodes[0] run return 0
data modify storage nonios:arena n set value {r:2,h:3,btxt:""}
data modify storage nonios:arena n.bonus set from storage nonios:arena config.bonus
data modify storage nonios:arena n.every set from storage nonios:arena config.payout_every
data modify storage nonios:arena n merge from storage nonios:arena tmp.nodes[0]
function nonios:arena/node/btxt with storage nonios:arena n
# rune: the node's own, else the one of its bonus (config.rune_of); label = "<glyph> <Name>" (bossbar, chat)
execute unless data storage nonios:arena n.rune run function nonios:arena/rune/of_bonus with storage nonios:arena n
function nonios:arena/rune/resolve with storage nonios:arena n
# zone box: x0 = x - r, z0 = z - r, dx = dz = 2r, dy = h - 1 (selector boxes span d + 1 blocks)
execute store result score #x nx.arena run data get storage nonios:arena n.x
execute store result score #z nx.arena run data get storage nonios:arena n.z
execute store result score #r nx.arena run data get storage nonios:arena n.r
execute store result score #h nx.arena run data get storage nonios:arena n.h
# ground outline half width e = r + 0.5; glyph centre gy = h + lift/10 above the floor
scoreboard players operation #e nx.arena = #r nx.arena
scoreboard players operation #e nx.arena *= #2 nx.arena
scoreboard players add #e nx.arena 1
execute store result storage nonios:arena n.e double 0.5 run scoreboard players get #e nx.arena
scoreboard players operation #gy nx.arena = #h nx.arena
scoreboard players operation #gy nx.arena *= #10 nx.arena
execute store result score #lift nx.arena run data get storage nonios:arena config.rune.lift
scoreboard players operation #gy nx.arena += #lift nx.arena
execute store result storage nonios:arena n.gy double 0.1 run scoreboard players get #gy nx.arena
scoreboard players operation #x nx.arena -= #r nx.arena
scoreboard players operation #z nx.arena -= #r nx.arena
execute store result storage nonios:arena n.x0 int 1 run scoreboard players get #x nx.arena
execute store result storage nonios:arena n.z0 int 1 run scoreboard players get #z nx.arena
scoreboard players operation #r nx.arena += #r nx.arena
execute store result storage nonios:arena n.dx int 1 run scoreboard players get #r nx.arena
scoreboard players remove #h nx.arena 1
execute store result storage nonios:arena n.dy int 1 run scoreboard players get #h nx.arena
function nonios:arena/node/spawn with storage nonios:arena n
data remove storage nonios:arena tmp.nodes[0]
function nonios:arena/node/setup_next
