execute unless data storage nonios:arena tmp.evs[0] run return 0
execute store result score #wgt nx.arena run data get storage nonios:arena tmp.evs[0].weight
scoreboard players operation #r nx.arena -= #wgt nx.arena
execute if score #r nx.arena matches ..0 run return run function nonios:arena/event/fire
data remove storage nonios:arena tmp.evs[0]
function nonios:arena/event/pick_next
