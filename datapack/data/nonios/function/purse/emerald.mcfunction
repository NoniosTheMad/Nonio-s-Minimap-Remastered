# advancement nonios:purse/emerald: emeralds / emerald blocks reached the inventory (arena nodes, surges, frogs, rabbit...).
# They are coins: straight into the purse at #emerald_item / #emerald_block_item nx.coinval, never kept as items.
# So nobody holds an emerald block to place (the emerald blocks/ores themselves drop nothing: data/minecraft/loot_table/blocks).
advancement revoke @s only nonios:purse/emerald
execute store result score #n nx.purse run clear @s minecraft:emerald
scoreboard players operation #n nx.purse *= #emerald_item nx.coinval
scoreboard players operation @s nx.coins += #n nx.purse
execute store result score #n nx.purse run clear @s minecraft:emerald_block
scoreboard players operation #n nx.purse *= #emerald_block_item nx.coinval
scoreboard players operation @s nx.coins += #n nx.purse
