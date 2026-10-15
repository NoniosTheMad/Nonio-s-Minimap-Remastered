# as + at a generator marker: a new outcome grows now (the demos' "drop now" goes through generator/drop)
scoreboard players operation @s nx.gen_t = @s nx.gen_iv
# single-block mode (#47): the same block every time, the outcome is rolled when it is mined (generator/one/mined)
execute if score #single nx.gen matches 1 run return run function nonios:generator/one/grow
function nonios:generator/grow_m with entity @s data
particle minecraft:happy_villager ~ ~0.5 ~ 0.3 0.3 0.3 0 8
playsound minecraft:block.amethyst_block.chime block @a[distance=..16] ~ ~ ~ 0.7 1.3
