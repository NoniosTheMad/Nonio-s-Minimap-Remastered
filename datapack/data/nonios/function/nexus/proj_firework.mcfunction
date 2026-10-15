# as a firework rocket that hit: (5 + 2 per star) x10 x 20%; nothing without stars (like vanilla)
execute store result score #ad nx.tmp run data get entity @s FireworksItem.components."minecraft:fireworks".explosions
execute if score #ad nx.tmp matches 0 run return 0
scoreboard players operation #ad nx.tmp *= #2 nx.const
scoreboard players add #ad nx.tmp 5
scoreboard players operation #ad nx.tmp *= #2 nx.const
execute at @s run particle minecraft:firework ~ ~ ~ 0.3 0.3 0.3 0.1 20
