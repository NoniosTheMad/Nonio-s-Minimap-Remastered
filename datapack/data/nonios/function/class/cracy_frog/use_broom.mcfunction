# Magic Broom used (using_item, every tick it's held in use): climb on. Needs a third of the fuel.
execute if score @s nx.cls_fly matches 1.. run return 0
execute if score @s nx.cls_fuel matches 50.. run function nonios:class/cracy_frog/mount
execute unless score @s nx.cls_fuel matches 50.. run title @s actionbar {"text":"The broom is tired.","color":"gray"}
