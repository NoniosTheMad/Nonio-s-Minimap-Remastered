execute at @e[type=rabbit,tag=nx.lrabbit] run summon minecraft:lightning_bolt ~ ~ ~
scoreboard players operation #lt_t nx.arena += #lt_every nx.arena
execute if score #lt_t nx.arena matches ..0 run scoreboard players operation #lt_t nx.arena = #lt_every nx.arena
scoreboard players add #bolts nx.arena 1
