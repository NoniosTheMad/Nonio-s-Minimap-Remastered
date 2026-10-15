# reward of advancement nonios:generator/click (a player right-clicked a generator's interaction entity)
advancement revoke @s only nonios:generator/click
tag @s add nx.gen_clicker
execute as @e[type=interaction,tag=nx.gen_click,distance=..8] if data entity @s interaction at @s run function nonios:generator/click_check
tag @s remove nx.gen_clicker
