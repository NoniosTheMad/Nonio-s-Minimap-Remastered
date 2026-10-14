execute as @e[type=interaction,tag=nx.shield,tag=nx.white] at @s run function nonios:nexus/shield_tick {team:"white",enemy:"black"}
execute as @e[type=interaction,tag=nx.shield,tag=nx.black] at @s run function nonios:nexus/shield_tick {team:"black",enemy:"white"}
execute as @e[type=marker,tag=nx.core,tag=nx.white] at @s unless block ~ ~ ~ minecraft:obsidian run function nonios:nexus/destroyed {team:"white",Team:"WHITE",enemy:"black"}
execute as @e[type=marker,tag=nx.core,tag=nx.black] at @s unless block ~ ~ ~ minecraft:obsidian run function nonios:nexus/destroyed {team:"black",Team:"BLACK",enemy:"white"}
# #48 centre pressure + decay, once a second while on (nexus/press/start at battle start, press/stop at the end)
execute if score #on nx.nxs matches 1 run scoreboard players add #pt nx.nxs 1
execute if score #on nx.nxs matches 1 if score #pt nx.nxs matches 20.. run function nonios:nexus/press/tick
