# as an event mob: it vanishes in smoke, no loot
execute at @s run particle minecraft:large_smoke ~ ~0.8 ~ 0.3 0.5 0.3 0.02 12
data modify entity @s DeathLootTable set value "minecraft:empty"
kill @s
