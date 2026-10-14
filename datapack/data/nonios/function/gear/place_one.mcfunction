# one copy of the probe's item: preferred slot #gs (1-5 = hotbar.0-4) if empty, else the first free slot outside 1-5
# (hotbar 6-9, inventory, then the other reserved hotbar slots). Fails when the inventory is full.
execute if score #gs nx.tmp matches 1 unless items entity @s hotbar.0 * run return run item replace entity @s hotbar.0 from entity @e[type=item_display,tag=nx.gear_probe,limit=1] contents
execute if score #gs nx.tmp matches 2 unless items entity @s hotbar.1 * run return run item replace entity @s hotbar.1 from entity @e[type=item_display,tag=nx.gear_probe,limit=1] contents
execute if score #gs nx.tmp matches 3 unless items entity @s hotbar.2 * run return run item replace entity @s hotbar.2 from entity @e[type=item_display,tag=nx.gear_probe,limit=1] contents
execute if score #gs nx.tmp matches 4 unless items entity @s hotbar.3 * run return run item replace entity @s hotbar.3 from entity @e[type=item_display,tag=nx.gear_probe,limit=1] contents
execute if score #gs nx.tmp matches 5 unless items entity @s hotbar.4 * run return run item replace entity @s hotbar.4 from entity @e[type=item_display,tag=nx.gear_probe,limit=1] contents
execute unless items entity @s hotbar.5 * run return run item replace entity @s hotbar.5 from entity @e[type=item_display,tag=nx.gear_probe,limit=1] contents
execute unless items entity @s hotbar.6 * run return run item replace entity @s hotbar.6 from entity @e[type=item_display,tag=nx.gear_probe,limit=1] contents
execute unless items entity @s hotbar.7 * run return run item replace entity @s hotbar.7 from entity @e[type=item_display,tag=nx.gear_probe,limit=1] contents
execute unless items entity @s hotbar.8 * run return run item replace entity @s hotbar.8 from entity @e[type=item_display,tag=nx.gear_probe,limit=1] contents
execute unless items entity @s inventory.0 * run return run item replace entity @s inventory.0 from entity @e[type=item_display,tag=nx.gear_probe,limit=1] contents
execute unless items entity @s inventory.1 * run return run item replace entity @s inventory.1 from entity @e[type=item_display,tag=nx.gear_probe,limit=1] contents
execute unless items entity @s inventory.2 * run return run item replace entity @s inventory.2 from entity @e[type=item_display,tag=nx.gear_probe,limit=1] contents
execute unless items entity @s inventory.3 * run return run item replace entity @s inventory.3 from entity @e[type=item_display,tag=nx.gear_probe,limit=1] contents
execute unless items entity @s inventory.4 * run return run item replace entity @s inventory.4 from entity @e[type=item_display,tag=nx.gear_probe,limit=1] contents
execute unless items entity @s inventory.5 * run return run item replace entity @s inventory.5 from entity @e[type=item_display,tag=nx.gear_probe,limit=1] contents
execute unless items entity @s inventory.6 * run return run item replace entity @s inventory.6 from entity @e[type=item_display,tag=nx.gear_probe,limit=1] contents
execute unless items entity @s inventory.7 * run return run item replace entity @s inventory.7 from entity @e[type=item_display,tag=nx.gear_probe,limit=1] contents
execute unless items entity @s inventory.8 * run return run item replace entity @s inventory.8 from entity @e[type=item_display,tag=nx.gear_probe,limit=1] contents
execute unless items entity @s inventory.9 * run return run item replace entity @s inventory.9 from entity @e[type=item_display,tag=nx.gear_probe,limit=1] contents
execute unless items entity @s inventory.10 * run return run item replace entity @s inventory.10 from entity @e[type=item_display,tag=nx.gear_probe,limit=1] contents
execute unless items entity @s inventory.11 * run return run item replace entity @s inventory.11 from entity @e[type=item_display,tag=nx.gear_probe,limit=1] contents
execute unless items entity @s inventory.12 * run return run item replace entity @s inventory.12 from entity @e[type=item_display,tag=nx.gear_probe,limit=1] contents
execute unless items entity @s inventory.13 * run return run item replace entity @s inventory.13 from entity @e[type=item_display,tag=nx.gear_probe,limit=1] contents
execute unless items entity @s inventory.14 * run return run item replace entity @s inventory.14 from entity @e[type=item_display,tag=nx.gear_probe,limit=1] contents
execute unless items entity @s inventory.15 * run return run item replace entity @s inventory.15 from entity @e[type=item_display,tag=nx.gear_probe,limit=1] contents
execute unless items entity @s inventory.16 * run return run item replace entity @s inventory.16 from entity @e[type=item_display,tag=nx.gear_probe,limit=1] contents
execute unless items entity @s inventory.17 * run return run item replace entity @s inventory.17 from entity @e[type=item_display,tag=nx.gear_probe,limit=1] contents
execute unless items entity @s inventory.18 * run return run item replace entity @s inventory.18 from entity @e[type=item_display,tag=nx.gear_probe,limit=1] contents
execute unless items entity @s inventory.19 * run return run item replace entity @s inventory.19 from entity @e[type=item_display,tag=nx.gear_probe,limit=1] contents
execute unless items entity @s inventory.20 * run return run item replace entity @s inventory.20 from entity @e[type=item_display,tag=nx.gear_probe,limit=1] contents
execute unless items entity @s inventory.21 * run return run item replace entity @s inventory.21 from entity @e[type=item_display,tag=nx.gear_probe,limit=1] contents
execute unless items entity @s inventory.22 * run return run item replace entity @s inventory.22 from entity @e[type=item_display,tag=nx.gear_probe,limit=1] contents
execute unless items entity @s inventory.23 * run return run item replace entity @s inventory.23 from entity @e[type=item_display,tag=nx.gear_probe,limit=1] contents
execute unless items entity @s inventory.24 * run return run item replace entity @s inventory.24 from entity @e[type=item_display,tag=nx.gear_probe,limit=1] contents
execute unless items entity @s inventory.25 * run return run item replace entity @s inventory.25 from entity @e[type=item_display,tag=nx.gear_probe,limit=1] contents
execute unless items entity @s inventory.26 * run return run item replace entity @s inventory.26 from entity @e[type=item_display,tag=nx.gear_probe,limit=1] contents
execute unless items entity @s hotbar.0 * run return run item replace entity @s hotbar.0 from entity @e[type=item_display,tag=nx.gear_probe,limit=1] contents
execute unless items entity @s hotbar.1 * run return run item replace entity @s hotbar.1 from entity @e[type=item_display,tag=nx.gear_probe,limit=1] contents
execute unless items entity @s hotbar.2 * run return run item replace entity @s hotbar.2 from entity @e[type=item_display,tag=nx.gear_probe,limit=1] contents
execute unless items entity @s hotbar.3 * run return run item replace entity @s hotbar.3 from entity @e[type=item_display,tag=nx.gear_probe,limit=1] contents
execute unless items entity @s hotbar.4 * run return run item replace entity @s hotbar.4 from entity @e[type=item_display,tag=nx.gear_probe,limit=1] contents
return fail
