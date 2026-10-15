# as + at a generator marker (single-block mode): the generator block grows; tagged so its mining is noticed
function nonios:generator/one/set with storage nonios:gen single
tag @s add nx.gen_one
particle minecraft:happy_villager ~ ~0.5 ~ 0.3 0.3 0.3 0 8
playsound minecraft:block.amethyst_block.chime block @a[distance=..16] ~ ~ ~ 0.7 1.3
