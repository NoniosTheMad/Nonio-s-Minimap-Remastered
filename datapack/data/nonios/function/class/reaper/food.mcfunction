# as the Reaper, each tick (#137): no healing from food (hunger held at 17, under vanilla's 18 for natural regen),
# a permanent Regeneration I instead
execute if score @s nx.food matches 18.. run effect give @s minecraft:hunger 1 99 true
execute if score @s nx.food matches ..17 if predicate nonios:class/reaper/hungry run effect clear @s minecraft:hunger
execute unless predicate nonios:class/reaper/regen run effect give @s minecraft:regeneration infinite 0 true
