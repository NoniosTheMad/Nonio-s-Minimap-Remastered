# as a visible Reaper that still has hidden items (see vanish): give them their models back, wherever they are now
execute if items entity @s armor.head *[minecraft:custom_data~{nx_hidden:1b}] run item modify entity @s armor.head nonios:class/reaper/show_head
execute if items entity @s weapon.offhand *[minecraft:custom_data~{nx_item:"reaper_scythe",nx_hidden:1b}] run item modify entity @s weapon.offhand nonios:class/reaper/show_scythe
execute if items entity @s weapon.offhand *[minecraft:custom_data~{nx_item:"reaper_lantern",nx_hidden:1b}] run item modify entity @s weapon.offhand nonios:class/reaper/show_lantern
data remove storage nonios:class sc
data modify storage nonios:class sc.slot set from entity @s Inventory[{components:{"minecraft:custom_data":{nx_item:"reaper_scythe",nx_hidden:1b}}}].Slot
execute if data storage nonios:class sc.slot run function nonios:class/reaper/unvanish_slot with storage nonios:class sc
data remove storage nonios:class sc
data modify storage nonios:class sc.slot set from entity @s Inventory[{components:{"minecraft:custom_data":{nx_item:"reaper_lantern",nx_hidden:1b}}}].Slot
execute if data storage nonios:class sc.slot run function nonios:class/reaper/unvanish_lantern with storage nonios:class sc
