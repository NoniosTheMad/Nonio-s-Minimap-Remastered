# at (site x, 0, site z), not decided yet. #tr (0..99) picks the tier: #p_none / #p_minor / #p_major / #p_grand, rest nightmare
scoreboard players set #tier nx.dream 0
scoreboard players operation #c nx.dream = #p_none nx.dream
execute if score #tr nx.dream >= #c nx.dream run scoreboard players set #tier nx.dream 1
scoreboard players operation #c nx.dream += #p_minor nx.dream
execute if score #tr nx.dream >= #c nx.dream run scoreboard players set #tier nx.dream 2
scoreboard players operation #c nx.dream += #p_major nx.dream
execute if score #tr nx.dream >= #c nx.dream run scoreboard players set #tier nx.dream 3
scoreboard players operation #c nx.dream += #p_grand nx.dream
execute if score #tr nx.dream >= #c nx.dream run scoreboard players set #tier nx.dream 4
# one nightmare per world: later ones become grand sites
execute if score #tier nx.dream matches 4 if score #nightmare nx.dream matches 1.. run scoreboard players set #tier nx.dream 3
execute if score #force_tier nx.dream matches 1..4 run scoreboard players operation #tier nx.dream = #force_tier nx.dream
scoreboard players reset #force_tier nx.dream
execute if score #tier nx.dream matches 0 run return run setblock ~ ~ ~ minecraft:barrier
summon minecraft:marker ~ 250 ~ {Tags:["nx.dream","nx.dream_site_new"]}
execute as @e[type=marker,tag=nx.dream_site_new,limit=1] run function nonios:dream/site/gen/pick
# a grand or major site that finds no room here falls back to the tier below (the nightmare waits for another cell)
execute if score #res nx.dream matches 2 if score #tier nx.dream matches 3 run function nonios:dream/site/down
execute if score #res nx.dream matches 2 if score #tier nx.dream matches 2 run function nonios:dream/site/down
execute if score #res nx.dream matches 1..2 run setblock ~ ~ ~ minecraft:barrier
kill @e[type=marker,tag=nx.dream_site_new]
