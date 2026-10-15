# its watch is over: it sinks away (no loot)
scoreboard players set #wd_t nx.arena 0
execute as @e[type=wither_skeleton,tag=nx.ev_warden] run function nonios:arena/event/mob/quiet
kill @e[type=marker,tag=nx.ev_guard]
tellraw @a [{text:"★ ",color:"gold"},{text:"The Gilded Warden withdraws.",color:"gray"}]
