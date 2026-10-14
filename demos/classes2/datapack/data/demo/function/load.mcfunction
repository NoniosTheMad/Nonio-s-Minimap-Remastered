# demo classes2: the real game (nonios:) runs the match with generators, arena nodes and Dream portals;
# this pack only adds solo-test buttons (G > Demo: Classes II).
scoreboard objectives add demo.c2 trigger
gamerule spawn_mobs false
gamerule advance_time false
time set noon
# the game takes over players once the map exists (#map nx.state = 1)
execute unless score #map nx.state matches 1 run schedule function nonios:map/build 5t
