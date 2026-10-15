tag @s remove nx.cls_rage
scoreboard players set @s nx.cls_blvl 0
scoreboard players set @s nx.cls_brg 0
attribute @s minecraft:attack_damage modifier remove nonios:berserk_fury
attribute @s minecraft:attack_speed modifier remove nonios:berserk_haste
function nonios:class/berserker/uncap
scoreboard players reset @s nx.cls_bhp
scoreboard players set @s nx.cls_bgr 0
