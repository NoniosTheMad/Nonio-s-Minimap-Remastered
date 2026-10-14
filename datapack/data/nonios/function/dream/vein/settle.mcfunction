# keep a new vein only on real ground near the lander and not on top of another vein; then grow its ore
execute unless block ~ ~-1 ~ #nonios:dream_vein_host run return run kill @s
execute unless entity @e[tag=nx.dream_lander,distance=..40] run return run kill @s
execute if entity @e[type=marker,tag=nx.dream_vein,tag=!nx.dream_vnew,distance=..1.5] run return run kill @s
tag @s remove nx.dream_vnew
execute align xyz run tp @s ~0.5 ~ ~0.5
scoreboard players operation @s nx.dvs = #now nx.dream
execute at @s run function nonios:dream/vein/grow
