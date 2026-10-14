item replace entity @s armor.head with minecraft:diamond_helmet
item replace entity @s armor.chest with minecraft:diamond_chestplate
item replace entity @s armor.legs with minecraft:diamond_leggings
item replace entity @s armor.feet with minecraft:diamond_boots
give @s minecraft:diamond_sword
give @s minecraft:diamond_pickaxe[enchantments={"minecraft:efficiency":5}]
give @s minecraft:cooked_beef 16
tellraw @s {"text":"[demo] Diamond gear.","color":"yellow"}
