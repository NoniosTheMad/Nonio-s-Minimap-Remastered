$scoreboard players set #v demo.c $(v)
$scoreboard players operation #v demo.c *= @s $(o)
scoreboard players operation @s nx.coins += #v demo.c
$scoreboard players set @s $(o) 0
playsound minecraft:entity.experience_orb.pickup player @s ~ ~ ~ 0.5 1.4
