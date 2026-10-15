# as a gliding dreamer who just pressed jump
execute if score @s nx.dchg < #wing_cost nx.dream run return run function nonios:dream/wings/empty
scoreboard players operation @s nx.dchg -= #wing_cost nx.dream
scoreboard players operation @s nx.dboost = #wing_ticks nx.dream
playsound minecraft:entity.firework_rocket.launch player @a ~ ~ ~ 0.9 1.3
playsound minecraft:block.amethyst_block.resonate player @a ~ ~ ~ 0.5 1.8
particle minecraft:end_rod ~ ~0.6 ~ 0.2 0.2 0.2 0.08 12
function nonios:dream/wings/hud
