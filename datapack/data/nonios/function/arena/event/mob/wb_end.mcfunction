# the Warband's time is up: survivors leave (no loot)
scoreboard players set #wb_t nx.arena 0
scoreboard players set #wb_waves nx.arena 0
execute unless entity @e[tag=nx.ev_raider,limit=1] run return 0
execute as @e[tag=nx.ev_raider] run function nonios:arena/event/mob/quiet
tellraw @a [{text:"★ ",color:"dark_red"},{text:"The Warband withdraws.",color:"gray"}]
