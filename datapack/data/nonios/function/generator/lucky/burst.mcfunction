# as + at a generator whose lucky block was just mined (same tick). The block's own drop disappears; the nearest
# player gets a random outcome: coins 8/20 (flung emeralds), item 7/20 (loot generator/lucky_item), trap 5/20.
tag @s remove nx.gen_lucky
scoreboard players operation @s nx.gen_t = @s nx.gen_iv
kill @e[type=item,distance=..2,nbt={Item:{id:"minecraft:yellow_glazed_terracotta"}}]
particle minecraft:firework ~ ~0.5 ~ 0.3 0.3 0.3 0.15 30
playsound minecraft:entity.firework_rocket.twinkle block @a[distance=..16] ~ ~ ~ 1 1
execute store result score #lr nx.gen run random value 1..20
execute if score #lr nx.gen matches 1..8 run return run function nonios:generator/lucky/coins
execute if score #lr nx.gen matches 9..15 run return run loot spawn ~ ~0.5 ~ loot nonios:generator/lucky_item
function nonios:generator/lucky/trap
