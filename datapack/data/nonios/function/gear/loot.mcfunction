# function nonios:gear/loot {table:"nonios:class/archer/bow"}  as the player: gear/give for a one-item loot table
# (class kits). Gear: its slot (see gear/give); anything else: /loot give.
kill @e[type=item_display,tag=nx.gear_probe]
execute at @s run summon minecraft:item_display ~ ~ ~ {Tags:["nx.gear_probe"],view_range:0f}
$loot replace entity @e[type=item_display,tag=nx.gear_probe,limit=1] contents loot $(table)
execute store result score #gs nx.tmp run function nonios:gear/category
execute store result score #gn nx.tmp run data get entity @e[type=item_display,tag=nx.gear_probe,limit=1] item.count
data modify entity @e[type=item_display,tag=nx.gear_probe,limit=1] item.count set value 1
execute if score #gs nx.tmp matches 1.. run function nonios:gear/place_loop
$execute if score #gs nx.tmp matches 0 run loot give @s loot $(table)
kill @e[type=item_display,tag=nx.gear_probe]
