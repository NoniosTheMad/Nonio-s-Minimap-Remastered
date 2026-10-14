execute unless data storage nonios:arena tmp.evs[0] run return 0
execute store result score #wgt nx.arena run data get storage nonios:arena tmp.evs[0].weight
scoreboard players operation #wsum nx.arena += #wgt nx.arena
data remove storage nonios:arena tmp.evs[0]
function nonios:arena/event/sum_next
