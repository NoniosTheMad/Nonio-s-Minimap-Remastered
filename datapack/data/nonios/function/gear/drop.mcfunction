# inventory full: one copy drops at the player's feet (like /give does)
execute at @s run summon minecraft:item ~ ~ ~ {Tags:["nx.gear_drop"],Item:{id:"minecraft:stone",count:1},PickupDelay:0s}
data modify entity @e[type=item,tag=nx.gear_drop,limit=1] Item set from entity @e[type=item_display,tag=nx.gear_probe,limit=1] item
tag @e[type=item,tag=nx.gear_drop] remove nx.gear_drop
