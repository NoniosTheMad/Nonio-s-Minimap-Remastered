# as an arriving player, at them: wait for the chunk, then look for ground straight down
scoreboard players add @s nx.dtry 1
execute if score @s nx.dtry matches 400.. run return run function nonios:dream/arrive/fallback
execute unless dimension nonios:emerald_dream run return run function nonios:dream/arrive/roll
execute unless loaded ~ ~ ~ run return run tp @s ~ 250 ~
scoreboard players set #sy nx.dream 251
execute positioned ~ 250 ~ run function nonios:dream/arrive/scan
