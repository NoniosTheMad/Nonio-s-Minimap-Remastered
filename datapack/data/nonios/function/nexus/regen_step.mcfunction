scoreboard players add @s nx.hp 1
scoreboard players operation @s nx.regen -= #regen_unit nx.const
execute if score @s nx.hp >= @s nx.hp_max run return run scoreboard players operation @s nx.hp = @s nx.hp_max
execute if score @s nx.regen >= #regen_unit nx.const run function nonios:nexus/regen_step
