# returns the preferred hotbar slot (1-5) of the probe's item, 0 = not gear. custom_data nx_gear overrides the item tags
# (class items on plain bases: a stick scythe is a weapon). Tags: #nonios:gear/weapon|bow|pickaxe|bucket|tool.
execute if items entity @e[type=item_display,tag=nx.gear_probe,limit=1] contents *[minecraft:custom_data~{nx_gear:"none"}] run return 0
execute if items entity @e[type=item_display,tag=nx.gear_probe,limit=1] contents *[minecraft:custom_data~{nx_gear:"weapon"}] run return 1
execute if items entity @e[type=item_display,tag=nx.gear_probe,limit=1] contents *[minecraft:custom_data~{nx_gear:"bow"}] run return 2
execute if items entity @e[type=item_display,tag=nx.gear_probe,limit=1] contents *[minecraft:custom_data~{nx_gear:"pickaxe"}] run return 3
execute if items entity @e[type=item_display,tag=nx.gear_probe,limit=1] contents *[minecraft:custom_data~{nx_gear:"bucket"}] run return 4
execute if items entity @e[type=item_display,tag=nx.gear_probe,limit=1] contents *[minecraft:custom_data~{nx_gear:"tool"}] run return 5
execute if items entity @e[type=item_display,tag=nx.gear_probe,limit=1] contents #nonios:gear/weapon run return 1
execute if items entity @e[type=item_display,tag=nx.gear_probe,limit=1] contents #nonios:gear/bow run return 2
execute if items entity @e[type=item_display,tag=nx.gear_probe,limit=1] contents #nonios:gear/pickaxe run return 3
execute if items entity @e[type=item_display,tag=nx.gear_probe,limit=1] contents #nonios:gear/bucket run return 4
execute if items entity @e[type=item_display,tag=nx.gear_probe,limit=1] contents #nonios:gear/tool run return 5
return 0
