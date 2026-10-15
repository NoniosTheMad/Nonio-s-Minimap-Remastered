# storage mob {x, y, z, r}: scatter the new mobs (nx.ev_new) over the ground within r blocks of (x, z), on the highest
# block below y + 4; they claw out of the soil
execute store result score #top nx.arena run data get storage nonios:arena mob.y
scoreboard players add #top nx.arena 4
execute store result storage nonios:arena mob.top int 1 run scoreboard players get #top nx.arena
function nonios:arena/event/mob/spread_m with storage nonios:arena mob
execute as @e[tag=nx.ev_new] at @s run particle minecraft:block{block_state:"minecraft:coarse_dirt"} ~ ~0.3 ~ 0.4 0.2 0.4 0 25
execute as @e[tag=nx.ev_new] at @s run particle minecraft:large_smoke ~ ~0.5 ~ 0.3 0.4 0.3 0.02 6
execute as @e[tag=nx.ev_new] at @s run playsound minecraft:block.rooted_dirt.break hostile @a ~ ~ ~ 1.5 0.6
tag @e[tag=nx.ev_new] remove nx.ev_new
kill @e[type=marker,tag=nx.ev_at]
