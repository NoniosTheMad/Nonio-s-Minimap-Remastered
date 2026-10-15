# demo arena3: the real game (nonios:) runs the match on the placeholder map; this pack only adds solo-test buttons
# (G > Demo: Arena v3) and builds the map on first load.
scoreboard objectives add demo.ar3 trigger
gamerule spawn_mobs false
gamerule advance_time false
time set noon
execute unless score #map nx.state matches 1 run schedule function nonios:map/build 5t
