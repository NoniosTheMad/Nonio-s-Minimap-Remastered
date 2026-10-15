tag @s add demo.init
# demo: the G-menu shop entry works anywhere (game: only at your own team's shopkeeper)
tag @s add nx.shop_anywhere
gamemode survival @s
clear @s
effect give @s minecraft:saturation infinite 0 true
scoreboard players set @s nx.coins 50
scoreboard objectives setdisplay sidebar nx.coins
tp @s 0.5 64 3.5 180 0
