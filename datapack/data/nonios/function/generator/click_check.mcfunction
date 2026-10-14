# as + at an interaction entity that someone clicked: only act if it was this clicker
scoreboard players set #me nx.gen 0
execute on target if entity @s[tag=nx.gen_clicker] run scoreboard players set #me nx.gen 1
execute unless score #me nx.gen matches 1 run return fail
data remove entity @s interaction
execute positioned ~ ~1 ~ as @e[type=marker,tag=nx.gen,distance=..1,limit=1] at @s run function nonios:generator/ui/click
