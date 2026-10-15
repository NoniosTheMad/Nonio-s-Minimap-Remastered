tag @s remove nx.cls_rage
scoreboard players set @s nx.cls_blvl 0
attribute @s minecraft:attack_damage modifier remove nonios:berserk_fury
function nonios:class/berserker/uncap
scoreboard players reset @s nx.cls_bhp
scoreboard players set @s nx.cls_bgr 0
