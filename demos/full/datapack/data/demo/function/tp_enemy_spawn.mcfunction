# onto the enemy spawn pad: the spawn defense hurts you there (prep: the walls / containment send you back first)
execute if entity @s[team=] run return run tellraw @s {"text":"[demo] Join a team first.","color":"red"}
execute if entity @s[team=white] run function demo:tp_pad with storage nonios:map black.spawn
execute if entity @s[team=black] run function demo:tp_pad with storage nonios:map white.spawn
tellraw @s {"text":"[demo] Enemy spawn. Step off the pad (4 blocks) to stop the damage.","color":"yellow"}
