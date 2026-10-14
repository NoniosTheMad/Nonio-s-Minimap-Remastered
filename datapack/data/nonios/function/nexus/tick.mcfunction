execute as @e[type=interaction,tag=nx.shield,tag=nx.white] at @s run function nonios:nexus/shield_tick {team:"white",enemy:"black"}
execute as @e[type=interaction,tag=nx.shield,tag=nx.black] at @s run function nonios:nexus/shield_tick {team:"black",enemy:"white"}
execute as @e[type=marker,tag=nx.core,tag=nx.white] at @s unless block ~ ~ ~ minecraft:obsidian run function nonios:nexus/destroyed {team:"white",Team:"WHITE"}
execute as @e[type=marker,tag=nx.core,tag=nx.black] at @s unless block ~ ~ ~ minecraft:obsidian run function nonios:nexus/destroyed {team:"black",Team:"BLACK"}
