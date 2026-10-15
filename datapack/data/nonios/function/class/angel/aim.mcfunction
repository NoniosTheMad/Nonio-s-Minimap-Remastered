# as the beamed ally: its chest -> storage nonios:tmp ang {x,y,z}
data modify storage nonios:tmp ang.x set from entity @s Pos[0]
data modify storage nonios:tmp ang.z set from entity @s Pos[2]
execute store result score #y nx.cls_tmp run data get entity @s Pos[1] 100
scoreboard players add #y nx.cls_tmp 100
execute store result storage nonios:tmp ang.y double 0.01 run scoreboard players get #y nx.cls_tmp
