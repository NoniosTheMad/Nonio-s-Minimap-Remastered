# as/at a Balrog pushing into a wall: rise (Levitation V, ~5 b/s); seen by others as dripping lava
effect give @s minecraft:levitation 1 4 true
tag @s add nx.bal_climb
tag @s add nx.cls_pself
execute if predicate nonios:class/coin run particle minecraft:falling_lava ~ ~1 ~ 0.3 0.5 0.3 0 1 normal @a[tag=!nx.cls_pself]
tag @s remove nx.cls_pself
