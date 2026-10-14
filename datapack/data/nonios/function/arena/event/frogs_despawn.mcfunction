# leftover event frogs vanish without loot
scoreboard players set #frog_t nx.arena 0
execute as @e[type=frog,tag=nx.ev_frog] at @s run particle minecraft:poof ~ ~0.3 ~ 0.2 0.2 0.2 0.02 8
execute as @e[type=frog,tag=nx.ev_frog] run data modify entity @s DeathLootTable set value "minecraft:empty"
kill @e[type=frog,tag=nx.ev_frog]
