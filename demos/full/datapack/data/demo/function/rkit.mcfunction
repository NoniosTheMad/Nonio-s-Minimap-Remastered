function nonios:gear/give {item:'minecraft:bow[enchantments={"minecraft:power":5,"minecraft:infinity":1}]',count:1}
function nonios:gear/give {item:'minecraft:crossbow[enchantments={"minecraft:quick_charge":3}]',count:1}
function nonios:gear/give {item:'minecraft:trident[enchantments={"minecraft:loyalty":3}]',count:1}
give @s minecraft:arrow 64
give @s minecraft:firework_rocket[fireworks={flight_duration:1,explosions:[{shape:"large_ball",colors:[I;65280]},{shape:"star",colors:[I;16776960]}]}] 32
give @s minecraft:wind_charge 16
tellraw @s {"text":"[demo] Bow, crossbow (load a rocket in the off-hand), trident, wind charges. Shoot the enemy Barrier.","color":"yellow"}
