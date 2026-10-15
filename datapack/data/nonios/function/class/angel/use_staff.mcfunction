# Seraph Staff held up (every tick while right-click is held; it is never used up). The first ally along the aim
# (16 blocks, through glass and plants) is locked and stays locked while it stays within 16 blocks: the beam
# (angel/beam) mends it, or empowers it while the Angel sneaks.
scoreboard players set @s nx.cls_abm 2
scoreboard players operation #me nx.cls_tmp = @s nx.pid
tag @s add nx.cls_me
function nonios:class/angel/allies
execute if score @s nx.cls_alk matches 1 unless function nonios:class/angel/has_target run function nonios:class/angel/unlock
scoreboard players set #r nx.cls_tmp 0
execute unless score @s nx.cls_alk matches 1 anchored eyes positioned ^ ^ ^ run function nonios:class/angel/ray
execute if score @s nx.cls_alk matches 1 run function nonios:class/angel/beam
execute unless score @s nx.cls_alk matches 1 run function nonios:class/angel/search
tag @e[tag=nx.cls_ally] remove nx.cls_ally
tag @s remove nx.cls_me
