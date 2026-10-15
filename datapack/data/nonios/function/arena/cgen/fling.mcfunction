# as a fresh emerald: random outward push (0.10..0.22 blocks/tick each axis, random sign)
tag @s remove nx.cg_new
execute store result entity @s Motion[0] double 0.001 run random value -220..220
execute store result entity @s Motion[2] double 0.001 run random value -220..220
