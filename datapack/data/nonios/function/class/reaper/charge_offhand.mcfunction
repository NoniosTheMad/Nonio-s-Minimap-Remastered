data remove storage nonios:class sc
data modify storage nonios:class sc.rem set from entity @s equipment.offhand
data modify storage nonios:class sc.at set value "weapon"
data modify storage nonios:class sc.slot set value "offhand"
function nonios:class/reaper/charge_slot with storage nonios:class sc
