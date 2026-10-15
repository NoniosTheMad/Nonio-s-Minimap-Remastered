# as/at every Reaper, each tick
# scythe state follows the souls (charged = glint + burst on right-click, dormant = "No souls")
execute if score @s nx.cls_souls matches 1.. if items entity @s container.* *[minecraft:custom_data~{nx_item:"reaper_scythe",nx_state:"dormant"}] run function nonios:class/reaper/charge
execute if score @s nx.cls_souls matches 1.. if items entity @s weapon.offhand *[minecraft:custom_data~{nx_item:"reaper_scythe",nx_state:"dormant"}] run function nonios:class/reaper/charge
execute unless score @s nx.cls_souls matches 1.. if items entity @s container.* *[minecraft:custom_data~{nx_item:"reaper_scythe",nx_state:"charged"}] run function nonios:class/reaper/discharge
# invisible = really unseen: worn/held class items lose their model while it lasts
execute if predicate nonios:class/reaper/invisible run function nonios:class/reaper/vanish
execute unless predicate nonios:class/reaper/invisible if items entity @s armor.head *[minecraft:custom_data~{nx_hidden:1b}] run function nonios:class/reaper/unvanish
execute unless predicate nonios:class/reaper/invisible if items entity @s weapon.offhand *[minecraft:custom_data~{nx_hidden:1b}] run function nonios:class/reaper/unvanish
execute unless predicate nonios:class/reaper/invisible if items entity @s container.* *[minecraft:custom_data~{nx_hidden:1b}] run function nonios:class/reaper/unvanish
# flight: off on the ground, in fluids and outside survival/adventure
execute if entity @s[gamemode=!survival,gamemode=!adventure] run return run function nonios:class/reaper/fly_off
execute if predicate nonios:class/on_ground run return run function nonios:class/reaper/fly_off
execute if block ~ ~ ~ #nonios:class/reaper_fluid run return run function nonios:class/reaper/fly_off
execute unless score @s nx.cls_rfly matches 1 run function nonios:class/reaper/fly_on
function nonios:class/reaper/fly
