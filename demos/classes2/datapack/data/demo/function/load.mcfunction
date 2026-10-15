# demo classes2: the real game (nonios:) runs the match with generators, arena nodes and Dream portals;
# this pack only adds solo-test buttons (G > Demo: Classes II).
scoreboard objectives add demo.c2 trigger
gamerule spawn_mobs false
# no spawn guard here (#88): the solo tester walks into the empty enemy spawn and gets Instant Damage from nowhere
data modify storage nonios:config spawn_guard set value 0b
gamerule advance_time false
time set noon
# the game takes over players once the map exists (#map nx.state = 1)
execute unless score #map nx.state matches 1 run schedule function nonios:map/build 5t
# worlds built before the deposit pads (#87): add the gold pressure plates around each vault (map/gen/bank does it now)
execute as @e[type=marker,tag=nx.bank_zone] at @s run fill ~-1 ~ ~-1 ~1 ~ ~1 minecraft:light_weighted_pressure_plate replace minecraft:air
