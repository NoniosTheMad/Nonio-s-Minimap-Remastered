# Spelunker Brew drunk (15 s cooldown, the horn puts it on): 6 s of ore sense. Every ore within 8 blocks
# (6 up/down) gets a marker; miner/spel_tick draws a coloured dot towards each, seen only by this Miner.
function nonios:class/miner/spel_end
scoreboard players set @s nx.cls_spel 120
scoreboard players operation #me nx.cls_tmp = @s nx.pid
scoreboard players set #n nx.cls_tmp 0
scoreboard players set #sx nx.cls_tmp 0
execute align xyz positioned ~-8 ~-6 ~-8 run function nonios:class/miner/spel_x
playsound minecraft:block.amethyst_block.chime player @s ~ ~ ~ 1 0.8
particle minecraft:wax_off ~ ~1 ~ 0.4 0.6 0.4 0.5 12 normal @s
