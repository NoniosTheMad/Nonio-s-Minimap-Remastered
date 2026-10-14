# as + at a generator marker: a new outcome grows now (the demos' "drop now" goes through generator/drop)
scoreboard players operation @s nx.gen_t = @s nx.gen_iv
tag @s remove nx.gen_lucky
execute if score #lucky nx.gen matches 1 store result score #lr nx.gen run random value 1..1000
execute if score #lucky nx.gen matches 1 run scoreboard players operation #lr nx.gen %= #lucky_n nx.gen
execute if score #lucky nx.gen matches 1 if score #lr nx.gen matches 0 run return run function nonios:generator/lucky/grow with storage nonios:gen lucky
function nonios:generator/grow_m with entity @s data
particle minecraft:happy_villager ~ ~0.5 ~ 0.3 0.3 0.3 0 8
playsound minecraft:block.amethyst_block.chime block @a[distance=..16] ~ ~ ~ 0.7 1.3
