# Hotbar convention (CLAUDE.md "Gear slots"): every item the game hands out goes through gear/give or gear/loot.
# function nonios:gear/give {item:"minecraft:stone_sword[...]",count:1}  as the player (any position).
# item is pasted raw (components may hold double quotes): call it "with storage" when the string comes from data.
# Gear goes to its slot (weapon 1, bow 2, pickaxe 3, bucket 4, other tool 5), one copy at a time; if that slot is
# taken, the first free slot outside 1-5 (hotbar 6-9, the inventory, then the other reserved slots); no room = dropped.
# Anything else is a plain /give (stacks onto what you carry).
kill @e[type=item_display,tag=nx.gear_probe]
execute at @s run summon minecraft:item_display ~ ~ ~ {Tags:["nx.gear_probe"],view_range:0f}
$item replace entity @e[type=item_display,tag=nx.gear_probe,limit=1] contents with $(item)
execute store result score #gs nx.tmp run function nonios:gear/category
$scoreboard players set #gn nx.tmp $(count)
execute if score #gs nx.tmp matches 1.. run function nonios:gear/place_loop
$execute if score #gs nx.tmp matches 0 run give @s $(item) $(count)
kill @e[type=item_display,tag=nx.gear_probe]
