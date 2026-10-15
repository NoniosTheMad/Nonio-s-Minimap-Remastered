# test "last life": your own Nexus is destroyed (Barrier removed first, then the obsidian)
execute if entity @s[team=] run return run tellraw @s {"text":"[demo] Join a team first.","color":"red"}
execute if entity @s[team=white] run function demo:break with storage nonios:map white.nexus
execute if entity @s[team=black] run function demo:break with storage nonios:map black.nexus
