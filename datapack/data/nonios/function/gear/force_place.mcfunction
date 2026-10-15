# the probe's item into hotbar.$(slot); the slot's old item is bumped first (gear/bump)
$execute if items entity @s hotbar.$(slot) * run function nonios:gear/bump {slot:$(slot)}
$item replace entity @s hotbar.$(slot) from entity @e[type=item_display,tag=nx.gear_probe,limit=1] contents
