# at the first air block above the ground at the site point
execute if entity @s[y=0,dy=23] run return run scoreboard players set #res nx.dream 2
execute if block ~-12 ~-1 ~-12 #nonios:dream_passable if block ~-12 ~-2 ~-12 #nonios:dream_passable if block ~-12 ~-3 ~-12 #nonios:dream_passable if block ~-12 ~-4 ~-12 #nonios:dream_passable run return run scoreboard players set #res nx.dream 2
execute if block ~-12 ~-1 ~12 #nonios:dream_passable if block ~-12 ~-2 ~12 #nonios:dream_passable if block ~-12 ~-3 ~12 #nonios:dream_passable if block ~-12 ~-4 ~12 #nonios:dream_passable run return run scoreboard players set #res nx.dream 2
execute if block ~12 ~-1 ~-12 #nonios:dream_passable if block ~12 ~-2 ~-12 #nonios:dream_passable if block ~12 ~-3 ~-12 #nonios:dream_passable if block ~12 ~-4 ~-12 #nonios:dream_passable run return run scoreboard players set #res nx.dream 2
execute if block ~12 ~-1 ~12 #nonios:dream_passable if block ~12 ~-2 ~12 #nonios:dream_passable if block ~12 ~-3 ~12 #nonios:dream_passable if block ~12 ~-4 ~12 #nonios:dream_passable run return run scoreboard players set #res nx.dream 2
function nonios:dream/site/gen/place_crystal_grotto
scoreboard players set #res nx.dream 1
