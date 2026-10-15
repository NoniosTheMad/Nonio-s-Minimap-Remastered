# as the Reaper with souls: wake the dormant scythe wherever it is (glint, right-click = 0.25 s heal). Its use_remainder
# is an exact copy of the dormant one, so a heal turns it back to sleep in place.
execute if items entity @s weapon.offhand *[minecraft:custom_data~{nx_item:"reaper_scythe",nx_state:"dormant"}] run return run function nonios:class/reaper/charge_offhand
data remove storage nonios:class sc
data modify storage nonios:class sc.rem set from entity @s Inventory[{components:{"minecraft:custom_data":{nx_item:"reaper_scythe",nx_state:"dormant"}}}]
execute unless data storage nonios:class sc.rem run return 0
data modify storage nonios:class sc.slot set from storage nonios:class sc.rem.Slot
data remove storage nonios:class sc.rem.Slot
data modify storage nonios:class sc.at set value "container"
function nonios:class/reaper/charge_slot with storage nonios:class sc
