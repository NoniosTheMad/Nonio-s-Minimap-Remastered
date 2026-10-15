scoreboard players operation #wd_t nx.arena -= #speed nx.arena
# slain (its loot table already spilled the hoard where it fell)
execute unless entity @e[type=wither_skeleton,tag=nx.ev_warden,limit=1] run return run function nonios:arena/event/mob/wd_slain
execute if score #wd_t nx.arena matches ..0 run return run function nonios:arena/event/mob/wd_leave
# leash: strayed too far from its post = back on it
execute at @e[type=marker,tag=nx.ev_guard,limit=1] run function nonios:arena/event/mob/wd_leash with storage nonios:arena mob
