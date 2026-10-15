execute unless data storage nonios:arena tmp.cbl[0] run return 0
execute store result score #wgt nx.arena run data get storage nonios:arena tmp.cbl[0].w
scoreboard players operation #r nx.arena -= #wgt nx.arena
execute if score #r nx.arena matches ..0 run return run data modify storage nonios:arena core_pick set from storage nonios:arena tmp.cbl[0]
scoreboard players add #ci nx.arena 1
data remove storage nonios:arena tmp.cbl[0]
function nonios:arena/core/pick_next
