# Priority mode of gear/give (#135, class signature items): function nonios:gear/force {item:"...",slot:0}  as the player.
# One copy goes into hotbar.<slot> (0-based: class kits fill 0, 1, 2... in src/classes.json order). Whatever held that slot
# moves to the first free slot (hotbar 6-9, inventory, then hotbar 1-5) or drops at the feet when the inventory is full.
kill @e[type=item_display,tag=nx.gear_probe]
execute at @s run summon minecraft:item_display ~ ~ ~ {Tags:["nx.gear_probe"],view_range:0f}
$item replace entity @e[type=item_display,tag=nx.gear_probe,limit=1] contents with $(item)
$function nonios:gear/force_place {slot:$(slot)}
kill @e[type=item_display,tag=nx.gear_probe]
