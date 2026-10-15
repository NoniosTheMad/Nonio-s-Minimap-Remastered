item replace entity @s armor.head with minecraft:diamond_helmet
item replace entity @s armor.chest with minecraft:diamond_chestplate
item replace entity @s armor.legs with minecraft:diamond_leggings
item replace entity @s armor.feet with minecraft:diamond_boots
function nonios:gear/give {item:'minecraft:diamond_sword',count:1}
function nonios:gear/give {item:'minecraft:diamond_pickaxe[enchantments={"minecraft:efficiency":5}]',count:1}
function nonios:gear/give {item:'minecraft:cooked_beef',count:16}
tellraw @s {"text":"[demo] Diamond gear.","color":"yellow"}
