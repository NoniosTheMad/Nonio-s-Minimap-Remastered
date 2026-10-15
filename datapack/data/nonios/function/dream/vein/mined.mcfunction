scoreboard players operation @s nx.dvt = #now nx.dream
scoreboard players operation @s nx.dvt += #regrow_ticks nx.dream
particle minecraft:end_rod ~ ~-0.5 ~ 0.2 0.2 0.2 0.05 8
playsound minecraft:block.amethyst_cluster.break block @a ~ ~ ~ 0.8 0.7
# user #80: each break may spread the deposit into a neighbouring plain block (capped per deposit)
execute store result score #r nx.dream run random value 1..100
execute if score #r nx.dream <= #spread_pct nx.dream positioned ~ ~-1 ~ run function nonios:dream/vein/spread
