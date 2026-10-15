# Every tick (nonios:tick): each node's rune, ground outline and smooth capture bar (feedback #126).
# Runs while the arena is stopped too (the rune is the node's identity); the bar only moves while it runs.
# #ph = ticks since the last capture check (arena/loop resets it), #gt = game time.
scoreboard players add #ph nx.arena 1
execute store result score #gt nx.arena run time query gametime
execute as @e[type=marker,tag=nx.node] at @s run function nonios:arena/rune/node
