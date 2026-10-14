# Every tick (nonios:tick), one score check while shut. On a gate pad -> into the arena at the active slot's landing;
# in the active exit -> back out at your team's gate.
execute unless score #gon nx.arena matches 1 run return 0
execute as @e[type=marker,tag=nx.agate] at @s as @a[distance=..1,gamemode=!spectator] run function nonios:arena/gate/enter
execute as @e[type=marker,tag=nx.aslot_on] at @s as @a[distance=..1,gamemode=!spectator] run function nonios:arena/gate/leave
