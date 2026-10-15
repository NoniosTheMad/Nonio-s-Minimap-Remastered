# test the win: the enemy Nexus is destroyed; with no enemy players/dummies alive the match ends at once
execute if entity @s[team=] run return run tellraw @s {"text":"[demo] Join a team first.","color":"red"}
execute if entity @s[team=white] run function demo:break with storage nonios:map black.nexus
execute if entity @s[team=black] run function demo:break with storage nonios:map white.nexus
