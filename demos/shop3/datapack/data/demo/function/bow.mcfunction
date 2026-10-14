# a Power V bow and arrows, through the gear helper (bow -> slot 2)
function nonios:gear/give {item:'minecraft:bow[enchantments={"minecraft:power":5}]',count:1}
function nonios:gear/give {item:"minecraft:arrow",count:64}
tellraw @s {"text":"[demo] Power V bow + 64 arrows.","color":"yellow"}
