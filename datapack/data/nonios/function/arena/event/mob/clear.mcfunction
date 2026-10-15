# Enemy events off at once (arena/stop, arena/reset, demo): every event mob vanishes without loot, timers zeroed.
execute as @e[tag=nx.ev_mob] run function nonios:arena/event/mob/quiet
kill @e[type=marker,tag=nx.ev_guard]
kill @e[type=marker,tag=nx.ev_at]
scoreboard players set #wb_t nx.arena 0
scoreboard players set #wb_waves nx.arena 0
scoreboard players set #wd_t nx.arena 0
scoreboard players set #gr_t nx.arena 0
scoreboard players set #mob_ev nx.arena 0
