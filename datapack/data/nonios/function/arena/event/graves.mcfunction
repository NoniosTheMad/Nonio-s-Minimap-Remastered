# EVENT (global): GRAVES OPEN. config.graves {per_node, life}: at every capture node `per_node` husks claw out of the
# ground, one of them a big Grave Lord. They drop emeralds (loot nonios:arena/grave, grave_lord). Leftovers crumble after `life`.
execute as @e[type=marker,tag=nx.node] at @s run function nonios:arena/event/mob/gr_node
execute store result score #gr_t nx.arena run data get storage nonios:arena config.graves.life
scoreboard players operation #ev_run nx.arena = #gr_t nx.arena
scoreboard players set #mob_ev nx.arena 1
execute as @a at @s run playsound minecraft:entity.zombie_villager.cure hostile @s ~ ~ ~ 0.6 0.5
