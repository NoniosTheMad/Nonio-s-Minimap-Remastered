execute as @e[type=rabbit,tag=nx.lrabbit] run data modify entity @s DeathLootTable set value "minecraft:empty"
execute as @e[type=rabbit,tag=nx.lrabbit] at @s run particle minecraft:electric_spark ~ ~0.3 ~ 0.3 0.3 0.3 0.2 20
kill @e[type=rabbit,tag=nx.lrabbit]
