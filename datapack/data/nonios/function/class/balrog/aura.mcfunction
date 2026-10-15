# enchantment nonios:class/balrog_aura (tick, 50%): shadow and flame, seen by everyone but the Balrog itself (#86)
tag @s add nx.cls_pself
particle minecraft:flame ~ ~1.5 ~ 0.4 0.8 0.4 0.01 1 normal @a[tag=!nx.cls_pself]
execute if predicate nonios:class/coin run particle minecraft:large_smoke ~ ~2.2 ~ 0.3 0.3 0.3 0.01 1 normal @a[tag=!nx.cls_pself]
execute if predicate nonios:class/coin if predicate nonios:class/coin run particle minecraft:lava ~ ~1.5 ~ 0.3 0.6 0.3 0 1 normal @a[tag=!nx.cls_pself]
tag @s remove nx.cls_pself
