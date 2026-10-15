# Berserker with the axe out, tier 1..4, every 5 ticks: red mist, thicker with Rage; full Rage smoulders.
# Not drawn for the Berserker itself (it would fill its view).
tag @s add nx.cls_pself
execute if score @s nx.cls_blvl matches 1 run particle minecraft:dust{color:[0.6,0.05,0.05],scale:0.8} ~ ~1 ~ 0.35 0.5 0.35 0 1 normal @a[tag=!nx.cls_pself]
execute if score @s nx.cls_blvl matches 2 run particle minecraft:dust{color:[0.75,0.05,0.05],scale:1.0} ~ ~1 ~ 0.35 0.5 0.35 0 2 normal @a[tag=!nx.cls_pself]
execute if score @s nx.cls_blvl matches 3 run particle minecraft:dust{color:[0.9,0.05,0.05],scale:1.2} ~ ~1 ~ 0.4 0.55 0.4 0 4 normal @a[tag=!nx.cls_pself]
execute if score @s nx.cls_blvl matches 4 run particle minecraft:dust{color:[1,0.1,0.05],scale:1.4} ~ ~1 ~ 0.45 0.6 0.45 0 6 normal @a[tag=!nx.cls_pself]
execute if score @s nx.cls_blvl matches 4 run particle minecraft:large_smoke ~ ~1.9 ~ 0.2 0.1 0.2 0.01 1 normal @a[tag=!nx.cls_pself]
tag @s remove nx.cls_pself
