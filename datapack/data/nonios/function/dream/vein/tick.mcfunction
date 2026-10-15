# as a vein marker, at it, every 5 ticks (veins belong to exploration sites; markers only tick while their chunk is loaded)
# v1/v2 veins (planted around arrival points) are gone in v3: only site deposits regrow
execute unless entity @s[tag=nx.dv3] run return run kill @s
# intact: sparkle now and then
execute if block ~ ~-1 ~ #nonios:dream_vein_ore run return run function nonios:dream/vein/idle
# just mined: start the regrow timer (and maybe spread)
execute if score @s nx.dvt matches 0 run return run function nonios:dream/vein/mined
# still regrowing
execute if score #now nx.dream < @s nx.dvt run return run function nonios:dream/vein/wait
# due: only into air/plants, and never inside a player
execute unless block ~ ~-1 ~ #nonios:dream_regrow_into run return 0
execute positioned ~-0.5 ~-1 ~-0.5 if entity @a[dx=0,dy=0,dz=0] run return 0
function nonios:dream/vein/grow
