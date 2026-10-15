# EVENT (global): THE GILDED WARDEN. config.warden {hp, life, leash}: a giant gold-clad wither skeleton rises at the
# centre generator (config.cgen, else config.center) and guards it: it never strays more than `leash` blocks from it.
# Killed = its hoard of emeralds spills (loot nonios:arena/warden). Still alive after `life` ticks: it withdraws.
execute as @e[type=wither_skeleton,tag=nx.ev_warden] run function nonios:arena/event/mob/quiet
kill @e[type=marker,tag=nx.ev_guard]
data modify storage nonios:arena mob set from storage nonios:arena config.center
execute if data storage nonios:arena config.cgen.x run data modify storage nonios:arena mob set from storage nonios:arena config.cgen
data modify storage nonios:arena mob.hp set from storage nonios:arena config.warden.hp
data modify storage nonios:arena mob.l set from storage nonios:arena config.warden.leash
function nonios:arena/event/mob/wd_spawn with storage nonios:arena mob
execute store result score #wd_t nx.arena run data get storage nonios:arena config.warden.life
scoreboard players operation #ev_run nx.arena = #wd_t nx.arena
scoreboard players set #mob_ev nx.arena 1
