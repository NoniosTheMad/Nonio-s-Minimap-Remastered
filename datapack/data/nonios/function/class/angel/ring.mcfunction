# {r}: one of 24 points of the Sanctuary ring
$particle minecraft:dust{color:[1.0,0.84,0.35],scale:1.3} ^ ^0.2 ^$(r) 0 0.05 0 0 1 normal
$particle minecraft:end_rod ^ ^0.2 ^$(r) 0 0 0 0 1 normal
scoreboard players add #a nx.cls_tmp 1
execute if score #a nx.cls_tmp matches ..23 rotated ~15 0 run function nonios:class/angel/ring with storage nonios:tmp aw
