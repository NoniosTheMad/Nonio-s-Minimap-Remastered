# no ground remembered (fell right after arriving): pick a new arrival point
tag @s add nx.dream_arriving
scoreboard players set @s nx.dtry 0
scoreboard players set @s nx.drol 0
effect give @s minecraft:blindness 3 0 true
function nonios:dream/arrive/roll
