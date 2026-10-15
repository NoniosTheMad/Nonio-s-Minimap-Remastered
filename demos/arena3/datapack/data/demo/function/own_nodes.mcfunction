# every capture node now belongs to your team (bonuses apply from the next arena check)
execute if entity @s[team=] run return run tellraw @s {"text":"[demo] Join a team first.","color":"red"}
execute if entity @s[team=white] as @e[type=marker,tag=nx.node] run function demo:own {o:1}
execute if entity @s[team=black] as @e[type=marker,tag=nx.node] run function demo:own {o:2}
tellraw @s {"text":"[demo] All nodes are yours: West = Haste in your field, Centre = bank interest, East = generator regrows faster.","color":"yellow"}
