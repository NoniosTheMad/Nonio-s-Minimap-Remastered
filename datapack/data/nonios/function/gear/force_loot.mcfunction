# gear/force for a one-item loot table: function nonios:gear/force_loot {table:"nonios:class/angel/staff",slot:0}  as the player.
kill @e[type=item_display,tag=nx.gear_probe]
execute at @s run summon minecraft:item_display ~ ~ ~ {Tags:["nx.gear_probe"],view_range:0f}
$loot replace entity @e[type=item_display,tag=nx.gear_probe,limit=1] contents loot $(table)
$function nonios:gear/force_place {slot:$(slot)}
kill @e[type=item_display,tag=nx.gear_probe]
