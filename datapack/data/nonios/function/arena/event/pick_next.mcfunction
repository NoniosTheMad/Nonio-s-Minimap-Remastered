execute unless data storage nonios:arena tmp.evs[0] run return 0
execute store result score #wgt nx.arena run data get storage nonios:arena tmp.evs[0].weight
execute if data storage nonios:arena tmp.evs[0]{troll:1b} unless score #trolls nx.arena matches 1 run scoreboard players set #wgt nx.arena 0
scoreboard players operation #r nx.arena -= #wgt nx.arena
execute if score #wgt nx.arena matches 1.. if score #r nx.arena matches ..0 run return run function nonios:arena/event/fire
data remove storage nonios:arena tmp.evs[0]
function nonios:arena/event/pick_next
