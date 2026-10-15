# demo arena2: the real game (nonios:) runs the match with the V2 arena gates and regrowing core;
# this pack only adds solo-test buttons (G > Demo: Arena gates + core).
scoreboard objectives add demo.ar2 trigger
scoreboard objectives add demo.tal dummy
gamerule spawn_mobs false
gamerule advance_time false
time set noon
# the game takes over players once the map exists (#map nx.state = 1)
execute unless score #map nx.state matches 1 run schedule function nonios:map/build 5t
