# fill the inventory with cobblestone, leaving one free slot (to test partial purchases and "bag full")
clear @s
give @s minecraft:cobblestone 2240
item replace entity @s hotbar.8 with minecraft:air
tellraw @s {"text":"[demo] Bag full but one slot.","color":"yellow"}
