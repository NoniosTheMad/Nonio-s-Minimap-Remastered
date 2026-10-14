# #f nx.purse = Fortune level (0-5) of the tool in @s's main hand (item predicate: works for any holder)
scoreboard players set #f nx.purse 0
execute unless items entity @s weapon.mainhand *[minecraft:enchantments~[{enchantments:"minecraft:fortune"}]] run return 0
scoreboard players set #f nx.purse 1
execute if items entity @s weapon.mainhand *[minecraft:enchantments~[{enchantments:"minecraft:fortune",levels:{min:2}}]] run scoreboard players set #f nx.purse 2
execute if items entity @s weapon.mainhand *[minecraft:enchantments~[{enchantments:"minecraft:fortune",levels:{min:3}}]] run scoreboard players set #f nx.purse 3
execute if items entity @s weapon.mainhand *[minecraft:enchantments~[{enchantments:"minecraft:fortune",levels:{min:4}}]] run scoreboard players set #f nx.purse 4
execute if items entity @s weapon.mainhand *[minecraft:enchantments~[{enchantments:"minecraft:fortune",levels:{min:5}}]] run scoreboard players set #f nx.purse 5
