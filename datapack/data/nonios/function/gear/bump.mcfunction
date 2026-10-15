# hotbar.$(slot)'s item -> the first free slot (place_one with no preferred slot; the target is still occupied so it can't land
# back there), else dropped at the feet. The bumped item borrows the probe tag while the class item waits as nx.gear_hold.
tag @e[type=item_display,tag=nx.gear_probe] add nx.gear_hold
tag @e[type=item_display,tag=nx.gear_probe] remove nx.gear_probe
execute at @s run summon minecraft:item_display ~ ~ ~ {Tags:["nx.gear_probe"],view_range:0f}
$item replace entity @e[type=item_display,tag=nx.gear_probe,limit=1] contents from entity @s hotbar.$(slot)
scoreboard players set #gs nx.tmp 0
execute unless function nonios:gear/place_one run function nonios:gear/drop
kill @e[type=item_display,tag=nx.gear_probe]
tag @e[type=item_display,tag=nx.gear_hold] add nx.gear_probe
tag @e[type=item_display,tag=nx.gear_hold] remove nx.gear_hold
