# as a player: pay the next level's cost (#cost<N>, the V2 prices) and upgrade the nearest generator (8 blocks)
tag @s add nx.gen_buyer
execute unless entity @e[type=marker,tag=nx.gen,distance=..8] run tellraw @s {text:"No generator within 8 blocks.",color:"red"}
execute as @e[type=marker,tag=nx.gen,distance=..8,sort=nearest,limit=1] at @s run function nonios:generator/buy_m
tag @s remove nx.gen_buyer
