scoreboard players add #now nx.dream 1
scoreboard players operation #t nx.dream = #now nx.dream
scoreboard players operation #t nx.dream %= #5 nx.dream
scoreboard players operation #t10 nx.dream = #now nx.dream
scoreboard players operation #t10 nx.dream %= #10 nx.dream
scoreboard players operation #t20 nx.dream = #now nx.dream
scoreboard players operation #t20 nx.dream %= #20 nx.dream
execute as @a[tag=nx.dream_arriving] at @s run function nonios:dream/arrive/tick
execute in nonios:emerald_dream as @a[distance=0..,tag=!nx.dream_arriving] at @s run function nonios:dream/exit/tick
execute in nonios:emerald_dream as @a[distance=0..,tag=nx.in_dream,tag=!nx.dream_arriving] at @s run function nonios:dream/player
execute in nonios:emerald_dream run scoreboard players reset @a[distance=0..] nx.dhit
execute in nonios:emerald_dream run scoreboard players reset @a[distance=0..] nx.dabs
# left the dream some other way (death, admin tp): forget their way back
execute as @a[tag=nx.in_dream,tag=!nx.dream_arriving] at @s unless dimension nonios:emerald_dream run function nonios:dream/exit/lost
# veins every 5 ticks
execute if score #t nx.dream matches 0 in nonios:emerald_dream as @e[type=marker,tag=nx.dream_vein,distance=0..] at @s run function nonios:dream/vein/tick
# Dream gifts never leave the Dream
execute if score #t10 nx.dream matches 0 run function nonios:dream/wings/scan
execute if score #t20 nx.dream matches 0 in nonios:emerald_dream positioned 0 64 0 run function nonios:dream/second
