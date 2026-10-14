# as an item / mob: random upward kick
tag @s add nx.flung
execute store result entity @s Motion[0] double 0.01 run random value -28..28
execute store result entity @s Motion[1] double 0.01 run random value 35..60
execute store result entity @s Motion[2] double 0.01 run random value -28..28
