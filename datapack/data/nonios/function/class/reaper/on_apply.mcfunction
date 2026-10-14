# Reaper Invocation (V2 shop kit, 200 coins)
scoreboard players set @s nx.cls_souls 0
scoreboard players set @s nx.cls_heal 0
particle minecraft:soul ~ ~1 ~ 0.4 0.8 0.4 0.03 40
particle minecraft:large_smoke ~ ~1 ~ 0.4 0.8 0.4 0.02 30
playsound minecraft:entity.wither.ambient player @a ~ ~ ~ 0.8 0.6
title @s actionbar {"text":"Only the souls of the living can grant eternal life... or Death","color":"dark_purple","italic":true}
