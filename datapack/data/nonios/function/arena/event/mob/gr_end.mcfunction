# the graves close: leftover husks crumble (no loot)
scoreboard players set #gr_t nx.arena 0
execute unless entity @e[tag=nx.ev_grave,limit=1] run return 0
execute as @e[tag=nx.ev_grave] run function nonios:arena/event/mob/quiet
tellraw @a [{text:"★ ",color:"dark_green"},{text:"The graves close.",color:"gray"}]
