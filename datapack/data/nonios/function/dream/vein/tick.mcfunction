# as a vein marker, at it, every 5 ticks
execute if entity @a[distance=..64] run scoreboard players operation @s nx.dvs = #now nx.dream
scoreboard players operation #age nx.dream = #now nx.dream
scoreboard players operation #age nx.dream -= @s nx.dvs
execute if score #age nx.dream > #ttl nx.dream run return run kill @s
# intact: sparkle now and then
execute if block ~ ~-1 ~ #nonios:dream_vein_ore run return run function nonios:dream/vein/idle
# just mined: start the regrow timer
execute if score @s nx.dvt matches 0 run return run function nonios:dream/vein/mined
# still regrowing
execute if score #now nx.dream < @s nx.dvt run return run function nonios:dream/vein/wait
# due: only into air/plants, and never inside a player
execute unless block ~ ~-1 ~ #nonios:dream_regrow_into run return 0
execute positioned ~-0.5 ~-1 ~-0.5 if entity @a[dx=0,dy=0,dz=0] run return 0
function nonios:dream/vein/grow
