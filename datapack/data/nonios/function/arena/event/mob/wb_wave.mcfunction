# one Warband wave around config.center
execute store result score #wb_next nx.arena run data get storage nonios:arena config.warband.gap
scoreboard players remove #wb_waves nx.arena 1
scoreboard players set #3 nx.arena 3
execute store result score #left nx.arena run data get storage nonios:arena config.warband.size
data modify storage nonios:arena mob set from storage nonios:arena config.center
data modify storage nonios:arena mob.r set from storage nonios:arena config.warband.range
function nonios:arena/event/mob/at with storage nonios:arena mob
execute at @e[type=marker,tag=nx.ev_at,limit=1] run function nonios:arena/event/mob/wb_one
function nonios:arena/event/mob/spread
execute as @a at @s run playsound minecraft:event.raid.horn hostile @s ~ ~ ~ 0.7 1.3
