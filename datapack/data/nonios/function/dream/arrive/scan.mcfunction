# walk down the column (as the arriving player) until something solid; gives up below #land_min_y
scoreboard players remove #sy nx.dream 1
execute if score #sy nx.dream < #land_min_y nx.dream run return run function nonios:dream/arrive/reroll
execute if block ~ ~ ~ #nonios:dream_passable positioned ~ ~-1 ~ run return run function nonios:dream/arrive/scan
execute if block ~ ~ ~ #nonios:dream_landing run return run function nonios:dream/arrive/found
function nonios:dream/arrive/reroll
