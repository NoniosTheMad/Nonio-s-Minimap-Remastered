execute unless data storage nonios:arena tmp.cbl[0] run return 0
execute store result score #wgt nx.arena run data get storage nonios:arena tmp.cbl[0].w
scoreboard players operation #cwsum nx.arena += #wgt nx.arena
data remove storage nonios:arena tmp.cbl[0]
function nonios:arena/core/sum_next
