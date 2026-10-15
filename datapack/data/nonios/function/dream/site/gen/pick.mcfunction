# generated: as the new site marker, #tier (1 minor 2 major 3 grand 4 nightmare) and #pick (0..) set.
# Tries the tier's templates in turn from #pick until one fits (#res 1) or needs loaded chunks (#res 3).
scoreboard players set #res nx.dream 2
scoreboard players set #n nx.dream 3
execute if score #tier nx.dream matches 1 run scoreboard players operation #pick nx.dream %= #n nx.dream
execute if score #tier nx.dream matches 1 if score #pick nx.dream matches 0 run return run function nonios:dream/site/gen/order_minor_0
execute if score #tier nx.dream matches 1 if score #pick nx.dream matches 1 run return run function nonios:dream/site/gen/order_minor_1
execute if score #tier nx.dream matches 1 if score #pick nx.dream matches 2 run return run function nonios:dream/site/gen/order_minor_2
scoreboard players set #n nx.dream 2
execute if score #tier nx.dream matches 2 run scoreboard players operation #pick nx.dream %= #n nx.dream
execute if score #tier nx.dream matches 2 if score #pick nx.dream matches 0 run return run function nonios:dream/site/gen/order_major_0
execute if score #tier nx.dream matches 2 if score #pick nx.dream matches 1 run return run function nonios:dream/site/gen/order_major_1
scoreboard players set #n nx.dream 1
execute if score #tier nx.dream matches 3 run scoreboard players operation #pick nx.dream %= #n nx.dream
execute if score #tier nx.dream matches 3 if score #pick nx.dream matches 0 run return run function nonios:dream/site/gen/order_grand_0
scoreboard players set #n nx.dream 1
execute if score #tier nx.dream matches 4 run scoreboard players operation #pick nx.dream %= #n nx.dream
execute if score #tier nx.dream matches 4 if score #pick nx.dream matches 0 run return run function nonios:dream/site/gen/order_nightmare_0
