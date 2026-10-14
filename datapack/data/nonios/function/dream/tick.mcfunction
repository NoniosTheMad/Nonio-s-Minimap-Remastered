scoreboard players add #now nx.dream 1
execute as @a[tag=nx.dream_arriving] at @s run function nonios:dream/arrive/tick
execute in nonios:emerald_dream as @a[distance=0..,tag=!nx.dream_arriving] at @s run function nonios:dream/exit/tick
execute in nonios:emerald_dream run scoreboard players reset @a[distance=0..] nx.dhit
execute in nonios:emerald_dream run scoreboard players reset @a[distance=0..] nx.dabs
# left the dream some other way (death, admin tp): forget their way back
execute as @a[tag=nx.in_dream,tag=!nx.dream_arriving] at @s unless dimension nonios:emerald_dream run function nonios:dream/exit/lost
# veins every 5 ticks
scoreboard players operation #t nx.dream = #now nx.dream
scoreboard players operation #t nx.dream %= #5 nx.dream
execute if score #t nx.dream matches 0 in nonios:emerald_dream as @e[type=marker,tag=nx.dream_vein,distance=0..] at @s run function nonios:dream/vein/tick
