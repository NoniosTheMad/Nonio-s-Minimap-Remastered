# as + at a generator marker; macro $(block): the lucky block grows instead of a normal outcome
$setblock ~ ~ ~ $(block)
tag @s add nx.gen_lucky
particle minecraft:wax_on ~ ~0.5 ~ 0.4 0.4 0.4 0 20
playsound minecraft:block.note_block.chime block @a[distance=..16] ~ ~ ~ 1 1.6
