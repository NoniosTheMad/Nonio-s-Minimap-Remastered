# as + at the clicked interaction: only act if it was this clicker
scoreboard players set #me nx.arena 0
execute on target if entity @s[tag=nx.cg_clicker] run scoreboard players set #me nx.arena 1
execute unless score #me nx.arena matches 1 run return fail
data remove entity @s interaction
execute as @e[type=marker,tag=nx.cgen,distance=..1,limit=1] at @s run function nonios:arena/cgen/collect
