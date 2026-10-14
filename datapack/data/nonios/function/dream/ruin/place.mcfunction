# at a ruin marker: a random ruin (arch 3 : shrine 2 : well 2), random rotation, its floor replacing the ground
execute store result score #r nx.dream run random value 0..6
data modify storage nonios:dream ruin.t set value "arch"
execute if score #r nx.dream matches 3..4 run data modify storage nonios:dream ruin.t set value "shrine"
execute if score #r nx.dream matches 5..6 run data modify storage nonios:dream ruin.t set value "well"
execute store result score #r nx.dream run random value 0..3
data modify storage nonios:dream ruin.rot set value "none"
execute if score #r nx.dream matches 1 run data modify storage nonios:dream ruin.rot set value "clockwise_90"
execute if score #r nx.dream matches 2 run data modify storage nonios:dream ruin.rot set value "180"
execute if score #r nx.dream matches 3 run data modify storage nonios:dream ruin.rot set value "counterclockwise_90"
function nonios:dream/ruin/put with storage nonios:dream ruin
