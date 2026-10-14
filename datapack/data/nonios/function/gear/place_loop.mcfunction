# #gn copies of the probe's item (count 1) into the player's inventory, #gs = preferred slot; no room left = dropped
execute if score #gn nx.tmp matches ..0 run return 0
execute unless function nonios:gear/place_one run function nonios:gear/drop
scoreboard players remove #gn nx.tmp 1
function nonios:gear/place_loop
