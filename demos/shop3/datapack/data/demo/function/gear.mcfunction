# hotbar convention test: clear, then give in a scrambled order; everything lands in its slot (sword 1, bow 2, pickaxe 3,
# bucket 4, axe 5) whatever the order, the rest goes to free slots; a full inventory drops the extra at your feet
clear @s
function nonios:gear/give {item:"minecraft:oak_planks",count:64}
function nonios:gear/give {item:"minecraft:iron_axe",count:1}
function nonios:gear/give {item:"minecraft:water_bucket",count:1}
function nonios:gear/give {item:"minecraft:cooked_beef",count:16}
function nonios:gear/give {item:"minecraft:iron_pickaxe",count:1}
function nonios:gear/give {item:"minecraft:bow",count:1}
function nonios:gear/give {item:"minecraft:iron_sword",count:1}
function nonios:gear/give {item:"minecraft:iron_shovel",count:1}
tellraw @s {"text":"[demo] Gear given in scrambled order.","color":"yellow"}
