# as a player: core state (block now, regrow timer, regrowths since the last reset)
execute unless score #core nx.arena matches 1 run return run tellraw @s [{text:"[arena] core ",color:"aqua"},{text:"none (config.core not set)",color:"gray"}]
tag @s add nx.ar_ask
execute as @e[type=marker,tag=nx.acore,limit=1] at @s run function nonios:arena/core/status_at
tag @s remove nx.ar_ask
