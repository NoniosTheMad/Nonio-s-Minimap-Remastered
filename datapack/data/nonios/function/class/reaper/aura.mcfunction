# enchantment nonios:class/reaper_shroud (tick, 25%, only while visible): the V2 smoke + lava trail
particle minecraft:large_smoke ~ ~0.1 ~ 0.3 0.05 0.3 0.005 1
execute if predicate nonios:class/coin run particle minecraft:soul_fire_flame ~ ~0.2 ~ 0.25 0.1 0.25 0.01 1
execute if predicate nonios:class/coin if predicate nonios:class/coin run particle minecraft:lava ~ ~0.6 ~ 0.2 0.3 0.2 0 1
