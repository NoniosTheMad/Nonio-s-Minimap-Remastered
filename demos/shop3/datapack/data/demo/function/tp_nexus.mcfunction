# 12 blocks in front of the enemy Nexus, facing it (bow range)
execute if entity @s[team=] run return run tellraw @s {"text":"[demo] Join a team first (Start match).","color":"red"}
execute if entity @s[team=white] run function demo:tp_nexus_at with storage nonios:map black.nexus
execute if entity @s[team=black] run function demo:tp_nexus_at with storage nonios:map white.nexus
