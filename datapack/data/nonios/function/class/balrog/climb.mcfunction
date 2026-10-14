effect give @s minecraft:levitation 1 3 true
tag @s add nx.bal_climb
execute if predicate nonios:class/coin run particle minecraft:falling_lava ~ ~1 ~ 0.3 0.5 0.3 0 1
