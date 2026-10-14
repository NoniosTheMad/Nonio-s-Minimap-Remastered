# reward of advancement nonios:arena/cgen_click (a player right-clicked the centre generator)
advancement revoke @s only nonios:arena/cgen_click
tag @s add nx.cg_clicker
execute as @e[type=interaction,tag=nx.cgen_click,distance=..8] if data entity @s interaction at @s run function nonios:arena/cgen/click_check
tag @s remove nx.cg_clicker
