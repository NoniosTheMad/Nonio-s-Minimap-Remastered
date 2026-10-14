# as + at the generator: a small trap on the nearest player (silverfish / cobweb + poison / launch)
execute store result score #lr nx.gen run random value 1..3
execute if score #lr nx.gen matches 1 run summon minecraft:silverfish ~ ~0.3 ~
execute if score #lr nx.gen matches 1 run summon minecraft:silverfish ~ ~0.3 ~
execute if score #lr nx.gen matches 1 run summon minecraft:silverfish ~ ~0.3 ~
execute if score #lr nx.gen matches 2 as @p[distance=..8,gamemode=!spectator] at @s if block ~ ~ ~ #minecraft:air run setblock ~ ~ ~ minecraft:cobweb
execute if score #lr nx.gen matches 2 run effect give @p[distance=..8,gamemode=!spectator] minecraft:poison 4 0
execute if score #lr nx.gen matches 3 run effect give @p[distance=..8,gamemode=!spectator] minecraft:levitation 2 3
playsound minecraft:entity.witch.celebrate block @a[distance=..16] ~ ~ ~ 1 1
