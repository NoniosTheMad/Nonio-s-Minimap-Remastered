# pick a random column in [-range, range]^2 and hold @s high above it while the chunk generates
scoreboard players operation #span nx.dream = #range nx.dream
scoreboard players operation #span nx.dream *= #2 nx.dream
scoreboard players add #span nx.dream 1
execute store result score #rx nx.dream run random value 0..2000000000
scoreboard players operation #rx nx.dream %= #span nx.dream
scoreboard players operation #rx nx.dream -= #range nx.dream
execute store result score #rz nx.dream run random value 0..2000000000
scoreboard players operation #rz nx.dream %= #span nx.dream
scoreboard players operation #rz nx.dream -= #range nx.dream
execute store result storage nonios:dream roll.x int 1 run scoreboard players get #rx nx.dream
execute store result storage nonios:dream roll.z int 1 run scoreboard players get #rz nx.dream
function nonios:dream/arrive/goto with storage nonios:dream roll
