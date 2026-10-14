# 6 blocks in front of the enemy Nexus (arena side), looking at it
execute if entity @s[team=white] at @e[type=marker,tag=nx.core,tag=nx.black,limit=1] positioned ~0.5 ~ ~-5.5 run return run tp @s ~ ~ ~ facing ~ ~1 ~6
execute if entity @s[team=black] at @e[type=marker,tag=nx.core,tag=nx.white,limit=1] positioned ~0.5 ~ ~6.5 run return run tp @s ~ ~ ~ facing ~ ~1 ~-6
tellraw @s {"text":"[demo] Join a team and start a match first.","color":"red"}
