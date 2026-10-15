# at the cell point: try the next smaller tier
scoreboard players remove #tier nx.dream 1
execute as @e[type=marker,tag=nx.dream_site_new,limit=1] run function nonios:dream/site/gen/pick
