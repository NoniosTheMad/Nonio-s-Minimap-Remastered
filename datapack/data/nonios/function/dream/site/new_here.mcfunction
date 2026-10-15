execute store result score #pick nx.dream run random value 0..999
setblock ~ ~ ~ minecraft:air
function nonios:dream/site/new
execute if score #res nx.dream matches 2 run tellraw @s {"text":"no room for that site here (ground sites need an island, sky sites open air)","color":"gray"}
execute if score #res nx.dream matches 2 run setblock ~ ~ ~ minecraft:air
