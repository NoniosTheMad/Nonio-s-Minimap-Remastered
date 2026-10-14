# as/at the Reaper (tag nx.cls_me): hit every living thing within 6 blocks except itself, its team and armour stands
$execute as @e[distance=..6,tag=!nx.cls_me,tag=!nx.cls_ally,type=!minecraft:armor_stand] if data entity @s Health at @s run function nonios:class/reaper/burst_hit {dmg:$(dmg)}
