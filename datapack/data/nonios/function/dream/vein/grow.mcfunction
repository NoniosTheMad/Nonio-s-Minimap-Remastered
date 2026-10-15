# as a vein marker: the vein is the block under it. Weighted pick (percent), echoing the original 60/35/5 stone/emerald/emerald-block mix
scoreboard players set @s nx.dvt 0
execute store result score #r nx.dream run random value 1..100
execute if score #r nx.dream matches 1..55 run setblock ~ ~-1 ~ minecraft:emerald_ore
execute if score #r nx.dream matches 56..70 run setblock ~ ~-1 ~ minecraft:deepslate_emerald_ore
execute if score #r nx.dream matches 71..78 run setblock ~ ~-1 ~ minecraft:diamond_ore
execute if score #r nx.dream matches 79..87 run setblock ~ ~-1 ~ minecraft:gold_ore
execute if score #r nx.dream matches 88..95 run setblock ~ ~-1 ~ minecraft:lapis_ore
execute if score #r nx.dream matches 96..100 run setblock ~ ~-1 ~ minecraft:emerald_block
particle minecraft:happy_villager ~ ~-0.5 ~ 0.4 0.4 0.4 0 12
particle minecraft:end_rod ~ ~ ~ 0.15 0.3 0.15 0.03 6
playsound minecraft:block.amethyst_block.chime block @a ~ ~ ~ 1 1.3
