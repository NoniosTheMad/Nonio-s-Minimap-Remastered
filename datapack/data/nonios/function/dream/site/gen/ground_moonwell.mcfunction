# at the first air block above the ground at the site point
execute if entity @s[y=0,dy=23] run return run scoreboard players set #res nx.dream 2
execute if block ~-4 ~-1 ~-4 #nonios:dream_passable if block ~-4 ~-2 ~-4 #nonios:dream_passable if block ~-4 ~-3 ~-4 #nonios:dream_passable if block ~-4 ~-4 ~-4 #nonios:dream_passable run return run scoreboard players set #res nx.dream 2
execute if block ~-4 ~-1 ~4 #nonios:dream_passable if block ~-4 ~-2 ~4 #nonios:dream_passable if block ~-4 ~-3 ~4 #nonios:dream_passable if block ~-4 ~-4 ~4 #nonios:dream_passable run return run scoreboard players set #res nx.dream 2
execute if block ~4 ~-1 ~-4 #nonios:dream_passable if block ~4 ~-2 ~-4 #nonios:dream_passable if block ~4 ~-3 ~-4 #nonios:dream_passable if block ~4 ~-4 ~-4 #nonios:dream_passable run return run scoreboard players set #res nx.dream 2
execute if block ~4 ~-1 ~4 #nonios:dream_passable if block ~4 ~-2 ~4 #nonios:dream_passable if block ~4 ~-3 ~4 #nonios:dream_passable if block ~4 ~-4 ~4 #nonios:dream_passable run return run scoreboard players set #res nx.dream 2
function nonios:dream/site/gen/place_moonwell
scoreboard players set #res nx.dream 1
