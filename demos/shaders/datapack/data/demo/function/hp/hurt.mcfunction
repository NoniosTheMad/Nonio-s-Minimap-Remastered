damage @s 6 minecraft:generic
execute if entity @s[gamemode=creative] run tellraw @s [{"text":"[demo] ","color":"dark_gray"},{"text":"Creative ignores damage: switch to survival (F3+F4) to test your own colour, or watch the patients.","color":"gray"}]
