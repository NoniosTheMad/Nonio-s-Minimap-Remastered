# new match: loose drops around the core go, a fresh block is rolled
execute as @e[type=marker,tag=nx.acore] at @s run kill @e[type=item,distance=..3]
execute as @e[type=marker,tag=nx.acore] at @s run function nonios:arena/core/place
scoreboard players set #c_grown nx.arena 0
