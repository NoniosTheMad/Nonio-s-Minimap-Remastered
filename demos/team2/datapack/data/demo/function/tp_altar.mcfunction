# in front of my team's altar, facing it
execute if entity @s[team=] run return run tellraw @s {"text":"[demo] Join a team first.","color":"red"}
execute if entity @s[team=white] run function demo:tp_altar_at with storage nonios:map white.altar
execute if entity @s[team=black] run function demo:tp_altar_at with storage nonios:map black.altar
