# (generator/load, once per world: #single_v 2) the config default style (#109: single block), every generator regrows in it
scoreboard players set #single_v nx.gen 2
scoreboard players operation #single nx.gen = #single_def nx.gen
execute as @e[type=marker,tag=nx.gen] at @s run function nonios:generator/mode/regrow
